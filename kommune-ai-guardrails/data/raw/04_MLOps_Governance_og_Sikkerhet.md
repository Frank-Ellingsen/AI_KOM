# 04. MLOps Governance, EU AI Act og Sikkerhetskontroller

## 1. Regulatorisk Forankring
Modellforvaltning i offentlig sektor må tilfredsstille kravene i:
* **EU AI Act (KI-forordningen):** Kommuner er «idriftsettere» (*deployers*) og må sikre logging, overvåking, transparens og mennesker i sløyfen (*human-in-the-loop*).
* **GDPR (Personopplysningsloven):** Krav om dataminimering, behandlingsgrunnlag (art. 6/9) og rettigheter ved automatiserte avgjørelser (art. 22).
* **Forvaltningsloven § 25:** Krav om at automatisert saksforberedelse og vedtak skal være forståelige, begrunnede og etterprøvbare.
* **ISO 42001 (AIMS):** Internasjonalt styringssystem for kunstig intelligens.

---

## 2. Operativ Rollestruktur for Modellforvaltning

```
+-----------------------------------------------------------------------------------+
|                        ORGANISATORISK MLOPS GOVERNANCE                            |
+------------------------------------+----------------------------------------------+
| Rolle                              | MLOps-ansvar                                 |
+------------------------------------+----------------------------------------------+
| 1. Prosesseier (Fagavdeling)       | • Formelt eierskap til use-case og gevinst.  |
|                                    | • Endelig godkjenning for produksjon.        |
+------------------------------------+----------------------------------------------+
| 2. AI Lead & MLOps Engineer        | • Ansvar for MLOps-pipeline, AI Gateway,     |
|                                    |   modellregister, MLOps-dashbord og SLA.     |
+------------------------------------+----------------------------------------------+
| 3. CISO, Personvernombud & Jurist  | • Godkjenning av DPIA/FRIA, PII-skjerming,  |
|                                    |   audit-logger og sikkerhetskontroller.       |
+------------------------------------+----------------------------------------------+
| 4. Saksbehandler / Økonomirådgiver | • Reell faglig overprøving (HITL) før endelig|
|    (Human-in-the-Loop)             |   godkjenning eller lagring i fagsystem.     |
+------------------------------------+----------------------------------------------+
```

---

## 3. Pliktig Audit Logging og Tilsynsberedskap

Etter EU AI Act art. 26 og arkivlova skal MLOps-plattformen automatisk logge følgende for hver AI-genererte operasjon:
1. **Tidsstempel og Bruker-ID:** Hvem utløste forespørselen.
2. **Inndata og System-Prompt:** Eksakt tekst og parametere som ble sendt inn.
3. **Uthentet RAG-kontekst:** Hvilke spesifikke kildedokumenter og paragrafer som ble hentet ut.
4. **Modellidentifikator:** Eksakt modellnavn og versjonsnummer.
5. **Generert Utdata og Brukers Handling:** Om saksbehandler godkjente, endret eller forkastet AI-forslaget.

---

## 4. Teknisk Nødknapp (Kill-Switch Prosedyre)

Dersom det oppdages uventede feil, hallusinasjoner eller sikkerhetshull i produksjon:
1. **Teknisk deaktivering:** AI Gateway kobler umiddelbart ut endepunktet med én kommando.
2. **Fallback til manuell rutine:** Fagsystemet slår automatisk over til standard manuell arbeidsflyt.
3. **Avvikshåndtering:** Hendelsen logges i kommunens avvikssystem, og MLOps-teamet isolerer feilen i Staging-miljøet før eventuell re-publisering.

---
*Dokumentet inngår i MLOps-implementeringspakken for kommunal sektor.*
