# 🚀 Antigravity & Microsoft 365 Copilot AI Pilot — Subproject
**Single Source of Truth (SSOT) & Operasjonelt Subprosjekt**  
**Prosjekt:** Virksomhetsstyrt AI for Økonomi og Virksomhetsstyring  
**Virksomhet:** Kristiansand kommune (Stabsområde Rådhusgata 18)  
**Lead Controller & Prosjekteier:** Frank Ellingsen  
**Sist oppdatert:** 16. oktober 2026 | **Status:** Klar for Beslutningsport G2 (Pilot-oppstart)

---

## 📂 Mappe- og Prosjektstruktur (Context-Optimized Subproject)

```text
antigravity-ms-pilot/
├── README.md                            <-- Single Source of Truth (SSOT) Hovedindeks
├── pyproject.toml                       <-- Standalone subprosjekt-konfigurasjon
├── requirements.txt                     <-- Subprosjekt Python-avhengigheter
├── run_pilot.py                         <-- Operativt CLI-kjøreverktøy for compliance & tester
├── src/                                 <-- Operasjonell kildekode for AI Gateway & RAG
│   ├── gateway/                         <-- PII-skjerming & FinOps Token Rate Limiter
│   │   ├── __init__.py
│   │   └── pii_scrubber.py
│   ├── rag/                             <-- Hybrid-søk (BM25 + Paragraf) & Table-Aware Chunking
│   │   ├── __init__.py
│   │   └── hybrid_retriever.py
│   └── utils/                           <-- SHA-256 kryptografisk revisjonslogger (Port 9)
│       ├── __init__.py
│       └── audit_logger.py
├── tests/                               <-- Subprosjektets automatiserte testsuite
│   └── test_pilot_subproject.py
├── docs/
│   ├── governance/                      <-- Politiske sakspapirer, mandat, sponsorkort, RACI
│   │   ├── 01_saksframlegg-ai-veikart-okonomi.md
│   │   └── 02_cheat-sheet-sponsormote-ai.md
│   ├── architecture/                    <-- Technical Blueprint, Enterprise AI Gateway, MLOps
│   │   └── 01_maalarkitektur-okonomi-ai-kristiansand.md
│   ├── security_and_legal/              <-- Compliance, DPIA, FRIA, EU AI Act, Loggsjekk
│   │   └── 01_risikovurdering-og-evalueringsskjema-ai-pilot.md
│   ├── pilot_and_ops/                   <-- Operativveiledning, superbruker-instruks, husregler
│   │   └── 01_oppstartsnotat-pilotgruppe-ai.md
│   └── financials/                      <-- Følsomhetsanalyse, FinOps, Gevinstmodell
│       ├── 01_folsomhetsanalyse-gevinstmodell-ai.md
│       └── 02_folsomhetsanalyse-diagram.png
├── prompts/                             <-- Kvalitetssikrede mønster-prompter for M365 Copilot & RAG
│   └── 01_promptsett-m365-copilot-kostra.md
├── evals/                               <-- RAGAS-konfigurasjon, Ground Truth fasit-sett, CI/CD-tester
│   └── 01_ground_truth_eval_template.json
└── data/                                <-- Skjermet test-sett og KOSTRA-kontoplan-referanser
    └── README_DATA_PRIVACY.md
```

---

## 🎯 Kjerneingredienser i Subprosjektet

1. **Governance & Mandat:** Inneholder formelt saksfremlegg og sponsorkort til Kommunedirektøren.
2. **Arkitektur & Sikkerhet:** Beskriver Zero Trust Control Plane med AI Gateway, PII-anonymisering og arvet tilgangsstyring (RBAC/ABAC) via Entra ID.
3. **Juss & Compliance:** Dekker EU AI Act art. 26/27 (Deployer-krav), DPIA jf. GDPR art. 35, FRIA og Forvaltningsloven § 25.
4. **Menneskelig Kontroll (HITL):** Håndhever *Human-in-the-Loop* med 0 % feiltoleranse på regnskapstall.
5. **Finansiell Følsomhet:** Dokumenterer +1,06 mill. kr netto årlig gevinst, 4,9 måneders payback og 12,9 % break-even utaksgrad.
6. **M365 Copilot Promptsett:** Skriveklare prompter for Excel (`=PY`), Power BI / Fabric IQ i Teams og Word/PowerPoint.
7. **Operasjonell Python-motor:** Komplett implementasjon i `src/` for PII-maskering, hybrid-søk med tabellbevaring, FinOps token-begrenser og SHA-256 revisjonsstempling.

---

## ⚡ Hurtigkommandoer for Subprosjektet

Kjør verktøyene direkte fra subprosjektets rotmappe:

```bash
# Kjør operasjonell compliance- og PII-sjekk med revisjonsstempel
python run_pilot.py --check-compliance

# Kjør den automatiserte testsuiten for subprosjektet
python run_pilot.py --test
# eller direkte via pytest
pytest tests/
```
