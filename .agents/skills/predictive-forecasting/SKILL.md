---
name: predictive-forecasting-ai
description: Analytisk og prediktiv AI-spisskompetanse for kommunal økonomistyring og Project Controlling. Beregner sesongjusterte EOY-prognoser (p10/p50/p90), driverbasert Monte Carlo-usikkerhet, Earned Value (EAC/ETC) og uforanderlig SHA-256 revisjonsstempel.
---

# 🔮 Agent Skill: Predictive AI, Tidsserieprognoser & Project Controlling (EVM)

> **Dokument:** `SKILL_PREDICTIVE_FORECASTING_AI.md`  
> **Brukerprofil:** Frank Ellingsen (Senior Financial Controller & Project Controller)  
> **Kanonisk motor:** [`tools/predictive_forecasting_engine.py`](../../tools/predictive_forecasting_engine.py)  
> **Lovhjemmel & Standarder:** Kommuneloven § 14-5, FAST Standard, KS2 (P50/P85), Edward Tufte Data-Ink Ratio

---

## 🎯 Formål og Trigger-Kriterier

Aktiver denne ferdigheten når brukeren eller arbeidsflyten ber om:
* **Helårsprognose (End of Year - EOY):** Fremskriving av forventet resultat for kommunalsjefområder eller KOSTRA-funksjoner.
* **Earned Value Management (EVM):** Beregning av $EAC$ (Estimate at Completion), $ETC$ (Estimate to Complete), $CPI$, $SPI$ eller $VAC$ for investeringsprosjekter.
* **Usikkerhets- og Scenariomodellering (What-If):** Kjøring av Monte Carlo-simuleringer på sykefravær, vikarforbruk, renteeksponering eller prisstigning.
* **Varsling om budsjettubalanse:** Påvisning av avvik som krever politisk sak til Formannskapet jf. **Kommuneloven § 14-5**.

---

## ⚡ CLI Utførelse (Høyeste Token-Effektivitet)

Bruk alltid den sentrale CLI-driveren fremfor tunge MCP-kall eller in-prompt kodekjøring:

```bash
# Kjør full prognose (både drift og investering)
python tools/run_tool.py forecast --mode both

# Kjør kun driverbasert Monte Carlo for driftsenheter
python tools/run_tool.py forecast --mode drift

# Kjør kun Earned Value (EVM / KS2) for investeringsprosjekter
python tools/run_tool.py forecast --mode investering
```

### CLI Flagg & Parametere:
| Flagg | Type | Standardverdi | Beskrivelse |
| :--- | :--- | :--- | :--- |
| `--mode` | string | `both` | `drift` (Monte Carlo 10k løp), `investering` (EVM/KS2), eller `both` |
| `--db` | path | `erp_data/kommune_golden_record.db` | Sti til Golden Record SQLite database |

---

## 🛡️ Guardrails & Kontrollkrav (Stage-Gate Samsvar)

1. **Ingen Black-Box ekstrapolering:** Alle prognoser MÅ synliggjøre hvilke driverforutsetninger som ligger til grunn (`sykefravaer_rate = 8.4%`, `vikarpris_elastisitet = 1.05`).
2. **Obligatorisk usikkerhetsintervall:** Resultatet skal alltid oppgis som **p10 (stramt)**, **p50 (forventet)** og **p90 (konservativt)**.
3. **Kommuneloven § 14-5 Terskel:** Dersom p50-prognosen estimerer en sluttoverskridelse ($VAC < 0$), skal agenten automatisk fremme anbefaling om administrativ ansettelsesstopp eller sak om tilleggsbevilgning over disposisjonsfondet.
4. **Tufte Data-Ink Presentasjon:** Resultater i tabellform skal ha høyrejusterte tall, ingen vertikale linjer, og kun rød/oransje markering ved overskridelser.
5. **Kryptografisk Integritet:** Hvert utfall forsegles med SHA-256 og logges til `Fact_Prognose_Logg`.

---

## 📊 Forventet JSON-Utdata fra Motoren

```json
{
  "modell": "DRIVER_MONTE_CARLO_10K",
  "hittil_regnskap_ac": 3824000.0,
  "vedtatt_ramme_bac": 4850000.0,
  "p10_optimistisk": 4610000.0,
  "p50_forventet": 4895000.0,
  "p90_konservativt": 5240000.0,
  "estimert_avvik_p50": -45000.0,
  "status": "I_RUTE",
  "tiltaksanbefaling": "Forbruk i tråd med sesongramme.",
  "sha256_hash": "a4f8d9..."
}
```

> **Implementasjonsfil:** Full Python-kildekode for simuleringsmotoren finnes i [`tools/predictive_forecasting_engine.py`](../../tools/predictive_forecasting_engine.py).
