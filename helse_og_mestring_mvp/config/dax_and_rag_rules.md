# Standarder for DAX, EVM-beregninger, Visualer og RAG-kontekst
## Sektor: Helse og Mestring (Ansvar 5200 / KOSTRA 253, 254, 256)

### 1. DAX & ISO 21508 EVM-beregninger for Avvik og Vikarbruk

```dax
// Periodisert Budsjett YTD per M8 (Planlagt Verdi / PV)
Forventet_YTD_MNOK = [Budsjett_MNOK] * DIVIDE(8, 12)

// Budsjettavvik YTD i MNOK (Cost Variance CV = PV - AC; Negativt = Merforbruk)
Avvik_MNOK = [Forventet_YTD_MNOK] - [Regnskap_YTD_MNOK]

// Avvik YTD i Prosent (Målt mot periodisert YTD-budsjett, isolerer ABS i nevneren)
Avvik_Pct = DIVIDE([Avvik_MNOK], ABS([Forventet_YTD_MNOK]), 0)

// Kostnadsytelsesindeks (Cost Performance Index CPI = PV / AC)
CPI = DIVIDE([Forventet_YTD_MNOK], [Regnskap_YTD_MNOK], 1.0)

// Deterministisk Sluttprognose (Estimate at Completion EAC = BAC / CPI)
EAC_MNOK = DIVIDE([Budsjett_MNOK], [CPI], [Budsjett_MNOK])

// Netto Vikarbelastning (Art 1090 Overtid + Art 1100 Innleid Vikar - Art 1600 NAV Refusjon)
Netto_Vikarbelastning_MNOK = [Art_1090_Overtid] + [Art_1100_Vikarer] - ABS([Art_1600_NAV_Refusjon])
```

---

### 2. RAG-Statuskoder og Fargeprofil (Edward Tufte Data-Ink Standard)

* **🟢 GRØNN (`#27ae60`)**: `Avvik_Pct >= -2.0%` og `CPI >= 0.98` (I balanse innenfor godkjent ramme)
* **🟡 RAV (`#d35400`)**: `-5.0% <= Avvik_Pct < -2.0%` og `CPI >= 0.95` (Moderat observasjon og intern omdisponering)
* **🔴 RØD (`#c0392b`)**: `Avvik_Pct < -5.0%` eller `CPI < 0.95` (Obligatorisk handlingsplikt jf. Kommuneloven § 14-5)

---

### 3. Juridiske Prompter & Etterlevelseskrav (§§ 14-5, 14-6 og HTA § 4)
Dersom `Avvik_MNOK < 0` eller `CPI < 1.00`, skal AI-systemet generere følgende lovforankrede vurdering:
1. **Kommuneloven § 14-5 (Balansekrav & Tiltaksplikt)**: *"Sektoren Helse og Mestring har et estimert merforbruk ved årsavslutning på [X] MNOK. I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak for Formannskapet/Bystyret med forslag til kompenserende tiltak eller budsjettjustering for å sikre realistisk budsjettbalanse."*
2. **Hovedtariffavtalen (HTA) § 4 & AML § 10-12 (Drøftingsplikt ved Sykefravær ≥ 10 %)**: *"Innføring av felles vikarpool, årsturnus eller utvidet vaktlengde (12,5t helgevakter) krever formell drøftingsprotokoll med tillitsvalgte (NSF / Fagforbundet) før iverksettelse."*
3. **Kommuneloven § 14-6 (Bruttoprinsippet)**: *"Alle sykepengerefusjoner fra NAV skal føres brutto som inntekt på art 1600, og aldri salderes direkte mot lønnsutgifter på art 1010/1090/1100."*
