# Antigravity AI Pilot — Single Source of Truth (SSOT)
**Prosjekt:** Virksomhetsstyrt AI for Økonomi og Virksomhetsstyring  
**Virksomhet:** [VIRKSOMHETENS NAVN] (Stabsområde [HOVEDKONTOR])  
**Sist oppdatert:** 16. oktober 2026  
**Status:** Klar for Beslutningsport G2 (Pilot-oppstart)

---

## 📂 Mappe- og Prosjektstruktur (Context-Optimized)

```text
enterprise-ai-pilot/
├── README.md                            <-- Single Source of Truth (SSOT) Hovedindeks
├── data/                                <-- Skjermet test-sett og personvernpolicy
│   └── README_DATA_PRIVACY.md
├── dax_and_analytics/                   <-- Vendor-nøytrale DAX-målinger & RAG-formatering
│   └── 01_generisk_dax_og_rag_formatering.dax
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
└── evals/                               <-- RAGAS-konfigurasjon, Ground Truth fasit-sett, CI/CD-tester
    └── 01_ground_truth_eval_template.json
```

---

## 🎯 Kjerneingredienser i Prosjektpakken

1. **Governance & Mandat:** Inneholder formelt saksfremlegg og sponsorkort til Kommunedirektøren.
2. **Arkitektur & Sikkerhet:** Beskriver Zero Trust Control Plane med AI Gateway, PII-anonymisering og arvet tilgangsstyring (RBAC/ABAC) via Entra ID.
3. **Juss & Compliance:** Dekker EU AI Act art. 26/27 (Deployer-krav), DPIA jf. GDPR art. 35, FRIA og Forvaltningsloven § 25.
4. **Menneskelig Kontroll (HITL):** Håndhever *Human-in-the-Loop* med 0 % feiltoleranse på regnskapstall.
5. **Finansiell Følsomhet:** Dokumenterer +1,06 mill. kr netto årlig gevinst, 4,9 måneders payback og 12,9 % break-even utaksgrad.
6. **M365 Copilot Promptsett:** Skriveklare prompter for Excel (`=PY`), Power BI / Fabric IQ i Teams og Word/PowerPoint.
