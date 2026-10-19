# Forenklet Økonomistyring for Enhetsledere — Enkel Hverdag med Full Lovlighet og Kontroll

> **Sammendrag:** Denne veilederen forklarer hvordan budsjettansvarlige enhetsledere kan utføre effektiv, selvbetjent økonomistyring på minimum tid, samtidig som alle lovkrav, internkontrollregler og revisjonskrav overholdes uavkortet.

---

## 1. Formål og Filosofi: "Minst Mulig Støy — Full Kontroll"

Målet med forenklet økonomistyring er at enhetsledere ikke skal bruke tid på manuelle registreringer, kompliserte tabeller eller unødvendig rapportering når driften går som planlagt. 

Gjennom **unntaksbasert styring ("Management by Exception")** forholder du deg kun til sakene som krever handling, mens systemet automatisk ivaretar lovmessig kontroll, personvern og sporbarhet i bakgrunnen.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ DRIVENDE PRINSIPP: UNNTAKSBASERT STYRING ("MANAGEMENT BY EXCEPTION")    │
├─────────────────────────────────────────────────────────────────────────┤
│ 🟢 GRØNN STATUS (I Balanse / Avvik < 2 %):                             │
│    -> Ingen handling kreves. Automatisk månedsoppgjør i bakgrunnen.   │
├─────────────────────────────────────────────────────────────────────────┤
│ 🔴 RØD STATUS (Forventet Merforbruk):                                  │
│    -> Triage-varsel utløses. Systemet foreslår ferdig tiltaksnotat.     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Den Månedlige Rutinen i 3 Steg

I stedet for å gå gjennom lange rapporter, følger du denne 3-stegs rutinen ved månedsslutt:

### Steg 1: Sjekk Triage-Feeden (10 sekunder)
Åpne dashbordet. Systemet viser din status:
* **🟢 Grønn**: Alt er innenfor rammen. Du er ferdig for måneden.
* **🔴 Rød**: Det er oppdaget et projisert avvik (f.eks. merforbruk på overtid/vikarer). Gå til Steg 2.

### Steg 2: Gjennomgå Automatisk Tiltaksnotat (1 minutt)
Når status er rød, har systemet ferdigstilt et utkast til avviksnotat basert på faktiske tall fra Visma ERP og Framsikt:
* Avviket forklares automatisk (f.eks. sykefravær og forsinket NAV-refusjon).
* Konsekvenser for årsavslutning (P50/P90-prognose) er ferdig beregnet.
* Lovhjemmel jf. *Kommuneloven § 14-5* er automatisk lagt inn.

### Steg 3: Signer og Godkjenn (Stage-Gate Port 9)
Du leser gjennom, gjør eventuelle egne tilpasninger, og klikker **Godkjenn**. 
* Beslutningen stemples med et **kryptografisk SHA-256 revisjonsstempel**.
* Notatet oversendes automatisk til økonomirådgiver og Formannskapet.

---

## 3. Ufravikelige Lovkrav og Kontrollmekanismer

Selv om hverdagen forenkles, prutes det aldri på lovlighet eller kontroll. Systemet opprettholder følgende krav automatisk:

| Lov / Regelverk | Hva kravet sier | Hvordan systemet sikrer det |
| :--- | :--- | :--- |
| **Kommuneloven § 14-5** *(Budsjettbalanse)* | Kommunedirektøren plikter å fremme sak om innsparing eller omdisponering ved forventet underskudd. | Automatisk avviksdeteksjon som genererer ferdig saksfremlegg ved merforbruk. |
| **Kommuneloven § 14-6** *(Bruttoprinsippet)* | Alle utgifter og inntekter skal føres brutto. Det er forbudt å motregne utgifter mot inntekter. | Konteringskontroll stopper forsøk på nettobudsjettering og sikrer korrekt art (f.eks. salgsinntekt art 600–790). |
| **Attestasjon & Anvisning** *(Internkontroll)* | Ingen kan godkjenne sine egne bilag. To-trinns godkjenning kreves. | Rollebassert tilgangskontroll (RLS) skiller saksbehandler (attestasjon) fra budsjettansvarlig (anvisning). |
| **GDPR / Personvern** *(Port 4)* | Personopplysninger og fødselsnumre skal skjermes. | Automatisk lokal PII-scrubber sladder 11-sifrede fødselsnumre, bankkonti og helseopplysninger før lagring. |
| **EU AI Act Art. 14** *(Menneskelig kontroll)* | AI kan gi anbefalinger, men aldri fatte autonome juridiske/økonomiske vedtak. | Mennesket i løkka (Human-In-The-Loop) må eksplisitt godkjenne alle AI-notater med SHA-256 stempel. |

---

## 4. Praktiske Sjekklister for Hverdagen

### A. Utgående Fakturering (Når din enhet leverer tjenester eksternt)
Når din enhet har levert tjenester, utstyr eller personell til eksterne aktører eller nabokommuner:
1. **Bruk Selvkostkalkulatoren**: Beregn direkte kostnader + indirekte overhead % + ev. avskrivninger.
2. **Brutto Kontering**: Fakturer hele beløpet på utgående salgsinntekt/refusjon (salgsart). Ikke trekk beløpet direkte fra på utgiftsarten din.
3. **MVA-sjekk**: Sjekk om tjenesten utløser ordinær MVA (25 %) eller MVA-kompensasjon jf. *MVA-kompensasjonsloven*.
4. **EHF-Utsendelse**: Send fakturaen via kommunens centraliserte EHF-fakturamottak.

### B. Inngående Bilagsbehandling og Attestasjon
1. **Sjekk Bilaget**: Er varen/tjenesten mottatt i henhold til avtale?
2. **Korrekt Kontering**: Sjekk at **Kontoklasse (1/2)**, **Funksjon (KOSTRA)**, **Art** og **Ansvar** stemmer.
3. **To-trinns Godkjenning**: Attester bilaget og send til overordnet leder for anvisning dersom beløpet overstiger din fullmakt.

---

## 5. Oppsummering for Ledere

* **Ved grønn status**: Gjør ingenting — systemet dokumenterer at alt er i orden.
* **Ved rød status**: Bruk 1 minutt på å godkjenne det ferdige avviksnotatet.
* **Ved spørsmål om regler/kontering**: Bruk den integrerte Økonomi-GPT-assistenten i stedet for å vente på e-postsvar.
* **Trygghet**: Alle prosesser er lovlige, sporbare og revisjonsgodkjente.
