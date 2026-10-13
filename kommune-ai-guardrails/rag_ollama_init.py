#!/usr/bin/env python3
"""
Kommune AI Guardrails — Lokal RAG-motor med Ollama, sqlite-vec og audit-logging.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any

# Sikre at Windows-konsollen håndterer UTF-8/emojis uten charmap UnicodeEncodeError
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

import ollama
from sentence_transformers import SentenceTransformer
import sqlite_vec

# ==========================================
# 1. KONFIGURASJON OG STIER
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("KOMMUNE_DB_PATH", str(BASE_DIR / "data" / "db" / "kommune_rag_store.db")))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")


# ==========================================
# 2. AUDIT LOGGING OPPSETT (STAGE-GATE PORT 9)
# ==========================================
def init_audit_log(conn: sqlite3.Connection) -> None:
    """Oppretter uforanderlig tabell for revisjonssporing ifm. Kommunerevisjonen."""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT NOT NULL,
        retrieved_chunk_ids TEXT NOT NULL,
        llm_response TEXT NOT NULL,
        action_type TEXT DEFAULT 'OLLAMA_RAG_LEGAL_QUERY',
        sha256_hash TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()


def log_audit_trail(conn: sqlite3.Connection, query: str, chunk_ids: list[Any], response_text: str) -> str:
    """Genererer kryptografisk SHA-256 hash og logger spørring og svar."""
    payload = f"{query}|{json.dumps(chunk_ids)}|{response_text}"
    sha256_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Audit_AI_Actions (user_query, retrieved_chunk_ids, llm_response, sha256_hash)
        VALUES (?, ?, ?, ?)
        """,
        (query, json.dumps(chunk_ids), response_text, sha256_hash),
    )
    conn.commit()
    return sha256_hash


# ==========================================
# 3. HYBRID SØKEMOTOR (BM25 + VEKTOR + RRF)
# ==========================================
def get_db_connection() -> sqlite3.Connection:
    """Åpner SQLite-tilkobling med sqlite-vec utvidelsen aktivert."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    init_audit_log(conn)
    return conn


def ensure_legal_tables(conn: sqlite3.Connection) -> bool:
    """Sjekker om nødvendige tabeller for hybrid-søk eksisterer i databasen."""
    cursor = conn.cursor()
    existing_tables = {
        row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    required = {"legal_chunks", "legal_fts", "vec_legal_chunks"}
    return required.issubset(existing_tables)


def hybrid_search(conn: sqlite3.Connection, query: str, embedding_model: Any, top_k: int = 4) -> list[tuple]:
    """Kombinerer FTS5 fulltekstsøk (§-numre) og sqlite-vec (semantikk) med RRF."""
    cursor = conn.cursor()

    if not ensure_legal_tables(conn):
        return []

    # --- A. BM25 / FTS5 EKSATTSØK (§-numre) ---
    clean_fts_query = "".join(
        [c if c.isalnum() or c.isspace() else " " for c in query]
    ).strip()
    fts_results = []
    if clean_fts_query:
        try:
            fts_sql = "SELECT rowid, rank FROM legal_fts WHERE legal_fts MATCH ? ORDER BY rank LIMIT 10"
            fts_results = cursor.execute(fts_sql, (clean_fts_query,)).fetchall()
        except sqlite3.OperationalError:
            fts_results = []

    # --- B. VEKTORSØK VIA SQLITE-VEC ---
    query_emb = embedding_model.encode(
        f"query: {query}", normalize_embeddings=True
    )
    query_blob = sqlite_vec.serialize_float32(query_emb)

    vec_results = []
    try:
        vec_sql = "SELECT chunk_id, distance FROM vec_legal_chunks WHERE embedding MATCH ? AND k = 10 ORDER BY distance ASC"
        vec_results = cursor.execute(vec_sql, (query_blob,)).fetchall()
    except sqlite3.OperationalError:
        vec_results = []

    # --- C. RECIPROCAL RANK FUSION (RRF) ---
    rrf_scores: dict[Any, float] = {}
    k_constant = 60

    for rank, (chunk_id, _) in enumerate(fts_results):
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (
            1.0 / (k_constant + (rank + 1))
        )

    for rank, (chunk_id, _) in enumerate(vec_results):
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (
            1.0 / (k_constant + (rank + 1))
        )

    sorted_chunks = sorted(
        rrf_scores.items(), key=lambda x: x[1], reverse=True
    )[:top_k]
    selected_ids = [chunk_id for chunk_id, _ in sorted_chunks]

    if not selected_ids:
        return []

    # --- D. HENT FULLSTENDIGE CHUNKS & METADATA ---
    placeholders = ",".join("?" * len(selected_ids))
    fetch_sql = f"SELECT id, source_file, category, section_ref, title, content FROM legal_chunks WHERE id IN ({placeholders})"
    try:
        rows = cursor.execute(fetch_sql, selected_ids).fetchall()
    except sqlite3.OperationalError:
        return []

    id_map = {row[0]: row for row in rows}
    ordered_results = [id_map[cid] for cid in selected_ids if cid in id_map]

    return ordered_results


# ==========================================
# 4. RAG PROMPT & OLLAMA LOKALT KALL
# ==========================================
def ask_kommune_ai_ollama(
    query: str,
    embedding_model: Any,
    model_name: str = OLLAMA_MODEL,
) -> tuple[str, list[Any], str]:
    """Utfører hybrid RAG-søk og sender kontekstuelt prompt til lokal Ollama-modell."""
    conn = get_db_connection()
    try:
        chunks = hybrid_search(conn, query, embedding_model, top_k=4)

        if not chunks:
            return (
                "❌ Finner ingen relevante lover eller forskrifter i lokaldatabasen som dekker dette spørsmålet.",
                [],
                "",
            )

        # Bygg kildekontekst
        context_blocks = []
        chunk_ids = []

        for row in chunks:
            cid, source, category, section_ref, title, content = row
            chunk_ids.append(cid)
            sec_str = f" ({section_ref})" if section_ref else ""
            context_blocks.append(
                f"--- KILDE: {source} | {category}{sec_str} - {title} ---\n{content}"
            )

        context_text = "\n\n".join(context_blocks)

        # Glass-Box System Prompt
        system_prompt = """Du er en spesialisert juridisk og økonomisk rådgiver for Kristiansand kommune.
Besvar brukerens spørsmål basert UTLUKKENDE på den oppgitte kildekonteksten.

STRENGE REGLER:
1. Svaret må VÆRE 100 % FORANKRET i de oppgitte kildene.
2. Du må EKSPLISITT SITERE kildene og paragrafer i svaret ditt (f.eks. "Jfr. Kommuneloven § 14-5...").
3. Dersom kildene ikke gir tilstrekkelig svar, sier du: "Finner ikke tilstrekkelig hjemmel for dette i kommunens regelverksdatabase."
4. Svar på et ryddig, profesjonelt norsk språk.
"""

        user_prompt = f"""BRUKERENS SPØRSMÅL:
{query}

TILGJENGELIG REGELVERKSKONTEKST:
{context_text}
"""

        print(
            f"🦙 Sender forespørsel til lokal Ollama-modell ('{model_name}')..."
        )

        try:
            response = ollama.chat(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={"temperature": 0.1},
            )
            if isinstance(response, dict):
                answer = response.get("message", {}).get("content", "")
            else:
                answer = getattr(getattr(response, "message", None), "content", str(response))
        except AttributeError:
            try:
                response = ollama.generate(
                    model=model_name,
                    prompt=f"{system_prompt}\n\n{user_prompt}",
                    options={"temperature": 0.1},
                )
                answer = (
                    response.get("response", str(response))
                    if isinstance(response, dict)
                    else getattr(response, "response", str(response))
                )
            except Exception as gen_err:
                answer = f"⚠️ Feil ved generering via Ollama: {gen_err}"
        except Exception as e:
            answer = f"⚠️ Feil ved tilkobling til Ollama. Sjekk at Ollama kjører. Feilmelding: {e}"

        # Lagre uforanderlig audit trail (Port 9)
        hash_val = log_audit_trail(conn, query, chunk_ids, answer)
        return answer, chunk_ids, hash_val
    finally:
        conn.close()


# ==========================================
# 5. TEST KJØRING
# ==========================================
if __name__ == "__main__":
    print("\n🤖 Kommune AI Guardrails — Ollama Local RAG Tester")
    print("=" * 60)

    print("⏳ Laster embedding-modell for vektorsøk...")
    embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")

    test_query = (
        "Hvilke regler gjelder dersom vi må endre budsjettet i løpet av året?"
    )
    print(f"\n❓ Spørsmål: {test_query}\n")

    answer, used_chunks, audit_hash = ask_kommune_ai_ollama(
        test_query, embedding_model
    )

    print("💬 Svar fra Ollama RAG-motoren:")
    print("-" * 60)
    print(answer)
    print("-" * 60)
    print(f"📌 Benyttede Chunk ID-er: {used_chunks}")
    print(f"🛡️ SHA-256 Audit Trail Hash: {audit_hash}")
