# Strategisk Implementasjonsplan: Selvbetjent Økonomistyring og AI-Beslutningsstøtte i Kristiansand Kommune

**Dokument-ID:** AI_KOM-STRAT-2026-04  
**Målgruppe:** Kommunedirektøren, Kommunalsjefer, Enhetsledere (Budsjettansvarlige) og Økonomirådgivere  
**Prosjekt:** AI_KOM — Control Office Hub  

---

## 1. Executive Summary & Visjon

Hovedmålet med denne implementasjonsplanen er å **demokratisere økonomistyringen** i Kristiansand kommune. Ved å gi alle 81 enhetsledere og budsjettansvarlige direkte tilgang til selvbetjente, AI-assisterte verktøy, reduseres den manuelle oppfølgingsbyrden på kommunens økonomirådgivere. 

Rollen til økonomirådgiveren transformeres fra å være en "manuell tallknuser og regeloppslagsverk" til å bli en **strategisk sparringspartner og kvalitetssikrer**.

```
[ Dagens Situasjon ]                                  [ Målbilde: AI_KOM Selvbetjening ]

Budsjettansvarlig                                      Budsjettansvarlig
       │                                                      │
       │ (Manuelle spørsmål, avviksforklaringer,              │ (Selvbetjent oppslag, auto-notat,
       │  konteringsregler, Framsikt-oppslag)                  │  Monte Carlo-prognoser & sjekklister)
       ▼                                                      ▼
Økonomirådgiver (Kapasitetsflaskehals)                 AI_KOM Control Office Hub (24/7)
       │                                                      │ (RAG, PII-skjermet, SHA-256 forseglet)
       ▼                                                      ▼
Manuelt Saksnotat / Rapport                            Økonomirådgiver (Strategisk Godkjenner / HITL)
```

---

## 2. Dagens Flaskehalser vs. Selvbetjent Løsning

| Område | Dagens Praksis (Høy Belastning på Rådgiver) | Selvbetjent AI_KOM Løsning | Tidsbesparelse / Effekt |
| :--- | :--- | :--- | :--- |
| **Avviksforståelse** | Leder ber rådgiver forklare hvorfor sektoren har merforbruk i Framsikt. | AI-assistenten analyserer KOSTRA-artsfordeling (f.eks. Art 1090 overtid) og viser nøkkelårsakene direkte. | **-80 % tidsbruk** på avviksanalyse |
| **Regeloppslag & Kontering** | E-post/telefon til rådgiver om mva-kompensasjon, selvkost eller KOSTRA-funksjoner. | RAG-basert Økonomi-GPT svarer umiddelbart med henvisning til Kommuneloven og interne retningslinjer. | **Svar på 2 sekunder** (døgnet rundt) |
| **Prognose & Årsavslutning** | Rådgiver kjører manuelle regneark for å beregne forventet årsavslutning. | Innebygget Monte Carlo-simulering (P10/P50/P90) gir automatisk årsavslutningsprognose. | **Proaktiv varsling** ved M8 |
| **Saksfremlegg & Notater** | Leder ber rådgiver skrive utkast til avviksnotat for Formannskapet. | Én-klikks generering av standardiserte saksfremlegg (Word `.docx`) med ferdige tabeller. | **Frigjør 3–5 timer** per politiske sak |

---

## 3. Fem Konkrete Implementasjonstiltak

### Tiltak 1: RAG-drevet "Økonomi-GPT" for Umiddelbar Regel- og Konteringsstøtte
* **Beskrivelse**: Etablere en intern, PII-skjermet chat-assistent for budsjettansvarlige som er matet med Kristiansand kommunes økonomireglement, attestasjonsinstruks, KOSTRA-konteringsveileder og Kommuneloven.
* **Funksjonalitet**: Budsjettansvarlig kan spørre: *"Hvilken art skal jeg bruke på innkjøp av konsulenttjenester til prosjekt X?"* eller *"Hvordan fakturere Nabokommune Y for vertskommunesamarbeid?"*.
* **Gevinst**: Fjerner opptil 70 % og henvendelser om rutinekontering og regelverk til økonomirådgiver.

### Tiltak 2: Interaktive Self-Service Dashboards med Kaskaderende Filtere
* **Beskrivelse**: Rulle ut Power BI-baserte selvhjelpsdashbord til alle 81 enhetsledere med automatisk Row-Level Security (RLS).
* **Funksjonalitet**: Lederen ser kun sine egne ansvarssteder, men kan enkelt filtrere på KOSTRA-funksjon, driftsarter (lønnsart 1010–1090 vs. varekjøp 1100–1270) og RAG-status.
* **Proaktivitets-alarm**: Systemet sender automatisk varsel når et enhetsavvik overstiger terskelen på \\(-2,0\\,\%\\) eller 250 000 kr, med ferdige forslag til tiltak.

### Tiltak 3: Én-klikks Generator for Saksfremlegg og Avviksnotater
* **Beskrivelse**: Automatisk utforming av skriftlige forklaringer når Formannskapet eller Kommunedirektøren krever avviksrapportering.
* **Funksjonalitet**: AI-motoren henter tall fra Visma ERP og Framsikt, sammenligner mot budsjettrammen jf. **Kommuneloven § 14-5**, og genererer et fyllestgjørende utkast til politisk saksfremlegg i Word (`.docx`).
* **Kvalitetssikring**: Økonomirådgiveren trenger kun å gjennomgå og godkjenne utkastet (Stage-Gate Port 9) i stedet for å skrive alt fra bunnen.

### Tiltak 4: Selvbetjente Selvkost- og Fakturakalkulatorer
* **Beskrivelse**: Gi budsjettansvarlige tilgang til ferdige Excel-verktøy (`selvkost_og_vertskommune_kalkyle.xlsx`) for beregning av tjenestesalg til eksterne parter.
* **Funksjonalitet**: Automatisk beregning av indirekte kostnader (overhead %), avskrivninger, kalkulatorisk rente og MVA-kompensasjon (25 %) etter selvkostforskriften.
* **Gevinst**: Sikrer at kommunen krever korrekte priser ved utgående fakturering uten at rådgiver må bygge manuelle kalkyler hver gang.

### Tiltak 5: "Cognitive Apprenticeship" & Kompetanseløft for Enhetsledere
* **Beskrivelse**: Implementere et strukturert opplæringsprogram basert på det internasjonale AI Literacy-rammeverket (8-kompetansemodellen) og Fitts & Posner læringstrinn.
* **Gjennomføring**: 
  1. *Modeling*: Økonomirådgiver viser hvordan AI-dashbordet benyttes i en avvikssak.
  2. *Scaffolding*: Lederen bruker AI-verktøyet med støtte fra sjekklister.
  3. *Fading*: Lederen håndterer sin egen økonomistyring selvstendig og søker råd kun ved komplekse strategiske valg.

---

## 4. Sikkerhets- og Governance-arkitektur

For at selvbetjening skal være trygt i kommunal sektor, bygges løsningen på tre ubøyelige sikkerhetsprinsipper:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PORT 4: LOKAL PII-SKJERMING (GDPR)                                        │
│ Vasker og anonymiserer fødselsnumre (11 siffer), bankkonti og helseopplysninger│
│ LOKALT før tekst sendes til språkmodellen.                                  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. ROW-LEVEL SECURITY (RLS) & BRUKERSTYRER                                  │
│ Tilgangsstyring integrert mot Azure AD / Entra ID.                          │
│ Enhetsleder (Ansvar 5200) ser kun sine data, Kommunalsjef ser sin sektor.  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. PORT 9: STAGE-GATE & SHA-256 REVISORSTEMPEL (EU AI Act Art. 14)          │
│ Ingenting sendes til politisk behandling uten menneskelig godkjenning.       │
│ Alle godkjente beslutninger får et kryptografisk SHA-256 stempel.           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Rullingsplan og Milepæler (M1 – M6)

```
Måned 1-2: PILOTERING          Måned 3-4: BREDDEUTVALG        Måned 5-6: FULL DRIFT
┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
│ • Pilot i Helse &      │    │ • Utrulling til alle   │    │ • Full selvbetjening   │
│   Mestring (Ansvar 5200)│───►│   81 enheter            │───►│   for 81 ledere        │
│ • Testing av PII-filter│    │ • Kursing i Økonomi-GPT│    │ • Rådgivere overgår    │
│ • Etablere RAG-kilde   │    │ • Power BI dashbord    │    │   til strategisk rolle │
└────────────────────────┘    └────────────────────────┘    └────────────────────────┘
```

* **Måned 1–2 (Pilotering)**: Lansere pilot for *Helse og mestring* (Ansvar 5200 / KOSTRA 254). Finpudse PII-filteret og RAG-oppslag på konteringsregler.
* **Måned 3–4 (Bredde-utrulling)**: Rulle ut Power BI-dashbordet og Økonomi-GPT til samtlige 81 enhetsledere på tvers av de 6 virksomhetsområdene. Arrangere 15-minutters mikrokurs.
* **Måned 5–6 (Effektmåling)**: Evaluere reduksjonen i e-post- og supporthenvendelser til økonomirådgiverne, samt måle kvaliteten på innsendte tertialrapporter.

---

## 6. Sjekkliste for Budsjettansvarlig (Selvbetjeningsrutine)

Ved månedlig periodelukking følger enhetslederen denne enkel selvbetjeningsrutinen i AI_KOM:

- [ ] **Trinn 1**: Åpne AI_KOM Dashboard og sjekk enhetens RAG-status (Grønn / Rav / Rød).
- [ ] **Trinn 2**: Ved Rød/Rav status: La AI-assistenten identifisere avviksartene (f.eks. merforbruk på overtid art 1090 mot manglende NAV-refusjon art 1600).
- [ ] **Trinn 3**: Kjør EVM Monte Carlo-prognosen for å se forventet årsavslutning per 31.12.
- [ ] **Trinn 4**: Generer automatisk utkast til avviksnotat dersom avviket krever politisk omdisponering jf. **Kommuneloven § 14-5**.
- [ ] **Trinn 5**: Godkjenn notatet (Stage-Gate Port 9) for å påføre SHA-256 revisjonsstempel før det oversendes økonomirådgiver for kort sluttkontroll.

---

*Utarbeidet av AI_KOM Control Office Hub for Kristiansand Kommune | v1.0 2026*
