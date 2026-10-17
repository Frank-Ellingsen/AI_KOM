# Power BI DAX Kodebibliotek: Top 3 KPIs og Budsjetthierarki
**Kristiansand kommune — Control Office Hub (AI_KOM / Antigravity)**

---

## 1. Oversikt over DAX-Modulen

Dette DAX-kodebiblioteket inneholder produksjonsklare formler for importering i **Power BI Desktop** (`.pbix` / `.pbip`). 

Kodebiblioteket dekker:
1. **Top 3 KPIs (Konsernnivå):** Netto driftsresultat (%), Disposisjonsfond (%) og Netto lånegjeld (%).
2. **Gauge Chart Betinget Formatering:** Dynamisk fargestyring (Hex-koder `#10B981`, `#F59E0B`, `#EF4444`) for takometer-visninger.
3. **Budsjetthierarkisk Kaskadering (Level 1–3):** Automatisk drill-down og aggregering fra Konsern -> Sektor -> Enhet using `ISINSCOPE()`.
4. **Virksomhetsspesifikke Nøkkeltall:** Vikar- og overtidsprosent (Art 1020/1090), NAV-refusjonsdekningsgrad (Art 1600) og VAR Selvkostgrad.

---

## 2. Struktur i Power BI Tabellmodellen

```
[ Fact_Regnskap ] ──► [ Dim_Organisasjon ] (Konsern -> Sektor -> Enhet -> Avdeling)
        │
        ├──► [ Dim_Kontoplan ] (Kontoklasse -> Funksjon -> Art -> ArtGroup)
        │
        └──► [ Dim_Kalender ] (År -> Kvartal -> Måned -> PeriodeType YTD)
```

---

## 3. Importeringsveiledning i Power BI Desktop

1. Åpne din Power BI rapport i **Power BI Desktop**.
2. Opprett en ny måltabell: **`_KPI_Tiltak_Measures`**.
3. Klikk **"New Measure"** (Nytt mål) og lim inn formlene fra `Top3_KPI_Cascading_Measures.dax`.
4. For Gauge Charts: Sett **`Gauge_Color_NettoDriftsresultat`** som betinget formateringsfarge under *Visual > Data Colors > FX (Field Value)*.

---

## 4. SHA-256 Integritet og Audit Trail
* **Versjon:** `v2.4.0`
* **Sist Oppdatert:** October 2026
* **Kompabilitet:** Power BI Service / Power BI Report Server / Tabular Model Version 1500+
