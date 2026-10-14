# Modul 3: Governance, Etikk, GDPR og EU AI Act

## 1. Det Juridiske og Regulatoriske Landskapet

Implementering av AI i offentlig økonomistyring reguleres av et samvirkende regelverk:

```
                  +-----------------------------------+
                  |           EU AI ACT               |
                  |  (Klassifisering & Deployer-krav) |
                  +-----------------+-----------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            ▼                                               ▼
+-----------------------+                       +-----------------------+
|         GDPR          |                       |   FORVALTNINGSLOVEN   |
| (Behandlingsgrunnlag, |                       | (§ 25 Begrunnelse,    |
| DPIA, Art. 22)        |                       |  Menneskelig skjønn)  |
+-----------------------+                       +-----------------------+
```

---

### 2. EU AI Act: Kommunens Rolle som "Deployer" (Idriftsetter)

I henhold til EU AI Act (KI-forordningen) vil kommunen som hovedregel opptre som **idriftsetter (*deployer*)** når man tar i bruk AI-systemer levert av eksterne leverandører.

#### Høyrisikosystemer (AI Act Vedlegg III):
Systemer som benyttes innen **HR/rekruttering**, **tildeling av velferds- og sosvitaltjenester**, eller **kritiske infrastrukturer** regnes som høyrisiko.
* **Plikter for kommunen:**
  1. Gjennomføre **FRIA (Fundamental Rights Impact Assessment)**.
  2. Sikre aktiv og kompetent **menneskelig overvåking (*Human-in-the-Loop*)**.
  3. Sørge for **automatisk logging** av systemhendelser i minimum 6 måneder.
  4. Sikre **AI-literacy (kompetansekrav)** hos alle ansatte som betjener systemet.
  5. Registrere systemet i **EUs felles datatilsynsdatabase**.

---

### 3. Personvern og GDPR i Økonomifunksjonen

1. **Behandlingsgrunnlag (GDPR Art. 6 & 9):** Behandling av personopplysninger i AI-modeller må ha hjemmel i offentlig myndighetsutøvelse (art. 6 nr. 1 e) supplerert av spesifikk lovhjemmel (f.eks. kommuneloven).
2. **Forbud mot Modelltrening på Kommunens Data:** Databehandleravtaler (DBA) må eksplisitt forby at leverandøren benytter inndata, prompter eller kommunale dokumenter til videre trening av sine kommersielle modeller.
3. **Automatiserte Avgjørelser (Art. 22):** Innbyggere og ansatte har rett til ikke å bli gjenstand for helautomatiske avgjørelser som har rettsvirkning. Menneskelig overprøving må være reell, ikke en pro forma godkjenning.

---

### 4. Styringssystem for AI (AIMS) basert på ISO 42001

For å sikre kontinuerlig kontroll må kommunen etablere et **AI Management System (AIMS)**:
* **Sentralt AI-Register:** Oversikt over alle aktiverte modeller, formål, risikoklasse, prosesseier og godkjenningsdato.
* **AI Ethics Board / Styringsgruppe:** Tverrfaglig organ som vurderer og godkjenner nye initiativer før pilotering og produksjonssetting.
* **Nødknapp (*Kill Switch*):** Tekniske og organisatoriske rutiner for å koble ut en AI-modell umiddelbart ved oppdagede feil, hallusinasjoner eller sikkerhetsbrudd.
