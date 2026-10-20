# Automatisk MVA-Balansekontroll (Konto 2130)

**Status:** `PASSED`  
**Tidspunkt:** `2026-10-20T09:35:59.397408`  
**Filnavn:** `Ompostering_Korreksjonsfil_ERP_Eksport_v2.xlsx`  
**SHA-256 Checksum:** `a0aa5bc17a4f1fd8adf57ad96a3d84fab357d47dfe54e9cb60c1163952074030`  

---

## 📊 Oppsummering

| Parameter | Verdi |
| :--- | :--- |
| **Total Beregnet MVA-Kompensasjon (Art 1640 / MVA 1-3)** | **kr 20,400.00** |
| **Bokført på Balansekonto 2130 (Momsrefusjon)** | **kr 20,400.00** |
| **Differanse / Avvik** | **kr 0.00** |
| **Valideringsresultat** | **✅ GODKJENT - Full MVA-balanse** |

---

## 🔍 Linjedetaljer og MVA-beregning

| Bilag | Art | MVA-Kode | Bruttobeløp (NOK) | Beregnet MVA-Kompensasjon (NOK) |
| :--- | :--- | :--- | :--- | :--- |
| 2026-10481 | 1240 | 1 | kr 45,000.00 | kr 9,000.00 |
| 2026-10522 | 1115 | 1 | kr 25,000.00 | kr 5,000.00 |
| 2026-10609 | 1020 | 0 | kr 18,000.00 | kr 0.00 |
| 2026-10711 | 1270 | 1 | kr 32,000.00 | kr 6,400.00 |

---

## 🛠️ Valideringsregler
1. **MVA-kode 1 (25 %):** Beregner `Bruttobeløp * (0.25 / 1.25)` og verifiserer mot driftskjøp.
2. **MVA-kode 2 (15 %):** Beregner `Bruttobeløp * (0.15 / 1.15)` for forpleining/kantine.
3. **MVA-kode 3 (12 %):** Beregner `Bruttobeløp * (0.12 / 1.12)` for transport/overnatting.
4. **Balansekontroll:** Summen av all beregnet MVA-kompensasjon skal nøyaktig motkonteres mot kortsiktig fordring **Balansekonto 2130** før filen godkjennes for overføring til ERP (Visma / Agresso).
