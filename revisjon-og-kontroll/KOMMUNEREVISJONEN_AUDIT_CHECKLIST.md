---
title: "Sjekkliste for Kommunerevisjonen: Årlig Kontroll og Revisjon av AI-systemer"
domain: "revisjon-og-kontroll"
category: "revisjon-sjekkliste"
document_id: "REV-AI-2026-v1"
author: "Frank Ellingsen"
statutory_references:
  - "Kommuneloven kap. 24"
  - "EU AI Act Art. 26/27/86"
  - "GDPR Art. 15/22/30/35"
  - "Eurocities Algorithmic Transparency Standard"
  - "ISO/IEC 42001"
summary: "Metodisk ramme for Kommunerevisjonens og Kontrollutvalgets årlige kontroll av kommunens AI-systemer, RAG-modeller, SHA-256 forsegling og Stage-Gate Port 9 HITL."
keywords: ["revisjon", "kontrollutvalget", "kommunerevisjonen", "SHA-256", "HITL", "DPIA", "FRIA", "EU AI Act"]
---

# 🛡️ Sjekkliste for Kommunerevisjonen: Årlig Kontroll og Revision av AI-systemer

**Dokument-ID:** REV-AI-2026-v1  
**Målgruppe:** Kommunerevisjonen, Kontrollutvalget og Internrevisjonen i Kristiansand kommune  
**Hjemmel & Standarder:** Kommuneloven kap. 24, EU AI Act (Art. 26/27/86), GDPR (Art. 15/22/30/35), Eurocities Algorithmic Transparency Standard, ISO/IEC 42001.  

---

## 🏛️ Formål og Omfang

Denne sjekklisten fastsetter den metodiske rammen for Kommunerevisjonens årlige kontroll av kommunens AI-systemer, rådgivende RAG-modeller (*Retrieval-Augmented Generation*) og automatiserte beslutningsstøtteverktøy. 

Kontrollen skal verifisere at AI-bruk innen økonomistyring, saksbehandling og virksomhetsstyring skjer i henhold til gjeldende lover, etiske retningslinjer, internkontroll og **Stage-Gate portmodellen (Port 1–10)**.

---

## 📋 Sjekkliste for Revisjonskontroll (6 Kontrollområder)

### 1. 🔒 Kryptografisk Audit Trail & Uforanderlighet (Stage-Gate Port 9)
> **Mål:** Verifisere at loggene ikke har blitt manipulert eller slettet i ettertid.

- [ ] **Sjekk 1.1 — Loggintegritet (SHA-256):** Utføre stikkprøver mot databasetabellen `Audit_AI_Actions` ved å rekalkulere SHA-256 fingeravtrykket for `(user_query + retrieved_chunk_ids + llm_response + user_action + timestamp)`.
- [ ] **Sjekk 1.2 — Fullstendighet:** Bekrefte at 100 % av utførte AI-spørringer har registrert tilhørende loggrad med unikt ID-stempel.
- [ ] **Sjekk 1.3 — Oppbevaringsfrist:** Verifisere at loggene oppbevares trygt i minimum 6 måneder jf. EU AI Act Art. 26(6).
- [ ] **Sjekk 1.4 — Tilgangskontroll:** Sikre at kun autoriserte revisorer har lesetilgang til revisjonssporet, og at skrive/slettestatus er deaktivert for vanlige brukere.

---

### 2. 👤 Human-in-the-Loop (HITL) & Automation Bias
> **Mål:** Sikre reell menneskelig overprøving og forhindre "gummistempling".

- [ ] **Sjekk 2.1 — Ingen Autonomi:** Verifisere at AI-systemet fatter **0 autonome vedtak**, og at alle utmatinger krever aktiv godkjenning (*APPROVED / MODIFIED / REJECTED*) fra en kvalifisert saksbehandler.
- [ ] **Sjekk 2.2 — Endringsfrekvens:** Analysere fordelingen av saksbehandlingshandlinger. Dersom `APPROVED`-raten er over 98 %, skal revisjonen undersøke om det foreligger ubevisst tilpasningsfelle (*automation bias*).
- [ ] **Sjekk 2.3 — Saksbehandlers Notater:** Utføre kvalitetsstikkprøve på saksbehandlers skriftlige begrunnelser ved `MODIFIED` eller `REJECTED` status.

---

### 3. 🛡️ PII-Skjerming & Dataminimering (Stage-Gate Port 4)
> **Mål:** Bekrefte at ingen personopplysninger leppes til LLM-modeller eller eksterne skyer.

- [ ] **Sjekk 3.1 — Lokal Databehandling:** Bekrefte at RAG-oppslag og LLM-kjøringer foregår 100 % lokalt (f.eks. via skjermet Ollama/SQLite-miljø) uten utveksling av data til usikrede tredjepartstjenester.
- [ ] **Sjekk 3.2 — Automatisk PII-Vask:** Kjøre testsett med syntetiske fødselsnumre, navn og e-postadresser gjennom skjermingsmodulen (`src/guardrails/pii_masker.py`) for å verifisere 100 % deteksjons- og anonymiseringsrate.
- [ ] **Sjekk 3.3 — Dataminimering (GDPR Art. 5):** Påse at kun nødvendige data fra Visma ERP og Framsikt EPM hentes inn for det konkrete analyseformålet.

---

### 4. 📚 Glass-Box RAG & Kildeforankring (Stage-Gate Port 8)
> **Mål:** Forhindre AI-hallusinasjoner og sikre at alle råd er direkte sporbare til gjeldende regelverk.

- [ ] **Sjekk 4.1 — Paragrafsitering (§):** Kontrollere at 100 % av genererte AI-svar i stikkprøven inneholder korrekte siteringer til relevante kilder (Kommuneloven, KOSTRA-veilederen, Økonomireglementet eller tertialrapportene).
- [ ] **Sjekk 4.2 — Kildeverifisering:** Sammenholde de hentede kilde-chunkene (`retrieved_chunk_ids`) med det faktiske svaret for å avdekke feiltolkninger eller manglende forankring.
- [ ] **Sjekk 4.3 — Atomisk Oppdatering:** Kontrollere at regelverksendringer (f.eks. ny KOSTRA-kontoplan eller oppdatert delegasjonsreglement) blir re-indeksert i `sqlite-vec` umiddelbart ved ikrafttredelse.

---

### 5. 🔍 Offentlig Transparens & Algoritmeregister (Stage-Gate Port 10)
> **Mål:** Sikre innbyggernes og folkevalgtes rett til innsyn jf. offentlighetsloven og EU AI Act.

- [ ] **Sjekk 5.1 — Algoritmeregister:** Bekrefte at AI-systemet er registrert i Kristiansand kommunes offentlige Algoritmeregister i henhold til *Eurocities Algorithmic Transparency Standard*.
- [ ] **Sjekk 5.2 — FRIA & DPIA Status:** Verifisere at konsekvensvurderinger for grunnleggende rettigheter (FRIA, EU AI Act Art. 27) og personvern (DPIA, GDPR Art. 35) er gjennomført, dokumentert og senest oppdatert siste 12 måneder.
- [ ] **Sjekk 5.3 — Klagerett:** Sikre at innbyggere og ansatte har en tydelig kanal for å be om utvidet forklaring eller klage på AI-støttede vurderinger.

---

### 6. 📊 Rapport og Oppfølging overfor Kontrollutvalget

- [ ] **Sjekk 6.1 — Avviksrapportering:** Utarbeide årlig revisjonsrapport med oversikt over eventuelle avvik, sikkerhetshendelser eller manglende kildeforankring.
- [ ] **Sjekk 6.2 — Tiltaksplan:** Påse at Kommunedirektøren har etablert bindende tidsfrister for utbedring av identifiserte avvik.
- [ ] **Sjekk 6.3 — Behandling i Kontrollutvalget:** Fremme revisjonsrapporten som egen sak for Kontrollutvalget og Bystyret.

---

## 📐 Metodikk for Stikkprøvekontroll (Statistisk Utvalg)

1. **Utvalgsstørrelse:** Minimum 5 % av samtlige registrerte spørringer i `Audit_AI_Actions` fra foregående 12 måneder, eller minimum 50 tilfeldige transaksjoner.
2. **Kritiske Kriterier for Stopp-Signal (Rød Rammefeil):**
   * Enkeltforekomst av manglende SHA-256 samsvar i audit-loggen.
   * Funn av umaskerte fødselsnumre (PII) i spørrehistorikken.
   * AI-svar uten kildehenvisning som har ført til feilaktig omdisponering i Framsikt/Visma.

---

*Sjekklisten er publisert som en del av Kommune AI Guardrails kvalitetssystem for Kristiansand kommune.*
