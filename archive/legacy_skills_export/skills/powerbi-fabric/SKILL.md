---
name: powerbi-fabric
description: >-
  Power BI-rapportering, DAX-beregninger, Star Schema-datamodeller, dynamiske formatstrenger og Row-Level Security (RLS).
---

# 📊 Agent Skill: Power BI & Microsoft Fabric Analytics (`SKILL_POWERBI_FABRIC_ANALYTICS`)

> **Versjon:** 1.0  
> **Kategori:** BI & Enterprise Reporting  
> **Sertifisering / Standard:** Power BI Star Schema Best Practice, DAX Pattern Standard, Microsoft Fabric DirectLake & RLS  

---

## 🎯 Formål
Dette agent-skill-et gjør AI-assistenten i stand til å designe, optimalisere og automatisere **Power BI-rapporter, DAX-beregninger, Star Schema-datamodeller og Row-Level Security (RLS)** for kommunale økonomi- og virksomhetsdata.

---

## 📐 Kjernekomponenter & Modeller

### 1. Star Schema & Hierarkidesign (KOSTRA & Kommunestruktur)
- **Faktatabeller:** `Fact_Regnskap` (Visma) og `Fact_Budsjett` (Framsikt).
- **Dimensjoner:** `Dim_Funksjon`, `Dim_Art`, `Dim_Ansvar` (Organisasjonstred), `Dim_Dato` (4-4-5 / Tertialer).
- **Relasjoner:** En-til-mange (1:N) fra Dimensjoner til Fakta med enkeltveis sifferfiltrering (*Single-direction filtering*).

### 2. Standardiserte DAX-Mønstre for Kommunal Økonomi

#### A. Avvik i kroner og prosent (Faktisk vs. Budsjett)
```dax
Faktisk_Belop = SUM(Fact_Regnskap[belop])

Vedtatt_Budsjett = SUM(Fact_Budsjett[budsjett_belop])

Budsjettavvik_Kr = [Faktisk_Belop] - [Vedtatt_Budsjett]

Budsjettavvik_Pct = 
DIVIDE([Budsjettavvik_Kr], [Vedtatt_Budsjett], 0)
```

#### B. Dynamisk Matrisenivå-Sjekk (`ISINSCOPE`)
For unngåelse av ugyldige summeringer på tvers av kontoklasser (Drift vs. Investering jf. Kommuneloven § 14-9):
```dax
Vis_Driftsavvik = 
IF(
    ISINSCOPE(Dim_Funksjon[funksjon_kode]),
    [Budsjettavvik_Kr],
    BLANK()
)
```

#### C. Dynamisk Formatering per Hierarkinivå
```dax
Dynamic_Format_String = 
SWITCH(
    TRUE(),
    ISINSCOPE(Dim_Art[art_kode]), "#,##0 kr",
    ISINSCOPE(Dim_Funksjon[tjenesteomrade]), "#,##0.0 't.kr'",
    "#,##0"
)
```

### 3. Row-Level Security (RLS) for Kommunal Organisasjon
Sikrer at kommunalsjefer og enhetsledere kun ser data for sine egne ansvarsområder:
```dax
-- RLS Filter uttrykk på Dim_Ansvar for Enhetsleder-rolle
[ansvar_kode] = LOOKUPVALUE(
    User_Permissions[ansvar_kode],
    User_Permissions[user_principal_name],
    USERPRINCIPALNAME()
)
```

---

## ⚙️ Eksekveringsregler & Kvalitetskrav
1. **Aldri implisitte mål:** Alle beregninger må opprettes som eksplisitte DAX-mål (*Measures*).
2. **Ingen Mange-til-Mange (N:M) uten brotabell:** Relasjoner må gå via reine Dimensjonstabeller.
3. **Fargepalett:** Følg tilgjengelighetskrav (WCAG 2.1) og unngå forvirrende *Rainbow Color Maps*. Bruk fargekontraster for positive/negative avvik.
