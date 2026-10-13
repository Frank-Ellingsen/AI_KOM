# 🛡️ Agent Skill: Audit, Governance & Algoritmeregister (`SKILL_AUDIT_GOVERNANCE_REGISTRY`)

> **Versjon:** 1.0  
> **Kategori:** Governance, Compliance & Security  
> **Standard:** Stage-Gate Port 9 & 10, Eurocities Algorithmic Transparency Standard, GDPR Art. 30/35, EU AI Act  

---

## 🎯 Formål
Dette agent-skill-et forvalter **uforanderlig revisjonslogging (SHA-256 Audit Trail)**, kontinuerlig overvåking av AI-modeller, samt automatisert registrering og oppdatering av kommunens offentlige **Algoritmeregister**.

---

## 📐 Funksjonalitet & Arbeidsflyt

### 1. Kryptografisk Audit Logging (Stage-Gate Port 9)
Hver gang AI-assistenten genererer et svar eller utfører et oppslag, registreres transaksjonen i SQLite-tabellen `Audit_AI_Actions`:

```sql
INSERT INTO Audit_AI_Actions (
    user_query, 
    retrieved_chunk_ids, 
    llm_response, 
    user_action, 
    sha256_hash
) VALUES (?, ?, ?, 'APPROVED', ?);
```

Fingeravtrykket beregnes som:  
`sha256_hash = SHA256(user_query + "|" + json(chunk_ids) + "|" + llm_response + "|" + timestamp)`

### 2. Eurocities Algoritmeregister Schema (Stage-Gate Port 10)
Genererer standardisert JSON-eksport for kommunens åpne algoritmeregister (innbyggerinnsyn):

```json
{
  "system_id": "KRISTIANSAND-AI-RAG-001",
  "system_name": "Rådgivende AI-Assistent for Økonomi og Regelverk",
  "owner_department": "Økonomi og virksomhetsstyring",
  "purpose": "Beslutningsstøtte og regelverks-RAG for saksbehandlere",
  "legal_basis": "Kommuneloven § 13-1 / Forvaltningsloven",
  "human_oversight": "Human-in-the-Loop (100 % manuell godkjenning av vedtak)",
  "data_sources": ["Kommuneloven", "KOSTRA-forskriften", "Økonomireglement", "Visma ERP", "Framsikt EPM"],
  "pii_handling": "Lokal maskering og vasking før oppslag",
  "audit_trail_status": "SHA-256 Immutable SQLite Storage"
}
```

### 3. Rapportering til Kommunerevisjonen
Klarerer uttrekk av verifiserbare audit-logger for Kontrollutvalget og Kommunerevisjonen ved forespørsel.
