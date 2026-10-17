---
name: excel-mcp
description: >-
  Automatisering av Power Query M-kode, DAX-formler og Excel FAST-rapportering via CLI og MCP.
---

# 🛠️ Agent Skill: Excel FAST & Power Query Copilot (`excel-mcp-integration`)

> **Formål:** Automatisering av Power Query M-kode, DAX-formler og FAST-standard økonomirapportering via lokal CLI og MCP.

---

## 📋 Skill Spesifikasjon & Metadata

| Egenskap | Verdi |
| :--- | :--- |
| **Skill Name** | `excel-mcp-integration` |
| **Standarder** | FAST Financial Modelling Standard, Edward Tufte Data-Ink Ratio |
| **CLI Inngangsport** | `python tools/run_tool.py excel` |

---

## ⚡ CLI Utførelse (Foretrukket for Agenter)

Autonome agenter skal alltid kjøre Excel-generatoren via CLI for å unngå token-overhead:

```bash
# Generer offisiell 14-arks FAST Excel-rapport med SHA-256 forsegling
python tools/run_tool.py excel --out reports/Kommune_Project_Controller_Reporting_2026.xlsx
```

---

## ⚙️ Standardiserte DAX & M-Kode Mønstre

### 1. DAX: Kanonisk Avviksoppstilling (`Avvik = Budsjett - Faktisk`)
```dax
Avvik_Budsjett_MNOK = 
IF(
    ISINSCOPE(Dim_Funksjon[funksjon_kode]),
    DIVIDE(SUM(Fact_Budsjett[budsjett_belop]) - SUM(Fact_Regnskap[belop]), 1000000, 0),
    BLANK()
)
```
> *Merk: Positivt tall = Mindreforbruk (🟢 Gunstig). Negativt tall = Merforbruk (🔴 Ugunstig).*

### 2. Power Query M-Kode: Automatisk Vasking fra Visma CSV
```powerquery
let
    Source = Csv.Document(File.Contents("erp_data/visma_export.csv"),[Delimiter=";", Encoding=1252]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanedTypes = Table.TransformColumnTypes(PromotedHeaders,{{"Belop", type number}, {"Dato", type date}})
in
    CleanedTypes
```
