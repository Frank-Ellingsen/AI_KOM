# Cheat Sheet: Sponsormøte om AI-Pilot i Økonomistyring

**Målgruppe:** Ikke-teknologisk sponsor, Kommunedirektørens ledergruppe, Formannskap eller Økonomidirektør  
**Formål:** Raskt og trygt oppslagsark (1-sider) til bruk før og under sponsormøtet.

---

## 1. Kjernebudskap (Elevator Pitch – 15 sekunder)

> *"Dette handler ikke om et nytt IT-prosjekt, men om å gi økonomirådgiverne våre mer tid til dype analyser og beslutningsstøtte for enhetslederne. Vi ber om et kontrollert 8-ukers forsøk på lavrisiko-oppgaver, der et menneske alltid har full overprøvingsrett, og der vi beviser gevinster før vi bruker én krone på skaleringsdrift."*

---

## 2. Nøkkeltall i Brystlommen

| Parameter | Tall / Verdi | Forklaring for Sponsor |
| :--- | :--- | :--- |
| **Pilotkostnad** | **185 000 kr** | Engangskostnad for rigging. Dekkes 100 % av avsatte KI-midler ("Teknologiløftet"). |
| **Frigjort tid** | **2,0 t/uke/rådgiver** | Tilsvarer **2 861 timer/år** eller **1,73 årsverk** (ved 30 rådgivere). |
| **Netto gevinst** | **+1 061 664 kr/år** | Netto innspart beløp på bunnlinjen etter fratrekk for årlig drift (v/ 70 % utaksgrad). |
| **Tilbakebetaling (Payback)** | **4,9 måneder** | Etableringskostnaden er nedbetalt på under et halvt år ved ordinær utrulling. |
| **Break-even krav** | **12,9 % utaksgrad** | Vi trenger kun å hente ut 1/8 av den innsparte tiden for at årlig drift går i null. |

---

## 3. De 4 Trygghetsgarantiene

1. **0 % feiltoleranse på regnskapstall:** Systemet må bestå et lukkets testsett (*Ground Truth*) uten tallfeil før produksjon.
2. **Kun lesetilgang (*Read-Only*):** Systemet har ingen skriveadgang til fagsystemene og kan hverken bokføre bilag, endre budsjetter eller tildele ytelser.
3. **Menneske i loopen (*Human-in-the-Loop*):** AI-en leverer kun uforpliktende utkast — en autorisert fagrådgiver må alltid overprøve, verifisere og godkjenne sluttproduktet.
4. **Full PII-skjerming:** En intern **AI Gateway** maskerer personopplysninger og forhindrer at kommunens data benyttes til videre modelltrening.

---

## 4. Raske Svar på 3 Typiske Motargumenter

* **«Hva om AI-en hallusinerer?»**  
  $
ightarrow$ *«RAG-arkitekturen tvinger AI-en til KUN å hente verifiserte tall fra våre egne kilder med direkte sidetallshenvisning. Finnes ikke svaret i kildegrunnlaget, svarer den 'Finner ikke'.»*
* **«Er ikke dette i strid med GDPR og EU AI Act?»**  
  $
ightarrow$ *«Nei, vi gjennomfører full DPIA- og FRIA-screening. Siden et menneske alltid overprøver svaret, rammes vi ikke av forbudet mot helautomatiske avgjørelser jf. GDPR art. 22.»*
* **«Hva om piloten mislykkes?»**  
  $
ightarrow$ *«Da utløser vi stopp-knappen ved Beslutningsport G3 etter 8 uker uten ytterligere driftsforpliktelser. Eksisterende manuelle rutiner kjører uforstyrret i parallell.»*

---

## 5. Det Du Formelt Ber om i Dag

1. Godkjenning av **8-ukers pilot** på Bølge 1 use-cases (kunnskaps- og rapportassistent).
2. Bruk av avsatte engangsmidler fra KI-potten (ingen ekstra budsjettbelastning).
3. At ledergruppen behandler den samlede evalueringsrapporten ved **Beslutningsport G3 (Go/No-Go)**.

---

## 6. Åpningsreplikk (De første 60 sekundene)

> *"Takk for tiden. Jeg vil starte med et enkelt spørsmål: Hvordan sikrer vi at økonomiavdelingen rekker å levere dype, verdiskapende analyser til enhetslederne våre når hverdagen spises opp av manuelle oppslag i reglement, bilagskontroll og rapportskriving?*
> 
> *I dag legger vi fram et forslag til en 8-ukers pilot med kunstig intelligens. Dette er ikke et dyrt IT-prosjekt, men et trygt og avskjermet forsøk på å fjerne rutinearbeid — under 100 % menneskelig kontroll og med null risikoforpliktelse."*

---

## 7. Q&A: Svar på 5 Dypere Spørsmål fra Sponsor

### Q1: Sikkerhet og Personvern
> **«Lekker vi følsomme personopplysninger eller taushetsbelagte regnskapsdata ut på internett?»**  
> *Svar:* Nei, all datatrafikk går via vår interne AI Gateway som automatisk maskerer personopplysninger (PII). Vår databehandleravtale har et eksplisitt forbud mot at leverandøren bruker våre data til å trene modeller. I tillegg arver RAG-søket brukerens eksisterende Entra ID/SSO-tilganger.

### Q2: Kvalitet og Tallfeil
> **«Hva gjør vi dersom AI-en regner feil i et sakspapir som skal til politisk behandling?»**  
> *Svar:* Vi stiller et ufravikelig krav om 0 % feiltoleranse på faktiske regnskapstall (Faithfulness = 1,00) mot et godkjent fasit-sett. Systemet har kun lesetilgang, og saksbehandleren er faglig ansvarlig for å kontrollere og godkjenne alt før publisering.

### Q3: Juss og Ansvar
> **«Hvem har det juridiske ansvaret dersom noe går galt, og oppfyller vi kravene i EU AI Act?»**  
> *Svar:* Kommunedirektøren og Økonomidirektøren eier systemansvaret, mens saksbehandleren eier det faglige innholdet. Piloten er i lavrisikokategorien under EU AI Act, og vi gjennomfører full FRIA- og DPIA-screening før oppstart.

### Q4: Gevinstrealisering
> **«Hvordan vet vi at dette faktisk gir innsparinger på bunnlinjen?»**  
> *Svar:* Piloten koster kun 185 000 kr og dekkes av KI-potten. Ved ordinær utrulling (30 rådgivere) sparer vi 2 861 timer i året. Med 70 % utaksgrad gir dette en netto årlig innsparing på 1,06 mill. kr og en nedbetalingstid på 4,9 måneder.

### Q5: Exit-strategi
> **«Hva gjør vi dersom piloten viser seg å ikke levere resultatene etter 8 uker?»**  
> *Svar:* Da stanser vi prosjektet ved Beslutningsport G3. Vi har ingen bindinger eller videre driftskostnader, og de ordinære rutinene fortsetter uforstyrret.
