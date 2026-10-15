# Lønnsbudsjettering i Kristiansand kommune med Framsikt

## 1. Oversikt og Lønnsområdets Betydning
Lønn og sosiale utgifter utgjør om lag **70–80 % av de totale driftskostnadene** i Kristiansand kommune. Presis stillings- og lønnsbudsjettering er derfor avgjørende for at sektorer som Oppvekst og Helse og mestring skal holde sine økonomiske rammer.

Kommunen benytter **Framsikt Årsbudsjettmodul** til stillings- og lønnsbudsjettering. Framsikt erstatter manuelle "hjemmelagde" Excel-modeller med en automatisert, stillingsbasert beregningsmotor knyttet direkte mot kommunens HR- og lønnssystem.

---

## 2. Arkitektur og Hovedprinsipper for Lønnsbudsjett i Framsikt

### A. Integrasjon mot Lønnssystemet
* Framsikt henter grunnlagsdata for alle ansatte, hjemler og stillingskoder direkte fra kommunens HR- og lønnssystem (Visma / Unit4).
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
[ August ]      1. Henting av oppdaterte HR-data til Framsikt
                2. Generering og eksport av Excel-maler per seksjon/ansvar
                  |
[ September ]   3. Seksjonsleder gjennomgår bemanning i Excel-malen:
                   - Registrerer planlagte permisjoner og vikarutgifter
                   - Justerer stillingsbrøker eller nye hjemler
                   - Legger inn vakante stillinger og forventet oppstart
                  |
[ September ]   4. Innlesing (import) av oppdatert Excel-mal tilbake til Framsikt
                5. Automatisk rekalkulering av AGA, pensjon og feriepenger
```

### Hvordan Excel-malene fungerer:
* **Kolonnevelger i Framsikt:** Økonomiavdelingen eller seksjonsleder kan tilpasse visningen i Framsikt og eksportere stillingstabellen til en ferdig strukturert Excel-fil.
* **Sikker Import:** Excel-filen beholder unike ID-er for stillingshjemler og ansatte, slik at endringer gjort i Excel leses inn direkte på riktig ansvar, funksjon og artskonto i Framsikt uten manuell dobbelttasting.

---

## 4. Sjekkliste for Seksjonsledere ved Lønnsbudsjettering

For å sikre et realistisk lønnsbudsjett må seksjonsleder gå gjennom følgende punkter i oppstartsfasen etter ferien:

- [ ] **Kvalitetssikre stillingsplanen:** Stemmer listen over faste ansatte med faktisk bemanning per august?
- [ ] **Legge inn planlagte endringer:** Er fremtidige pensjoneringer, foreldrepermisjoner eller utdanningspermisjoner lagt inn med riktig start- og sluttdato?
- [ ] **Budsjettere vakanser:** Er ledige stillinger lagt inn med realistisk tiltredelsesdato og forventet lønnstrinn?
- [ ] **Variabel lønn og vikarer:** Er det avsatt tilstrekkelig pott til helge-/kveldstillegg og vikardekning basert på historiske tall?
- [ ] **Refusjoner:** Er det lagt inn realistiske anslag for sykelønnsrefusjoner under tilhørende inntektskontoer?
- [ ] **Avstemming mot ramme:** Viser oppsummert lønns- og driftsbudsjett at seksjonen holder seg innenfor tildelt budsjettramme?
