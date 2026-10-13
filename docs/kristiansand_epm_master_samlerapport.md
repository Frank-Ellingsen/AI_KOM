# Kristiansand Kommune — Helhetlig EPM & AI Master-Spesifikasjon

## Executive Summary
Dette dokumentet samler alle tekniske, faglige, juridiske og visuelle spesifikasjoner for innføring av **Enterprise Performance Management (EPM)** og **Kunstig Intelligens (AI)** i Kristiansand kommune.

---

## Innholdsfortegnelse
1. [Rollearkitektur & Supervisor-modell ("The Office")](#1-rollearkitektur--supervisor-modell-the-office)
2. [Det Kommunale Årshjulet 2026 & Operativ Sjekkliste](#2-det-kommunale-årshjulet-2026--operativ-sjekkliste)
3. [AI Governance, Regulering & Anskaffelse (GDPR, EU AI Act, NIS2, CRA)](#3-ai-governance-regulering--anskaffelse)
4. [Teknisk Integrasjon: MCP, Tools, Skills, Hooks & API-er](#4-teknisk-integrasjon-mcp-tools-skills-hooks--api-er)
5. [Framsikt-Integrasjon & Deflator-Beregning](#5-framsikt-integrasjon--deflator-beregning)
6. [Visma ERP-støy & NAV-Etterslepslogikk (Art 1690 vs 1020)](#6-visma-erp-støy--nav-etterslepslogikk)
7. [Internasjonale & Norske Læringspunkter](#7-internasjonale--norske-læringspunkter)
8. [Anbefalte Online-Kurs & Kompetanseutvikling](#8-anbefalte-online-kurs--kompetanseutvikling)
9. [Designsystem for Datavisualisering (10-Sekunders Regelen, RAG & Power BI/Excel)](#9-designsystem-for-datavisualisering)

---

## 1. Rollearkitektur & Supervisor-modell ("The Office")
* **Økonomidirektør (Supervisor):** Overordnet strategisk resultatansvar, politisk innstilling av tertialrapporter og HØP, samt Stage-Gate portgodkjenning (Port 1–10).
* **Rådgiver Økonomistyring (HITL Controller):** Daglig avvikskontroll, nøytralisering av Visma ERP-etterslep (art 1690), What-If scenariomodellering, RAG Glass-Box evaluering og HITL-sign-off.
* **Kommunalsjef & Enhetsledere:** Sektor- og enhetsvis rammestyring, fraværstiltak og omdisponeringer innenfor administrative rammer (§ 4.2).
* **DPO & IT-Sikkerhetsansvarlig:** Overvåking av DPIA, FRIA, PII-skjerming og uforanderlig Audit Log.

---

## 2. Det Kommunale Årshjulet 2026 & Operativ Sjekkliste
Systemet følger de 16 kritiske styringshendelsene i norske kommuner:
* **K1:** KOSTRA-skjemaer og regnskapsinnlevering til SSB (15. jan / 23. feb), Årsrapport 2025 (31. mars).
* **K2:** Revisjonsberetning (15. april), 1. Tertialrapport T1 (25. mai), Revidert Nasjonalbudsjett RNB (2. juni), SSB endelige KOSTRA-tall (15. juni).
* **K3:** HØP-innspill fra sektorer (15. aug), Kommunedirektørens HØP-forslag (23. sept), 2. Tertialrapport T2 (28. sept).
* **K4:** Statsbudsjettet (7. okt), Formannskapets innstilling (25. nov), Bystyrets endelige HØP- og årsbudsjettvedtak (18. des).

**Operativ 8-Stegs Sjekkliste for Controlleren:**
1. Visma-eksport ➔ 2. PII-skjerming (lokal) ➔ 3. Visma-korreksjon i Power BI ➔ 4. What-If simulering i Excel ➔ 5. RAG Glass-Box diagnose ➔ 6. HITL Sign-Off (`APPROVED`/`MODIFIED`/`REJECTED`) ➔ 7. Teams-varsling ➔ 8. Iverksetting i Framsikt og journalføring i Public360.

---

## 3. AI Governance, Regulering & Anskaffelse
* **Kravspesifikasjon (A-Krav & T-Krav):**
  * **A-Krav (Minstekrav):** Forbud mot modelltrening på kommunens data, AES-256/TLS 1.3 kryptering, lokal PII-skjerming, Entra ID SSO med RLS, uforanderlig Audit Log med SHA-256 hash (EU AI Act art. 12/26).
  * **T-Krav (Tildeling):** Evaluering på 0–10 karakterskala fordelt på Funksjon/Kvalitet (35 %), Personvern/Etikk (30 %), M365/Gjennomføring (20 %) og Pris/TCO (15 %).
* **Standarder & Sertifiseringer:** NIS2, Cyber Resilience Act (CRA), ISO/IEC 27001, ISO/IEC 42001, SOC 2 Type II, Eurocities Algorithmic Transparency Standard.

---

## 4. Teknisk Integrasjon: MCP, Tools, Skills, Hooks & API-er
* **MCP (Model Context Protocol):** Standardisert abstraksjonslag.
  * `Excel MCP Server` (COM API for Power Query, DAX og makroer).
  * `Fabric & Power BI MCP Server` (Semantiske modeller og OneLake Direct Lake).
  * `SQL / Database MCP Server` (For `kristiansand_golden_record.db`).
* **Agent Skills:** `data-integration-etl-skill`, `dax-kostra-kpi-skill`, `hitl-governance-skill`.
* **Tools:** `pii_scrubber()`, `fxOpenAI_RAG()`, `post_teams_adaptive_card()`.
* **Hooks:** Pre-execution PII-sjekk, Pre-execution HITL Approval Guardrail, Post-execution SHA-256 Audit Hook.
* **API-er:** Visma REST API, Framsikt REST API, SSB PxWebApi v2, Public360 Sak/Arkiv API.

---

## 5. Framsikt-Integrasjon & Deflator-Beregning
* **Framsikt som Master Data Source:** Budsjett, Endringer, Nøkkeltall, Deflator.
* **Deflator RNB 2026:** Oppjustert fra 3,5 % til **4,1 %** (lønnsvekst 3,6 %, prisvekst 4,9 %), samlet **156 mill. kr** tilført tjenestedistriktene.
* **Formel:**  
  $$\text{Korrigert Ramme} = \text{Vedtatt Budsjett} + \text{Deflator Tillegg (4,1 \%)} + \text{Rammeendringer T1}$$

---

## 6. Visma ERP-støy & NAV-Etterslepslogikk
* **Bruttoprinsippet (Kommuneloven § 14-6):** Vikarer føres på Art 1020, NAV-refusjon på Art 1690.
* **60 dagers etterslep:** Visma-omleggingen i K1 2026 skapte teknisk etterslep på art 1690, som fikk enheter til å fremstå med kunstig stort merforbruk.
* **DAX-Nøytralisering:**  
  $$\text{Reelt Driftsavvik} = \text{Bokført Visma} - \text{Korrigert Ramme (Framsikt)} - \text{Visma NAV-Etterslep}$$

---

## 7. Internasjonale & Norske Læringspunkter
* **Internasjonalt:**
  * **Amsterdam & Barcelona:** Algoritmeregister og åpne etiske kontraktvilkår.
  * **NYC Local Law 144:** Årlig uavhengig bias audit; unngå smutthull ved "rådgivende" definisjoner.
  * **Hellas (National Cadastre):** Azure OpenAI kutter saksbehandlingstid med 2/3 med HITL.
  * **Nederland Riksrevisjonen:** 67 % av offentlige algoritmer feilet på datakvalitet/sikkerhet — krever Stage-Gate.
* **Norge:**
  * **KS 80/20 DPIA:** 80 % av personvernanalysen gjøres nasjonalt, 20 % lokalt.
  * **Helse Vest RHF:** Enkel *opt-out* reservasjonsrett for innbyggere.
  * **Jon Fosse-paradokset:** Modeller må finjusteres mot juridiske og forvaltningsmessige kilder.
  * **Skatteetaten, Vegvesenet, Stortinget:** Suksess ved å avgrense AI til interne saksbehandlerverktøy (HITL).

---

## 8. Anbefalte Online-Kurs & Kompetanseutvikling
* **Coursera:** *IBM AI for FP&A Automation & Modeling*, *University of Michigan Generative AI in Business*, *IBM Building AI Agents*, *Microsoft AI & ML Engineering*.
* **Offentlig sektor:** *Elements of AI*, *AI4GOV*, *Johns Hopkins Center for Govt Excellence*.
* **Etikk & Jus:** *Praxikon / LearnWize EU AI Act & FRIA Training*.

---

## 9. Designsystem for Datavisualisering
* **10-Sekunders Regelen & Aksjonstitler:** "PILOT GRUNNSKOLE: Reelt merforbruk er kun 150 tkr etter at Visma-etterslep på 300 tkr nøytraliseres".
* **Fargesystem:**
  * Mørkeblå (`#1B365D`) = Faktisk regnskap (Visma Bokført)
  * Stålblå (`#4A77A0`) = Budsjett og Framsikt-ramme (inkl. deflator)
  * Mellomgrå (`#95A5A6`) = Visma ERP-etterslep (art 1690)
* **Betinget Formatering (RAG):** 🔴 Merforbruk ($> +2,0 \%$), 🟡 Observasjon ($0-2 \%$), 🟢 Innenfor Ramme ($\le 0 \%$).
* **Interaktivitet:** Slicers, Drill-down (+/-), Betingede Data Bars, Dynamic Tooltips, Ingen hardkoding.
