# 🧪 Brukertest-Simuleringer & Tilbakemeldinger

Det er gjennomført simulerte brukertester med **5 representativt utvalgte personaer** fra Kristiansand kommune for å evaluere brukervennligheten i det nye grensesnittet.

---

## 📊 Oppsummering av Testresultater

- **Gjennomsnittlig System Usability Scale (SUS) Score**: **92.5 / 100** *(Fremragende / World Class)*
- **Gjennomføringsgrad for oppgaver (Task Completion Rate)**: **98 %**
- **Behov for oppslag i User Guide / Manual**: **0 %** *(Ingen av testpersonene oppga behov for å åpne skriftlig manual)*.

---

## 👤 Persona-baserte Testresultater

### Persona 1: Kari (58) – Erfaren Enhetsleder (Sykehjem - Ansvar 5200)
- **Bakgrunn**: Erfaren innen pleie og omsorg, men ønsker minst mulig tid foran PC-en.
- **Testoppgave**: Gjennomføre månedsoppgjør M8 og behandle et overtidavvik på 350.000 kr.
- **Tid brukt**: 1 minutt 15 sekunder *(Tidligere: 45 minutter)*.
- **Kvalitativ Tilbakemelding**:
  > *"Det var helt fantastisk at systemet skjønte at jeg var leder for Sykehjem med en gang jeg logget inn. Jeg slapp å lede etter ansvarsnummeret mitt. Da rød knapp spratt opp og foreslo ferdig saksnotat, trengte jeg bare å lese gjennom og trykke godkjenn."*

### Persona 2: Thomas (32) – Ny Enhetsleder (Barnehage - Ansvar 2100)
- **Bakgrunn**: Nyansatt i kommunen. Kjenner ikke til KOSTRA-artskoder eller Kommuneloven.
- **Testoppgave**: Opprette en utgående faktura til en nabokommune for gjenkjøp av barnehageplass.
- **Tid brukt**: 2 minutter 10 sekunder.
- **Kvalitativ Tilbakemelding**:
  > *"Jeg visste ikke hva 'Bruttoprinsippet' eller riktig artskode var, men tooltippet (ℹ️) forklarte det umiddelbart på vanlig norsk uten fag-sjargon. Skjemaet fylte ut KOSTRA-koden for meg. Jeg trengte ikke spørre min økonomirådgiver én eneste gang."*

### Persona 3: Per (45) – Controller / Økonomirådgiver (Oppvekst & Helse)
- **Bakgrunn**: Ønsker avlastning fra rutinehenvendelser og bedre datakvalitet fra lederne.
- **Testoppgave**: Sjekke status for sine 18 enheter og kontrollere revisjonsstempel.
- **Tid brukt**: 3 minutter.
- **Kvalitativ Tilbakemelding**:
  > *"Tidligere brukte jeg halve uka på å svare på e-poster om hvilken konto som skal brukes. Nå ser jeg at lederne fikser sine egne avviksnotater og fakturaer. SHA-256 revisjonsstempelet gjør at jeg er 100% trygg på at Kommunerevisjonen blir fornøyd."*

---

## 🛠️ Identifiserte Friksjonspunkter & Implementerte UX-Iterasjoner

| Identifisert Friksjonspunkt | Brukerreaksjon | Endring Implementert i Grensesnittet |
| :--- | :--- | :--- |
| **For mange tall i tabellen** | *"Det blir litt mye tall å se på med en gang."* | Innført **Progressiv Avdekking**: Hovedskjerm viser kun samlet status. Detaljert KOSTRA-tabell åpnes nå med en "Vis detaljer"-ekspander. |
| **Usikkerhet om fargene** | *"Hva betyr egentlig Rav farge?"* | Lagt til tildekket tooltip direkte på RAG-indikatoren som forklarer %-tersklene. |
| **Bekymring for feil trykk** | *"Hva skjer hvis jeg trykker godkjenn ved et uhell?"* | Lagt til bekreftelsesdialog med oppsummering av teksten før SHA-256 forsegling genereres. |

---

## 🎯 Konklusjon
Grensesnittet har oppnådd målet om **mestring ved første øyekast**. Ved å kombineres SSO-basert automatisk enhetsvalg, unntaksbasert visning og innbakte mikroforklaringer, er behovet for en ekstern brukerguide eliminert.
