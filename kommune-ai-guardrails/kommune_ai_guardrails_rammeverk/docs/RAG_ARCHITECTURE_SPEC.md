# ⚙️ Teknisk Spesifikasjon — Lokal Hybrid RAG-Arkitektur

> **Detaljert spesifikasjon av RAG-motoren for produksjonsklar, hybrid søke- og genereringsteknologi med SQLite-vec, FTS5 og lokal Ollama LLM.**

---

## 🏗️ Arkitekturoversikt

RAG-motoren kombinerer tre utfyllende søke- og rangeringsteknikker for å oppnå maksimal presisjon på tvers av lover, forskrifter, kontoplaner og politiske vedtak:

1. **BM25 / FTS5 Fulltekstsøk:** Fanger opp eksakte paragrafhenvisninger (§), tallkoder, kontonumre og spesifikke faguttrykk.
2. **Semantisk Vektorsøk (`sqlite-vec`):** Fanger opp den matematiske og konseptuelle meningen i spørsmålet via 384-dimensjonale embeddings.
3. **Reciprocal Rank Fusion (RRF):** Fletter resultatene fra BM25 og vektorsøket sammen til én rangert resultatliste.

```text
[ Spørsmål fra bruker ]
         │
         ├───► [ FTS5 / BM25 Eksattsøk ] ────┐
         │                                   ├───► [ RRF Rangering ] ──► [ Top-K Chunks ] ──► [ Ollama LLM ]
         └───► [ sqlite-vec Vektorsøk ] ─────┘
```

---

## 📊 Databasestruktur (SQLite Schema)

Databasen opprettes som én enkelt uavhengig fil (`data/db/kommune_rag_store.db`) og benytter tre koblede tabeller:

```sql
-- 1. Hovedtabell for kildetekst og metadata
CREATE TABLE IF NOT EXISTS legal_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    category TEXT NOT NULL,
    section_ref TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Vektortabell via sqlite-vec extension (384-dimensjoner for e5-small)
CREATE VIRTUAL TABLE IF NOT EXISTS vec_legal_chunks USING vec0(
    chunk_id INTEGER PRIMARY KEY,
    embedding float[384]
);

-- 3. Fulltekstindeks via FTS5
CREATE VIRTUAL TABLE IF NOT EXISTS legal_fts USING fts5(
    title,
    content,
    content='legal_chunks',
    content_rowid='id'
);
```

---

## 🔀 Hybrid RRF (Reciprocal Rank Fusion) Logikk

RRF beregner en felles poengsum for hver kilde-chunk basert på dens plassering i både BM25 og vektorsøket:

$$RRF\_Score(d) = \frac{1}{k + Rank_{BM25}(d)} + \frac{1}{k + Rank_{Vector}(d)}$$

der konstantverdien $k$ settes til **60**. De $K$ øverste chunkene med høyest RRF-score sendes videre som kontekst til Ollama.

---

## 🦙 Ollama LLM Integrasjon & Glass-Box Prompting

Når de relevante kilde-chunkene er hentet ut, pakkes de inn i et strengt forankret system-prompt:

```python
system_prompt = """Du er en spesialisert rådgiver for kommunal forvaltning.
Besvar brukerens spørsmål basert UTLUKKENDE på den oppgitte kildekonteksten.

STRENGE REGLER:
1. Svaret må være 100 % forankret i de oppgitte kildene.
2. Du må eksplisitt sitere kildene og paragrafer i svaret (f.eks. "Jfr. Kommuneloven § 14-5...").
3. Dersom kildene ikke gir tilstrekkelig svar, sier du: "Finner ikke tilstrekkelig hjemmel for dette i regelverksdatabasen."
4. Svar på et ryddig, profesjonelt norsk språk.
"""
```

---

## 🔄 Inkrementell Oppdatering og Sletting (Data Lifecycle)

Dersom en forskrift eller veiledende dokument utgår eller oppdateres, må det kunne fjernes atomisk fra alle tre tabeller samtidig:

```python
def delete_source_file(conn, source_filename):
    """Sletter alle chunks, vektorer og FTS-indekser knyttet til en kildefil."""
    cursor = conn.cursor()
    # 1. Hent ID-er
    cursor.execute("SELECT id FROM legal_chunks WHERE source_file = ?", (source_filename,))
    ids = [row[0] for row in cursor.fetchall()]
    
    if not ids:
        return 0
        
    placeholders = ",".join("?" * len(ids))
    # 2. Slett fra vektortabell
    cursor.execute(f"DELETE FROM vec_legal_chunks WHERE chunk_id IN ({placeholders})", ids)
    # 3. Slett fra FTS
    cursor.execute(f"DELETE FROM legal_fts WHERE rowid IN ({placeholders})", ids)
    # 4. Slett fra hovedtabell
    cursor.execute("DELETE FROM legal_chunks WHERE source_file = ?", (source_filename,))
    conn.commit()
    return len(ids)
```
