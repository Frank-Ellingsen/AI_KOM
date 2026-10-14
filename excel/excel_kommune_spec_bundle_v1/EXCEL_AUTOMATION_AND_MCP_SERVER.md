# ⚡ Excel MCP Server & Power Query Automatisering

**Virksomhetsområde:** Økonomi og Virksomhetsstyring, Kristiansand kommune  
**Standard:** Model Context Protocol (MCP) for Excel, Power Query M-Engine  

---

## 1. Excel MCP Server Arkitektur

Excel MCP Server gjør det mulig for kommunens AI-assistent (Gemini Flash / Ollama) å samhandle direkte med Excel-arbeidsbøker på en kontrollert og skrivebeskyttet/godkjent måte.

```text
┌──────────────────────────┐      MCP Protocol (JSON-RPC)     ┌────────────────────────────┐
│ AI Office Hub Chat       │ ───────────────────────────────> │ Excel MCP Server           │
│ (Gemini Flash / Ollama)  │ <─────────────────────────────── │ (OpenPyXL / xlwings / M)   │
└──────────────────────────┘                                  └─────────────┬──────────────┘
                                                                            │
                                                                 Read/Write Celler & Tabeller
                                                                            ▼
                                                              ┌────────────────────────────┐
                                                              │ Excel Arbg.bok (.xlsx)     │
                                                              └────────────────────────────┘
```

## 2. Automatisk Power Query M-Kode for Visma ERP

```m
let
    Kilde = Sql.Database("visma-db.kristiansand.kommune.no", "VismaEnterprise"),
    HentHovedbok = Kilde{[Schema="dbo",Item="Fact_Hovedbok"]}[Data],
    FiltrerAar = Table.SelectRows(HentHovedbok, each [Aar] == 2026),
    LeggTilYTD = Table.AddColumn(FiltrerAar, "Avvik_YTD", each [Regnskap_Belop] - [Budsjett_Belop]),
    VaskPII = Table.RemoveColumns(LeggTilYTD, {"Saksbehandler_Navn", "Fodselsnummer"})
in
    VaskPII
```
