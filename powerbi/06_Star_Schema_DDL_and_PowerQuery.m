// ==============================================================================
// KRISTIANSAND KOMMUNE — POWER QUERY M-CODE & STAR SCHEMA PIPELINE
// Datakilde: Visma Enterprise ERP / Framsikt EPM
// Spesifikasjon: POWER_BI_DATA_MODEL_STAR_SCHEMA.md & EXCEL_AUTOMATION_AND_MCP_SERVER.md
// ==============================================================================

section FactAndDimensions;

// ------------------------------------------------------------------------------
// 1. FACT_REGNSKAP (Transaksjonsdata fra Visma ERP)
// ------------------------------------------------------------------------------
shared Fact_Regnskap = let
    Kilde = Sql.Database("visma-db.kristiansand.kommune.no", "VismaEnterprise", [Query="
        SELECT 
            Bilagsnummer,
            Bokforingsdato,
            Periode,
            Konto_ID,
            Ansvar_ID,
            Tjeneste_ID,
            Prosjekt_ID,
            Debet_Belop,
            Kredit_Belop,
            (Debet_Belop - Kredit_Belop) AS Belop_YTD,
            Timer_Overtid,
            Timer_Vikar
        FROM dbo.Fact_Hovedbok
        WHERE Aar = 2026
    "]),
    // PII Sanitering: Fjern saksbehandlernavn og personnummer iht. GDPR
    FjernPII = Table.RemoveColumns(Kilde, {"Saksbehandler_Navn", "Fodselsnummer"}, MissingField.Ignore),
    EndreType = Table.TransformColumnTypes(FjernPII, {
        {"Bilagsnummer", type text},
        {"Bokforingsdato", type date},
        {"Periode", type text},
        {"Konto_ID", type text},
        {"Ansvar_ID", type text},
        {"Tjeneste_ID", type text},
        {"Prosjekt_ID", type text},
        {"Belop_YTD", type number},
        {"Timer_Overtid", type number},
        {"Timer_Vikar", type number}
    })
in
    EndreType;


// ------------------------------------------------------------------------------
// 2. FACT_BUDSJETT (Rammer fra Framsikt EPM)
// ------------------------------------------------------------------------------
shared Fact_Budsjett = let
    Kilde = Sql.Database("framsikt.kristiansand.kommune.no", "FramsiktEPM", [Query="
        SELECT 
            Konto_ID,
            Ansvar_ID,
            Tjeneste_ID,
            Aar,
            Periode,
            Budsjett_Opprinnelig,
            Budsjett_Revidert,
            Ramme_T1,
            Ramme_T2
        FROM dbo.Fact_BudsjettRammer
        WHERE Aar = 2026
    "]),
    EndreType = Table.TransformColumnTypes(Kilde, {
        {"Konto_ID", type text},
        {"Ansvar_ID", type text},
        {"Tjeneste_ID", type text},
        {"Aar", Int64.Type},
        {"Periode", type text},
        {"Budsjett_Opprinnelig", type number},
        {"Budsjett_Revidert", type number},
        {"Ramme_T1", type number},
        {"Ramme_T2", type number}
    })
in
    EndreType;


// ------------------------------------------------------------------------------
// 3. DIM_KONTO (KOSTRA Kontoplan)
// ------------------------------------------------------------------------------
shared Dim_Konto = let
    Kilde = Sql.Database("visma-db.kristiansand.kommune.no", "VismaEnterprise", [Query="
        SELECT 
            Konto_ID,
            Konto_Nummer,
            Konto_Navn,
            Klassifisering,
            KontoArt_Gruppe,
            KontoArt_Beskrivelse
        FROM dbo.Dim_KOSTRA_Konto
    "]),
    EndreType = Table.TransformColumnTypes(Kilde, {
        {"Konto_ID", type text},
        {"Konto_Nummer", type text},
        {"Konto_Navn", type text},
        {"Klassifisering", type text},
        {"KontoArt_Gruppe", type text},
        {"KontoArt_Beskrivelse", type text}
    })
in
    EndreType;


// ------------------------------------------------------------------------------
// 4. DIM_ANSVAR (Organisasjonsstruktur & RLS)
// ------------------------------------------------------------------------------
shared Dim_Ansvar = let
    Kilde = Sql.Database("visma-db.kristiansand.kommune.no", "VismaEnterprise", [Query="
        SELECT 
            Ansvar_ID,
            Enhet_Kode,
            Enhet_Navn,
            Seksjon_Navn,
            Kommunalsjef_Omraade,
            Kommunedirektoer_Nivaa,
            Leder_Epost AS Epost
        FROM dbo.Dim_Organisasjon
    "]),
    EndreType = Table.TransformColumnTypes(Kilde, {
        {"Ansvar_ID", type text},
        {"Enhet_Kode", type text},
        {"Enhet_Navn", type text},
        {"Seksjon_Navn", type text},
        {"Kommunalsjef_Omraade", type text},
        {"Kommunedirektoer_Nivaa", type text},
        {"Epost", type text}
    })
in
    EndreType;


// ------------------------------------------------------------------------------
// 5. DIM_TJENESTE (KOSTRA Funksjoner)
// ------------------------------------------------------------------------------
shared Dim_Tjeneste = let
    Kilde = Sql.Database("visma-db.kristiansand.kommune.no", "VismaEnterprise", [Query="
        SELECT 
            Tjeneste_ID,
            Funksjon_Kode,
            Funksjon_Navn,
            KOSTRA_Tjenesteomraade
        FROM dbo.Dim_KOSTRA_Funksjon
    "]),
    EndreType = Table.TransformColumnTypes(Kilde, {
        {"Tjeneste_ID", type text},
        {"Funksjon_Kode", type text},
        {"Funksjon_Navn", type text},
        {"KOSTRA_Tjenesteomraade", type text}
    })
in
    EndreType;


// ------------------------------------------------------------------------------
// 6. DIM_TID (Kommunal Styringskalender med Tertialer)
// ------------------------------------------------------------------------------
shared Dim_Tid = let
    StartDato = #date(2026, 1, 1),
    DagerTotalt = 365,
    DatoListe = List.Dates(StartDato, DagerTotalt, #duration(1, 0, 0, 0)),
    Tabell = Table.FromList(DatoListe, Splitter.SplitByNothing(), {"Dato"}, null, ExtraValues.Error),
    EndreType = Table.TransformColumnTypes(Tabell, {{"Dato", type date}}),
    LeggTilAar = Table.AddColumn(EndreType, "Aar", each Date.Year([Dato]), Int64.Type),
    LeggTilMaaned = Table.AddColumn(LeggTilAar, "Maaned", each Date.Month([Dato]), Int64.Type),
    LeggTilMaanedNavn = Table.AddColumn(LeggTilMaaned, "Maaned_Navn", each Date.MonthName([Dato]), type text),
    LeggTilKvartal = Table.AddColumn(LeggTilMaanedNavn, "Kvartal", each "Q" & Text.From(Date.QuarterOfYear([Dato])), type text),
    LeggTilTertial = Table.AddColumn(LeggTilKvartal, "Tertial", each 
        if [Maaned] <= 4 then "T1" 
        else if [Maaned] <= 8 then "T2" 
        else "T3", type text),
    LeggTilPeriodeNavn = Table.AddColumn(LeggTilTertial, "Periode_Navn", each Text.From([Aar]) & "-" & Text.PadStart(Text.From([Maaned]), 2, "0"), type text)
in
    LeggTilPeriodeNavn;
