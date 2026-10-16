# Oppstartsnotat og Veiledning for Pilotgruppen: AI i Økonomistyring

**Målgruppe:** Superbrukere, økonomirådgivere og testdeltakere i Bølge 1-piloten  
**Virksomhetsområde:** Økonomi og virksomhetsstyring, Kristiansand kommune  
**Periode:** Uke 1–8 (Testperiode uke 3–6)  
**Dokumentstatus:** Operativ oppstartsveileder v1.0  

---

## 1. Velkommen til Pilotgruppen

Velkommen som deltaker i pilotprosjektet for **kunst intelligens (AI) i kommunal økonomistyring**. 

Formålet med denne piloten er å utforske hvordan moderne språkmodeller og kildeforankret AI (RAG - *Retrieval-Augmented Generation*) kan avlaste økonomirådgivere for manuelle rutineoppgaver, som oppslag i regelverk og utarbeidelse av førsteutkast til tertialrapporter og avviksforklaringer.

Som superbruker i pilotgruppen er din rolle avgjørende. Det er dine faglige vurderinger, tilbakemeldinger og kvalitetsmålinger som vil danne grunnlaget for **Beslutningsport G3 (Go / No-Go)**, hvor kommunedirektørens ledergruppe beslutter om verktøyet skal produksjonssettes for hele økonomiavdelingen.

---

## 2. Bruksområder i Pilotfasen (Bølge 1 Use-Cases)

Piloten er strengt avgrenset til to leseorienterte (*read-only*) støtteoppgaver med lav risikoprofil:

1. **Use-Case A: Kunnskapsassistent (Regelverks- og avtaleoppslag)**
   * **Hva du kan gjøre:** Stille spørsmål på vanlig norsk mot kommunens økonomireglement, attestasjonsregler, innkjøpsavtaler, KOSTRA-veiledere og Prosjektveiviseren.
   * **Forventet resultat:** AI-assistenten gir et presist svar med **eksplisitte, klikkbare kildereferanser** (f.eks. *Økonomireglement § 4-2, side 12*).
2. **Use-Case B: Rapportassistent (Utkast til avviksforklaringer)**
   * **Hva du kan gjøre:** Be om førsteutkast til avviksforklaringer for tertial- og årsrapportering basert på historiske og låste regnskapsdata fra hovedboken (Visma ERP / Framsikt).
   * **Forventet resultat:** Et ferdig strukturert tekstutkast som sammenstiller tall, avvik og historikk, klart for din faglige overprøving.

---

## 3. Fire Ufravikelige Husregler (*Trygghetsgarantier*)

For at piloten skal gjennomføres på en juridisk og sikkerhetsmessig forsvarlig måte, gjelder følgende fire husregler for alle testdeltakere:

1. **100 % Menneskelig Kontroll (*Human-in-the-Loop - HITL*):**
   * AI-assistenten leverer **kun uforpliktende utkast**. Du som fagperson har alltid det fulle ansvaret for å overprøve, korrigere og godkjenne teksten før den benyttes i sakspapirer eller rapporter.
2. **0 % Feiltoleranse på Regnskapstall:**
   * Du må **alltid verifisere alle beløp, prosentsatser og kontokoder** mot fagsystemet (Visma/Framsikt) før du godkjenner utkastet. Hvis AI-en gjengir et feil tall, skal utkastet avvises i evalueringsskjemaet.
3. **Kun Leseadgang (`Read-Only`):**
   * AI-systemet har ingen skriveadgang til fagsystemene og kan *aldri* utføre automatisk bokføring, endre budsjetter eller tildele ytelser.
4. **Personvern og Dataforbud:**
   * All datatrafikk sluses gjennom en sikker **AI Gateway** som maskerer personopplysninger (PII). Likevel skal du *aldri* manuelt taste inn unødvendige personopplysninger, fødselsnumre eller sensitive personopplysninger i fritekstfeltet.

---

## 4. Steg-for-Steg Instruksjon for Testuke 1

I løpet av din første testuke skal du gjennomføre **3–5 testoppgaver** per dag ved å følge denne faste rutinen:

```
[Steg 1: Velg oppgave] ──► [Steg 2: Kjør AI-spørring] ──► [Steg 3: Verifiser kilde & tall] ──► [Steg 4: Fyll ut skjema]
```

### **Steg 1: Velg en testoppgave**
* Ta utgangspunkt i en reell, historisk oppgave fra din hverdag (f.eks. oppslag på en attestasjonsgrense eller analyse av et overtidssykefravær i 2. tertial).
* Notér hvor lang tid du **vanligvis bruker på denne oppgaven manuelt** (f.eks. 30 minutter).

### **Steg 2: Logg inn og kjør AI-spørringen**
* Logg inn i testportalen via kommunens vanlige Single Sign-On (Entra ID / SSO).
* Formuler spørsmålet ditt så tydelig som mulig. Eksempel:
  > *"Hva var hovedårsaken til merforbruket på ramme 300 i 2. tertial, og hva sier økonomireglementet om omdisponering av ubrukte midler?"*

### **Steg 3: Kontroller resultat og kildehenvisninger**
* **Les kildehenvisningene:** Klikk på dokumentreferansene og verifiser at AI-en har hentet informasjon fra riktig paragraf eller rapport.
* **Sjekk tallene:** Kontroller at alle tall og beløp stemmer 100 % med fagsystemet.

### **Steg 4: Fyll ut Evalueringsskjemaet (Underveiskontrollen)**
Etter hver gjennomførte testoppgave åpner du **Evalueringsskjema for Superbrukere** og registrerer følgende:
* **Oppgave-ID og Tidsbruk:** Registrer faktiske minutter brukt *med AI* sammenlignet med manuelle baseline-minutter.
* **Kvalitetsmåling (Score 1–5):**
  * *Kildepresisjon:* Ble riktige kildedokumenter funnet?
  * *Fakta- og Tallnøyaktighet:* Var tallene 100 % korrekte uden hallusinasjoner?
  * *Språk og Nytteverdi:* Var utkastet velskrevet og nyttig?
* **HITL Sign-Off Status:** Velg om utkastet ble:
  * `[ ] Godkjent uendret`
  * `[ ] Godkjent med mindre språkkorreksjoner`
  * `[ ] Krevde vesentlig omarbeiding`
  * `[ ] Forkastet (oppgi feilårsak: f.eks. tallfeil eller feil kilde)`

---

## 5. Ukentlig Rytme og Support i Pilotperioden

For å sikre god oppfølging og kontinuerlig læring er piloten strukturert med følgende ukentlige møtepunkter:

* **Daglig Chat-support (Teams-kanal `#AI-Pilot-Økonomi`):** Her kan du stille spørsmål om promting, melde fra om tekniske feil eller dele gode erfaringer med kollegaer.
* **Torsdager kl. 11:30–12:00 (Ukentlig "Puls og Læringscafé"):**
  * 15 min gjennomgang av ukesstatistikk og mest spennende test-cases.
  * 15 min åpen erfaringstrolling og avklaring av utfordringer.
* **Supportkontakter:**
  * **Operativ pilotleder:** Senior Controller / Prosjektleder
  * **IT- / AI Gateway-ansvarlig:** Data Steward / IT-avdelingen
  * **Sikkerhet og PII:** Personvernombud / CISO

---

> **Motto for pilotgruppen:** *"Vi tester ikke om datamaskinen kan erstatte økonomirådgiveren – vi tester om økonomirådgiveren med AI kan levere bedre beslutningsstøtte på kortere tid!"*
