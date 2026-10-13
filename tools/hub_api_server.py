#!/usr/bin/env python3
"""
Kristiansand Kommune — Control Office Hub API & Vector DB Bridge
Lettvekts lokal HTTP/JSON-tjener basert på standardbiblioteket (http.server).
Håndterer REST API-kall fra index.html for å oppdatere og sjekke status på SQLite/sqlite-vec vektordatabasen.
"""

from __future__ import annotations

import json
import mimetypes
import os
from pathlib import Path
import sqlite3
import sys
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Sikre UTF-8 på Windows konsoll
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Sett opp stier
ROOT_DIR = Path(__file__).resolve().parent.parent
GUARDRAILS_DIR = ROOT_DIR / "kommune-ai-guardrails"
SRC_DIR = GUARDRAILS_DIR / "src"
RAW_DATA_DIR = GUARDRAILS_DIR / "data" / "raw"
DB_PATH = GUARDRAILS_DIR / "data" / "db" / "kommune_rag_store.db"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Global tilstand for asynkron indeksering
UPDATE_STATE = {
    "is_updating": False,
    "state": "idle",  # idle, scanning, parsing, loading_model, embedding, done, error
    "message": "Klar til indeksering.",
    "current_file": "",
    "files_done": 0,
    "total_files": 0,
    "chunks_found": 0,
    "percent": 0,
    "error": None,
    "start_time": 0.0,
    "duration": 0.0,
    "last_result": None,
}
STATE_LOCK = threading.Lock()


def get_db_stats() -> dict:
    """Henter nøkkeltall direkte fra SQLite-databasen."""
    raw_files = [f.name for f in RAW_DATA_DIR.glob("*") if f.is_file()] if RAW_DATA_DIR.exists() else []
    
    if not DB_PATH.exists():
        return {
            "db_exists": False,
            "chunks_count": 0,
            "source_files": [],
            "source_files_count": 0,
            "raw_files_count": len(raw_files),
            "raw_files": raw_files,
            "db_path": str(DB_PATH),
            "db_size_mb": 0.0,
            "last_modified": None,
        }

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Sjekk om legal_chunks tabellen finnes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='legal_chunks'")
        if not cursor.fetchone():
            conn.close()
            return {
                "db_exists": True,
                "chunks_count": 0,
                "source_files": [],
                "source_files_count": 0,
                "raw_files_count": len(raw_files),
                "raw_files": raw_files,
                "db_path": str(DB_PATH),
                "db_size_mb": round(DB_PATH.stat().st_size / (1024 * 1024), 2),
                "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(DB_PATH.stat().st_mtime)),
            }

        chunks_count = cursor.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        sources = [r[0] for r in cursor.execute("SELECT DISTINCT source_file FROM legal_chunks ORDER BY source_file").fetchall()]
        conn.close()

        return {
            "db_exists": True,
            "chunks_count": chunks_count,
            "source_files": sources,
            "source_files_count": len(sources),
            "raw_files_count": len(raw_files),
            "raw_files": raw_files,
            "db_path": str(DB_PATH),
            "db_size_mb": round(DB_PATH.stat().st_size / (1024 * 1024), 2),
            "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(DB_PATH.stat().st_mtime)),
        }
    except Exception as exc:
        return {
            "db_exists": True,
            "error": str(exc),
            "raw_files_count": len(raw_files),
            "raw_files": raw_files,
            "db_path": str(DB_PATH),
        }


def _run_ingest_worker() -> None:
    """Kjører indeksering i en separat tråd med sanntidsoppdatering av fremdrift."""
    global UPDATE_STATE
    start_time = time.time()

    def progress_callback(data: dict) -> None:
        with STATE_LOCK:
            step = data.get("step", UPDATE_STATE["state"])
            UPDATE_STATE["state"] = step
            UPDATE_STATE["message"] = data.get("message", UPDATE_STATE["message"])
            if "file" in data:
                UPDATE_STATE["current_file"] = data["file"]
            if "current_file_idx" in data:
                UPDATE_STATE["files_done"] = data["current_file_idx"]
            if "total_files" in data:
                UPDATE_STATE["total_files"] = data["total_files"]
            if "chunks_found" in data:
                UPDATE_STATE["chunks_found"] = data["chunks_found"]

            # Estimer fremdrift i prosent
            if step == "scanning":
                UPDATE_STATE["percent"] = 5
            elif step == "parsing":
                tf = max(1, UPDATE_STATE["total_files"])
                UPDATE_STATE["percent"] = 5 + int((UPDATE_STATE["files_done"] / tf) * 45)
            elif step == "loading_model":
                UPDATE_STATE["percent"] = 52
            elif step == "inserting_text":
                UPDATE_STATE["percent"] = 58
            elif step == "embedding":
                UPDATE_STATE["percent"] = 70
            elif step == "writing_vectors":
                UPDATE_STATE["percent"] = 92
            elif step == "done":
                UPDATE_STATE["percent"] = 100

    try:
        from kommune_ai_guardrails.ingest import ingest_all

        with STATE_LOCK:
            UPDATE_STATE["is_updating"] = True
            UPDATE_STATE["state"] = "scanning"
            UPDATE_STATE["message"] = "Initialiserer skanning av data/raw..."
            UPDATE_STATE["percent"] = 2
            UPDATE_STATE["error"] = None
            UPDATE_STATE["start_time"] = start_time

        count = ingest_all(
            data_dir=RAW_DATA_DIR,
            db_path=DB_PATH,
            progress_callback=progress_callback,
        )

        duration = round(time.time() - start_time, 2)
        stats = get_db_stats()

        with STATE_LOCK:
            UPDATE_STATE["is_updating"] = False
            UPDATE_STATE["state"] = "done"
            UPDATE_STATE["percent"] = 100
            UPDATE_STATE["duration"] = duration
            UPDATE_STATE["message"] = f"Vellykket fullført! {count} biter indeksert på {duration} sekunder."
            UPDATE_STATE["last_result"] = {
                "chunks_indexed": count,
                "duration_seconds": duration,
                "db_stats": stats,
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

    except Exception as exc:
        duration = round(time.time() - start_time, 2)
        with STATE_LOCK:
            UPDATE_STATE["is_updating"] = False
            UPDATE_STATE["state"] = "error"
            UPDATE_STATE["error"] = str(exc)
            UPDATE_STATE["duration"] = duration
            UPDATE_STATE["message"] = f"Feil under indeksering: {exc}"


class HubApiHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler med full CORS-støtte og REST-endepunkter."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        # Tillat CORS for forespørsler fra file:/// og localhost
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self._set_headers(HTTPStatus.NO_CONTENT)

    def do_GET(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/status":
            stats = get_db_stats()
            with STATE_LOCK:
                progress = dict(UPDATE_STATE)
            response = {
                "ok": True,
                "db_stats": stats,
                "update_state": progress,
            }
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        elif path == "/api/progress":
            with STATE_LOCK:
                progress = dict(UPDATE_STATE)
                if progress["is_updating"]:
                    progress["elapsed_seconds"] = round(time.time() - progress["start_time"], 1)
                else:
                    progress["elapsed_seconds"] = progress["duration"]
            self._set_headers(200, "application/json; charset=utf-8")
            self.wfile.write(json.dumps({"ok": True, "progress": progress}, ensure_ascii=False).encode("utf-8"))
            return

        # Statisk servering av index.html og filer i AI_KOM
        file_to_serve = ROOT_DIR / "index.html" if path in ("/", "/index.html") else (ROOT_DIR / path.lstrip("/"))
        
        # Sikre mot path traversal
        try:
            file_to_serve = file_to_serve.resolve()
            if not str(file_to_serve).startswith(str(ROOT_DIR.resolve())):
                self._set_headers(HTTPStatus.FORBIDDEN, "text/plain")
                self.wfile.write(b"403 Forbidden")
                return
        except Exception:
            self._set_headers(HTTPStatus.NOT_FOUND, "text/plain")
            self.wfile.write(b"404 Not Found")
            return

        if file_to_serve.exists() and file_to_serve.is_file():
            mime_type, _ = mimetypes.guess_type(str(file_to_serve))
            mime_type = mime_type or "application/octet-stream"
            if mime_type.startswith("text/") or mime_type in ("application/javascript", "application/json"):
                mime_type += "; charset=utf-8"

            self._set_headers(HTTPStatus.OK, mime_type)
            with open(file_to_serve, "rb") as f:
                self.wfile.write(f.read())
        else:
            self._set_headers(HTTPStatus.NOT_FOUND, "application/json")
            self.wfile.write(json.dumps({"ok": False, "error": f"Fant ikke {path}"}).encode("utf-8"))

    def do_POST(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/update-vectordb":
            with STATE_LOCK:
                if UPDATE_STATE["is_updating"]:
                    self._set_headers(HTTPStatus.CONFLICT, "application/json; charset=utf-8")
                    self.wfile.write(
                        json.dumps({
                            "ok": False,
                            "error": "Indeksering pågår allerede.",
                            "progress": dict(UPDATE_STATE)
                        }, ensure_ascii=False).encode("utf-8")
                    )
                    return

                UPDATE_STATE["is_updating"] = True
                UPDATE_STATE["state"] = "starting"
                UPDATE_STATE["message"] = "Starter indekseringstråd..."
                UPDATE_STATE["percent"] = 1
                UPDATE_STATE["error"] = None

            worker = threading.Thread(target=_run_ingest_worker, daemon=True)
            worker.start()

            self._set_headers(HTTPStatus.ACCEPTED, "application/json; charset=utf-8")
            self.wfile.write(
                json.dumps({
                    "ok": True,
                    "message": "Indeksering startet i bakgrunnen.",
                    "status": "started",
                }, ensure_ascii=False).encode("utf-8")
            )
            return

        self._set_headers(HTTPStatus.NOT_FOUND, "application/json")
        self.wfile.write(json.dumps({"ok": False, "error": f"Ukjent POST-endepunkt {path}"}).encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        pass


def run_server(host: str = "127.0.0.1", port: int = 8766) -> None:
    server_address = (host, port)
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(server_address, HubApiHandler)
    print(f"=====================================================================")
    print(f"🏛️  KRISTIANSAND KOMMUNE — CONTROL OFFICE HUB API TJENER")
    print(f"    Lytter på: http://{host}:{port}")
    print(f"    Status API: http://{host}:{port}/api/status")
    print(f"    Oppdatering API: POST http://{host}:{port}/api/update-vectordb")
    print(f"    Dashboard: http://{host}:{port}/index.html")
    print(f"=====================================================================")
    sys.stdout.flush()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStenger API-tjener...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.getenv("HUB_API_PORT", "8766"))
    run_server(port=port)
