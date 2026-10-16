# 🌐 Generisk Enterprise AI Pilot-Pakke (Vendor-Neutral)
**Standardisert malverk for AI-piloter i kommunal og offentlig sektor**  
**Sist oppdatert:** 16. oktober 2026 | **Versjon:** 1.0 (Enterprise Template)  
**Målgruppe:** Kommunedirektører, økonomidirektører, IT-arkitekter, personvernombud og prosjektcontrollere.

---

## 🎯 Formål og Konsept

Denne pakken representerer et **leverandøruavhengig (vendor-neutral) og flyttbart malverk** for å etablere, styre og evaluere AI-piloter innen økonomi og virksomhetsstyring. Den er designet for å kunne tas i bruk av enhver kommune, fylkeskommune eller offentlig etat ved å erstatte variabler som `[VIRKSOMHETENS NAVN]` og `[HOVEDKONTOR]`.

Pakken ivaretar kravene i:
* **EU AI Act** (Art. 26/27 om idriftsetters plikter og risikostyring)
* **GDPR & Personopplysningsloven** (Art. 22 om automatiserte avgjørelser, Art. 35 DPIA)
* **Digitaliseringsdirektoratet (Digdir) & KS** retningslinjer for ansvarlig AI i offentlig sektor
* **ISO 42001 (Artificial Intelligence Management System - AIMS)**

---

## 📂 Mappestruktur: `enterprise-ai-pilot/`

Hovedinnholdet ligger i undermappen [`enterprise-ai-pilot/`](./enterprise-ai-pilot/README.md):

```text
generic-ai-pilot-pakke/
└── enterprise-ai-pilot/
    ├── README.md                            <-- Single Source of Truth (SSOT) Masteroversikt
    ├── data/
    │   └── README_DATA_PRIVACY.md           <-- Retningslinjer for syntetiske data og personvern
    ├── dax_and_analytics/
    │   └── 01_generisk_dax_og_rag_formatering.dax <-- Generiske DAX-avviksmålinger & RAG-formatering
    ├── docs/
    │   ├── architecture/
    │   │   └── 01_maalarkitektur-okonomi-ai-kristiansand.md <-- Enterprise AI Blueprint & MLOps
    │   ├── financials/
    │   │   ├── 01_folsomhetsanalyse-gevinstmodell-ai.md     <-- Gevinstkalkyle & 3-års FinOps
    │   │   └── 02_folsomhetsanalyse-diagram.png             <-- Visuelt følsomhetsdiagram
    │   ├── governance/
    │   │   ├── 01_saksframlegg-ai-veikart-okonomi.md        <-- Politisk saksfremlegg (Veikart)
    │   │   └── 02_cheat-sheet-sponsormote-ai.md             <-- 1-sides kort til toppledelsesmøte
    │   ├── pilot_and_ops/
    │   │   └── 01_oppstartsnotat-pilotgruppe-ai.md          <-- Veiledning for pilotgruppen (Uke 1–8)
    │   └── security_and_legal/
    │       └── 01_risikovurdering-og-evalueringsskjema-ai-pilot.md <-- DPIA/FRIA & loggsjekk
    ├── evals/
    │   └── 01_ground_truth_eval_template.json       <-- Fasit-testsett for RAG-evaluering
    └── prompts/
        └── 01_promptsett-m365-copilot-kostra.md     <-- Mønsterprompter for Excel, BI og Teams
```

---

## 📋 Oversikt over Kjernedokumentene

| Kategori | Fil | Tittel & Beskrivelse | Målgruppe |
| :--- | :--- | :--- | :--- |
| **SSOT** | [`README.md`](./enterprise-ai-pilot/README.md) | **Single Source of Truth** for enterprise-piloten | Prosjekteier |
| **Arkitektur** | [`docs/architecture/01_maalarkitektur...`](./enterprise-ai-pilot/docs/architecture/01_maalarkitektur-okonomi-ai-kristiansand.md) | **Enterprise AI Målarkitektur**: AI Gateway, PII-filter og Zero Trust | IT-arkitekter |
| **Finans** | [`docs/financials/01_folsomhetsanalyse...`](./enterprise-ai-pilot/docs/financials/01_folsomhetsanalyse-gevinstmodell-ai.md) | **Gevinstmodell & Følsomhetsanalyse**: Break-even, ROI og FinOps | Controllere |
| **Governance** | [`docs/governance/01_saksframlegg...`](./enterprise-ai-pilot/docs/governance/01_saksframlegg-ai-veikart-okonomi.md) | **Politisk Saksfremlegg**: AI-veikart for økonomi og virksomhetsstyring | Kommunedirektør |
| **Sponsormøte** | [`docs/governance/02_cheat-sheet...`](./enterprise-ai-pilot/docs/governance/02_cheat-sheet-sponsormote-ai.md) | **Cheat Sheet**: 1-sides beslutningsstøtte til toppledelsessponsor | Prosjektleder |
| **Pilotdrift** | [`docs/pilot_and_ops/01_oppstartsnotat...`](./enterprise-ai-pilot/docs/pilot_and_ops/01_oppstartsnotat-pilotgruppe-ai.md) | **Oppstartsnotat for Pilotgruppen**: Husregler, 100% HITL, read-only | Superbrukere |
| **Juss & Risiko** | [`docs/security_and_legal/01_risikovurdering...`](./enterprise-ai-pilot/docs/security_and_legal/01_risikovurdering-og-evalueringsskjema-ai-pilot.md) | **Risikovurdering & Evalueringsskjema**: FRIA, DPIA, etikk og avvik | Jurister & DPO |
| **Kvalitet (Eval)** | [`evals/01_ground_truth_eval_template.json`](./enterprise-ai-pilot/evals/01_ground_truth_eval_template.json) | **Ground Truth Fasitsett**: Kriterier for Faithfulness og Recall | QA-team |
| **Prompter** | [`prompts/01_promptsett-m365-copilot-kostra.md`](./enterprise-ai-pilot/prompts/01_promptsett-m365-copilot-kostra.md) | **Mønsterprompter**: KOSTRA, vikaravvik, overtid og scenarier | Økonomirådgivere |
| **Analytics/DAX** | [`dax_and_analytics/01_generisk_dax...`](./enterprise-ai-pilot/dax_and_analytics/01_generisk_dax_og_rag_formatering.dax) | **Generisk DAX-kode**: Korrigert avvikslogikk og RAG-formatering | BI-utviklere |

---

## 🚀 Hvordan ta i bruk pakken i din virksomhet

1. **Kopier mappen:** Kopier [`enterprise-ai-pilot/`](./enterprise-ai-pilot/) til et eget prosjekt- eller pilot-repositorium.
2. **Søk og erstatt parametere:**
   * `[VIRKSOMHETENS NAVN]` $\rightarrow$ Navnet på din kommune/virksomhet.
   * `[HOVEDKONTOR]` $\rightarrow$ Lokasjon (f.eks. *Rådhuset*).
   * Tilpass ERP-system (Visma, Unit4, Agresso, Xledger).
3. **Konfigurer Ground Truth:** Legg inn organisasjonens egne økonomireglement og attestasjonsinstrukser i `evals/01_ground_truth_eval_template.json`.
4. **Iverksett Bølge 1 Pilot:** Følg tidsplanen i oppstartsnotatet (Uke 1–8).
