// ==============================================================================
// KRISTIANSAND KOMMUNE - POWER QUERY (M) ETL SKRIPT FOR POWER BI
// ==============================================================================
// Dette skriptet definerer datainnlestingen for Kristiansand EPM Power BI-modellen.
// Støtter to innlesingsmetoder:
// METODE A: CSV-basert (Null driver-krav, universell på enhver PC)
// METODE B: SQLite ODBC-basert (Direkte kobling til kristiansand_golden_record.db)
// ==============================================================================

// ------------------------------------------------------------------------------
// PARAMETER: Prosjektmappe (Tilpass dersom prosjektet flyttes)
// ------------------------------------------------------------------------------
let
    ProsjektSti = "C:\Users\frank\Desktop\KrsKom\use cases" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
in
    ProsjektSti


// ==============================================================================
// METODE A: CSV-BASERTE POWER QUERY SPØRRINGER
// ==============================================================================

// 1. DIM_FUNKSJON (KOSTRA Tjenesteområder og Hovedfunksjoner)
let
    Kilde = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUfLILyopVkgsSsxLzMksA9LGqUmJOTmZeelKsTpARUYoCpWwK8QpVAwWMEXRZYpkmq6SUWZ5Bli9hQlQjSnG5rEAWiQW55fklmTm54H1QnQC5fDbgY0Gao/FgKLE3FQDg5LE5IKS/FwDY5iBMDFDE4y2OcbGEbEA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [funksjon_key = _t, funksjon_kode = _t, funksjon_navn = _t, hovedfunksjon_kode = _t, tjenesteomrade_navn = _t]),
    EndretType = Table.TransformColumnTypes(Kilde,{
        {"funksjon_key", Int64.Type},
        {"funksjon_kode", type text},
        {"funksjon_navn", type text},
        {"hovedfunksjon_kode", type text},
        {"tjenesteomrade_navn", type text}
    })
in
    EndretType


// 2. DIM_ANSVAR (Organisasjonsansvar Kristiansand Kommune)
let
    Kilde = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUfLILyopVkgsSsxLzMksA9LGRkqxOtFKRkBBRmARcyDHVCEtNS0VSJihyZki6YCpNQWqNTHFKWFsZGqK1wS4bCwA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [ansvar_key = _t, ansvar_kode = _t, ansvar_navn = _t, kommunalsjefomrade = _t]),
    EndretType = Table.TransformColumnTypes(Kilde,{
        {"ansvar_key", Int64.Type},
        {"ansvar_kode", type text},
        {"ansvar_navn", type text},
        {"kommunalsjefomrade", type text}
    })
in
    EndretType


// 3. DIM_DATO (Kalender 2024 og 2025)
let
    GenererDatoer = List.Dates(#date(2024, 1, 1), 731, #duration(1, 0, 0, 0)),
    TilTabell = Table.FromList(GenererDatoer, Splitter.SplitByNothing(), {"full_dato"}, null, ExtraValues.Error),
    EndretDatoType = Table.TransformColumnTypes(TilTabell,{{"full_dato", type date}}),
    LeggTilDatoKey = Table.AddColumn(EndretDatoType, "dato_key", each Date.Year([full_dato]) * 10000 + Date.Month([full_dato]) * 100 + Date.Day([full_dato]), Int64.Type),
    LeggTilAr = Table.AddColumn(LeggTilDatoKey, "ar", each Date.Year([full_dato]), Int64.Type),
    LeggTilManed = Table.AddColumn(LeggTilAr, "maned", each Date.Month([full_dato]), Int64.Type),
    LeggTilManedsnavn = Table.AddColumn(LeggTilManed, "manedsnavn", each Date.MonthName([full_dato], "nb-NO"), type text),
    LeggTilTertial = Table.AddColumn(LeggTilManedsnavn, "tertial", each if [maned] <= 4 then "T1" else if [maned] <= 8 then "T2" else "T3", type text),
    LeggTilTertialNr = Table.AddColumn(LeggTilTertial, "tertial_nr", each if [maned] <= 4 then 1 else if [maned] <= 8 then 2 else 3, Int64.Type),
    LeggTilArManed = Table.AddColumn(LeggTilTertialNr, "ar_maned", each Text.From([ar]) & "-" & Text.PadStart(Text.From([maned]), 2, "0"), type text)
in
    LeggTilArManed


// 4. FACT_REGNSKAP (Innlesting og normalisering fra BoMiljø.csv og Komskole.csv)
let
    // --- Del 1: Kommunal Boenhet (BOOM) ---
    StiBoMiljo = ProsjektSti & "\data\BoMiljø.csv",
    KildeBoMiljo = Csv.Document(File.Contents(StiBoMiljo),[Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoterteBoMiljo = Table.PromoteHeaders(KildeBoMiljo, [PromoteAllScalars=true]),
    BoMiljoFilter = Table.SelectRows(PromoterteBoMiljo, each ([Kontokode] <> null and [Kontokode] <> "")),
    BoMiljoTrans = Table.TransformColumns(BoMiljoFilter, {
        {"Budsjett", each Number.FromText(_, "en-US"), Currency.Type},
        {"Regnskap", each Number.FromText(_, "en-US"), Currency.Type},
        {"Avvik", each Number.FromText(_, "en-US"), Currency.Type},
        {"Merforbruk", each Number.FromText(_, "en-US"), Currency.Type},
        {"Måned_Nr", each Int64.FromText(_), Int64.Type}
    }),
    BoMiljoKey = Table.AddColumn(BoMiljoTrans, "dato_key", each 20240000 + [Måned_Nr] * 100 + 1, Int64.Type),
    BoMiljoFunksjon = Table.AddColumn(BoMiljoKey, "funksjon_kode", each "254", type text),
    BoMiljoAnsvar = Table.AddColumn(BoMiljoFunksjon, "ansvar_kode", each "2540", type text),
    BoMiljoKilde = Table.AddColumn(BoMiljoAnsvar, "kilde_system", each "Visma Enterprise (BOOM)", type text),
    BoMiljoValgte = Table.SelectColumns(BoMiljoKilde, {
        "kilde_system", "dato_key", "funksjon_kode", "ansvar_kode", "KOSTRA_Art", 
        "Kontokode", "Kontonavn", "Budsjett", "Regnskap", "Avvik", "Merforbruk"
    }),

    // --- Del 2: Kommunal Skole (Komskole) ---
    StiSkole = ProsjektSti & "\data\Komskole.csv",
    KildeSkole = Csv.Document(File.Contents(StiSkole),[Delimiter=",", Encoding=1252, QuoteStyle=QuoteStyle.None]),
    SkoleData = Table.Skip(KildeSkole, 3),
    SkoleOverskrifter = Table.RenameColumns(SkoleData, {
        {"Column4", "Periode_Tekst"}, {"Column5", "Lokasjon"}, {"Column6", "Funksjon_Raw"},
        {"Column7", "Ansvar_Raw"}, {"Column8", "Kontotype"}, {"Column9", "Post"},
        {"Column10", "Regnskap_Tusen"}, {"Column11", "Budsjett_Tusen"}, {"Column12", "Avvik_Tusen"}
    }),
    SkoleFiltrert = Table.SelectRows(SkoleOverskrifter, each ([Lokasjon] <> null and [Lokasjon] <> "")),
    SkoleTall = Table.TransformColumns(SkoleFiltrert, {
        {"Regnskap_Tusen", each (try Number.FromText(Text.Replace(_, " ", ""), "nb-NO") otherwise 0) * 1000, Currency.Type},
        {"Budsjett_Tusen", each (try Number.FromText(Text.Replace(_, " ", ""), "nb-NO") otherwise 0) * 1000, Currency.Type},
        {"Avvik_Tusen", each (try Number.FromText(Text.Replace(_, " ", ""), "nb-NO") otherwise 0) * 1000, Currency.Type}
    }),
    SkoleDatoKey = Table.AddColumn(SkoleTall, "dato_key", each 20250801, Int64.Type),
    SkoleFunksjon = Table.AddColumn(SkoleDatoKey, "funksjon_kode", each Text.Trim([Funksjon_Raw]), type text),
    SkoleAnsvar = Table.AddColumn(SkoleFunksjon, "ansvar_kode", each 
        if Text.Contains([Lokasjon], "Kommunal Skole") or Text.Contains([Lokasjon], "Skole") then "2020"
        else if Text.Contains([Lokasjon], "SFO") then "2021"
        else if Text.Contains([Lokasjon], "voksenopplæring") then "2130"
        else if Text.Contains([Lokasjon], "PPT") then "2029"
        else if Text.Contains([Lokasjon], "Skoleskyss") then "2230"
        else "2022", type text
    ),
    SkoleArt = Table.AddColumn(SkoleAnsvar, "KOSTRA_Art", each 
        if [Kontotype] = "Lønn" then (if Text.Contains([Post], "Fast") then "1010" else if Text.Contains([Post], "vikar") then "1020" else if Text.Contains([Post], "overtid") then "1040" else "1090")
        else if [Kontotype] = "Refusjoner" then "1690"
        else "1150", type text
    ),
    SkoleKilde = Table.AddColumn(SkoleArt, "kilde_system", each "Framsikt / Visma (Skole)", type text),
    SkoleMerforbruk = Table.AddColumn(SkoleKilde, "Merforbruk", each [Regnskap_Tusen] - [Budsjett_Tusen], Currency.Type),
    SkoleValgte = Table.SelectColumns(SkoleMerforbruk, {
        "kilde_system", "dato_key", "funksjon_kode", "ansvar_kode", "KOSTRA_Art",
        "KOSTRA_Art", "Post", "Budsjett_Tusen", "Regnskap_Tusen", "Avvik_Tusen", "Merforbruk"
    }),
    SkoleOmdopt = Table.RenameColumns(SkoleValgte, {
        {"KOSTRA_Art", "Kontokode"}, {"Post", "Kontonavn"}, 
        {"Budsjett_Tusen", "Budsjett"}, {"Regnskap_Tusen", "Regnskap"}, {"Avvik_Tusen", "Avvik"}
    }),

    // --- Del 3: Forening (Union) av begge use cases ---
    Konsolidert = Table.Combine({BoMiljoValgte, SkoleOmdopt}),
    GenererTransaksjonsId = Table.AddColumn(Konsolidert, "transaksjon_id", each 
        Text.NewGuid(), type text
    )
in
    GenererTransaksjonsId


// ==============================================================================
// METODE B: SQLITE DIREKTE ODBC IMPORT (KREVER SQLITE ODBC DRIVER)
// ==============================================================================
// Hvis SQLite ODBC Driver er installert:
// let
//     Source = Odbc.DataSource("Driver={SQLite3 ODBC Driver};Database=" & ProsjektSti & "\kristiansand_golden_record.db", [HierarchicalNavigation=true]),
//     FactTable = Source{[Name="Fact_Regnskap", Kind="Table"]}[Data]
// in
//     FactTable
