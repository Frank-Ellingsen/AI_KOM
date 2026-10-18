# Standarder for DAX, Visualer og RAG-kontekst
## Sektor: Helse og Mestring (Ansvar 5200 / KOSTRA 254)

### 1. DAX-beregninger for Avvik og Vikarbruk

```dax
// Budsjettavvik i MNOK (Positivt = Mindreforbruk/Innsparing, Negativt = Merforbruk/Underskudd)
Avvik_MNOK = [Budsjett_MNOK] - [Regnskap_MNOK]

// Avvik i Prosent (Isolerer ABS kun i nevneren)
Avvik_Pct = DIVIDE([Budsjett_MNOK] - [Regnskap_MNOK], ABS([Budsjett_MNOK]), 0)

// Netto Vikarbelastning (Art 1090 Overtid + Art 1100 Innleid Vikar - Art 1600 NAV Refusjon)
Netto_Vikarbelastning_MNOK = [Art_1090_Overtid] + [Art_1100_Vikarer] - ABS([Art_1600_NAV_Refusjon])
```

---

### 2. RAG-Statuskoder og Fargeprofil (Kristiansand Navy Palette)

* **🟢 GRØNN (`#388E3C`)**: `Avvik_Pct >= -2.0%` (Godkjent ramme uten tiltakskrav)
* **🟠 RAV (`#F57C00`)**: `-5.0% <= Avvik_Pct < -2.0%` (Månedlig observasjon og intern omdisponering)
* **🔴 RØD (`#D32F2F`)**: `Avvik_Pct < -5.0%` (Obligatorisk handlingsplikt jf. Kommuneloven § 14-5)

---

### 3. Juridiske Prompter for Kommuneloven § 14-5
Dersom `Avvik_MNOK < 0`, skal AI-systemet generere følgende lovforankrede vurdering:
> *"Sektoren Helse og Mestring har et udekket merforbruk på [X] MNOK. I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak for Formannskapet med forslag til innsparingstiltak eller omdisponering for å sikre budsjettbalanse innen årets utgang."*
