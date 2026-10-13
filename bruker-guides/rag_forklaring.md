
  Dersom du ønsker å teste nye spørsmål eller reindeksere senere:

  • Kjøre RAG-spørringer:
    py rag_ollama_init.py
    # eller
    py -m app.main

  • Kjøre reindeksering ved nye PDF-er i data/raw/:
    py ingest.py
	
# Hva er RAG og hvordan oppdateres RAG-databasen? 

> **En pedagogisk og teknisk guide til RAG (Retrieval-Augmented Generation), arkitektur og inkrementell databasestyring for kommunal AI.**

---

## 1. Hva er RAG? (Enkel forklaring)

**RAG** står for *Retrieval-Augmented Generation*, eller på norsk **Søksberiket generering**.

### 💡 Analogi: Eksamen med åpen bok

Tenk på en kunstig intelligens (LLM som f.eks. Llama 3.1, Qwen 2.5 eller GPT-4) som en student som skal ta en eksamen:

* **Uten RAG (Lukket bok):** AI-en må svare kun basert på det den husker fra sin opprinnelige "skolegang" (trening). Hvis den blir spurt om kommunens økonomireglement, selvkostforskriften eller spesifikke KOSTRA-regler, vil den enten gi et generelt svar, tippe feil, eller dikte opp detaljer (**hallusinasjon**).
* **Med RAG (Åpen bok):** Før AI-en svarer, slår den opp i et **lokalt digitalt oppslagsverk** (databasen med lover, forskrifter og KOSTRA-regler). Den finner den nøyaktige paragrafen, leser den, og former deretter et 100 % presist svar med kildehenvisning.

---

## 2. Visuell Arkitektur & Arbeidsflyt (End-to-End Pipeline)

Diagrammet nedenfor viser hvordan dokumenter prosesseres fra råfiler til søkbar SQLite-vektordatabase, og hvordan spørringer behandles i henhold til kommunens Stage-Gate AI Governance:

```text
========================================================================================
                          DEL 1: DATAINNLADING & CHUNKING (INGESTION)
========================================================================================

 [ Råfiler i data/raw/ ]
  ├── Lover (.pdf)
  ├── Forskrifter (.pdf)
  ├── KOSTRA (.csv)
  └── Årshjul (.md)
          │
          ▼
 [ 1. Tekst- & Metadata-ekstraksjon ] ──► PII-sjekk / Anonymisering (Gate 4)
          │
          ▼
 [ 2. Smart Paragraf-Chunking ] ──────► Deler opp ved §-merker (f.eks. § 14-5)
          │
          ▼
 [ 3. Embedding-generering ] ─────────► multilingual-e5-small (384 float32 vektorer)
          │
          ▼
 [ 4. Hybrid Lagring i SQLite (kommune_rag_store.db) ]
    ├── legal_chunks       (Relasjonal: Tekst, Kilde, Paragraf, Kategori)
    ├── vec_legal_chunks   (Vektorstøtte: sqlite-vec 384-dimensjonale indekser)
    └── legal_fts          (Fulltekstindeks: FTS5 BM25 for eksakte §-treff)

========================================================================================
                          DEL 2: HYBRID SPØRRESLØYFE & AUDIT LOG (RAG)
========================================================================================

 [ Saksbehandler / Bruker ]
          │
          ▼ (Forespørsel)
 [ Hybrid Søkemotor ]
    ├── BM25 (FTS5)   ─────► Eksakte §-treff (f.eks. "§ 14-5")
    └── sqlite-vec    ─────► Semantisk vektor-søk (mening og kontekst)
          │
          ▼
 [ Reciprocal Rank Fusion (RRF) ] ──► Vekting og topp 4 mest relevante §-chunks
          │
          ▼
 [ Prompt Construction ] ─────────► Pakker spørsmål + §-kildekontekst (Glass-Box)
          │
          ▼
 [ Lokal Ollama LLM (Llama 3.1) ] ──► Genererer kildeforankret svar med §-sitering
          │
          ▼
 [ Audit Logging (Gate 9) ] ───────► Skriver til Audit_AI_Actions med SHA-256 hash
```

---

## 3. Hvordan RAG-prosessen fungerer trinn for trinn

### Steg 1: Henting (Retrieval)
Når en saksbehandler stiller et spørsmål (f.eks. *"Hvilke regler gjelder ved budsjettendring i løpet av året?"*), gjør systemet et lynhurtig kombinert søk i databasen:
1. **Eksaktsøk (BM25 / FTS5):** Søker etter spesifikke paragrafer (f.eks. "§ 14-5") og faguttrykk.
2. **Semantisk Vektorsøk (`sqlite-vec`):** Søker etter *meningen* bak spørsmålet, slik at den finner mønstre og regler selv om brukeren ikke brukte de eksakte lovordene.

### Steg 2: Berikelse (Augmentation)
Systemet plukker ut de mest relevante paragrafene (f.eks. Kommuneloven § 14-5) og pakker dem inn som kildekontekst sammen med brukerens spørsmål.

### Steg 3: Generering (Generation)
AI-modellen (f.eks. den lokale Ollama-modellen) leser spørsmålet *sammen med* de hentede kildetekstene, og former et ryddig svar på norsk som oppgir nøyaktige paragrafhenvisninger.

---

## 4. Inkrementell Databasestyring & Re-indeksering

RAG-databasen er dynamisk. Når nye forskrifter vedtas, lover endres, eller gamle veiledere erstattes, må databasen oppdateres uten at hele databasen må re-bygges fra bunnen av.

### Kodesnutt: Inkrementell Oppdatering og Sletting (`update_rag_db.py`)

Følgende skript viser hvordan du programmatisk fjerner utdaterte dokumenter fra **alle tre SQLite-tabellene** (`legal_chunks`, `vec_legal_chunks`, og `legal_fts`), samt re-indekserer nye eller oppdaterte filer:

```python
import sqlite3
import sqlite_vec
from pathlib import Path
from sentence_transformers import SentenceTransformer

DB_PATH = Path("data/db/kommune_rag_store.db")
model = SentenceTransformer("intfloat/multilingual-e5-small")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn

# ---------------------------------------------------------
# 1. SLETT UTDATERT ELLER ERSTATTET DOKUMENT
# ---------------------------------------------------------
def delete_source_file(source_filename):
    """
    Sletter alle poster knyttet til en spesifikk fil fra:
    - legal_chunks (Hovedtabell)
    - vec_legal_chunks (Vektortabell)
    - legal_fts (Fulltekstsøk)
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Hent alle chunk_id-er for denne filen
    cursor.execute("SELECT id FROM legal_chunks WHERE source_file = ?", (source_filename,))
    chunk_ids = [row[0] for row in cursor.fetchall()]
    
    if not chunk_ids:
        print(f"ℹ️ Ingen poster funnet for filen '{source_filename}'.")
        conn.close()
        return 0

    placeholders = ",".join("?" * len(chunk_ids))
    
    # A. Slett fra sqlite-vec vektortabellen
    cursor.execute(f"DELETE FROM vec_legal_chunks WHERE chunk_id IN ({placeholders})", chunk_ids)
    
    # B. Slett fra FTS5 fulltekstindeksen
    cursor.execute(f"DELETE FROM legal_fts WHERE rowid IN ({placeholders})", chunk_ids)
    
    # C. Slett fra hovedtabellen legal_chunks
    cursor.execute("DELETE FROM legal_chunks WHERE source_file = ?", (source_filename,))
    
    conn.commit()
    conn.close()
    print(f"🗑️ Slettet {len(chunk_ids)} chunks knyttet til '{source_filename}' fra alle tabeller.")
    return len(chunk_ids)

# ---------------------------------------------------------
# 2. INKREMENTELL OPPDATERING / RE-INDEKSERING
# ---------------------------------------------------------
def reindex_source_file(source_filename, new_chunks):
    """
    Sletter eksisterende utgave og legger inn ny versjon av et dokument.
    """
    print(f"\n🔄 Starter inkrementell oppdatering for: {source_filename}")
    delete_source_file(source_filename)
    
    conn = get_db()
    cursor = conn.cursor()
    added_count = 0
    
    for item in new_chunks:
        content = item["content"]
        sec_ref = item["section_ref"]
        title = item["title"]
        category = item.get("category", "Oppdatert Bestemmelse")
        
        # Generer ny embedding
        embedding = model.encode(f"passage: {content}", normalize_embeddings=True)
        
        # Sett inn i hovedtabell
        cursor.execute("""
            INSERT INTO legal_chunks (source_file, category, section_ref, title, content)
            VALUES (?, ?, ?, ?, ?)
        """, (source_filename, category, sec_ref, title, content))
        
        chunk_id = cursor.lastrowid
        
        # Sett inn i sqlite-vec
        embedding_blob = sqlite_vec.serialize_float32(embedding)
        cursor.execute("INSERT INTO vec_legal_chunks (chunk_id, embedding) VALUES (?, ?)", (chunk_id, embedding_blob))
        
        # Sett inn i FTS5
        cursor.execute("INSERT INTO legal_fts (rowid, content, section_ref, title) VALUES (?, ?, ?, ?)", (chunk_id, content, sec_ref, title))
        
        added_count += 1
        
    conn.commit()
    conn.close()
    print(f"✅ Inkrementell oppdatering ferdig: Indeksert {added_count} nye chunks for '{source_filename}'.")

# ---------------------------------------------------------
# EKSEMPEL PÅ BRUK:
# ---------------------------------------------------------
if __name__ == "__main__":
    # Eksempel: Erstatt gammel selvkostveileder med ny versjon
    sample_updated_chunks = [
        {
            "section_ref": "§ 3-1",
            "title": "Beregning av indirekte kostnader",
            "content": "Ved beregning av selvkost skal indirekte driftskostnader fordelest etter dokumentert ressursbruk eller hensiktsmessig fordelingsnøkkel.",
            "category": "Forskrift"
        }
    ]
    
    reindex_source_file("Forskrift om beregning av samlet selvkost.pdf", sample_updated_chunks)
```

---

## 5. Hvorfor er denne RAG-arkitekturen trygg for kommunen?

* 🔒 **100 % Lokal og Skjermet:** Med SQLite og Ollama kjører **alt** lokalt på din maskin. Ingen personopplysninger (PII) eller sensitive vurderinger sendes ut på Internett.
* 🛡️ **Null Hallusinasjon (Glass-Box):** AI-en får streng beskjed om *kun* å svare basert på treff i databasen. Hvis svaret ikke står i kildene, sier den fra.
* ⚖️ **Revisjonsklar Audit Trail (Stage-Gate Port 9):** Hver spørring og hentet kilde lagres med en uforanderlig **SHA-256 hash** i tabellen `Audit_AI_Actions`. Kommunerevisjonen kan i ettertid verifisere nøyaktig hva AI-en bygget sine svar på.
