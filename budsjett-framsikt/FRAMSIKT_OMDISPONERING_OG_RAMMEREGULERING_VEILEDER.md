---
title: "Framsikt EPM: Veileder for Rammeregulering, Budsjettparaply og Omdisponering mellom Enheter"
canonical_path: "budsjett-framsikt/FRAMSIKT_OMDISPONERING_OG_RAMMEREGULERING_VEILEDER.md"
version: "2.1"
domain: "Kommunal Finans, EPM og Prosjektcontrolling"
statutory_basis: "Kommuneloven § 14-5, § 14-6, Bystyrets Økonomireglement (11.10.2023)"
lead_controller: "Frank Ellingsen (Senior Financial Controller)"
target_audience: "Kommunalsjefer (Nivå 1), Områdeledere (Nivå 2), Enhetsledere (Nivå 3), Sektorcontrollere"
summary: "Trinn-for-trinn veiledning for administrativ omdisponering av overskudd og dekning av underskudd under Kommunalsjefens budsjettparaply i Framsikt EPM, med konkrete konteringsregler og CSV batch-format."
---

# 🏛️ Framsikt EPM: Veileder for Rammeregulering & Budsjettparaply

## 1. Rettslig Grunnlag og Delegeringsfullmakter

### A. Kommunelovens Krav (§ 14-5 og § 14-6)
* **Kommuneloven § 14-5 (Budsjettbalanse og tiltaksplikt):**
  Årsbudsjettet er en bindende plan for kommunens virksomhet og økonomi. Dersom det underveis i regnskapsåret oppstår avvik som truer budsjettbalansen ($VAC < 0$), plikter Kommunedirektøren og ansvarlige ledere å iverksette korrigerende tiltak for å bringe forbruket i balanse innen årets slutt (Netto Null Avvik ved 31.12).
* **Kommuneloven § 14-6 (Bruttoprinsippet):**
  Alle utgifter og inntekter skal budsjetteres og regnskapsføres fullt ut (brutto). Det er **ikke tillatt å nettoføre** vikarlønn (art 1020) mot fast lønn (art 1010) eller mot sykelønnsrefusjon fra NAV (art 1690).

### B. Bystyrets Økonomireglement og Fullmaktspyramiden
Bystyret i Kristiansand vedtar årlig samlet rammebevilgning per virksomhetsområde/sektor. Innenfor disse rammene gjelder følgende delegering:

| Nivå | Rolle / Tittel | Eksempler i Kristiansand | Omdisponeringsfullmakt i Framsikt |
| :--- | :--- | :--- | :--- |
| **Nivå 0** | Bystyret / Formannskapet | Politisk ledelse | Tilleggsbevilgninger og endringer i samlet netto kommuneramme. |
| **Nivå 1** | Kommunalsjefer & Kommunedirektør | Kristin Robstad (Oppvekst), Brede Skeie (Helse), Ragnar Evensen (Byutv) | **Full omdisponeringsrett** mellom enheter innenfor eget rammeområde uten politisk behandling (sum endring = 0 NOK). |
| **Nivå 2** | Områdeledere | Svein Tore Kvernes (Skole), Mette Syvertsen (Institusjon) | Kan foreslå rammeflyttinger mellom underliggende skoler/sykehjem. |
| **Nivå 3** | Enhetsledere / Rektorer | Trond Jensen (2020 / Lovisenlev), Solveig Grimstad (Strai 401), Hans Petter Vik (Byggesak 301) | Fullmakt til å omdisponere mellom artskonti innenfor **egen tildelt enhetsramme** (art 1000–1270). |

---

## 2. Budsjettparaplyen: Solidaritets- og Omdisponeringsmekanismen

Budsjettparaplyen er Kristiansand kommunes operative modell for å sikre at sektorene når **Netto Null Avvik** uten å trekke på kommunens sentrale disposisjonsfond.

```
       [ NIVÅ 1: KOMMUNALSJEFENS BUDSJETTPARAPLY ]
              (Felles sektorramme og bufferpott)
                     ▲                     │
     Avstått overskudd│                     │ Rammekompensasjon
     (Surplus / +kr) │                     ▼ (Inndekning / -kr)
       ┌─────────────┴────────┐   ┌────────┴─────────────┐
       │   ENHET MED SURPLUS  │   │  ENHET MED DEFICIT   │
       │ (Byggesak / Bibliot) │   │ (Strai / Lovisenlev) │
       │ Avvik: +kr 350 000   │   │ Avvik: -kr 512 000   │
       └──────────────────────┘   └──────────────────────┘
```

### A. Hva gjør enheten ved Surplus (Mindreforbruk / Overskudd)?
1. **Identifisering og verifisering:**
   * Månedsrapporten viser et positivt avvik ($Budsjett - Actuals > 0$).
   * Sektorcontroller verifiserer at mindreforbruket er reelt (f.eks. ubesatte stillinger/vakanser, lavere barnekull, eller merinntekter) og ikke etterslep i fakturamottak.
2. **Frigjøring til Paraplybufferen:**
   * Enhetsleder melder inn overskytende disponibel ramme til Kommunalsjefen.
   * Midlene overføres administrativt i Framsikt fra enhetens ramme til Kommunalsjefens paraplybuffer (f.eks. `5000-SJEF-HELSE` eller `4000-SJEF-OPPV`).
3. **Mål og gevinst:**
   * Enheten avslutter året i perfekt balanse (Netto Null Avvik).
   * Overskuddet redder søsterenheter som har uforutsett sykdom eller lovpålagte ressurskrevende brukere.

### B. Hva gjør enheten ved Deficit (Merforbruk / Underskudd)?
1. **Obligatorisk iverksetting av interne preskripsjoner:**
   Før enheten kan søke om paraplymidler, må følgende interne tiltak dokumenteres i månedsrapporten:
   * **Vikarstopp (Art 1020):** Alle vikartimer må forhåndsgodkjennes; interne vikarringer prioriteres.
   * **Overtidsbrems (Art 1090):** Overtid begrenses strengt til liv og helse jf. AML § 10-6/§ 10-12.
   * **Inndriving av NAV-refusjoner (Art 1690):** Utestående sykelønnsrefusjoner eldre enn 14 dager må purres for å tette refusjonsgapet.
   * **Driftsbrems (Art 1150/1200):** Frys av innkjøp, kurs og reiser.
2. **Søknad om Rammekompensasjon:**
   * Dersom sesongjustert EOY-prognose (P50) fortsatt viser negativt sluttavvik, oversendes saken til Kommunalsjefen med forslag til rammeregulering.
3. **Tildeling fra Paraplyen:**
   * Kommunalsjefen godkjenner overføring fra sektorens bufferpott/overskuddsenheter direkte til enhetens vikarbudsjett (art 1020).

---

## 3. Trinn-for-Trinn Veiledning i Framsikt EPM

### Steg 1: Åpne Framsikt og Naviger til Reguleringsmodulen
1. Logg inn på **Framsikt EPM** (`https://kristiansand.framsikt.no/`) via Feide / Azure AD.
2. Velg modulen **Budsjett & Prognose** i toppmenyen.
3. Klikk på **Tertialoppfølging / Budsjettreguleringer**.
4. Velg gjeldende regnskapsår (**2026**) og gjeldende periode (f.eks. **M09 — September** eller **T2 — 2. Tertial**).

---

### Steg 2: Opprett Ny Rammereguleringssak
1. Klikk på knappen **+ Ny Budsjettregulering**.
2. Fyll ut metadata i dialogboksen:
   * **Reguleringsnavn:** `Administrativ Paraplyomdisponering M09 — Sektor [Oppvekst / Helse]`
   * **Reguleringstype:** `Intern omdisponering innen rammeområde (Nivå 1)`
   * **Hjemmel:** `Bystyrets Økonomireglement punkt 4.2 / Kommuneloven § 14-5`
   * **Saksbehandler:** `Frank Ellingsen (Senior Controller)`
   * **Godkjenner:** `Kommunalsjef [Navn]`

---

### Steg 3: Registrer Konteringslinjer (Debet / Kredit Ramme)

Hver regulering **MÅ gå i null** totalt på rammeområdet ($\sum \Delta = 0\text{ NOK}$).

#### Eksempel A: Strai Sykehjem (Underskudd dekkes av Helseparaplyen)
| Linje | Type | Ansvar | Funksjon | KOSTRA Art | Beløp (NOK) | Tekst / Begrunnelse |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **1** | Avgiver (Kredit) | `5000-SJEF-HELSE` | `254` | `1020` | **-511 961** | Omdisponering fra bufferpott Helse- og mestringsparaplyen |
| **2** | Mottaker (Debet) | `5200-ENH-401` | `254` | `1020` | **+511 961** | Rammestyrking vikarbudsjett Strai Sykehjem etter vikarstopp |
| **SUM** | **Netto Balanse** | - | - | - | **kr 0,00** | **Avstemt og klar for godkjenning** |

#### Eksempel B: Byggesak og Tilsyn (Overskudd avgis til Byutviklingsparaplyen)
| Linje | Type | Ansvar | Funksjon | KOSTRA Art | Beløp (NOK) | Tekst / Begrunnelse |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **1** | Avgiver (Kredit) | `3300-ENH-301` | `301` | `1020` | **-2 023 436** | Frigjøring av mindreforbruk Byggesak til sektorbuffer |
| **2** | Mottaker (Debet) | `3000-SJEF-BYUTV` | `301` | `1020` | **+2 023 436** | Tilførsel felles reservepott By- og stedsutvikling |
| **SUM** | **Netto Balanse** | - | - | - | **kr 0,00** | **Avstemt og klar for godkjenning** |

---

### Steg 4: Kontroll, Godkjenning og Låsing
1. Kontroller at **Netto Endring i Framsikt viser 0 kr**.
2. Klikk **Kontroller Regler**: Framsikt verifiserer at:
   * Kontokombinasjonene (Ansvar/Funksjon/Art) er gyldige i KOSTRA.
   * Arbeidsgiveravgift og pensjon er automatisk hensyntatt.
3. Klikk **Send til Godkjenning**:
   * Sektorcontroller (Frank Ellingsen) attesterer.
   * Kommunalsjef (Nivå 1) mottar varsel og signerer digitalt med BankID / Azure MFA.
4. Når Kommunalsjefen godkjenner, settes status til **LÅST OG GODKJENT**.

---

### Steg 5: Eksport og Synkronisering til Visma / Unit4 ERP
* Hver månedsslutt eksporteres godkjente reguleringer automatisk fra Framsikt til Visma/Unit4 via kommunens integrasjonsmotor.
* Justert ramme vises umiddelbart i neste måneds kontoutskrift og Power BI Teams-dashboard.

---

## 4. Automatisk Batch-Import via CSV

Dersom det gjennomføres mange omdisponeringer samtidig, kan Framsikts batch-importmodul benyttes. Skriptet `tools/generate_monthly_pdf_reports.py` genererer automatisk filen:
`reports/monthly_pdf_packets/FRAMSIKT_BATCH_OMDISPONERING_M9_2026.csv`

### Filspesifikasjon:
* **Tegnsett:** UTF-8 med BOM (`utf-8-sig`)
* **Skilletegn:** Semikolon (`;`)
* **Kolonnestruktur:**
  1. `regulerings_id`: Unik ID per reguleringspar (f.eks. `REG-2026-M9-1001`)
  2. `periode`: Periodekode (`2026-M09`)
  3. `sektor_kode`: Sektorkode (`HELSE`, `OPPVEKST`, etc.)
  4. `type`: Reguleringstype (`RAMMEREGULERING`)
  5. `ansvar_kode`: KOSTRA-ansvarsnummer
  6. `funksjon_kode`: KOSTRA-funksjonsnummer
  7. `art_kode`: KOSTRA-artskonto (`1010`, `1020`, etc.)
  8. `belop_nok`: Beløp med desimaler (negativt for avgiver, positivt for mottaker)
  9. `tekst`: Forklarende saksbeskrivelse
  10. `attestant_upn`: E-post til ansvarlig leder
  11. `controller_upn`: E-post til kvalitetssikrende controller
  12. `status`: `FORSLAG_TIL_KOMMUNALSJEF`

### Slik importeres filen i Framsikt:
1. Gå til **Framsikt Administrasjon ➜ Dataimport ➜ Budsjettjusteringer**.
2. Velg filen `FRAMSIKT_BATCH_OMDISPONERING_M9_2026.csv`.
3. Klikk **Valider fil**. Systemet bekrefter at alle posteringspar balanserer mot 0 kr.
4. Klikk **Utfør import**. Alle sakene opprettes automatisk og legges i Kommunalsjefens godkjenningskø.

---

## 5. Oppsummering og Sjekkliste for Budsjettansvarlig

- [ ] **1. Har du sjekket månedens avvik ($Budsjett - Actuals$)?**
  - Positivt avvik = Mindreforbruk (Surplus). Vurder frigjøring til paraplyen.
  - Negativt avvik = Merforbruk (Deficit). Iverksett interne tiltak umiddelbart.
- [ ] **2. Er interne innstramminger iverksatt før søknad om paraplymidler?**
  - Vikarstopp (art 1020), overtidsbrems (art 1090), driftsbrems (art 1150).
- [ ] **3. Er NAV-sykelønnsrefusjoner purret for å tette refusjonsgapet?**
- [ ] **4. Går omdisponeringsposteringen i Framsikt i nøyaktig 0 kr?**
- [ ] **5. Er saken forankret hos Sektorcontroller (Frank Ellingsen) før Kommunalsjefens godkjenning?**

---
*Dokumentet er utarbeidet av Frank Ellingsen (Senior Financial Controller) i samsvar med Kristiansand kommunes økonomireglement og Edward Tufte Data-Ink standarder.*
