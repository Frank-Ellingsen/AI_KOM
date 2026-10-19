---
name: my_custom_skill
description: "Kort, presis L1-beskrivelse av hva denne skillen gjør og når agenten skal aktivere den."
version: "1.0.0"
author: "Kristiansand Kommune AI Lab"
---

# My Custom Skill - Kjerneprosedyre

Denne filen inneholder **kjerneinstruksjonene (L2)** for utførelse av oppgaven.
Hold denne filen spisset og konsis (< 500 linjer) for å unngå token-sløsing i kontekstvinduet.

---

## 📋 Prosedyre og Trinn

### Trinn 1: Forberedelse & Datainnsamling
- Identifiser inndata fra brukeren eller oppgaven.
- Sjekk om det finnes utdypende regler i `references/domain_knowledge.md`.

### Trinn 2: Eksekvering via Skript (L3)
- Kjør det relevante skriptet i `scripts/`-mappen for tunge beregnings- eller transformasjonsoppgaver.
- *Merk:* Eksekvering via CLI forbruker 0 kode-tokens fra kontekstvinduet!

### Trinn 3: Kvalitetssikring & Leveranse
- Verifiser at utdata oppfyller forretningsreglene.
- Generer sluttresultat til brukeren med spisset oppsummering.
