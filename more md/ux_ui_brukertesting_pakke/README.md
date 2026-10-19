# 🎨 UX/UI Designarkitektur & Null-Manual Prinsipp ("Zero-Guide Interface")

## Executive Summary
Dette dokumentet definerer designarkitekturen for **`AI_KOM` Control Office Hub** i Kristiansand kommune. Målet er et grensesnitt som er så intuitivt at enhetsledere og budsjettansvarlige kan utføre sine månedlige oppgaver (månedsoppgjør, avviksnotater, kontering og fakturering) uten oppslag i brukermanualer.

---

## 🏛️ Tre Kjerneprinsipper for Null-Manual Grensesnitt

### 1. Automatisk Kontekstgjenkjenning (Zero-Click Context)
- **SSO/UPN-Gjenkjenning**: Når enhetsleder logger inn, henter systemet automatisk brukerens enhet (f.eks. *Ansvar 5200 - Sykehjem*) basert på Microsoft Entra ID (Azure AD).
- **Ingen manuelle søk**: Lederen slipper å lete i menyer for å finne sin enhet; dashbordet åpnes ferdig filtrert for deres ansvarsområde.

### 2. Unntaksbasert Visning ("Management by Exception")
- **Statusfarging**:
  - 🟢 **Grønn status (Balanse)**: "Driften er i balanse. Ingen handling kreves." (Brukertid: 5 sekunder).
  - 🔴 **Rød status (Merforbruk)**: Systemet viser **kun én handlingsknapp**: *"Generer avviksnotat til Formannskapet"*.
- **Progressiv Avdekking (Progressive Disclosure)**: Detaljerte KOSTRA-tabeller og grafer skjules som standard, men er tilgjengelige med 1 klikk for spesielt interesserte.

### 3. Innbakte Mikro-tekster & "Just-In-Time" Tooltips
- Alle fagbegreper (som *KOSTRA 254*, *Art 1090*, *Kommuneloven § 14-5*, *Bruttoprinsippet*) har **hjelpe-ikoner (ℹ️)** som forklarer regelen i 1-2 korte setninger rett der handlingen utføres.

---

## 📁 Filstruktur i denne pakken

- `README.md`: Hovedoversikt over UX-arkitektur og prinsipper.
- `config/ui_navigation_and_tooltips_spec.md`: Detaljert spesifikasjon av menystruktur, knappetekster og innbakte tooltips.
- `simuleringer/brukertest_simuleringer_og_tilbakemeldinger.md`: Resultater og tilbakemeldinger fra simulerte brukertester med 5 typiske enhetsleder-personaer i Kristiansand kommune.
