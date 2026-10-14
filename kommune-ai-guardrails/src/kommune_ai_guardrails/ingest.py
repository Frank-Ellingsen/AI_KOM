#!/usr/bin/env python3
"""
Dokumentinnlesing og indeksering for Kommune AI Guardrails.
Bygger hybrid søkeindeks i SQLite (FTS5 + sqlite-vec).
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any

# Sikre konsoll-encoding på Windows
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

try:
    import sqlite_vec
except ModuleNotFoundError:
    sqlite_vec = None

try:
    import pypdf
except ModuleNotFoundError:
    pypdf = None

try:
    from sentence_transformers import SentenceTransformer
except ModuleNotFoundError:
    SentenceTransformer = None

from .config import get_settings
from .rag import init_audit_log


def init_rag_schema(conn: sqlite3.Connection) -> None:
    """Oppretter relasjonstabell, FTS5-fullteksttabell og sqlite-vec-vektortabell."""
    cursor = conn.cursor()

    # 1. Hovedtabell for tekstbiter
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legal_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_file TEXT NOT NULL,
        category TEXT NOT NULL,
        section_ref TEXT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    );
    """)

    # 2. FTS5 fulltekstsøk (§-numre, tittel, innhold)
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS legal_fts USING fts5(
        title,
        section_ref,
        content
    );
    """)

    # 3. sqlite-vec vektortabell (384 dimensjoner for intfloat/multilingual-e5-small)
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS vec_legal_chunks USING vec0(
        chunk_id INTEGER PRIMARY KEY,
        embedding float[384]
    );
    """)

    # 4. Audit logging tabell
    init_audit_log(conn)

    conn.commit()


def clean_text(text: str) -> str:
    """Renser overflødige linjeskift og kontrolltegn."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_markdown_file(file_path: Path) -> list[dict[str, str]]:
    """Parser en markdown-fil oppdelt etter overskrifter (#, ##, ###)."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    chunks = []
    lines = text.split("\n")

    current_title = file_path.stem
    current_lines: list[str] = []
    current_ref = ""

    sec_regex = re.compile(r"§\s*[\d]+(?:-[\d]+)?(?:[a-z])?", re.IGNORECASE)

    # Identifiser meningsfull kategori
    lower_name = file_path.name.lower()
    if "mlops" in lower_name:
        category = "MLOps-Rammeverk"
    elif "modul" in lower_name or "aipakke" in lower_name or "innhold" in lower_name or "fria" in lower_name or "gevinstmodell" in lower_name:
        category = "AI-Implementeringspakke"
    elif "aarshjul" in lower_name:
        category = "Årshjul og Veiledere"
    else:
        category = "Kommunale Veiledere"

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_lines:
                content = clean_text("\n".join(current_lines))
                if content and len(content) > 30:
                    chunks.append({
                        "source_file": file_path.name,
                        "category": category,
                        "section_ref": current_ref,
                        "title": current_title,
                        "content": content,
                    })
                current_lines = []

            # Ny overskrift
            current_title = stripped.lstrip("#").strip()
            match = sec_regex.search(current_title)
            current_ref = match.group(0) if match else ""
        else:
            current_lines.append(line)
            if not current_ref:
                match = sec_regex.search(line)
                if match:
                    current_ref = match.group(0)

    if current_lines:
        content = clean_text("\n".join(current_lines))
        if content and len(content) > 30:
            chunks.append({
                "source_file": file_path.name,
                "category": category,
                "section_ref": current_ref,
                "title": current_title,
                "content": content,
            })

    return chunks


def parse_csv_file(file_path: Path) -> list[dict[str, str]]:
    """Parser KOSTRA kontoplan CSV-fil og grupperer inn i meningsfulle chunks."""
    chunks = []
    with file_path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return []

    # Grupper per 15-20 rader for balansert kontekst
    batch_size = 20
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        lines = []
        for r in batch:
            lines.append(" | ".join(f"{k}: {v}" for k, v in r.items() if v))
        content = "\n".join(lines)
        chunks.append({
            "source_file": file_path.name,
            "category": "KOSTRA Kontoplan",
            "section_ref": "KOSTRA",
            "title": f"KOSTRA kontoplan (del {i // batch_size + 1})",
            "content": content,
        })
    return chunks


def parse_pdf_file(file_path: Path) -> list[dict[str, str]]:
    """Parser PDF-dokumenter med avsnitt/paragraf-oppdeling."""
    if pypdf is None:
        return []

    try:
        reader = pypdf.PdfReader(str(file_path))
    except Exception as exc:
        print(f"⚠️ Kunne ikke lese {file_path.name}: {exc}")
        return []

    full_text = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        full_text.append(txt)

    combined = "\n".join(full_text)
    combined = clean_text(combined)

    # Identifiser kategori fra filnavn
    lower_name = file_path.name.lower()
    if "kommunelov" in lower_name:
        category = "Kommuneloven"
    elif "forskrift" in lower_name:
        category = "Kommunal Forskrift"
    elif "veileder" in lower_name:
        category = "Kommunal Veileder"
    elif "reglement" in lower_name:
        category = "Lokalt Reglement"
    else:
        category = "Kommunale Dokumenter"

    # Søk etter paragrafer (§ X eller § X-Y)
    pattern = re.compile(r"(§\s*\d+(?:-\d+)?\.?\s*([^\n\.\;]{1,80}))", re.MULTILINE)
    matches = list(pattern.finditer(combined))

    chunks = []
    if matches:
        for idx, match in enumerate(matches):
            start = match.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(combined)
            section_raw = match.group(1).strip()
            title_part = match.group(2).strip()
            sec_num_match = re.search(r"§\s*\d+(?:-\d+)?", section_raw)
            sec_num = sec_num_match.group(0) if sec_num_match else ""

            body = combined[start:end].strip()
            # Begrens chunk-størrelse til ca 2500 tegn
            if len(body) > 2500:
                body = body[:2500]

            if len(body) > 40:
                chunks.append({
                    "source_file": file_path.name,
                    "category": category,
                    "section_ref": sec_num,
                    "title": f"{sec_num} {title_part}".strip(),
                    "content": body,
                })
    else:
        # Fallback: del opp i biter på ca. 1200 tegn
        chunk_len = 1200
        for i in range(0, len(combined), chunk_len):
            part = combined[i : i + chunk_len].strip()
            if len(part) > 50:
                chunks.append({
                    "source_file": file_path.name,
                    "category": category,
                    "section_ref": "",
                    "title": f"{file_path.stem} (del {i // chunk_len + 1})",
                    "content": part,
                })

    return chunks


def ingest_all(
    data_dir: Path | None = None,
    db_path: Path | None = None,
    embedding_model: Any | None = None,
    progress_callback: Any | None = None,
    force_reindex: bool = False,
) -> int:
    """Leser inn råfiler fra data_dir og oppdaterer SQLite-databasen inkrementelt eller fullt."""
    settings = get_settings()
    base_dir = Path(__file__).resolve().parents[2]
    
    if data_dir is None:
        data_dir = base_dir / "data" / "raw"
    elif not isinstance(data_dir, Path):
        data_dir = Path(data_dir)
    if not data_dir.is_absolute():
        data_dir = (base_dir / data_dir).resolve()

    if db_path is None:
        db_path = Path(settings["db_path"])
    elif not isinstance(db_path, Path):
        db_path = Path(db_path)
    if not db_path.is_absolute():
        db_path = (base_dir / db_path).resolve()

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    if sqlite_vec is not None:
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

    init_rag_schema(conn)
    cursor = conn.cursor()

    raw_files = [f for f in data_dir.glob("*") if f.is_file()]
    total_files = len(raw_files)

    # Undersøk eksisterende kilder
    existing_sources = set(r[0] for r in cursor.execute("SELECT DISTINCT source_file FROM legal_chunks").fetchall())
    
    # Håndter slettede filer dersom noen ble fjernet fra data_dir
    current_names = {f.name for f in raw_files}
    deleted_sources = existing_sources - current_names
    if deleted_sources:
        for ds in deleted_sources:
            ids = [r[0] for r in cursor.execute("SELECT id FROM legal_chunks WHERE source_file = ?", (ds,)).fetchall()]
            if ids:
                if sqlite_vec is not None:
                    cursor.executemany("DELETE FROM vec_legal_chunks WHERE chunk_id = ?", [(i,) for i in ids])
                cursor.executemany("DELETE FROM legal_fts WHERE rowid = ?", [(i,) for i in ids])
                cursor.execute("DELETE FROM legal_chunks WHERE source_file = ?", (ds,))
        conn.commit()
        print(f"🧹 Fjernet {len(deleted_sources)} utgåtte kilder fra databasen.")

    # Velg hvilke filer som skal indekseres
    if force_reindex or not existing_sources:
        files_to_process = raw_files
        print("🔄 Kjører full re-indeksering av alle dokumenter...")
        cursor.execute("DELETE FROM legal_chunks")
        cursor.execute("DELETE FROM legal_fts")
        if sqlite_vec is not None:
            cursor.execute("DELETE FROM vec_legal_chunks")
        conn.commit()
    else:
        files_to_process = [f for f in raw_files if f.name not in existing_sources]
        print(f"⚡ Inkrementell oppdatering: {len(files_to_process)} nye filer å indeksere (av {total_files} totalt).")

    # Hvis ingen nye filer, kjør eventuelle kategori-oppdateringer og returner
    if not files_to_process:
        cursor.execute("""
            UPDATE legal_chunks SET category = 'AI-Implementeringspakke'
            WHERE category = 'Årshjul og Veiledere'
            AND (source_file LIKE '%MODUL%' OR source_file LIKE '%INNHOLD%' OR source_file LIKE '%FRIA%' OR source_file LIKE '%GEVINSTMODELL%')
        """)
        cursor.execute("""
            UPDATE legal_chunks SET category = 'MLOps-Rammeverk'
            WHERE category != 'MLOps-Rammeverk'
            AND (source_file LIKE '%MLOps%')
        """)
        conn.commit()
        total_chunks = cursor.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        print(f"✅ Vektordatabasen er allerede oppdatert ({total_chunks} biter fra {len(existing_sources)} kilder).")
        if progress_callback:
            progress_callback({
                "step": "done",
                "total_chunks": total_chunks,
                "total_files": total_files,
                "db_path": str(db_path),
                "message": f"Vektordatabasen er fullstendig synkronisert ({total_chunks} biter fra {total_files} dokumenter)."
            })
        conn.close()
        return total_chunks

    # Finn biter fra nye filer
    new_chunks: list[dict[str, str]] = []
    print(f"📂 Parser {len(files_to_process)} nye dokumenter...")
    if progress_callback:
        progress_callback({"step": "scanning", "message": f"Søker etter nye dokumenter i {data_dir.name}..."})

    for idx, file_path in enumerate(files_to_process, start=1):
        ext = file_path.suffix.lower()
        parsed: list[dict[str, str]] = []
        if ext == ".md":
            parsed = parse_markdown_file(file_path)
        elif ext == ".csv":
            parsed = parse_csv_file(file_path)
        elif ext == ".pdf":
            parsed = parse_pdf_file(file_path)

        if parsed:
            new_chunks.extend(parsed)
            print(f"  ✓ {file_path.name}: {len(parsed)} biter")

        if progress_callback:
            progress_callback({
                "step": "parsing",
                "file": file_path.name,
                "current_file_idx": idx,
                "total_files": len(files_to_process),
                "chunks_found": len(new_chunks),
                "message": f"Parser [{idx}/{len(files_to_process)}] {file_path.name} ({len(parsed)} biter)"
            })

    if not new_chunks:
        print("⚠️ Ingen nye dokumentbiter funnet.")
        total_chunks = cursor.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
        conn.close()
        return total_chunks

    print(f"\n🔢 {len(new_chunks)} nye biter klare for lagring og semantisk embedding.")

    # Last inn embedding-modell
    if embedding_model is None and SentenceTransformer is not None:
        print("⏳ Laster embedding-modell intfloat/multilingual-e5-small...")
        if progress_callback:
            progress_callback({"step": "loading_model", "message": "Laster semantisk modell intfloat/multilingual-e5-small..."})
        try:
            import os
            os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
            import transformers.utils.logging as hf_logging
            hf_logging.disable_progress_bar()
        except Exception:
            pass
        embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")

    # 1. Sett inn i legal_chunks og legal_fts
    if progress_callback:
        progress_callback({"step": "inserting_text", "message": f"Lagrer {len(new_chunks)} nye biter i SQLite..."})

    chunk_records = []
    for chunk in new_chunks:
        cursor.execute(
            """
            INSERT INTO legal_chunks (source_file, category, section_ref, title, content)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                chunk["source_file"],
                chunk["category"],
                chunk["section_ref"],
                chunk["title"],
                chunk["content"],
            ),
        )
        chunk_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO legal_fts (rowid, title, section_ref, content)
            VALUES (?, ?, ?, ?)
            """,
            (chunk_id, chunk["title"], chunk["section_ref"], chunk["content"]),
        )
        chunk_records.append((chunk_id, chunk))

    conn.commit()

    # 2. Beregn vektorer for de nye bitene
    if embedding_model is not None and sqlite_vec is not None:
        print(f"⏳ Beregner semantiske vektorer for {len(chunk_records)} nye biter...")
        if progress_callback:
            progress_callback({"step": "embedding", "total_chunks": len(chunk_records), "message": f"Beregner 384D semantiske vektorer for {len(chunk_records)} biter..."})

        texts_to_embed = [
            f"passage: {c['title']} {c['section_ref']} {c['content']}"
            for _, c in chunk_records
        ]
        
        embeddings = embedding_model.encode(
            texts_to_embed,
            batch_size=64,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        print("⚡ Skriver nye vektorer til vec_legal_chunks...")
        if progress_callback:
            progress_callback({"step": "writing_vectors", "message": "Skriver vektorer til sqlite-vec..."})

        vec_rows = []
        for (chunk_id, _), emb_vec in zip(chunk_records, embeddings):
            emb_blob = sqlite_vec.serialize_float32(emb_vec)
            vec_rows.append((chunk_id, emb_blob))

        cursor.executemany(
            """
            INSERT INTO vec_legal_chunks (chunk_id, embedding)
            VALUES (?, ?)
            """,
            vec_rows,
        )
        conn.commit()

    # Kategori-oppdatering for eventuelle historiske biter
    cursor.execute("""
        UPDATE legal_chunks SET category = 'AI-Implementeringspakke'
        WHERE category = 'Årshjul og Veiledere'
        AND (source_file LIKE '%MODUL%' OR source_file LIKE '%INNHOLD%' OR source_file LIKE '%FRIA%' OR source_file LIKE '%GEVINSTMODELL%')
    """)
    conn.commit()

    total_chunks = cursor.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
    total_sources = len(set(r[0] for r in cursor.execute("SELECT DISTINCT source_file FROM legal_chunks").fetchall()))
    conn.close()

    print(f"🎉 Fullført! Totalt {total_chunks} biter indeksert fra {total_sources} dokumenter.")
    if progress_callback:
        progress_callback({
            "step": "done",
            "total_chunks": total_chunks,
            "total_files": total_sources,
            "db_path": str(db_path),
            "message": f"Fullført! {len(new_chunks)} nye biter indeksert. Totalt {total_chunks} biter fra {total_sources} dokumenter."
        })
    return total_chunks


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Indeksering for Kommune AI Guardrails")
    parser.add_argument("--force", action="store_true", help="Tving full re-indeksering av alle filer")
    args = parser.parse_args()
    ingest_all(force_reindex=args.force)
