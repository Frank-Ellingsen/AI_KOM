---
title: "Controller Sjekkliste & Periodelukkingsrutine"
domain: "revisjon-og-kontroll"
category: "operativ-rutine"
author: "Frank Ellingsen"
statutory_references:
  - "Kommuneloven § 14-5"
  - "Kommuneloven § 14-6"
  - "Forskrift om økonomiplan, årsbudsjett, årsregnskap og årsberetning for kommuner"
summary: "Operativ sjekkliste for månedsavslutning, tertialrapportering (T1/T2), prosjektkontroll (EVM) og revisjonsdokumentasjon i Kristiansand kommune."
keywords: ["periodelukking", "månedsavslutning", "tertialrapport", "avstemming", "bankavstemming", "EVM", "Tufte"]
---

# 🛡️ Controller Sjekkliste & Periodelukkingsrutine
> **Operativ sjekkliste for månedsavslutning, tertialrapportering (T1/T2), prosjektkontroll (EVM) og revisjonsdokumentasjon i Kristiansand kommune.**  
> *Samsvarer med Edward Tufte Data-Ink standard, Kommuneloven §§ 14-5/14-6, internkontrollforskriften og EU AI Act.*

---

## 📅 1. Månedlig Periodelukking (Periode 1–12)

| Nr. | Sjekkpunkt | Beskrivelse & Metodikk | Ansvarlig | Frist | Status |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **M-01** | **Bankavstemming** | Avstemme samtlige kommunale drifts- og skattetrekkskontoer mot bankkontoutskrift. Null uforklarte differanser. | Regnskapsfører | Virkedag 3 | [x] Fullført |
| **M-02** | **Mellomregningskontoer** | Gjennomgå kontoer for midlertidige transaksjoner (f.eks. 2100–2190). Ingen uoppgjorte poster eldre enn 30 dager. | Regnskapsfører | Virkedag 4 | [x] Fullført |
| **M-03** | **Lønn & A-melding** | Avstemme utbetalt lønn (Visma Lønn) mot A-melding kvittering fra Skatteetaten for tilhørende måned. | Lønnsansvarlig | Virkedag 5 | [x] Fullført |
| **M-04** | **Inngående Fakturaer (EHF)** | Påse at alle mottatte EHF-fakturaer med leveringsdato i perioden er attestert og bokført. | Regnskap / Innkjøp | Virkedag 5 | [x] Fullført |
| **M-05** | **Periodiseringer** | Foreta manuelle periodiseringer for kjente vesentlige kostnader og inntekter som ikke er fakturert. | Controller | Virkedag 6 | [x] Fullført |
| **M-06** | **Månedlig Driftsrapport** | Kjøre `duckdb_controller_views.py` og generere avviksoppstilling til enhetsledere. | Controller | Virkedag 8 | [x] Fullført |

---

## 📊 2. Tertialavslutning & Årsavvik (1. og 2. Tertial)

| Nr. | Sjekkpunkt | Beskrivelse & Metodikk | Ansvarlig | Frist | Status |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **T-01** | **ERP vs. EPM Avstemming** | Sammenholde faktisk forbruk i Visma ERP mot vedtatte rammer i Framsikt. Avdekke poster med avvik > 500k kr. | Senior Controller | T-frist -10 dager | [x] Fullført |
| **T-02** | **Sykepengerefusjoner (NAV)** | Beregne etterslep på NAV-refusjoner (konto 7100). Korrigere for manglende utbetalinger før avvik beregnes. | Controller Helse/Skole | T-frist -8 dager | [x] Fullført |
| **T-03** | **Vikar- & Overtidsanalyse** | Detaljert analyse av art 020 (Vikarer) og art 030 (Overtid) for skole og helse. Kartlegge årsak til timeoverskridelse. | Controller | T-frist -6 dager | [x] Fullført |
| **T-04** | **EOY Sluttprognose (EAC)** | Etablere ny helårsprognose (Estimate at Completion) for samtlige kommunalsjefområder. | Senior Controller | T-frist -5 dager | [x] Fullført |
| **T-05** | **Netto Driftsresultat Sjekk** | Verifisere at kommunens samlede netto driftsresultat tilfredsstiller handlingsregelen (> 1,75 % av brutto driftsinntekter). | Økonomidirektør | T-frist -3 dager | [x] Fullført |
| **T-06** | **Politisk Saksnotat** | Utarbeide formelt saksnotat til Formannskapet med obligatorisk tiltaksplan jf. Kommuneloven § 14-5. | Senior Controller | T-frist -1 dag | [x] Fullført |

---

## 🏗️ 3. Prosjektcontroller Sjekkliste (Investeringer & EVM)

| Nr. | Sjekkpunkt | Beskrivelse & Metodikk | Ansvarlig | Standard / Hjemmel | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **P-01** | **EVM Måltallsberegning** | Beregne BAC, PV, EV, AC, CPI og SPI for alle prosjekter over 10 MNOK (f.eks. Vågsbygd skole, Randesund boenhet). | Prosjektcontroller | PMI / FAST Standard | [x] Fullført |
| **P-02** | **Endringsordrer & Krav** | Registrere og kvalitetssikre alle godkjente og varslede endringsordrer (byggherrekrav / entreprenørkrav). | Prosjektleder / Controller | NS 8405 / 8407 | [x] Fullført |
| **P-03** | **Usikkerhetsanalyse & Buffer** | Oppdatere estimat for usikkerhetsavsetning (P50 / P85) basert på markedspriser og grunnforhold. | Prosjektcontroller | KS2 Metodikk | [x] Fullført |
| **P-04** | **Fremdriftskontroll (Kritisk Sti)**| Kontrollere om prosjekter med SPI < 0.90 har forsinkelser på kritisk linje som påvirker ferdigstillelsesdato. | Byggeleder / Controller | Gantt / Fremdriftsplan | [x] Fullført |
| **P-05** | **Låneopptak & Likviditet** | Sammenholde periodens investeringsutbetalinger mot kommunens låneramme og rentefølsomhet. | Finansrådgiver | Finansreglementet | [x] Fullført |

---

## 🛡️ 4. AI-Governance & Kommunerevisjon (Kvalitetssikring)

| Nr. | Sjekkpunkt | Beskrivelse & Metodikk | Ansvarlig | Kontrollfrekvens | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **REV-01**| **Kryptografisk Hash (SHA-256)**| Rekalkulere SHA-256 fingeravtrykk i `Audit_AI_Actions`. Bekrefte uforanderlighet for samtlige HITL-handlinger. | Internrevisjonen | Kvartalsvis stikkprøve | [x] 100% Samsvar |
| **REV-02**| **0 Autonome Vedtak (HITL)** | Bekrefte at 100 % av AI-genererte forslag har blitt godkjent av autorisert saksbehandler før iverksetting. | Kommunerevisjonen | Årlig revisjon | [x] Fullført |
| **REV-03**| **PII-Skjerming (GDPR)** | Verifisere at personopplysninger (fødselsnumre/navn) er vasket ut før analyse via `src/guardrails/pii_masker.py`. | Personvernombud | Løpende kontroll | [x] 0 Lekkasjer |
| **REV-04**| **Kildeforankring (§)** | Kontrollere at samtlige genererte rapporter siterer relevante paragrafer i Kommuneloven og reglementet. | AI Guardrails | Løpende logging | [x] 100% Sitert |
