# 🛠️ Agent Skill: Excel MCP & Power Query Copilot (`excel-mcp-integration`)

> **Formål:** Automatisering av Power Query M-kode, DAX-formler og Excel-funksjoner for finansiell modellering i henhold til FAST Standard.

---

## 📋 Skill Spesifikasjon & Metadata

| Egenskap | Verdi |
| :--- | :--- |
| **Skill Name** | `excel-mcp-integration` |
| **Versjon** | `1.0.0` |
| **Standarder** | FAST Financial Modelling Standard, ICAEW Spreadsheet Practice |

---

## ⚙️ DAX & M-Kode Eksempler

### 1. DAX: Dynamisk Avviksoppstilling med ISINSCOPE
```dax
Avvik_Budsjett_MNOK = 
IF(
    ISINSCOPE(Dim_Funksjon[funksjon_kode]),
    DIVIDE(SUM(Fact_Regnskap[belop]) - SUM(Fact_Budsjett[budsjett_belop]), 1000000, 0),
    BLANK()
)
```

### 2. Power Query M-Kode: Automatisk Vasking fra Visma CSV
```powerquery
let
    Source = Csv.Document(File.Contents("C:\Data\visma_export.csv"),[Delimiter=";", Encoding=1252]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanedTypes = Table.TransformColumnTypes(PromotedHeaders,{{"Belop", type number}, {"Dato", type date}})
in
    CleanedTypes
```
