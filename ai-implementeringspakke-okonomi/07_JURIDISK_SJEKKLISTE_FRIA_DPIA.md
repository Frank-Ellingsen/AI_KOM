# Operasjonell Juridisk Sjekkliste for AI (FRIA & DPIA)

Dette dokumentet fungerer som en skriveklar sjekkliste for jurister, personvernombud og prosjektledere ved innføring av AI-løsninger i kommunal sektor.

---

### Trinn 1: Innledende Screening og Risikoklassifisering

* [ ] **Rolleavklaring (EU AI Act):** Er kommunen «idriftsetter» (*deployer*) av en ekstern løsning?
* [ ] **Klassifisering (AI Act Vedlegg III):** Faller bruksområdet inn under Høyrisiko (f.eks. HR/rekruttering, velferdsytelser)?
* [ ] **GDPR Art. 35 Utløser:** Innebærer løsningen behandling av personopplysninger i stor skala eller evaluering av enkeltpersoner?

---

### Trinn 2: Behandlingsgrunnlag og Hjemmelskontroll

* [ ] **GDPR Art. 6 Hjemmel:** Er behandlingen nødvendig for utøvelse av offentlig myndighet (bokstav e)?
* [ ] **Supplerende Lovhjemmel:** Finnes det presis hjemmel i kommuneloven, forvaltningsloven eller sektorlovgivning?
* [ ] **GDPR Art. 9 Særlige Kategorier:** Dersom helse- eller fraværsdata behandles, er unntaket i art. 9 nr. 2 g (viktige allmenne hensyn) oppfylt og dokumentert?
* [ ] **Forbud mot Leverandørtrening:** Er det bekreftet i databehandleravtalen (DBA) at leverandøren **ikke** kan bruke dataene til modelltrening?

---

### Trinn 3: DPIA (Personvernkonsekvenser)

* [ ] **Dataminimering:** Er PII-anonymiseringsfilter aktivert før data sendes til språkmodellen?
* [ ] **Innsynsrett (GDPR Art. 15):** Er det tilrettelagt for at berørte kan få innsyn i hvilke data som er behandlet?
* [ ] **Automatisert Behandling (Art. 22):** Er reell menneskelig overprøving sikret slik at helautomatiske vedtak unngås?
* [ ] **Datasikkerhet:** Er data lagret innenfor EU/EØS med tilfredsstillende kryptering i hvile og transport?

---

### Trinn 4: FRIA (Grunnleggende Rettigheter)

* [ ] **Menneskelig Kontroll (*Human-in-the-Loop*):** Er navngitte saksbehandlere utpekt med mandat til å overstyre AI-forslag?
* [ ] **Transparens og Forklarbarhet (XAI):** Leverer systemet direkte kildehenvisninger til dokumenter og paragrafer?
* [ ] **Bias- og Diskrimineringssjekk:** Er datagrunnlaget analysert for skjevheter eller uheldige historiske mønstre?
* [ ] **Sikkerhet mot Hallusinasjoner:** Er løsningen testet mot et godkjent fasit-sett (*Ground Truth*) med akseptabel nøyaktighet?

---

### Trinn 5: Governance, Logging og Registrering

* [ ] **Automatisk Logging:** Er hendelseslogging aktivert og oppbevares i minimum 6 måneder (AI Act Art. 26)?
* [ ] **Kommunalt AI-Register:** Er løsningen innført i kommunens oversikt over aktiverte AI-systemer?
* [ ] **EUs AI-Database:** Dersom høyrisiko, er løsningen klargjort for registrering i EUs felles database?
* [ ] **Signert Godkjenning:** Formell godkjenning fra Personvernombud, CISO og Prosjekteier er innhentet.
