---
title: "Saksnotat til Kontrollutvalget og Kommunerevisjonen"
domain: "revisjon-og-kontroll"
category: "saksnotat"
document_id: "NOTAT-KU-REV-2026-01"
author: "Frank Ellingsen"
statutory_references:
  - "Kommuneloven kap. 24"
  - "GDPR Art. 22"
  - "EU AI Act Art. 26/27"
summary: "Redegjørelse for sikkerhets-, personverns- og internkontrollmekanismer ved innføring av Kommune AI Guardrails som beslutningsstøtteverktøy i Kristiansand kommune."
keywords: ["kontrollutvalget", "kommunerevisjonen", "sikkerhet", "personvern", "internkontroll", "HITL", "SHA-256", "PII"]
---

# 🏛️ Saksnotat til Kontrollutvalget og Kommunerevisjonen

**Dokument-ID:** NOTAT-KU-REV-2026-01  
**Mottaker:** Kontrollutvalget, Kommunerevisjonen og IKT Agder  
**Avsender:** Frank Ellingsen, Senior Controller / Prosjektøkonom  
**Dato:** 13. oktober 2026  
**Tema:** Sikkerhet, personvern og internkontroll ved innføring av «Kommune AI Guardrails» som rådgivende beslutningsstøtteverktøy  

---

## 1. Bakgrunn og Hensikt

Økonomi og virksomhetsstyring har utviklet og pilotert en rådgivende AI-assistent (**Kommune AI Guardrails**) for oppslag i komplekst regelverk (Kommuneloven, KOSTRA-forskriften, Selvkostforskriften og lokalt Økonomireglement), samt automatisert avviksoppfølging mellom Visma ERP og Framsikt EPM.

Formålet med dette notatet er å redegjøre for systemets **sikkerhets- og kontrollmekanismer**, og demonstrere at løsningen oppfyller alle krav fastsatt i **Kommuneloven kap. 24**, **GDPR**, **EU AI Act** og god forvaltningsskikk.

---

## 2. Juridiske og Forvaltningsmessige Garantier

### A. 0 Autonome Vedtak — 100 % Human-in-the-Loop (HITL)
* AI-assistenten fatter **ingen rettslig bindende vedtak**.
* Systemet fungerer utelukkende som en rådgivende saksbehandlerassistent.
* Alle utkast til tertialrapporter og politiske saker merkes med: `[UTKAST — KREVER GODKJENNING AV SAKSBEHANDLER]`.
* Saksbehandler må aktivt vurdere og godkjenne (*APPROVED*), endre (*MODIFIED*) eller avvise (*REJECTED*) ethvert råd.

### B. Automatisk Skjerming av Personopplysninger (Stage-Gate Port 4)
* Før en tekst sendes til analyse eller språkmodeller, passerer den en klientside PII-vasker.
* Norske fødselsnumre (FNR), D-numre (DNR), telefonnumre (`+47`) og e-postadresser maskeres automatisk (`[FNR_MASKED]`, etc.).
* Ingen personopplysninger forlater kommunens godkjente soner.

### C. Glass-Box Kildekrav og Paragrafsitering (§) (Stage-Gate Port 8)
* Systemet opererer etter et strengt **Glass-Box prinsipp**: AI-en har ikke tillatelse til å ekstrapolere eller gjette.
* 100 % av svarene krever direkte paragrafsitering (§) til godkjente kommunale dokumenter.
* Dersom hjemmel mangler, returnerer systemet: *"Finner ikke tilstrekkelig hjemmel for dette i regelverksdatabasen."*

---

## 3. Uforanderlig Kryptografisk Revisjonsspor (Stage-Gate Port 9)

For å sikre at Kommunerevisjonen til enhver tid kan etterprøve systemets bruk, logges samtlige transaksjoner med et **SHA-256 fingeravtrykk**:

$$\text{Audit Hash} = \text{SHA-256}(\text{Brukerspørring} \parallel \text{Kilde-Chunks} \parallel \text{AI-Svar} \parallel \text{Saksbehandler-Handling} \parallel \text{Tidsstempel})$$

* **Integritetsgaranti:** Loggene lagres i tabellen `Audit_AI_Actions` i SQLite med skrivebeskyttelse. Enhver manipulering av loggen i ettertid vil umiddelbart bryte hash-kjeden og flagges ved revisjon.
* **Oppbevaring:** Loggene oppbevares i minimum 6 måneder jf. EU AI Act Art. 26(6).

---

## 4. Offentlig Innsyn & Algoritmeregister (Stage-Gate Port 10)

I tråd med prinsippet om åpenhet i offentlig forvaltning er systemet forberedt for registrering i kommunens offentlige **Algoritmeregister** etter *Eurocities Algorithmic Transparency Standard*:
* **System-ID:** `KRISTIANSAND-AI-RAG-001`
* **Ansvarlig enhet:** Økonomi og virksomhetsstyring
* **Rettslig grunnlag:** Kommuneloven § 13-1 / Forvaltningsloven § 11

---

## 5. Konklusjon og Forslag til Vedtak

Gjennomførte kontroller og pilotkjøringer viser at Kommune AI Guardrails gir betydelig tidsbesparelse i saksforberedelse og avvikskontroll, samtidig som rettssikkerhet, personvern og sporbarhet er fullt ivaretatt.

### Forslag til Vedtak for Kontrollutvalget:
> 1. *Kontrollutvalget tar orienteringen om sikkerhets- og kontrollarkitekturen i «Kommune AI Guardrails» til etterretning.*
> 2. *Kontrollutvalget slutter seg til at systemet driftes med 100 % Human-in-the-Loop og kryptografisk SHA-256 revisjonslogging.*
> 3. *Kommunerevisjonen gis full innsyns- og revisjonstilgang til tabellen `Audit_AI_Actions` for årlige stikkprøvekontroller.*
