# 🤖 Kommune AI Agenter — Økonomi- og Virksomhetsstyring

Dette biblioteket inneholder den operative agentarkitekturen for **Kommune AI Guardrails** i Kristiansand kommune. Agentene er modulære, spesialiserte personas som samhandler for å automatisere dataintegrasjon, avviksdeteksjon, prognostisering, juridisk etterlevelse og ledelsesrapportering.

---

## 🧭 Samlet Agentmatrise (1–12)

| Nr. | Agentfil | Domene / Rolle | Nøkkelteknologi & Lovverk |
| :--- | :--- | :--- | :--- |
| **01** | [`01_dataintegrasjon_etl_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/01_dataintegrasjon_etl_agent.md) | **ETL & Golden Record**<br>Datainntak og validering | SQLite / DuckDB, SHA-256 deduplisering, Kommuneloven § 14-6, KOSTRA |
| **02** | [`02_bi_dax_modellering_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/02_bi_dax_modellering_agent.md) | **Power BI & DAX Modellerer**<br>Stjerneskjema og ytelsesoptimalisering | Star Schema, DAX Time Intelligence, VertiPaq, `ISINSCOPE` |
| **03** | [`03_prediktiv_anomali_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/03_prediktiv_anomali_agent.md) | **Prediktiv & Avviksdeteksjon**<br>Tidligvarsling 60–90 dager før tertial | Z-score, rullende tidsserier, sesongjustering, NAV-refusjonsfilter |
| **04** | [`04_preskriptiv_hitl_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/04_preskriptiv_hitl_agent.md) | **Preskriptiv Beslutningsstøtte**<br>Human-in-the-Loop (HITL) tiltaksmeny | Delegasjonsreglementet, `Audit_AI_Actions`, formannskapsfullmakter |
| **05** | [`05_etikk_styring_portvakt_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/05_etikk_styring_portvakt_agent.md) | **Etikk, Risiko & Portvakt**<br>10 Stage-Gate styringsrammeverk | EU AI Act (FRIA), GDPR (DPIA), Hovedavtalen § 4, vetorett |
| **06** | [`06_ledelsesrapport_skribent_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/06_ledelsesrapport_skribent_agent.md) | **Ledelsesrapportør & Ghostwriter**<br>Saksfremlegg og direktørnotater | Formelt forvaltningsspråk, tertialnotater, politisk saksbehandling |
| **07** | [`07_excel_powerbi_rapportering_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/07_excel_powerbi_rapportering_agent.md) | **Excel & Power BI Ekspert**<br>FAST Financial Standard og dashboards | FAST Financial Modelling, Query Folding, Tufte visual vocabulary |
| **08** | [`08_flerniva_interessent_rapportering_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/08_flerniva_interessent_rapportering_agent.md) | **Flernivå Interessentrapportør**<br>Tilpasset rapportering nivå 1–5 | Enhetsleder $\rightarrow$ Kommunalsjef $\rightarrow$ Økonomidirektør $\rightarrow$ Kommunedirektør $\rightarrow$ Bystyret |
| **09** | [`09_prosjektcontroller_eac_etc_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/09_prosjektcontroller_eac_etc_agent.md) | **Prosjektcontroller & Investering**<br>EVM, EAC/ETC, Capex og S-kurver | Kontoklasse 2, Earned Value ($CPI$, $SPI$), P50/P85 usikkerhet, Tufte S-kurve |
| **10** | [`10_likviditet_finans_renteeksponering_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/10_likviditet_finans_renteeksponering_agent.md) | **Likviditet, Finans & Renterisiko**<br>Gjeldsportefølje og rentestresstesting | Finansforskriften, NIBOR-sensitivitet (+/- bps), gjeldstak (8,8 mrd. kr) |
| **11** | [`11_selvkost_gebyr_kalkyle_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/11_selvkost_gebyr_kalkyle_agent.md) | **Selvkost, Gebyrregulativ & Fond**<br>Full kostnadsdekning og kalkylerente | Selvkostforskriften, 5-årsregelen, 5-årig swaprente + 0,50 %, VAR-sektoren |
| **12** | [`12_revisjon_internkontroll_sporbarhet_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/12_revisjon_internkontroll_sporbarhet_agent.md) | **Revisjon & Mislighetskontroll**<br>Kontrollutvalget og revisjonsspor | Kommuneloven kap. 25, Anskaffelsesloven (FOA), Benfords lov, SHA-256 bevis |
| **13** | [`13_evaluering_kvalitetssikring_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/13_evaluering_kvalitetssikring_agent.md) | **Evaluering & Kvalitetssikring (QA)**<br>Golden Dataset, RAG-evaluering, LLM-as-a-Judge | Evals over vibes, Recall@k, Faithfulness, Trajectory loop check, 90 % CI/CD Gate |
| **14** | [`14_database_data_engineering_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/14_database_data_engineering_agent.md) | **Database & Data Engineering**<br>Optimalisering, hybridsøk og sikkerhet | Read-Only default, Parameterized SQL, FTS5 + sqlite-vec, EXPLAIN QUERY PLAN, PII-vask |
| **15** | [`15_ai_engineering_infrastruktur_agent.md`](file:///c:/Users/frank/Desktop/AI_KOM/agenter/15_ai_engineering_infrastruktur_agent.md) | **AI Engineering & Infrastruktur**<br>4-lags arkitektur, semantisk cache og ruting | Systems first/models second, kontekstkomprimering, Ollama/Gemini ruting, TTFT/latens |

---

## 🔄 End-to-End Arbeidsflyt og Dataflyt

```text
  [ERP: Visma / Framsikt / Agresso / SSB]
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────┐
  │  01_dataintegrasjon_etl_agent (Golden Record SQLite/Vec) │
  └──────────────────────────┬───────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│ 02_bi_dax_modellering   │       │ 09_prosjektcontroller   │
│ (Drift / Kontoklasse 1) │       │ (Investering / Klass 2) │
└───────────┬─────────────┘       └───────────┬─────────────┘
            │                                 │
            ├─────────────────┬───────────────┤
            ▼                 ▼               ▼
┌──────────────────────┐ ┌───────────────┐ ┌───────────────┐
│ 03_prediktiv_anomali │ │ 10_likviditet │ │ 11_selvkost   │
└───────────┬──────────┘ └───────┬───────┘ └───────┬───────┘
            │                    │                 │
            ▼                    ▼                 ▼
  ┌──────────────────────────────────────────────────────────┐
  │ 04_preskriptiv_hitl_agent (Tiltaksmeny & Saksbehandler) │
  └──────────────────────────┬───────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│ 05_etikk_styring_port   │       │ 12_revisjon_internktrl  │
│ (Stage-Gate / FRIA/DPIA)│       │ (SHA-256 Revisjonsspor) │
└───────────┬─────────────┘       └───────────┬─────────────┘
            │                                 │
            └────────────────┬────────────────┘
                             ▼
  ┌──────────────────────────────────────────────────────────┐
  │ 13_evaluering_kvalitetssikring (90% CI/CD Gate, Evals)   │
  │ 14_database_data_eng (Hybridsøk, Schema, PII-vask)       │
  │ 15_ai_engineering_infra (4-Layer, Caching, LLM-Routing) │
  └──────────────────────────┬───────────────────────────────┘
                             ▼
  ┌──────────────────────────────────────────────────────────┐
  │ 06_ledelsesrapport_skribent & 08_flerniva_rapportering   │
  │     (Formannskap, Bystyre, Kommunedirektør & Enheter)    │
  └──────────────────────────────────────────────────────────┘
```

---

## 📊 Datavisualiseringsstandarder (Edward Tufte)
Alle agenter som produserer tabeller, diagrammer eller rapporter skal overholde:
- **Høy data-blekk-faktor (Data-Ink Ratio):** Fjern unødvendige 3D-elementer, bakgrunnsskygger og fargerike gradienter.
- **Ingen vertikale gitterlinjer:** Tabeller og S-kurver skal være åpne og ryddige.
- **Direkte merking:** Skriv forklarende etiketter direkte på linjene i S-kurver og tidsserier fremfor separate fargebokser.
- **Dempede farger:** Nøytrale gråtoner og marineblått som basisfarger. Rødt eller ravgult (amber) reserveres utelukkende for aktive avvik eller brudd på handlingsregler.
- **Tallformatering:** Venstrejustert tekst, høyrejusterte tall med konsistente desimaler og tusenseparatorer.
