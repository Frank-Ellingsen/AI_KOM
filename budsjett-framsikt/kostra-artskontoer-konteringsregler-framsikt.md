# KOSTRA Artskontoer og Konteringsregler for Lønnsområdet i Framsikt

## 1. Innledning og Systematikk
I norsk kommunal økonomi styres kontoplanen etter **KOSTRA-forskriften** og **Budsjett- og regnskapsforskriften**. Kontoplanen sikrer at alle utgifter og inntekter konteres enhetlig på tvillingaksel:
* **Funksjon:** *Hvilken tjeneste/formål* pengene brukes til (f.eks. funksjon 202 Grunnskole eller 253 Hjemmesykepleie).
* **Art:** *Hvilken type utgift/inntekt* det gjelder (f.eks. art 1010 Fast lønn eller art 1690 Sykelønnsrefusjon).

I **Framsikt** kobles KOSTRA-artene direkte til modulene for **Stillingsbudsjett** (fast lønn og sosiale utgifter) og **Konto-/Potbudsjett** (variabel lønn, overtid og refusjoner).

---

## 2. Oversikt over Artskontoer for Lønn, Sosiale Utgifter og Refusjoner

### A. Utgiftskontoer: Lønn og Sosiale Kostnader (1000-serien / 000-120)

| KOSTRA Art (4-siffer) | KOSTRA Art (3-siffer) | Kontonavn | Framsikt-modul | Konteringsregel og Innhold |
| :--- | :--- | :--- | :--- | :--- |
| **1010** | **010** | Fast lønn / fastlønn | Stillingsoversikt | Bruttolønn for faste stillinger og faste engasjementer. Beregnes automatisk per stilling/ansatt i Framsikt. |
| **1020** | **020** | Lønn til vikarer | Konto / Pot | Lønn til timelønte sykevikarer og kortere vikariater ved fravær. Budskjetteres som kronepott per ansvar. |
| **1030** | **030** | Lønn til ekstrahjelp | Konto / Pot | Timelønte ekstrahjelper ved sesongtopper, prosjekter eller uforutsett arbeidsmengde utenom sykdom. |
| **1040** | **040** | Lønn til lærlinger | Stilling / Pot | Lønn og godtgjørelse til kommunale lærlinger etter gjeldende læretekst og lærlingelønnssatser. |
| **1050** | **050** | Annen lønn og godtgjørelser | Stilling / Pot | Trekkpliktige uregelmessige tillegg, utrykningstillegg, klesgodtgjørelse og stasjonsvakter. |
| **1090** | **090** | Overtid og ubekvem tid | Konto / Pot | Overtidsbetaling jf. HTA, samt turnustillegg (kvelds-, natt- og helgetillegg, lørdags-/søndagstillegg). |
| **1099** | **099** | Påløpt feriepengeavsetning | Automatisk (System) | Regnskapsmessig avsetning for opptjente feriepenger (12,0 % / 14,3 %). Håndteres maskinelt i Framsikt. |
| **1200** | **120** | Pensjonsinnskudd (KLP/SPK) | Automatisk (Stilling) | Arbeidsgivers lovpålagte pensjonspremie. Framsikt beregner ut fra stillingens pensjonskassetilhørighet. |
| **1210** | **121** | Arbeidsgiveravgift (AGA) | Automatisk (System) | AGA av lønn, tillegg og pensjon. Beregnes ut fra kommunens sone (14,1 % for Kristiansand / Sone 1). |
| **1220** | **122** | Yrkesskade/gruppeliv | Automatisk (Stilling) | Lovpålagte personalforsikringer og gruppelivsordninger for kommunalt ansatte. |

---

### B. Inntektskontoer: Trygde- og Refusjonsinntekter (1600-1700-serien / 690-750)

| KOSTRA Art (4-siffer) | KOSTRA Art (3-siffer) | Kontonavn | Framsikt-modul | Konteringsregel og Innhold |
| :--- | :--- | :--- | :--- | :--- |
| **1690** | **690** | Sykelønnsrefusjon fra NAV | Konto / Pot (Inntekt) | Refusjon av sykepenger og fødselspenger/foreldrepenger fra NAV etter arbeidsgiverperioden (16 dager). |
| **1691** | **691** | Andre NAV-refusjoner | Konto / Pot (Inntekt) | Refusjoner for tilrettelagt arbeid, kvalifiseringsstønad (KVP), pleiepenger og opplæringspenger. |
| **1700** | **700** | Refusjon fra staten | Konto / Pot (Inntekt) | Øremerkede statlige tilskudd til lønn/stilling (f.eks. IMDi-tilskudd, Helsedirektoratet, Udir). |
| **1750** | **750** | Refusjon fra andre kommuner | Konto / Pot (Inntekt) | Refusjonskrav sendt nabokommuner for verts- eller interkommunale samarbeid og gjesteelever. |

---

## 3. Konteringsregler og Budsjettprinsipper i Framsikt

### A. Fast Lønn (Art 1010) vs. Vikarbruk (Art 1020)
1. **Hovedregel for Fast Lønn:** Alle faste årsverk og godkjente hjemler skal budsjetteres på **Art 1010** via Stillingsoversikten i Framsikt. Lønnen skal tilpasses den enkeltes faktiske lønnstrinn/ansiennitet eller vakansens forventede lønnstrinn.
2. **Kopling mellom Sykefravær og Vikarbruk:**
   * Sykefravær skal **ikke** føre til reduksjon i budsjettet på Art 1010 (da den sykemeldte har rett til full lønn fra kommunen).
   * Behov for erstatningsarbeidskraft/vikarer ved sykefravær skal budsjetteres på **Art 1020 (Lønn til vikarer)**.
   * Forventet refundert sykelønn fra NAV etter arbeidsgiverperioden skal budsjetteres under inntektskonto **Art 1690 (Sykelønnsrefusjon)**.

> ⚠️ **Fallgruve å unngå:** Seksjonsleder må unngå å "nettoføre" vikarkostnader direkte mot fast lønn. Fast lønn (Art 1010), vikarlønn (Art 1020) og sykelønnsrefusjon (Art 1690) må alltid føres bruttokorrigerte på sine respektive artskontoer for at KOSTRA-rapporteringen og de automatiske sosiale utgiftene skal bli korrekte.

---

### B. Variabel Lønn, Turnus og Overtid (Art 1050 og Art 1090)
1. **Ubekvem arbeidstid (Helg, kveld, natt):**
   * Turnustillegg som utbetales etter fast turnusplan skal føres på **Art 1090** (eller dedikert underkonto i Framsikt).
   * For turnusintensive sektorer (som Helse og mestring) skal historisk dekningsgrad og turnusplanens faktiske matrise legges til grunn i Framsikt.
2. **Overtid (Art 1090):**
   * Overtidsbudsjettet skal dekke planlagt og uforutsett akutt overtid jf. Hovedtariffavtalen (HTA). Overtidsbruken må avgrenses mot ordinær vikarbruk.

---

### C. Automatisk Beregning av Sosiale Kostnader i Framsikt
I Framsikt genereres de sosiale kostnadene automatisk basert på det som registreres på art 1010, 1020, 1030, 1040, 1050 og 1090:

$$\text{Bruttolønn (1010-1090)} \xrightarrow{+\text{Feriepenger (12\% / 14,3\%)}} \xrightarrow{+\text{Pensjon (KLP/SPK)}} \xrightarrow{\times \text{AGA-sats (14,1\%)}} \text{Total Lønnskostnad}$$

* **Pensjon (Art 1200):** Framsikt skiller automatisk mellom KLP (sykepleiere, fagarbeidere, konsulenter) og SPK (lærere). Premiesatsen legges inn sentralt av økonomiavdelingen.
* **Arbeidsgiveravgift (Art 1210):** Beregnes av samlet bruttolønn + feriepenger + pensjonsinnskudd.

---

## 4. Sjekkliste for Kvalitetskontroll før Låsing av Lønnsbudsjettet

Seksjonsleder og økonomirådgiver bør gjennomgå følgende sjekkliste før detaljbudsjettet låses i Framsikt:

- [ ] **1. Fullstendig Hjemmelsavstemming:** Er alle faste og midlertidige stillinger i seksjonen registrert på riktig ansvar og funksjon?
- [ ] **2. Bruttoføring av Vikarer og NAV-refusjon:** Er det et realistisk forhold mellom avsatt vikarpott på Art 1020 og estimert sykelønnsrefusjon på Art 1690?
- [ ] **3. Korrekt Arbeidsgiveravgiftssone:** Er alle konteringer satt med riktig avgiftssone (Sone 1 / 14,1 % for Kristiansand)?
- [ ] **4. Pensjonskassetilhørighet:** Er lærere koblet mot SPK og øvrige ansatte koblet mot KLP?
- [ ] **5. Kontroll av Turnustillegg og Overtid:** Er historiske turnustillegg på Art 1090 oppdatert i tråd med nye turnus- og bemanningsplaner?
- [ ] **6. Avstemming mot Tildelt Ramme:** Viser Framsikts konsoliderte rapport at seksjonens samlede lønns- og driftsbudsjett ligger innenfor rammevedtaket?
