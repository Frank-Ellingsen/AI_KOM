---
title: "Lønnsbudsjettering i Kristiansand kommune med Framsikt"
canonical_path: "budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md"
version: "2.1"
domain: "Stillings- og Lønnsbudsjettering"
statutory_basis: "Kommuneloven § 14-6 (Bruttoprinsippet), HTA § 4, KRS 6"
key_rules:
  aga_sone: "Sone 1 (14,1 % på Lønn + Feriepenger + Pensjon)"
  feriepenger: "12,0 % under 60 år / 14,3 % ved 60+ år"
  pensjonsordning: "SPK (13,8 %) for lærere, KLP (15,2 %) for øvrige"
  bruttoprinsipp: "Ingen nettobudsjettering av vikarmidler (1020) mot NAV-refusjon (1690)"
summary: "Stillings- og bemanningsbudsjettering i Framsikt EPM, skille mellom fast lønn (1010) og variable potter (1020/1050/1090), Excel eksport/import og pensjonskontroll."
---

# Lønnsbudsjettering i Kristiansand kommune med Framsikt

## 1. Oversikt og Lønnsområdets Betydning
Lønn og sosiale utgifter utgjør om lag **70–80 % av de totale driftskostnadene** i Kristiansand kommune. Presis stillings- og lønnsbudsjettering er derfor avgjørende for at sektorer som Oppvekst og Helse og mestring skal holde sine økonomiske rammer.

Kommunen benytter **Framsikt Årsbudsjettmodul** til stillings- og lønnsbudsjettering. Framsikt erstatter manuelle "hjemmelagde" Excel-modeller med en automatisert, stillingsbasert beregningsmotor knyttet direkte mot kommunens HR- og lønnssystem (Visma / Unit4).

---

## 2. Arkitektur og Hovedprinsipper for Lønnsbudsjett i Framsikt

### A. Integrasjon mot Lønnssystemet
* Framsikt henter grunnlagsdata for alle ansatte, hjemler og stillingskoder direkte fra kommunens HR- og lønnssystem.
* Systemet importerer data som fødselsdato, stillingsbrøk, fast lønn, ansiennitet, pensjonskasse (KLP/SPK) og organisatorisk plassering (ansvar og funksjon).

### B. Skille mellom Fast og Variabel Lønn
Framsikt deler lønnsbudsjetteringen i to hovedstrukturer:

1. **Fast Lønn (Stillingsoversikten):**
   * Budskjetteres per person eller vakant stillingshjemmel.
   * Inkluderer grunnlønn, faste månedlige tillegg, samt faste engasjementer.
   * Framsikt beregner automatisk per måned:
     * **Feriepenger**
     * **Arbeidsgiveravgift (AGA)**
     * **Pensjonskostnader** (KLP, SPK osv.)
2. **Variabel Lønn (Konto- og Potbudsjettering):**
   * Budskjetteres som samlede kronepotter på artskontoer i detaljbudsjettet.
   * Omfatter variabler som overtid, kvelds-/helgetillegg, vikarutgifter og uforutsett fravær.
   * Motregnes mot forventede sykelønns- og foreldrepengerefusjoner.

---

## 3. Arbeidsflyt for Seksjonsledere etter Sommerferien (Excel Eksport/Import)

Når det administrative budsjettarbeidet rulles ut i **august/september**, starter seksjonslederne og enhetslederne arbeidet med neste års lønns- og bemanningsplan:

```
[ Primo August ]    1. Henting av oppdaterte HR-data til Framsikt
                    2. Generering og eksport av Excel-maler per seksjon/ansvar
                      |
[ Medio August -   3. Seksjonsleder gjennomgår bemanning i Excel-malen:
  Primo Sept ]        - Registrerer planlagte permisjoner og vikarutgifter
                      - Justerer stillingsbrøker eller nye hjemler
                      - Legger inn vakante stillinger og forventet oppstart
                      |
[ Medio Sept ]      4. Innlesing (import) av oppdatert Excel-mal tilbake til Framsikt
                    5. Automatisk rekalkulering av AGA, pensjon og feriepenger
```

---

## 4. Utvidet Sjekkliste: Kontroll av Pensjon, Arbeidsgiveravgift og Sosiale Kostnader i Excel-malene

For å unngå budsjetteringsfeil ved eksport og import mellom Framsikt og Excel, må seksjonsleder og økonomikonsulent gjennomføre følgende spesifikke kontrollpunkter:

### A. Kontroll av Pensjonsberegninger
- [ ] **Pensjonsinnmelding (KLP vs. SPK):** Kontroller at lærere er registrert på Statens pensjonskasse (SPK) og øvrige ansatte på Kommunal Landspensjonskasse (KLP) eller egen kommunal pensjonskasse.
- [ ] **Satskontroll:** Sjekk at samlet pensjonssats (ordinær premie + reguleringspremie) ligger inne med gjeldende prosentsats (normalt 14–18 % i kommunal sektor avhengig av pensjonsordning).
- [ ] **Gjennomsnittlig uføre- og etterlattepremie:** Forutsetninger om fremtidig premieavvik skal være i henhold til kommunens finansreglement og regnskapsstandard KRS 6.

### B. Kontroll av Arbeidsgiveravgift (AGA) og Feriepenger
- [ ] **Arbeidsgiveravgiftssone:** Kontroller at ansatte er koblet til korrekt AGA-sone (Kristiansand ligger i sone 1 med **14,1 %** AGA).
- [ ] **AGA på pensjon og feriepenger:** Påse at Excel-beregningen eller Framsikt-importen automatisk legger AGA (14,1 %) på både feriepengeavsetningen og pensjonskostnaden.
- [ ] **Feriepengesats:** Verify at feriepenger er beregnet med **12,0 %** for ansatte under 60 år, og **14,3 %** for ansatte over 60 år (ekstra ferieuke).

### C. Variabel Lønn, Vikarer og Refusjoner
- [ ] **Koble variabel lønn mot AGA:** Husk at variable pot-avsetninger på overtid (art 1090) og kvelds-/helgetillegg (art 1050) også må generere AGA.
- [ ] **Sykepenge- og foreldrepengerefusjoner:**
  - Sjekk at refusjoner inntektsføres på riktige artskontoer (arts serie 1690/1790).
  - Bruk historiske tall for fravær som grunnlag – **ikke** overbudsjetter urealistisk høye refusjonsinntekter uten tilsvarende vikarutgifter.
- [ ] **Kollektive avtaler og lønnsoppgjør:** Sjekk om det er lagt inn en sentral avsetning til lønnsoppgjør/prosentvis lønnsvekst, slik at seksjonen ikke legger inn uavklarte lønnstillegg manuelt på enkeltpersoner.

### D. Teknisk Kontroll ved Excel-import
- [ ] **Behold Unike ID-er:** Endre aldri ID-kolonnene (Stilling ID, Ansatt ID, Ansvar) i Excel-filen. Dette sikrer at Framsikt matcher data korrekt ved re-import.
- [ ] **Månedsoppdeling:** Sjekk at endringer i stillingsbrøk eller nye oppstarter legges på riktig startmåned (f.eks. fra 01.08 for skoleelever/lærere), slik at lønnskostnaden ikke fordeles over 12 måneder ved feiltakelse.
- [ ] **Bildekontroll i Framsikt:** Etter import, kjør rapporten "Lønnsbudsjett per ansvar/seksjon" i Framsikt for å verifisere at totalsummen i Framsikt stemmer nøye overens med oppsummert Excel-ark.
