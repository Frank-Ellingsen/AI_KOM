---
name: sqlite-vec-executor
description: >-
  Lavnivå-databasekjerne for SQLite, WAL-modus, FTS5 fritekstsøk og 384D vektor-KNN via sqlite-vec.
---

# 🛠️ Tool Skill: SQLite & sqlite-vec Database Executor

> **Teknisk lavnivå-driver for administrasjon, indeksering, migrering og hybrid-spørringer i SQLite med `sqlite-vec` og `FTS5`.**

---

## 1. Oversikt og Formål

Denne verktøy-skillen gir agenten direkte lavnivå-tilgang til å opprette, migrere, optimalisere og vedlikeholde den kommunale databasen (`kommune_golden_record.db`). Den håndterer både relasjonelle faktatabeller (Star Schema), FTS5 fulltekstsøk, og 384-dimensjonale vektorer via `sqlite-vec`.

---

## 2. Tekniske Funksjoner & Operasjoner

### A. Tilkobling og Modullasting
```python
import os
import sqlite3
import sqlite_vec

def connect_db(db_path=None):
    if db_path is None:
        db_path = os.getenv("KOMMUNE_DB_PATH", "data/db/kommune_golden_record.db")
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")  # Write-Ahead Logging for ytelse
    return conn
```

### B. Vektor- og FTS5-indeksering
* **Vektortabell (`vec_legal_chunks`):** Bruker `float[384]` med Cosine / L2 distance.
* **FTS5-tabell (`legal_fts`):** Inkluderer norsk stemmer/tokenizer for treff på juridiske faguttrykk og §-numre.

### C. Databaseutforming & Skjemamigrering
* Sjekker og oppgraderer tabellstrukturer uten datatap.
* Atomiske transaksjoner med `conn.commit()` og automatisk `rollback()` ved feil.

---

## 3. Eksempel på Lavnivå Vektorsøk

```python
def execute_vector_knn(conn, query_embedding, top_k=5):
    cursor = conn.cursor()
    query_blob = sqlite_vec.serialize_float32(query_embedding)
    sql = """
        SELECT chunk_id, distance
        FROM vec_legal_chunks
        WHERE embedding MATCH ? AND k = ?
        ORDER BY distance ASC;
    """
    return cursor.execute(sql, (query_blob, top_k)).fetchall()
```

---

## 4. Kvalitetsmål
* **Ytelse:** Spørretid < 10 ms for hybridsøk over 50 000 chunks.
* **Sikkerhet:** Bruker parametriserte SQL-spørringer for å forhindre SQL-injection.
