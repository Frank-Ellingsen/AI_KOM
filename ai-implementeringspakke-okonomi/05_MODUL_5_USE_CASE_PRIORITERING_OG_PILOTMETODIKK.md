# Modul 5: Use-Case-Prioritering og Pilotmetodikk

## 1. Netto Prioriteringsmodell for Økonomi-Use-Cases

For å unngå tilfeldige prosjekter prioriteres initiativer etter følgende formel:

$$\text{Netto Prioritet} = (\text{Strategisk Verdi} + \text{Gevinst} + \text{Læringsverdi}) - (\text{Risiko} + \text{Kompleksitet} + \text{Readiness-gap})$$

---

### 2. Bølgeinndeling av Use-Cases

```
+-----------------------------------------------------------------------------------+
| BØLGE 1: LAV RISK / HØY VERDI (År 1)                                              |
| • RAG-Kunnskapsassistent for Økonomireglement & Innkjøpsavtaler                   |
| • Førsteutkast til avvikskort og rapporttekst i tertialrapportering               |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| BØLGE 2: MODERAT RISK / INTEGRERT (År 2)                                          |
| • Automatisk avviksanalyse på transaksjons- og bilagsnivå                         |
| • Prediktive scenariomodeller ved budsjett- og økonomiplanrullering              |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| BØLGE 3: AVANSERT / AUTONOM (År 3+)                                               |
| • Agentbaserte arbeidsflyter for kontinuerlig budsjettkontroll                    |
| • Prediktiv analysestøtte for sykefravær og bemanningsplanlegging                 |
+-----------------------------------------------------------------------------------+
```

---

### 3. Den 4-Trinns Pilotmetodikken

En profesjonell pilot må skille skarpt mellom uforpliktende demoer og produksjonsklare løsninger:

1. **Fase 1: Mål, Baseline og "Ikke-Mål":**
   * Kartlegge tidsbruk og feilfrekvens før pilotering (Baseline).
   * Definere klare "ikke-mål" (f.eks. "AI skal ikke automatisk postere i hovedbok uden godkjenning").
2. **Fase 2: Skjerming og Juridisk Avklaring:**
   * Gjennomføre innledende DPIA/FRIA-screening og sikre data-skjerming.
3. **Fase 3: Kontrollert Testmiljø med Fasit-sett:**
   * Kjøre piloten i 6–8 uker med en avgrenset testgruppe (superbrukere).
   * Verifisere svar mot fasit-settet (*Ground Truth*).
4. **Fase 4: Evaluering ved Beslutningsport G3 (Gate G3):**
   * Evaluere om piloten oppfyller go/no-go kravene for produksjonssetting.

---

### 4. Kriterier ved Beslutningsport G3

For å godkjennes for produksjonssetting må piloten oppfylle:
* [ ] **Dokumentert tidsbesparelse:** Minst 30 % reduksjon i tidsbruk sammenlignet med baseline.
* [ ] **Feilmargin:** 0 % kritiske tallfeil i endelig godkjent rapport.
* [ ] **Kildeforankring:** 100 % sporbare referanser ved RAG-søk.
* [ ] **Beredskap:** Etablert manuell reserveprosedyre ved nedetid.
* [ ] **Finansiell bærekraft:** Forutsigbare FinOps-kostnader som står i rimelig forhold til gevinsten.
