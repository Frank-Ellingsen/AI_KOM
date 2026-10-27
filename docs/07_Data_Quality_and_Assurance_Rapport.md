# Data Quality & Assurance (DQA) Rapport for KOSTRA i Power BI

En dedikert **Data Quality & Assurance (DQA) rapport** er et avgjørende kontrollverktøy for økonomiavdelingen og BI-ansvarlige. Den sikrer at alle perioder og sektorer er korrekt innlest via Folder Import, at ingen nøkler mangler i dimensjonene, og at ingen duplikater eller uventede datagap påvirker regnskapsrapporteringen.

---

## 1. Hovedstruktur for DQA-rapporten (4 Kontrollsider)

Anbefalt oppbygging i Power BI Desktop:

| Side | Navn | Formål |
| :--- | :--- | :--- |
| **Side 1** | **Dekning & Kompletthet (Data Coverage)** | Matrise som viser hvilke månedlige perioder som er lest inn per Funksjon, Sektor og Ansvar. |
| **Side 2** | **Nøkkel- og Relasjonsavstemming (Integrity & Unmapped)** | Avdekker faktarader som mangler kobling til Kontoplan, Funksjon eller Ansvarsstruktur (Orphan keys). |
| **Side 3** | **Fil- og Ingestion-kontroll (Folder Metadata)** | Sporbarhet på filnivå (`Source.Name`), radantall, oppdateringstidspunkt og varsling om duplikate filer. |
| **Side 4** | **Anomali- og Konsistenskontroll (Validation & Outliers)** | Identifiserer ubudsjetterte posteringer, datagap, ekstreme avvik og uventede fortegnsfeil. |

---

## 2. Side 1: Deknings- og Kompletthetsmatrise (Coverage Matrix)

### A. Rapportoppsett (Visual: Matrix)
* **Rows (Rader):** `dim_kostra_funksjon[Tjenesteomrade_Navn]` -> `dim_kostra_funksjon[Funksjonsgruppe_Kode_Navn]` -> `fact_regnskap[Sektor]`
* **Columns (Kolonner):** `dim_date[Ar_Maned]` (f.eks. `2024-01`, `2024-02`, ... `2024-08`)
* **Values (Verdier):** `[QA Dekningsstatus Indikator]` (Formatert med fargekoder)

### B. DAX for Dekningsstatus
```dax
QA Har Regnskap = 
IF ( NOT ISBLANK ( SUM ( 'fact_regnskap'[Regnskap] ) ), 1, 0 )

QA Har Budsjett = 
IF ( NOT ISBLANK ( SUM ( 'fact_regnskap'[Budsjett] ) ), 1, 0 )

QA Dekningsstatus Indikator = 
VAR _HarRegnskap = [QA Har Regnskap]
VAR _HarBudsjett = [QA Har Budsjett]
RETURN
    SWITCH (
        TRUE (),
        _HarRegnskap = 1 && _HarBudsjett = 1, "🟢 OK (Regnskap & Budsjett)",
        _HarRegnskap = 1 && _HarBudsjett = 0, "🟡 Kun Regnskap (Mangler Budsjett)",
        _HarRegnskap = 0 && _HarBudsjett = 1, "🔵 Kun Budsjett (Mangler Regnskap)",
        "🔴 Mangler Data"
    )
```

---

## 3. Side 2: Integrasjons- og Nøkkelavstemming (Unmapped Keys)

Når det opprettes nye ansvarssteder, kontokoder eller funksjoner i økonomisystemet, må disse finnes i dimensjonstabellene. Hvis en nøkkel mangler, vil faktarader bli "foreldreløse" (*Blank/Blank*) i rapportene.

### A. DAX for å identifisere umappede nøkler
```dax
QA Umappede Kontokoder Antall = 
CALCULATE (
    COUNTROWS ( 'fact_regnskap' ),
    FILTER (
        'fact_regnskap',
        ISBLANK ( RELATED ( 'dim_kostra_kontoplan'[Kontonavn] ) )
    )
)

QA Umappede Kontokoder Regnskap Kr = 
CALCULATE (
    SUM ( 'fact_regnskap'[Regnskap] ),
    FILTER (
        'fact_regnskap',
        ISBLANK ( RELATED ( 'dim_kostra_kontoplan'[Kontonavn] ) )
    )
)

QA Umappede Ansvar Antall = 
CALCULATE (
    COUNTROWS ( 'fact_regnskap' ),
    FILTER (
        'fact_regnskap',
        ISBLANK ( RELATED ( 'dim_ansvar'[Ansvar_Navn] ) )
    )
)

QA Umappede Funksjoner Antall = 
CALCULATE (
    COUNTROWS ( 'fact_regnskap' ),
    FILTER (
        'fact_regnskap',
        ISBLANK ( RELATED ( 'dim_kostra_funksjon'[KOSTRA_Funksjon_Navn] ) )
    )
)
```

---

## 4. Side 3: Fil- og Ingestion-kontroll (Folder Import Audit)

Siden faktadata importeres via mappe (*Folder Import*), er det kritisk å overvåke at ingen filer har blitt lest inn dobbelt (f.eks. `2024_08_fact_bomiljo.csv` og `2024_08_fact_bomiljo_v2.csv`).

### A. Power Query M-kode for å bevare kildemetadata
I Power Query, sørg for at `Source.Name` beholdes som en kolonne i `fact_regnskap`:

```powerquery
let
    Kilde = Folder.Files("C:\PowerBI_Data\faktatabeller"),
    FiltrerCSV = Table.SelectRows(Kilde, each ([Extension] = ".csv")),
    LesInnhold = Table.AddColumn(FiltrerCSV, "Innhold", each Csv.Document([Content], [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None])),
    BeholdKildeNavn = Table.SelectColumns(LesInnhold, {"Name", "Innhold"}),
    Ekspander = Table.ExpandTableColumn(BeholdKildeNavn, "Innhold", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7"}, {"Dato", "KOSTRA_Funksjonsgruppe_Kode", "Kontokode_6Siffer", "Ansvar_Kode", "Sektor", "Budsjett", "Regnskap"}),
    OmdopFilnavn = Table.RenameColumns(Ekspander, {{"Name", "Kilde_Filnavn"}})
in
    OmdopFilnavn
```

### B. DAX for å oppdage duplikater og filoversikt
```dax
QA Antall Filer Importert = 
DISTINCTCOUNT ( 'fact_regnskap'[Kilde_Filnavn] )

QA Antall Rader Per Fil = 
COUNTROWS ( 'fact_regnskap' )

QA Duplikatsjekk Filnavn = 
VAR _AntallFilerPerPeriodeOgSektor = 
    CALCULATETABLE (
        ADDCOLUMNS (
            SUMMARIZE ( 'fact_regnskap', 'dim_date'[Ar_Maned], 'fact_regnskap'[Sektor] ),
            "@FilCount", CALCULATE ( DISTINCTCOUNT ( 'fact_regnskap'[Kilde_Filnavn] ) )
        ),
        ALL ( 'fact_regnskap'[Kilde_Filnavn] )
    )
VAR _MaksFiler = MAXX ( _AntallFilerPerPeriodeOgSektor, [@FilCount] )
RETURN
    IF ( _MaksFiler > 1, "⚠️ ADVARSEL: Dupliserte filer for samme periode!", "🟢 Ingen filduplikater" )
```

---

## 5. Side 4: Anomali- og Konsistenskontroll (Validation & Outliers)

### A. DAX for anomalisjekk
```dax
QA Ubudsjetterte Kostnader Kr = 
CALCULATE (
    SUM ( 'fact_regnskap'[Regnskap] ),
    'fact_regnskap'[Budsjett] = 0 && 'fact_regnskap'[Regnskap] > 0
)

QA Ekstreme MoM Endringer = 
VAR _Endring = [Regnskap MoM Endring Kr]
VAR _Snitt = CALCULATE ( AVERAGE ( 'fact_regnskap'[Regnskap] ), ALL ( 'dim_date' ) )
RETURN
    IF ( ABS ( _Endring ) > (_Snitt * 2), "⚠️ Uvanlig stort avvik MoM", "OK" )
```

---

## 6. Slik overvåkes oppdateringer i Power BI Service

1. **Sist Oppdatert Stempel (Power Query M):**
   Legg til en liten tabell `dim_oppdatering` i Power Query:
   ```powerquery
   let
       Kilde = #table(type table [Sist_Oppdatert = datetime], {{DateTime.LocalNow()}})
   in
       Kilde
   ```
2. **Kort-visual på DQA-siden:**
   Vis `MAX(dim_oppdatering[Sist_Oppdatert])` øverst i rapporten slik at du og revisor til enhver tid ser eksakt når siste oppdatering ble kjørt.
