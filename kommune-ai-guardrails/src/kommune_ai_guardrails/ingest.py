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

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_lines:
                content = clean_text("\n".join(current_lines))
                if content and len(content) > 30:
                    chunks.append({
                        "source_file": file_path.name,
                        "category": "Årshjul og Veiledere",
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
                "category": "Årshjul og Veiledere",
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
) -> int:
    """Leser inn alle råfiler fra data_dir og lagrer i db_path."""
    settings = get_settings()
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = data_dir or (base_dir / "data" / "raw")
    db_path = db_path or Path(settings["db_path"])

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    if sqlite_vec is not None:
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

    init_rag_schema(conn)

    # Finn alle filer
    all_chunks: list[dict[str, str]] = []
    print(f"📂 Søker etter dokumenter i {data_dir}...")

    raw_files = list(data_dir.glob("*"))
    for file_path in raw_files:
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext == ".md":
                parsed = parse_markdown_file(file_path)
                all_chunks.extend(parsed)
                print(f"  ✓ {file_path.name}: {len(parsed)} biter")
            elif ext == ".csv":
                parsed = parse_csv_file(file_path)
                all_chunks.extend(parsed)
                print(f"  ✓ {file_path.name}: {len(parsed)} biter")
            elif ext == ".pdf":
                parsed = parse_pdf_file(file_path)
                all_chunks.extend(parsed)
                print(f"  ✓ {file_path.name}: {len(parsed)} biter")

    if not all_chunks:
        print("⚠️ Ingen dokumentbiter funnet for indeksering.")
        conn.close()
        return 0

    print(f"\n🔢 Totalt {len(all_chunks)} biter klare for embedding og indeksering.")

    # Last inn embedding-modell dersom den ikke er oppgitt
    if embedding_model is None and SentenceTransformer is not None:
        print("⏳ Laster embedding-modell intfloat/multilingual-e5-small...")
        embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")

    cursor = conn.cursor()

    # Tøm eksisterende data dersom vi reindekserer
    cursor.execute("DELETE FROM legal_chunks")
    cursor.execute("DELETE FROM legal_fts")
    if sqlite_vec is not None:
        cursor.execute("DELETE FROM vec_legal_chunks")

    print("💾 Lagrer og indekserer i SQLite...")
    
    # 1. Sett inn i legal_chunks og legal_fts først for å få chunk_ids
    chunk_records = []
    for chunk in all_chunks:
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

    # 2. Beregn vektorer i batches for maksimal ytelse (130+ biter/sek)
    if embedding_model is not None and sqlite_vec is not None:
        print(f"⏳ Beregner semantiske vektorer for {len(chunk_records)} biter (batch-størrelse 64)...")
        texts_to_embed = [
            f"passage: {c['title']} {c['section_ref']} {c['content']}"
            for _, c in chunk_records
        ]
        
        # Batch-koding med SentenceTransformer
        embeddings = embedding_model.encode(
            texts_to_embed,
            batch_size=64,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        print("⚡ Skriver vektorer til vec_legal_chunks...")
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


    conn.commit()
    conn.close()
    print(f"🎉 Fullført! {len(all_chunks)} biter indeksert i {db_path}")
    return len(all_chunks)


if __name__ == "__main__":
    ingest_all()
