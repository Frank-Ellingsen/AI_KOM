# 🔄 Agent Skill: Data Integration & ETL Pipeline (`SKILL_DATA_INTEGRATION_ETL`)

> **Versjon:** 1.0  
> **Kategori:** Data Engineering & Pipeline  
> **Standard:** Star Schema Standardization, Idempotent Processing, PII Masking  

---

## 🎯 Formål
Dette agent-skill-et orkestrerer datainnlading, vasking, PII-skjerming og harmonisering fra eksterne fagsystemer (**Visma ERP, Framsikt EPM, SSB API, CSV/Excel**) inn i kommunens sentrale **SQLite Star Schema** (`Fact_Regnskap`, `Fact_Budsjett`, `Dim_*`).

---

## 📐 Ingestion-steg & Transformasjonsregler

### 1. Kildeadaptere & Formater
* **Visma ERP (Regnskapstext/CSV):** Parser bilag, poster, art, funksjon, ansvar og beløp.
* **Framsikt EPM (Budsjett/Prognose):** Parser periodiserte rammekall, tertialjusteringer og HØP-tall.
* **SSB API (KOSTRA-tall):** Henter nasjonale og regionaliserte nøkkeltall via SSB sitt JSON-STAT API.

### 2. Transformasjonssteg i Python
1. **PII-Skjerming (Port 4):** Fjerner navn, fødselsnumre og fritekstmerknader som kan inneholde personopplysninger.
2. **Nøkkel-Harmonisering:** Sjekker og mapper `funksjon_kode` mot `Dim_Funksjon` og `art_kode` mot `Dim_Art`.
3. **SHA-256 Transaksjonshash:** Genererer unikk ID per linje for å forhindre duplikater:
   `transaksjon_id = SHA256(kilde + dato + funksjon + art + ansvar + belop)`
4. **Idempotent Insetting:** Bruker `INSERT OR REPLACE INTO` i SQLite.

```python
# Eksempel på Idempotent ETL pipeline
def ingest_visma_csv(conn, csv_path):
    import pandas as pd
    import hashlib
    
    df = pd.read_csv(csv_path)
    # Perform transformation & PII wash
    # Insert to Fact_Regnskap
```
