# 🛡️ Kommunalt Stage-Gate Rammeverk for AI-Styring (Governance)

> **En generisk, strukturert styringsmodell for risikohåndtering, etikk, personvern og juridisk etterrettelighet i kommunale AI-prosjekter.**

---

## 📋 Innledning og Formål

Kommunale virksomheter forvalter offentlig myndighet, personopplysninger og felles fellesskapsressurser. **Stage-Gate rammeverket** sikrer at AI-initiativer ikke rulles ut ukontrollert, men gjennomgår systematisk tverrfaglig evaluering i ti definerte beslutningsporter (*gates*).

Modellen er tilpasset kravene i:
* **EU AI Act** (Art. 27 FRIA - Fundamental Rights Impact Assessment)
* **GDPR** (Art. 35 DPIA - Data Protection Impact Assessment)
* **Kommuneloven** (Internkontroll, anordningsprinsipp og delegering)
* **Offentleglova** (Åpenhet og rett til innsyn)

---

## 🚪 Oversikt over Beslutningsportene (Gate 1 – 10)

```text
[ Gate 1–3: Behov, Nytte & Etikk ] ──► [ Gate 4–5: PII-Vask & Leveransemodell ]
                                                      │
                                                      ▼
[ Gate 10: Algoritmeregister ] ◄── [ Gate 9: HITL & SHA-256 Audit Log ] ◄── [ Gate 6–8: Sandkasse, DPIA/FRIA & Reglement ]
```

| Port / Gate | Hovedfokus & Arbeidsfase (*Stage*) | Krav & Leveranser |
| :--- | :--- | :--- |
| **Gate 1: Organisasjonsgrunnlag** | Avklare strategisk forankring, ressurser og kompetanse. | Lederforankring, prosjektmandat og oppnevning av tverrfaglig team. |
| **Gate 2: Problemdefinisjon** | Definisjon av bruksområde (*use case*) og gevinstpotensial. | Konkretisering av brukerbehov, måleparametere og forventet samfunnsnytte. |
| **Gate 3: Etisk Screening** | Evaluering av etiske prinsipper, åpenhet og likebehandling. | Etisk egenvurdering jf. nasjonale retningslinjer for ansvarlig AI. |
| **Gate 4: Datastyring & PII** | Kartlegging av datakilder, eierskap og PII-skjerming. | Datakvalitetsanalyse og etablering av automatisk PII-vasking (fødselsnummer, navn). |
| **Gate 5: Leveransemodell** | Valg av arkitektur (Hybrid: Gemini med automatisk PII-skjold for lav CPU-belastning vs. lokal Ollama for isolerte miljøer) og vilkår. | Vurdering av datasuverenitet, maskinvarekrav (CPU/GPU-belastning), avtalevilkår og TCO (totalkostnad). |
| **Gate 6: Testing & Sandkasse** | Utprøving og validering i lukkede testmiljøer (*sandboxes*). | Pilotering med anonymiserte data, måling av treffsikkerhet og hallusinasjonsfrekvens. |
| **Gate 7: Risikovurdering** | Tvingende konsekvens- og risikovurderinger. | Utfylt **DPIA** (GDPR Art. 35) og **FRIA** (EU AI Act Art. 27), samt bias-analyse. |
| **Gate 8: Policy & Reglement** | Forankring i kommunale reglementer og delegeringsfullmakter. | Juridisk validering mot Kommuneloven, offentleglova og kommunens økonomireglement. |
| **Gate 9: Operativ Drift & HITL** | Produksjonssetting med **Human-in-the-Loop** og **Audit Log**. | Sikre at AI kun gir forslag, samt registrere alle spørringer med kryptografisk **SHA-256 hash**. |
| **Gate 10: Overvåking & Innsyn** | Kontinuerlig overvåking, modellvedlikehold og innbyggerinnsyn. | Registrering i offentlig **Algoritmeregister** og årlig revisjon for Kommunerevisjonen. |

---

## ⚡ Skalert Modell (Minimum Viable Stage-Gate Pathway)

For mindre kommuner eller avgrensede prosjekter tillater rammeverket en skalert snarvei bestående av de 5 mest kritiske portene:

1. **Gate 1 (Behov & Forankring):** Behovsavklaring og ledelsesforankring.
2. **Gate 3 (Etisk screening):** Hurtigvurdering av innbyggerrettigheter.
3. **Gate 4 (Datastyring & PII):** Sikre at ingen følsomme personopplysninger lekker.
4. **Gate 7 (DPIA & FRIA):** Gjennomføre lovpålagte risikovurderinger.
5. **Gate 9 (Human-in-the-Loop):** Garanti for at menneske fatter alle endelige beslutninger.

---

## 🔍 Revisjonssporbarhet (SHA-256 Audit Trail)

I Gate 9 kreves det at alle RAG-oppslag lagres i en uforanderlig tabell (`Audit_AI_Actions`) med følgende struktur:

```sql
CREATE TABLE Audit_AI_Actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT NOT NULL,
    retrieved_chunk_ids TEXT NOT NULL,
    llm_response TEXT NOT NULL,
    sha256_hash TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Dette gjør det mulig for **Kommunerevisjonen** og **Kontrollutvalget** å etterprøve nøyaktig hvilke kilder og logikk AI-modellen bygde sine svar på ved et gitt tidspunkt.
