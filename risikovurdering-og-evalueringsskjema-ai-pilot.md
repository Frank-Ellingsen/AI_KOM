# Risikovurdering (DPIA/FRIA) og Evalueringsskjema for AI-Pilot

Dette dokumentet utgjør den operative **juridiske risikovurderingen (DPIA/FRIA)** og det praktiske **evalueringsskjemaet for superbrukere** under gjennomføringen av Bølge 1-piloten for kunstig intelligens i økonomiavdelingen.

---

## DEL 1: Operasjonelt Oppsett for Risikovurdering (DPIA & FRIA)

I henhold til **EU AI Act art. 26/27**, **GDPR art. 35**, **Forvaltningsloven § 25** og nasjonale retningslinjer fra Digdir og Datatilsynet, er dette risikovurderingsoppsettet obligatorisk for alle kommunale AI-piloter.

### 1. Prosjekt- og Systemidentifikasjon
* **Systemnavn:** Bølge 1 AI-Assistent for Økonomi og Virksomhetsstyring
* **Virksomhet / Enhet:** Kristiansand kommune – Stabsområde Økonomi og Virksomhetsstyring
* **Systemansvarlig / Prosesseier:** Økonomidirektør
* **Kommunal AI Act-rolle:** Idriftsetter (*Deployer*)
* **Mål-use-cases:** 
  1. *Use-Case A (Kunnskapsassistent):* RAG-oppslag i økonomireglement, attestasjonsregler og innkjøpsavtaler.
  2. *Use-Case B (Rapportassistent):* Utkast til avviksforklaringer i tertial- og årsrapportering basert på regnskapsdata.

---

### 2. Trinnvis DPIA- og FRIA-Matrise

| Trinn / Område | Hovedkriterium & Hjemmel | Identifisert Risiko | Risikoreduserende Tiltak | Restrisiko |
| :--- | :--- | :--- | :--- | :--- |
| **Trinn 1: Formål & Hjemmel** | GDPR art. 6(1)(e) / Supplerende rettsgrunnlag i Kommuneloven § 14. | Uklarhet om hjemmelsgrunnlag ved bruk av KI på virksomhetsdata. | AI-modellen avgrenses til *read-only* støtte for forberedende saksbehandling. Ingen automatiserte eneltvedtak fattet av KI. | **Lav** |
| **Trinn 2: Personvern & PII (DPIA)** | GDPR art. 35 / Dataminimering jf. art. 5(1)(c). | Utilsiktet lekkasje av personopplysninger (fødselsnr, helse/fravær) til KI-modell. | 1. Obligatorisk PII-vasking i AI Gateway før spørring sendes.<br>2. Eksplisitt avtalevilkår mot modelltrening hos leverandør.<br>3. Kun aggergerte regnskapstall i Use-Case B. | **Lav** |
| **Trinn 3: Tilgangsstyring** | GDPR art. 32 / Arvet tilgangskontroll. | Bruker får tilgang til skjermede bilag eller fortrolige dokumenter via RAG-søk. | RAG-søket integreres mot Entra ID (SSO) og arver brukerens formelle lesehjemmel (RBAC/ABAC) fra ERP og arkiv. | **Lav** |
| **Trinn 4: Rettssikkerhet & Menneskelig Kontroll (FRIA)** | EU AI Act art. 27 / Forvaltningsloven § 25. | Pro forma-godkjenning av AI-utkast som fører til feilaktige tall eller vedtak (*over-reliance*). | **Obligatorisk Human-in-the-Loop (HITL):**<br>AI leverer kun uforpliktende utkast. Fagansvarlig rådgiver må aktivt gjennomgå, korrigere og godkjenne sluttproduktet. | **Lav** |
| **Trinn 5: Kildekritikk & Tallkvalitet** | Krav om 0 % feiltoleranse på regnskapstall. | AI-hallusinasjoner eller feilaktige tall gjengis i sakspapirer til politisk behandling. | Systemet valideres mot et lukket fasit-sett (*Ground Truth*) med krav om Faithfulness = 1,00 før publisering. | **Lav** |
| **Trinn 6: Logging & Tilsyn** | EU AI Act art. 26 / Arkivlova § 9. | Manglende sporbarhet over AI-genererte forslag ved tilsyn fra Datatilsynet/Nkom. | Automatisk audit-logging i AI Gateway for bruker-ID, prompt, kildekontekst, AI-svar og fagpersonens endelige godkjenning. | **Lav** |

---

### 3. Konklusjon og Sign-Off for Risikovurdering
* **Er produksjonssetting forsvarlig?** Ja, forutsatt at alle risikoreduserende tiltak i tabellen overholdes under piloteringen.
* **Behov for forhåndshøring hos Datatilsynet (GDPR art. 36)?** Nei, restrisikoen vurderes som lav etter tiltak.

---

## DEL 2: Evalueringsskjema for Superbrukere (Underveiskontroll)

Dette skjemaet fylles ut av superbrukerne (økonomirådgiverne) under testperioden (Uke 3–6) for å samle empirisk datagrunnlag til **Beslutningsport G3 (Go / No-Go)**.

---

### **A. Registrering av Test-Sesjon**

* **Dato:** `____________________`
* **Testbruker (Initianter):** `____________________`
* **Oppgave / Use-Case:**
  * [ ] **Use-Case A:** RAG-oppslag i økonomireglement, attestasjonsregler eller avtaler.
  * [ ] **Use-Case B:** Utkast til avviksforklaring / tertialrapportnotat.
* **Testet dokument / regnskapslinje:** `________________________________________`

---

### **B. Kvantitativ Måling og Kvalitetssjekk**

Vurder AI-assistentens utkast på en skala fra **1 til 5** (der 1 = Svært dårlig, 5 = Utmerket):

| Måleparameter | Kriterium | Score (1–5) | Merknad / Observerte avvik |
| :--- | :--- | :---: | :--- |
| **1. Kildehenvisninger (Precision)** | Oppga AI-en eksakte og korrekte dokumentnavn, paragrafer og sidetall? | `[  ]` | |
| **2. Fravær av hallusinasjoner** | Holdt AI-en seg 100 % til kildedokumentet uten å dikte opp regler eller tall? | `[  ]` | |
| **3. Tallnøyaktighet (0 % feiltoleranse)** | Stemmer alle oppgitte beløp, prosenter og kontokoder 100 % mot fagsystemet? | `[  ]` | **MÅ være 100 % korrekt** |
| **4. Tidsbesparelse** | Opplevde du at førsteutkastet sparte deg for tid sammenlignet med manuell prosess? | `[  ]` | Estimated time saved: ____ min |
| **5. Språk og struktur** | Var utkastet velformulert og tilpasset kommunal rapportstandard? | `[  ]` | |

---

### **C. Tidsmåling mot Baseline**

* **Estimert tid på manuell gjennomføring (uten AI):** `______` minutter
* **Tid brukt med AI-assistent (Inkludert din overprøving/HITL):** `______` minutter
* **Beregnet tidsinnsparing (%):** `______` % *(Målsetting: $\ge$ 30 %)*

---

### **D. Menneskelig Overprøving (HITL Sign-Off)**

* **Handling utført av rådgiver:**
  * [ ] **Godkjent uten endringer:** AI-utkastet var 100 % korrekt og trengte ingen modifikasjon.
  * [ ] **Godkjent med mindre justeringer:** AI-utkastet ga et godt fundament, men krevde språklig eller tallmessig korreksjon.
  * [ ] **Forkastet / Avvist:** AI-utkastet inneholdt feil, mangelfulle kilder eller misforsto oppgaven.

* **Dersom utkastet ble endret/avvist, oppgi årsak:**
  * [ ] Feil i kildesøk / RAG fant ikke riktig avsnitt.
  * [ ] Tallfeil eller feilberegning i regnskapsdata.
  * [ ] Språklige misforståelser eller feil begrepsbruk.
  * [ ] Annet: `__________________________________________________`

---

### **E. Evaluering for Beslutningsport G3**

* **Superbrukerens samlede konklusjon:**
  * [ ] **Anbefales for produksjon:** Verktøyet gir opplevd merverdi, høy trygghet og tidsbesparelse.
  * [ ] **Krever iterering / justering:** Verktøyet er lovende, men trenger bedre RAG-indeksering eller fagsystemintegrasjon.
  * [ ] **Bør ikke produksjonssettes:** Verktøyet gir liten verdi eller øker tidsbruken på grunn av omfattende rettingsarbeid.

**Signatur Superbruker:** `________________________________________`  
**Dato:** `____________________`
