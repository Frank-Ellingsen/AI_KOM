---
name: kostra-analyzer
description: >-
  Kontoplanvalidering (Kontoklasse 1 Drift vs 2 Investering jf. Kommuneloven § 14-9), selvkostberegninger og KOSTRA-nøkkeltall.
---

# 🛠️ Agent Skill: KOSTRA Account & Service Analyzer (`kostra-analyzer`)

> **Formål:** Klassifisering, kontoplanvalidering og nøkkeltallsanalyse i henhold til KOSTRA-forskriften og SSB sine innrapporteringsstandarder for kommunal sektor.

---

## 📋 Skill Spesifikasjon & Metadata

| Egenskap | Verdi |
| :--- | :--- |
| **Skill Name** | `kostra-analyzer` |
| **Versjon** | `1.0.0` |
| **Innebygde Gate-sjekker** | Gate 4 (Datakvalitet), Gate 8 (Kontoplan-samsvar) |
| **Inndata** | `Fact_Regnskap`, `Dim_Funksjon`, `Dim_Art` (SQLite Star Schema) |

---

## ⚙️ Regler & Valideringslogikk

### 1. Kontoklasse-sjekk (Kommuneloven § 14-9)
* **Kontoklasse 1 (Drift):** Funksjoner 100–399, Arter 010–590.
* **Kontoklasse 2 (Investering):** Funksjoner 020–080, Arter 600–990.
* *Avvik:* Blanding av kontoklasser i samme bilagsføring flagges som ugyldig.

### 2. Formel for Korrigert Brutto Driftsresultat
$$Brutto Driftsresultat = Driftsinntekter - Driftsutgifter$$

### 3. Selvkostberegning (Selvkostforskriften)
For selvkosttjenester (Vann, Avløp, Renovasjon, Feiing - Funksjon 340–355):
* Sjekker at direkte og indirekte kostnader er korrekt henført.
* Beregner kalkulatorisk rente og avskrivninger jf. forskriftens kapittel 3.
