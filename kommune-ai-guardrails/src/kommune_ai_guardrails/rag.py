from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from typing import Any

try:
    from .config import get_settings
except (ImportError, ValueError):
    import sys
    from pathlib import Path
    src_dir = Path(__file__).resolve().parent.parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    from kommune_ai_guardrails.config import get_settings


def sanitize_pii(text: str) -> str:
    """Fjerner norske fødselsnumre og D-numre (11 siffer), telefonnumre og e-postadresser (Stage-Gate Port 4)."""
    # Norsk fødselsnummer (01-31) og D-nummer (41-71, dvs. første siffer + 4)
    fnr_pattern = r"\b(?:0[1-9]|[12][0-9]|3[01]|4[1-9]|[56][0-9]|7[01])(?:0[1-9]|1[012])\d{7}\b"
    text = re.sub(fnr_pattern, "[SKJERMET FNR]", text)

    # Telefonnummer (8 siffer, evt med +47/0047)
    tlf_pattern = r"\b(\+47|0047)?\s*([2-9]\d{1})\s*(\d{2})\s*(\d{2})\s*(\d{2})\b"
    text = re.sub(tlf_pattern, "[SKJERMET TLF]", text)

    # E-postadresser
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    text = re.sub(email_pattern, "[SKJERMET E-POST]", text)

    return text


def validate_output_citation(answer: str, required_keyword: str = "§") -> bool:
    """Verifiserer at AI-svaret inneholder minst én paragraf- eller kildehenvisning."""
    return required_keyword in answer or "Jfr." in answer or "KILDE:" in answer


try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    genai = None
    types = None

try:
    import sqlite_vec  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    sqlite_vec = None

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    SentenceTransformer = None

try:
    import ollama  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    ollama = None


def query_gemini(system_prompt: str, user_prompt: str, model_name: str = "gemini-3.8-flash") -> str:
    """Kaller Google Gemini API via google.genai med lynrask respons og null CPU-belastning."""
    if genai is None:
        return "⚠️ Python-pakken 'google-genai' er ikke installert. Kjør: pip install google-genai"
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ Fant ingen GEMINI_API_KEY eller GOOGLE_API_KEY i miljøet eller .env-filen."

    try:
        client = genai.Client(api_key=api_key)
        if types is not None and hasattr(types, "GenerateContentConfig"):
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.1,
                ),
            )
        else:
            full_content = f"SYSTEMINSTRUKSJON:\n{system_prompt}\n\n{user_prompt}"
            response = client.models.generate_content(
                model=model_name,
                contents=full_content,
            )
        return response.text or "⚠️ Tom respons mottatt fra Gemini."
    except Exception as exc:
        return f"⚠️ Feil ved tilkobling til Gemini API: {exc}"


def get_db_path() -> str:
    settings = get_settings()
    db_path = settings["db_path"]
    from pathlib import Path

    path = Path(db_path).expanduser()
    if not path.is_absolute():
        path = (Path(__file__).resolve().parents[2] / path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def init_audit_log(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            retrieved_chunk_ids TEXT NOT NULL,
            llm_response TEXT NOT NULL,
            action_type TEXT DEFAULT 'OLLAMA_RAG_LEGAL_QUERY',
            sha256_hash TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def log_audit_trail(conn: sqlite3.Connection, query: str, chunk_ids: list[Any], response_text: str) -> str:
    payload = f"{query}|{json.dumps(chunk_ids)}|{response_text}"
    sha256_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    conn.execute(
        """
        INSERT INTO Audit_AI_Actions (user_query, retrieved_chunk_ids, llm_response, sha256_hash)
        VALUES (?, ?, ?, ?)
        """,
        (query, json.dumps(chunk_ids), response_text, sha256_hash),
    )
    conn.commit()
    return sha256_hash


def ensure_legal_tables(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    existing_tables = {
        row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    }
    required = {"legal_chunks", "legal_fts", "vec_legal_chunks"}
    return required.issubset(existing_tables)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    if sqlite_vec is not None:
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
    init_audit_log(conn)
    return conn


def hybrid_search(conn: sqlite3.Connection, query: str, embedding_model: Any | None = None, top_k: int = 4, k_constant: int = 60):
    if embedding_model is None:
        raise RuntimeError("Missing embedding model: install 'sentence-transformers' and pass an initialized model.")

    cursor = conn.cursor()
    clean_fts_query = "".join(c if c.isalnum() or c.isspace() else " " for c in query).strip()
    fts_results: list[tuple[int, float]] = []
    if clean_fts_query:
        try:
            fts_sql = "SELECT rowid, rank FROM legal_fts WHERE legal_fts MATCH ? ORDER BY rank LIMIT 10"
            fts_results = cursor.execute(fts_sql, (clean_fts_query,)).fetchall()
        except sqlite3.OperationalError:
            fts_results = []

    try:
        query_emb = embedding_model.encode(f"query: {query}", normalize_embeddings=True)
        query_blob = sqlite_vec.serialize_float32(query_emb) if sqlite_vec is not None else None
    except Exception as exc:  # pragma: no cover - depends on model library
        raise RuntimeError(f"Embedding failed: {exc}") from exc

    vec_results: list[tuple[int, float]] = []
    if sqlite_vec is not None and query_blob is not None:
        vec_sql = "SELECT chunk_id, distance FROM vec_legal_chunks WHERE embedding MATCH ? AND k = 10 ORDER BY distance ASC"
        vec_results = cursor.execute(vec_sql, (query_blob,)).fetchall()

    rrf_scores: dict[int, float] = {}
    for rank, (chunk_id, _) in enumerate(fts_results):
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k_constant + rank + 1))
    for rank, (chunk_id, _) in enumerate(vec_results):
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k_constant + rank + 1))

    sorted_chunks = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
    selected_ids = [chunk_id for chunk_id, _ in sorted_chunks]
    if not selected_ids:
        return []

    placeholders = ",".join("?" for _ in selected_ids)
    rows = cursor.execute(
        f"SELECT id, source_file, category, section_ref, title, content FROM legal_chunks WHERE id IN ({placeholders})",
        selected_ids,
    ).fetchall()

    id_map = {row["id"]: row for row in rows}
    return [id_map[cid] for cid in selected_ids if cid in id_map]


def ask_kommune_ai(
    query: str,
    embedding_model: Any | None = None,
    model_name: str | None = None,
    provider: str | None = None,
):
    settings = get_settings()
    # Bestem leverandør (Gemini som førstevalg for lynrask respons og null CPU-belastning)
    provider = provider or settings.get("llm_provider", "gemini")

    # Hvis modellnavn er oppgitt, ruter vi automatisk til riktig leverandør
    if model_name:
        if model_name.startswith("gemini"):
            provider = "gemini"
        elif any(m in model_name.lower() for m in ["llama", "qwen", "mistral", "gemma", ":latest"]):
            provider = "ollama"
    else:
        model_name = (
            settings.get("gemini_model", "gemini-3.8-flash")
            if provider == "gemini"
            else settings.get("ollama_model", "llama3.1")
        )

    # Skjerm sensitive personopplysninger før søk og inferens (Stage-Gate Port 4)
    clean_query = sanitize_pii(query)
    conn = get_db_connection()

    try:
        if not ensure_legal_tables(conn):
            conn.close()
            return (
                "❌ Finner ingen relevante lover eller forskrifter i lokaldatabasen som dekker dette spørsmålet.",
                [],
                "",
            )

        chunks = hybrid_search(conn, clean_query, embedding_model, top_k=settings["top_k"], k_constant=settings["k_constant"])
        if not chunks:
            conn.close()
            return (
                "❌ Finner ingen relevante lover eller forskrifter i lokaldatabasen som dekker dette spørsmålet.",
                [],
                "",
            )

        context_blocks: list[str] = []
        chunk_ids: list[Any] = []
        for row in chunks:
            cid = row["id"]
            source = row["source_file"]
            category = row["category"]
            section_ref = row["section_ref"]
            title = row["title"]
            content = row["content"]
            chunk_ids.append(cid)
            sec_str = f" ({section_ref})" if section_ref else ""
            context_blocks.append(f"--- KILDE: {source} | {category}{sec_str} - {title} ---\n{content}")

        context_text = "\n\n".join(context_blocks)
        system_prompt = settings["system_prompt"]
        user_prompt = f"""BRUKERENS SPØRSMÅL:\n{clean_query}\n\nTILGJENGELIG REGELVERKSKONTEKST:\n{context_text}\n"""

        if provider == "gemini":
            answer = query_gemini(system_prompt, user_prompt, model_name=model_name)
        else:
            if ollama is None:
                answer = "⚠️ Python-pakken 'ollama' er ikke installert. Installer den for å bruke lokal RAG-motor."
            else:
                try:
                    response = ollama.chat(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        options={"temperature": settings["temperature"]},
                    )
                    if isinstance(response, dict):
                        answer = response.get("message", {}).get("content", "")
                    else:
                        answer = getattr(getattr(response, "message", None), "content", str(response))
                except AttributeError:
                    response = ollama.generate(
                        model=model_name,
                        prompt=f"{system_prompt}\n\n{user_prompt}",
                        options={"temperature": settings["temperature"]},
                    )
                    answer = response["response"] if isinstance(response, dict) else str(response)
                except Exception as exc:  # pragma: no cover - external service
                    answer = f"⚠️ Feil ved tilkobling til Ollama. Sjekk at Ollama kjører. Feilmelding: {exc}"

        hash_val = log_audit_trail(conn, clean_query, chunk_ids, answer)
        return answer, chunk_ids, hash_val
    finally:
        conn.close()


# Bakoverkompatibelt alias
ask_kommune_ai_ollama = ask_kommune_ai


if __name__ == "__main__":
    print("\n🤖 Kommune AI Guardrails — RAG CLI Tester & Helsesjekk")
    print("=" * 60)
    test_conn = get_db_connection()
    try:
        tables_ok = ensure_legal_tables(test_conn)
        print(f"Tabellstatus i SQLite: {'OK (FTS5 + vec0)' if tables_ok else 'MANGLER TABELLER'}")
        if tables_ok:
            count = test_conn.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()[0]
            print(f"Antall indekserte chunks: {count}")
    finally:
        test_conn.close()

    test_raw = "Hvilke regler gjelder for budsjettendring? Saksbehandler tlf 91234567, fnr 12058512345"
    test_clean = sanitize_pii(test_raw)
    print("\n🛡️ Verifisering av PII-maskering (Stage-Gate Port 4):")
    print(f"Før:   {test_raw}")
    print(f"Etter: {test_clean}")
    print("=" * 60)
