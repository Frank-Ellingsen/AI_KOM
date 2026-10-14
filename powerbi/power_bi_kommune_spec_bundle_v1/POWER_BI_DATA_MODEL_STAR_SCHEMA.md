# Power BI Data Model: Star Schema & Dimensjonsmodellering for Kristiansand Kommune

## 1. Målsetting og Arkitektur
Dette dokumentet spesifiserer Stjerneschema (Star Schema) datamodellen for Kristiansand kommune i Power BI, optimalisert for ytelse, skalerbarhet og presis KOSTRA- og regnskapsrapportering.

## 2. Tabelloversikt & Relasjoner

### Faktatabeller (Fact Tables)
1. **`Fact_Regnskap`**
   - Transaksjons- og månedstall fra Visma ERP.
   - Nøkler: `Konto_ID`, `Ansvar_ID`, `Tjeneste_ID`, `Dato_ID`, `Prosjekt_ID`.
   - Verdier: `Belop_YTD`, `Belop_Maaned`, `Timer_Overtid`, `Timer_Vikar`.

2. **`Fact_Budsjett`**
   - Opprinnelig årsbudsjett og reviderte rammer fra Framsikt EPM.
   - Nøkler: `Konto_ID`, `Ansvar_ID`, `Tjeneste_ID`, `Dato_ID`.
   - Verdier: `Budsjett_Opprinnelig`, `Budsjett_Revidert`, `Ramme_T1`, `Ramme_T2`.

### Dimensjonstabeller (Dimension Tables)
1. **`Dim_Konto`** (KOSTRA Kontoplan)
   - `Konto_ID`, `Konto_Nummer`, `Konto_Navn`, `Klassifisering` (Drift/Investering), `KontoArt_Gruppe` (1000 Lønn, 1200 Kjøp av varer, 1600 Refusjoner).
2. **`Dim_Ansvar`** (Organisasjonshierarki)
   - `Ansvar_ID`, `Enhet_Kode`, `Enhet_Navn`, `Seksjon_Navn`, `Kommunalsjef_Omraade`, `Kommunedirektoer_Nivaa`.
3. **`Dim_Tjeneste`** (KOSTRA Funksjoner)
   - `Tjeneste_ID`, `Funksjon_Kode`, `Funksjon_Navn`, `KOSTRA_Tjenesteomraade` (Grunnskole, Pleie og omsorg, etc.).
4. **`Dim_Tid`** (Kommunal Styringskalender)
   - `Dato_ID`, `Dato`, `Aar`, `Maaned`, `Kvartal`, `Tertial` (T1, T2, T3), `Periode_Navn`, `ISO_Uke`.

## 3. Row-Level Security (RLS) & Hierarkitilgang
Dynamic RLS konfigureres med `USERPRINCIPALNAME()` koblet mot organisasjonsstrukturen i `Dim_Ansvar`:
```dax
[Kommunalsjef_Omraade] = LOOKUPVALUE(
    Dim_Ansvar[Kommunalsjef_Omraade],
    Dim_Ansvar[Epost], USERPRINCIPALNAME()
)
```
