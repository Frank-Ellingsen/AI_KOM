# Promptsett for Microsoft 365 Copilot: KOSTRA-Analyse & Økonomistyring
**Spesialtilpasset for Økonomi og virksomhetsstyring i Kristiansand kommune**

---

## 📌 Innledning & Bruksanvisning

Dette promptsettet er utformet for økonomirådgivere, controllere og enhetsledere i Kristiansand kommune som benytter **Microsoft 365 Copilot** i kombinasjon med **Excel (med Python `=PY`)**, **Power BI / Fabric**, **MS Teams** og **Word/PowerPoint**.

### **Gylne regler for M365 Copilot i kommunal økonomi:**
1. **Kontekst (Rolle & Struktur):** Angi alltid at du jobber med KOSTRA-kontoplanen (Kontoklasse 1 Drift, Funksjon 100–890, Art 1000–1990) og spesifiser virksomhetsområdet (*Oppvekst, Helse og mestring, etc.*).
2. **Kildeforankring:** Be alltid Copilot hente data fra de oppgitte tabellene/modellene i Excel eller Power BI uten å estimere eller fylle inn manglende regnskapstall.
3. **Menneskelig overprøving (HITL):** M365 Copilot leverer *lese- og utkaststøtte*. Rådgiveren har alltid det faglige og juridiske ansvaret for å verifisere tall før publisering eller politisk behandling.

---

## 📊 KATEGORI 1: Excel + Python (`=PY`) — Avviksanalyser & KOSTRA-Filtering

Disse promptene benyttes direkte i **Copilot-panelet i Excel** for å automatisere datavasking, avvikssøk og scenario-simuleringer.

---

### **Prompt 1.1: Identifisere vikar- og overtidssmitte (Art 1020 & 1090)**
> **Formål:** Avdekke hvilke enheter som har høyest overskridelse på vikar- og overtidskostnader sammenlignet med vedtatt ramme (Art 1010 fastlønn).
>
> **Prompt:**
> ```text
> Du er en senior økonomirådgiver i Kristiansand kommune. Analyse-tabellen 'Regnskap_T2' inneholder KOSTRA-regnskapslinjer med Kolonne [Virksomhetsområde], [Enhetsnummer], [Enhetsnavn], [Art], [Budsjett_YTD] og [Regnskap_YTD].
>
> 1. Bruk Python til å filtrere ut alle rader der [Virksomhetsområde] = "Oppvekst" og [Art] IN (1020, 1090).
> 2. Beregn kroneavvik = [Regnskap_YTD] - [Budsjett_YTD] og prosentavvik = ([Regnskap_YTD] - [Budsjett_YTD]) / [Budsjett_YTD] * 100.
> 3. Sorter enhetene etter største kroneavvik og lag en sammendragstabell som viser de 5 enhetene med høyest overskridelse.
> 4. Lag et horisontalt stolpediagram som viser avviket i tNOK per enhet.
> ```

---

### **Prompt 1.2: Simulering av vikarstopp / ansettelsesstopp (Scenario-analyse)**
> **Formål:** Simulere helårseffekten dersom det innføres vikarstopp fra 1. oktober for et tjenesteområde.
>
> **Prompt:**
> ```text
> Bruk Python i Excel til å kjøre en scenariesimulering for Virksomhetsområde 'Helse og mestring' på kontogruppe Art 1020 (Vikarer):
>
> 1. Ekstrapoler nåværende mønster (snitt per måned hittil i år) for å beregne forventet regnskap ved årets slutt (EOY) uten tiltak.
> 2. Kjøre Scenario A: Reduksjon i vikarforbruk på 40 % fra oktober til desember.
> 3. Kjøre Scenario B: Fullstendig vikarstopp (100 % reduksjon) fra oktober til desember.
> 4. Presenter resultatet i en oversiktlig sammeligningstabell som viser [Opprinnelig EOY Prognose], [Scenario A EOY], [Scenario B EOY] og [Innsparing i tNOK].
> ```

---

### **Prompt 1.3: Automatisk avviksforklaring på KOSTRA-funksjonsnivå**
> **Formål:** Raskt identifisere hovedårsakene til at en hel funksjon (f.eks. Funksjon 242 Barnehage eller 253 Helse- og omsorgstjenester) avviker fra budsjett.
>
> **Prompt:**
> ```text
> Analyser tabellen 'KOSTRA_Månedsrapport'. Grupper dataene på [Funksjon] og [Artsgruppe] (Lønn 1000-1090, Driftsutgifter 1100-1500, Inntekter/Refusjoner 1600-1990).
>
> 1. Beregn regnskapsavviket i kroner og prosent hittil i år (YTD).
> 2. Skriv et kort, punktvis sammendrag på norsk (maks 150 ord) som forklarer hvilke artsgrupper som driver hovedavviket for Funksjon 242.
> 3. Angi eksplisitt om avviket skyldes lønnsvekst/merforbruk eller forsinkede statlige refusjoner (Art 1600/1700).
> ```

---

## 💬 KATEGORI 2: Power BI + Fabric IQ + Copilot i MS Teams — Ledelsesdialog

Disse promptene benyttes av ledere og rådgivere i **M365 Copilot Chat i Microsoft Teams** når Power BI-rapportene er integrert i Teams-kanaler.

---

### **Prompt 2.1: Rask statusspørring for Kommunalsjef i Teams**
> **Formål:** Gi kommunalsjefen umiddelbar status på sitt virksomhetsområde direkte fra Teams-chatten uten å måtte navigere manuelt i Power BI.
>
> **Prompt:**
> ```text
> Slå opp i Power BI-rapporten 'Økonomi og Virksomhetsstyring Kristiansand' for Virksomhetsområde 'Oppvekst':
> 
> Hva er forventet helårsavvik (EOY) for grunnskolesektoren (Funksjon 202), og hvilke tre skoler har de største negative budsjettavvikene per T2? Oppgi tallene i millioner kroner (mNOK) med én dekadisk presisjon.
> ```

---

### **Prompt 2.2: Generere månedlig avviksnotat til Enhetsleder**
> **Formål:** Økonomirådgiveren ber Copilot i Teams utarbeide et utkast til e-post/Teams-melding til en enhetsleder som har passert avviksterskelen.
>
> **Prompt:**
> ```text
> Basert på de seneste tallene i Power BI for Enhet 202 Lovisenlev skole:
>
> Utarbeid et vennlig, men profesjonelt utkast til en Teams-melding fra økonomirådgiveren til enhetslederen.
> - Trekk frem at rullende prognose viser et forventet merforbruk på 420 000 kr ved årets slutt.
> - Pek på at det er Art 1020 (Vikarer) og Art 1150 (Innkjøp) som driver avviket.
> - Inviter til et kort 15-minutters avklaringmøte neste uke for å drøfte korrigerende tiltak før T3-rapporteringen.
> ```

---

## 📝 KATEGORI 3: Word & PowerPoint — Saksfremlegg & Politisk Behandling

Disse promptene benyttes i **Copilot i Microsoft Word og PowerPoint** for å utarbeide vedtaksnotater og slidedecks for politiske utvalg (Formannskapet / Bystyret).

---

### **Prompt 3.1: Utkast til Saksfremlegg om tertialrapportering (Word)**
> **Formål:** Generere et strukturert førsteutkast til kommunedirektørens saksfremlegg om budsjettavvik og tiltak.
>
> **Prompt:**
> ```text
> Du er kommunedirektørens rådgiver i Kristiansand kommune. Skriv et utkast til saksfremlegg i Word basert på regnskapstallene i vedlagte notat 'Tertialrapport_T2_Oppvekst.docx'.
>
> Saksfremlegget skal følge kommunens standard mal for politiske saker:
> 1. Kommunedirektørens forslag til vedtak (punktvis, formelt språk jf. Kommuneloven § 14-5).
> 2. Bakgrunn for saken og økonomisk status (tabell med Rammeregnskap vs Prognose).
> 3. Vurdering og avviksforklaring (fokus på demografisk utvikling og vikarforbruk).
> 4. Foreslåtte inndekningstiltak og konsekvenser for tjenestetilbudet.
>
> Tonesett: Objektiv, forvaltningsmessig korrekthet, med 0 % feiltoleranse på oppgitte tall.
> ```

---

### **Prompt 3.2: Generere Bystyre-presentasjon fra godkjent saksfremlegg (PowerPoint)**
> **Formål:** Konvertere et godkjent Word-saksfremlegg til en visuell 7-slides presentasjon for politikerne.
>
> **Prompt:**
> ```text
> Lag en presentasjon på 7 lysbilder basert på det godkjente saksfremlegget 'Saksfremlegg_Tertial_T2.docx'.
>
> Slidestruktur:
> - Slide 1: Tittel og hovedbudskap (Status T2 2026).
> - Slide 2: Hovedtall i brystlommen (Inntekt, Utgift, Netto Avvik i mNOK).
> - Slide 3: Hvor trykker skoen? (Avvik per virksomhetsområde med visuell oppstilling).
> - Slide 4: Dypdykk: Vikar- og overtidskostnader i helse og oppvekst.
> - Slide 5: Foreslåtte innsparingstiltak og korrigeringer.
> - Slide 6: Fremdriftsplan og milepæler mot årsavslutning.
> - Slide 7: Kommunedirektørens innstilling til vedtak.
>
> Visuell stil: Ren, profesjonell, bruk av tabeller og fremhevede tallbokser. Ingen teknisk jargon.
> ```

---

## 🛠️ Feilsøking & Tipskort for M365 Copilot

| Problem / Feilmelding | Årsak | Løsning / Prompt-justering |
| :--- | :--- | :--- |
| **«Finner ikke Python i Excel»** | Cellen er ikke satt til `=PY`-modus. | Skriv `=PY` i formellinjen eller velg *Python* fra Formel-fanen før du stiller spørsmålet til Copilot. |
| **Copilot oppgir feil regnskapstall** | Usynlige tomme felt eller feil datatype i Excel-kolonnen. | Be Copilot: *"Sjekk at kolonne [Regnskap_YTD] er formatert som numerisk verdi og erstatt blanke felt med 0 før du summerer."* |
| **Svaret blir for generelt** | Manglende spesifisering av KOSTRA-hierarki. | Legg til spesifikke artskoder eller funksjonsnumre i prompten (f.eks. *"Spesifiser KUN for Art 1020 og Funksjon 202"*). |
| **Power BI-oppslag i Teams gir feil tilgang** | Brukeren mangler rettigheter i Power BI-workspace. | Verifiser at brukerens Entra ID (SSO) har lesetilgang til den underliggende semantiske modellen i Fabric. |

---
*Dokumentet er utarbeidet som en del av AI-implementeringen for Økonomi og virksomhetsstyring i Kristiansand kommune.*
