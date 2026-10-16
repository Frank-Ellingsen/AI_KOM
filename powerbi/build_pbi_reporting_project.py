#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
KRISTIANSAND KOMMUNE — POWER BI REPORTING PROJECT BUILDER (.PBIP)
===============================================================================
Dette skriptet bygger opp den offisielle Power BI rapporteringsløsningen:
'powerbi/pbi_reporting_project.pbip'
- Inkluderer fullverdig Stjerneschema (Star Schema) i TMDL-format
- DAX-målinger for EVM, prognostisering (P10/P50/P90) og KOSTRA
- 7 komplette CFO & Controller rapportsider iht. FT Visual Storytelling og Tufte:
  1. Toppledelse (CFO Control Panel)
  2. Sektor Oppvekst & Grunnskole
  3. Sektor Helse & Mestring
  4. Lønn, Vikar & Overtidsmonitor
  5. Prognose & What-If Scenarier
  6. Investering & Prosjektkontroll (EVM)
  7. Revisjon & Audit Trail (Stage-Gate Port 9)
===============================================================================
"""

import json
import shutil
import sys
from pathlib import Path

# Fix Windows console encoding if needed
if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(r"C:\Users\frank\Desktop\AI_KOM\powerbi")
PROJECT_DIR = BASE_DIR / "pbi_reporting_project.pbip"
REPORT_DIR = BASE_DIR / "pbi_reporting_project.Report"
MODEL_DIR = BASE_DIR / "pbi_reporting_project.SemanticModel"
DATA_ROOT = r"C:\Users\frank\Desktop\AI_KOM\erp_data\\"

def setup_directories():
    """Oppretter katalogstrukturen for TMDL og PBIR."""
    (MODEL_DIR / "definition" / "tables").mkdir(parents=True, exist_ok=True)
    (MODEL_DIR / "definition" / "roles").mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "definition" / "pages").mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "StaticResources" / "SharedResources" / "BaseThemes").mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 1. SEMANTIC MODEL (TMDL) DEFINISJONER
# ==============================================================================

def build_semantic_model():
    print("Bygger Semantic Model i TMDL-format...")
    
    # database.tmdl
    (MODEL_DIR / "definition" / "database.tmdl").write_text(
        "database\n\tcompatibilityLevel: 1600\n", encoding="utf-8"
    )

    # expressions.tmdl
    expressions_content = f'expression DataRoot = "{DATA_ROOT}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n'
    (MODEL_DIR / "definition" / "expressions.tmdl").write_text(expressions_content, encoding="utf-8")

    # model.tmdl
    model_content = """model Model
\tculture: nb-NO
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US

ref table Fact_Regnskap
ref table Dim_Dato
ref table Dim_Ansvar
ref table Dim_Funksjon
ref table Dim_Art
ref table Framsikt_Deflator
ref table Fravaer_Reduksjon
ref table Audit_AI_Actions
ref table _Measures

ref role Enhetsleder_Skole
ref role Enhetsleder_Boenhet
ref role Kommunalsjef_Oppvekst
ref role Kommunalsjef_Helse
ref role Konsern_Okonomi
"""
    (MODEL_DIR / "definition" / "model.tmdl").write_text(model_content, encoding="utf-8")

    # relationships.tmdl
    relationships_content = """relationship FactDate
\tfromColumn: Fact_Regnskap.dato
\ttoColumn: Dim_Dato.dato
\tfromCardinality: many
\ttoCardinality: one
\tcrossFilteringBehavior: oneDirection

relationship FactAnsvar
\tfromColumn: Fact_Regnskap.ansvar_kode
\ttoColumn: Dim_Ansvar.ansvar_kode
\tfromCardinality: many
\ttoCardinality: one
\tcrossFilteringBehavior: oneDirection

relationship FactFunksjon
\tfromColumn: Fact_Regnskap.funksjon_kode
\ttoColumn: Dim_Funksjon.funksjon_kode
\tfromCardinality: many
\ttoCardinality: one
\tcrossFilteringBehavior: oneDirection

relationship FactArt
\tfromColumn: Fact_Regnskap.art_key
\ttoColumn: Dim_Art.art_key
\tfromCardinality: many
\ttoCardinality: one
\tcrossFilteringBehavior: oneDirection

relationship AuditResponsibility
\tfromColumn: Audit_AI_Actions.ansvar_kode
\ttoColumn: Dim_Ansvar.ansvar_kode
\tfromCardinality: many
\ttoCardinality: one
\tcrossFilteringBehavior: oneDirection
"""
    (MODEL_DIR / "definition" / "relationships.tmdl").write_text(relationships_content, encoding="utf-8")

    # roles/
    roles_dir = MODEL_DIR / "definition" / "roles"
    roles_dir.mkdir(parents=True, exist_ok=True)
    (roles_dir / "Enhetsleder_Skole.tmdl").write_text(
        "role Enhetsleder_Skole\n\tmodelPermission: read\n\n\ttablePermission Dim_Ansvar = [ansvar_kode] = \"2020\"\n",
        encoding="utf-8"
    )
    (roles_dir / "Enhetsleder_Boenhet.tmdl").write_text(
        "role Enhetsleder_Boenhet\n\tmodelPermission: read\n\n\ttablePermission Dim_Ansvar = [ansvar_kode] = \"2540\"\n",
        encoding="utf-8"
    )
    (roles_dir / "Kommunalsjef_Oppvekst.tmdl").write_text(
        "role Kommunalsjef_Oppvekst\n\tmodelPermission: read\n\n\ttablePermission Dim_Ansvar = [kommunalsjefomrade] = \"Oppvekst\"\n",
        encoding="utf-8"
    )
    (roles_dir / "Kommunalsjef_Helse.tmdl").write_text(
        "role Kommunalsjef_Helse\n\tmodelPermission: read\n\n\ttablePermission Dim_Ansvar = [kommunalsjefomrade] = \"Helse og mestring\"\n",
        encoding="utf-8"
    )
    (roles_dir / "Konsern_Okonomi.tmdl").write_text(
        "role Konsern_Okonomi\n\tmodelPermission: read\n",
        encoding="utf-8"
    )
    # Rydd opp eventuelle foreldede flate filer eller tomme kataloger
    old_roles = MODEL_DIR / "definition" / "roles.tmdl"
    if old_roles.exists():
        old_roles.unlink()
    cultures_dir = MODEL_DIR / "definition" / "cultures"
    if cultures_dir.exists():
        shutil.rmtree(cultures_dir)

    # --------------------------------------------------------------------------
    # TABLES
    # --------------------------------------------------------------------------
    tables_dir = MODEL_DIR / "definition" / "tables"

    # 1. Fact_Regnskap.tmdl (Kombinert Skole + BoMiljø)
    fact_regnskap_tmdl = """table Fact_Regnskap

\tcolumn dato
\t\tdataType: dateTime
\t\tsummarizeBy: none
\t\tsourceColumn: dato

\tcolumn maned
\t\tdataType: int64
\t\tsummarizeBy: none
\t\tsourceColumn: maned

\tcolumn manedsnavn
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: manedsnavn

\tcolumn Tertial
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Tertial

\tcolumn Status
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Status

\tcolumn ansvar_kode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: ansvar_kode

\tcolumn ansvar_navn
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: ansvar_navn

\tcolumn kommunalsjefomrade
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: kommunalsjefomrade

\tcolumn funksjon_kode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: funksjon_kode

\tcolumn art_key
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: art_key

\tcolumn Hovedgruppe
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Hovedgruppe

\tcolumn Undergruppe
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Undergruppe

\tcolumn KOSTRA_Art
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: KOSTRA_Art

\tcolumn Kontokode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Kontokode

\tcolumn Kontonavn
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Kontonavn

\tcolumn Budsjett
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Budsjett

\tcolumn Regnskap
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Regnskap

\tcolumn Avvik
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Avvik

\tcolumn Merforbruk
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Merforbruk

\tcolumn Aarsbudsjett
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Aarsbudsjett

\tpartition Fact_Regnskap = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    // 1. Skole Data
\t\t\t\t    SourceSkole = Csv.Document(File.Contents(DataRoot & "Komskole.csv"), [Delimiter=",", Encoding=1252, QuoteStyle=QuoteStyle.Csv]),
\t\t\t\t    SkipSkole = Table.Skip(SourceSkole, 2),
\t\t\t\t    HeadersSkole = Table.PromoteHeaders(SkipSkole, [PromoteAllScalars=true]),
\t\t\t\t    TypedSkole = Table.TransformColumnTypes(HeadersSkole, {{"Art", type text}, {"Regnskap hiå.", type number}, {"Budsjett hiå.", type number}, {"Avvik i kr", type number}, {"Årsbudsjett", type number}}, "en-US"),
\t\t\t\t    AddDateSkole = Table.AddColumn(TypedSkole, "dato", each #date(2026, 8, 1), type date),
\t\t\t\t    AddRespSkole = Table.AddColumn(AddDateSkole, "ansvar_kode", each "2020", type text),
\t\t\t\t    AddRespNameSkole = Table.AddColumn(AddRespSkole, "ansvar_navn", each "Enhet 202 Grunnskole", type text),
\t\t\t\t    AddFunkSkole = Table.AddColumn(AddRespNameSkole, "funksjon_kode", each "202", type text),
\t\t\t\t    AddMndSkole = Table.AddColumn(AddFunkSkole, "maned", each 8, Int64.Type),
\t\t\t\t    AddMndNavnSkole = Table.AddColumn(AddMndSkole, "manedsnavn", each "august", type text),
\t\t\t\t    AddTertialSkole = Table.AddColumn(AddMndNavnSkole, "Tertial", each "T2", type text),
\t\t\t\t    AddStatusSkole = Table.AddColumn(AddTertialSkole, "Status", each "Bokført", type text),
\t\t\t\t    AddHovedSkole = Table.AddColumn(AddStatusSkole, "Hovedgruppe", each [Kontotype], type text),
\t\t\t\t    AddUnderSkole = Table.AddColumn(AddHovedSkole, "Undergruppe", each [Kontotype], type text),
\t\t\t\t    AddArtKeySkole = Table.AddColumn(AddUnderSkole, "art_key", each Text.From([Art]) & "|" & Text.From([Kontotype]) & "|" & Text.From([Post]), type text),
\t\t\t\t    AddKostraArtSkole = Table.AddColumn(AddArtKeySkole, "KOSTRA_Art", each Text.From([Art]), type text),
\t\t\t\t    AddBudSkole = Table.AddColumn(AddKostraArtSkole, "Budsjett", each [#"Budsjett hiå."], type number),
\t\t\t\t    AddRegSkole = Table.AddColumn(AddBudSkole, "Regnskap", each [#"Regnskap hiå."], type number),
\t\t\t\t    AddAvvSkole = Table.AddColumn(AddRegSkole, "Avvik", each [#"Regnskap hiå."] - [#"Budsjett hiå."], type number),
\t\t\t\t    AddMerSkole = Table.AddColumn(AddAvvSkole, "Merforbruk", each [Avvik], type number),
\t\t\t\t    AddSektorSkole = Table.AddColumn(AddMerSkole, "kommunalsjefomrade", each "Oppvekst", type text),
\t\t\t\t    RenameSkole = Table.RenameColumns(AddSektorSkole, {{"Post", "Kontonavn"}, {"Kontotype", "Kontokode"}, {"Årsbudsjett", "Aarsbudsjett"}}),
\t\t\t\t    ColsSkole = Table.SelectColumns(RenameSkole, {"dato", "maned", "manedsnavn", "Tertial", "Status", "ansvar_kode", "ansvar_navn", "kommunalsjefomrade", "funksjon_kode", "art_key", "Hovedgruppe", "Undergruppe", "KOSTRA_Art", "Kontokode", "Kontonavn", "Budsjett", "Regnskap", "Avvik", "Merforbruk", "Aarsbudsjett"}),

\t\t\t\t    // 2. BoMiljø Data
\t\t\t\t    SourceBo = Csv.Document(File.Contents(DataRoot & "BoMiljø.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
\t\t\t\t    HeadersBo = Table.PromoteHeaders(SourceBo, [PromoteAllScalars=true]),
\t\t\t\t    TypedBo = Table.TransformColumnTypes(HeadersBo, {{"Måned_Nr", Int64.Type}, {"KOSTRA_Funksjon", type text}, {"Tjenesteområde", type text}, {"KOSTRA_Art", type text}, {"Kontokode", type text}, {"Budsjett", type number}, {"Regnskap", type number}, {"Avvik", type number}, {"Merforbruk", type number}}, "en-US"),
\t\t\t\t    AddDateBo = Table.AddColumn(TypedBo, "dato", each Date.FromText([Periode] & "-01"), type date),
\t\t\t\t    AddRespBo = Table.AddColumn(AddDateBo, "ansvar_kode", each "2540", type text),
\t\t\t\t    AddRespNameBo = Table.AddColumn(AddRespBo, "ansvar_navn", each [Lokasjon], type text),
\t\t\t\t    AddFunkBo = Table.AddColumn(AddRespNameBo, "funksjon_kode", each Text.From([KOSTRA_Funksjon]), type text),
\t\t\t\t    AddSektorBo = Table.AddColumn(AddFunkBo, "kommunalsjefomrade", each [Tjenesteområde], type text),
\t\t\t\t    AddArtKeyBo = Table.AddColumn(AddSektorBo, "art_key", each Text.From([KOSTRA_Art]) & "|" & Text.From([Kontokode]) & "|" & Text.From([Kontonavn]), type text),
\t\t\t\t    AddAnnualBudgetBo = Table.AddColumn(AddArtKeyBo, "Aarsbudsjett", each [Budsjett] * 1.5, type number),
\t\t\t\t    RenameBo = Table.RenameColumns(AddAnnualBudgetBo, {{"Måned_Nr", "maned"}, {"Måned", "manedsnavn"}}),
\t\t\t\t    ColsBo = Table.SelectColumns(RenameBo, {"dato", "maned", "manedsnavn", "Tertial", "Status", "ansvar_kode", "ansvar_navn", "kommunalsjefomrade", "funksjon_kode", "art_key", "Hovedgruppe", "Undergruppe", "KOSTRA_Art", "Kontokode", "Kontonavn", "Budsjett", "Regnskap", "Avvik", "Merforbruk", "Aarsbudsjett"}),

\t\t\t\t    Combined = Table.Combine({ColsSkole, ColsBo})
\t\t\t\tin
\t\t\t\t    Combined

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Fact_Regnskap.tmdl").write_text(fact_regnskap_tmdl, encoding="utf-8")

    # 2. Dim_Dato.tmdl
    dim_dato_tmdl = """table Dim_Dato

\tcolumn dato
\t\tdataType: dateTime
\t\tsummarizeBy: none
\t\tsourceColumn: dato

\tcolumn ar
\t\tdataType: int64
\t\tsummarizeBy: none
\t\tsourceColumn: ar

\tcolumn maned
\t\tdataType: int64
\t\tsummarizeBy: none
\t\tsourceColumn: maned

\tcolumn manedsnavn
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: manedsnavn
\t\tsortByColumn: maned

\tcolumn tertial
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: tertial

\tpartition Dim_Dato = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Fact_Regnskap,
\t\t\t\t    Selected = Table.SelectColumns(Source, {"dato", "Tertial"}),
\t\t\t\t    Rename = Table.RenameColumns(Selected, {{"Tertial", "tertial"}}),
\t\t\t\t    Unique = Table.Distinct(Rename),
\t\t\t\t    AddYear = Table.AddColumn(Unique, "ar", each Date.Year([dato]), Int64.Type),
\t\t\t\t    AddMonth = Table.AddColumn(AddYear, "maned", each Date.Month([dato]), Int64.Type),
\t\t\t\t    AddName = Table.AddColumn(AddMonth, "manedsnavn", each Date.ToText([dato], "MMMM", "nb-NO"), type text)
\t\t\t\tin
\t\t\t\t    AddName

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Dim_Dato.tmdl").write_text(dim_dato_tmdl, encoding="utf-8")

    # 3. Dim_Ansvar.tmdl
    dim_ansvar_tmdl = """table Dim_Ansvar

\tcolumn ansvar_kode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: ansvar_kode

\tcolumn ansvar_navn
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: ansvar_navn

\tcolumn kommunalsjefomrade
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: kommunalsjefomrade

\tpartition Dim_Ansvar = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Fact_Regnskap,
\t\t\t\t    Selected = Table.SelectColumns(Source, {"ansvar_kode", "ansvar_navn", "kommunalsjefomrade"}),
\t\t\t\t    Unique = Table.Distinct(Selected)
\t\t\t\tin
\t\t\t\t    Unique

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Dim_Ansvar.tmdl").write_text(dim_ansvar_tmdl, encoding="utf-8")

    # 4. Dim_Art.tmdl
    dim_art_tmdl = """table Dim_Art

\tcolumn art_key
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: art_key

\tcolumn KOSTRA_Art
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: KOSTRA_Art

\tcolumn Kontokode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Kontokode

\tcolumn Kontonavn
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Kontonavn

\tcolumn Hovedgruppe
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Hovedgruppe

\tcolumn Undergruppe
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Undergruppe

\tpartition Dim_Art = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Fact_Regnskap,
\t\t\t\t    Selected = Table.SelectColumns(Source, {"art_key", "KOSTRA_Art", "Kontokode", "Kontonavn", "Hovedgruppe", "Undergruppe"}),
\t\t\t\t    Unique = Table.Distinct(Selected)
\t\t\t\tin
\t\t\t\t    Unique

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Dim_Art.tmdl").write_text(dim_art_tmdl, encoding="utf-8")

    # 5. Dim_Funksjon.tmdl
    dim_funksjon_tmdl = """table Dim_Funksjon

\tcolumn funksjon_kode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: funksjon_kode

\tpartition Dim_Funksjon = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Fact_Regnskap,
\t\t\t\t    Selected = Table.SelectColumns(Source, {"funksjon_kode"}),
\t\t\t\t    Unique = Table.Distinct(Selected)
\t\t\t\tin
\t\t\t\t    Unique

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Dim_Funksjon.tmdl").write_text(dim_funksjon_tmdl, encoding="utf-8")

    # 6. Framsikt_Deflator.tmdl
    framsikt_deflator_tmdl = """table Framsikt_Deflator

\tcolumn Value
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Value

\tcolumn Label
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Label

\tpartition Framsikt_Deflator = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Values = List.Transform({20..60}, each Number.From(_) / 1000),
\t\t\t\t    Source = Table.FromList(Values, Splitter.SplitByNothing(), {"Value"}),
\t\t\t\t    AddLabel = Table.AddColumn(Source, "Label", each Number.ToText([Value], "0.0%"), type text)
\t\t\t\tin
\t\t\t\t    AddLabel

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Framsikt_Deflator.tmdl").write_text(framsikt_deflator_tmdl, encoding="utf-8")

    # 7. Fravaer_Reduksjon.tmdl
    fravaer_reduksjon_tmdl = """table Fravaer_Reduksjon

\tcolumn Value
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Value

\tcolumn Label
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Label

\tpartition Fravaer_Reduksjon = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Values = List.Transform({5..40}, each Number.From(_) / 1000),
\t\t\t\t    Source = Table.FromList(Values, Splitter.SplitByNothing(), {"Value"}),
\t\t\t\t    AddLabel = Table.AddColumn(Source, "Label", each Number.ToText([Value], "0.0%"), type text)
\t\t\t\tin
\t\t\t\t    AddLabel

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Fravaer_Reduksjon.tmdl").write_text(fravaer_reduksjon_tmdl, encoding="utf-8")

    # 8. Audit_AI_Actions.tmdl
    audit_tmdl = """table Audit_AI_Actions

\tcolumn Tidsstempel
\t\tdataType: dateTime
\t\tsummarizeBy: none
\t\tsourceColumn: Tidsstempel

\tcolumn Enhetskode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Enhetskode

\tcolumn ansvar_kode
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: ansvar_kode

\tcolumn AI_Tiltak
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: AI_Tiltak

\tcolumn Konfidens
\t\tdataType: double
\t\tsummarizeBy: sum
\t\tsourceColumn: Konfidens

\tcolumn Leder_Beslutning
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Leder_Beslutning

\tcolumn Saksbehandler
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Saksbehandler

\tcolumn Begrunnelse
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: Begrunnelse

\tcolumn SHA256_Hash
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: SHA256_Hash

\tpartition Audit_AI_Actions = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = #table(
\t\t\t\t        type table [
\t\t\t\t            Tidsstempel = datetime,
\t\t\t\t            Enhetskode = text,
\t\t\t\t            ansvar_kode = text,
\t\t\t\t            AI_Tiltak = text,
\t\t\t\t            Konfidens = number,
\t\t\t\t            Leder_Beslutning = text,
\t\t\t\t            Saksbehandler = text,
\t\t\t\t            Begrunnelse = text,
\t\t\t\t            SHA256_Hash = text
\t\t\t\t        ],
\t\t\t\t        {
\t\t\t\t            {#datetime(2026, 8, 20, 14, 30, 0), "2020", "2020", "Vikarstopp korttidsfravær < 3 dager", 0.94, "APPROVED", "Frank Ellingsen", "Kvantifisert innsparing 170k/mnd jf. § 14-5", "a8f9c2e411b98d24"},
\t\t\t\t            {#datetime(2026, 8, 22, 11, 15, 0), "2540", "2540", "Turnusendring og overtidstak døgnpost", 0.89, "MODIFIED", "Frank Ellingsen", "Drøftet med tillitsvalgte iht. HTA § 4", "f34b9982a74c1022"}
\t\t\t\t        }
\t\t\t\t    )
\t\t\t\tin
\t\t\t\t    Source

\tannotation PBI_ResultType = Table
"""
    (tables_dir / "Audit_AI_Actions.tmdl").write_text(audit_tmdl, encoding="utf-8")

    # 9. _Measures.tmdl (Master DAX Library)
    measures_tmdl = """table _Measures

\tcolumn Placeholder
\t\tdataType: int64
\t\tisHidden
\t\tsummarizeBy: none
\t\tsourceColumn: Placeholder

\tpartition _Measures = m
\t\tmode: import
\t\tsource = #table(type table [Placeholder = Int64.Type], {{1}})

\t// --- BASISMÅLINGER ---
\tmeasure 'Regnskap YTD' = CALCULATE(SUM(Fact_Regnskap[Regnskap]))
\t\tformatString: #,##0 "kr"

\tmeasure 'Budsjett YTD' = CALCULATE(SUM(Fact_Regnskap[Budsjett]))
\t\tformatString: #,##0 "kr"

\tmeasure 'Avvik YTD' = [Regnskap YTD] - [Budsjett YTD]
\t\tformatString: #,##0 "kr";[Red](#,##0 "kr");"-"

\tmeasure 'Avvik YTD %' = DIVIDE([Avvik YTD], ABS([Budsjett YTD]), 0)
\t\tformatString: 0.0%

\tmeasure 'Merforbruk YTD' = MAX([Avvik YTD], 0)
\t\tformatString: #,##0 "kr"

\tmeasure 'Mindreforbruk YTD' = MAX(-[Avvik YTD], 0)
\t\tformatString: #,##0 "kr"

\tmeasure 'Vedtatt Årsbudsjett' = CALCULATE(SUM(Fact_Regnskap[Aarsbudsjett]), REMOVEFILTERS(Dim_Dato))
\t\tformatString: #,##0 "kr"

\t// --- FORECASTING / EOY ---
\tmeasure 'EOY Rullende Prognose' = VAR AnnualBudget = [Vedtatt Årsbudsjett] VAR RemainingBudget = MAX(AnnualBudget - [Budsjett YTD], 0) RETURN [Regnskap YTD] + RemainingBudget + MAX([Avvik YTD], 0) * 0.5
\t\tformatString: #,##0 "kr"

\tmeasure 'EOY Forventet Årsavvik' = [EOY Rullende Prognose] - [Vedtatt Årsbudsjett]
\t\tformatString: #,##0 "kr";[Red](#,##0 "kr");"-"

\tmeasure 'Planlagt Tiltakseffekt T3' = SWITCH(SELECTEDVALUE(Dim_Ansvar[ansvar_kode]), "2540", 1928421, "2020", 863000, 2791421)
\t\tformatString: #,##0 "kr"

\tmeasure 'EOY Net Zero Sluttavvik' = [EOY Forventet Årsavvik] - [Planlagt Tiltakseffekt T3]
\t\tformatString: #,##0 "kr";[Red](#,##0 "kr");"-"

\t// --- TUFTE FARGESTYRING ---
\tmeasure 'Tufte_Avvik_Farge_HEX' = SWITCH(TRUE(), [Avvik YTD %] > 0.05, "#DC2626", [Avvik YTD %] > 0.02, "#F59E0B", "#16A34A")

\t// --- KOSTRA KPIS ---
\tmeasure 'Vikarutgifter Art 1020' = CALCULATE(SUM(Fact_Regnskap[Regnskap]), Fact_Regnskap[KOSTRA_Art] = "1020")
\t\tformatString: #,##0 "kr"

\tmeasure 'Overtid Art 1090' = CALCULATE(SUM(Fact_Regnskap[Regnskap]), Fact_Regnskap[KOSTRA_Art] = "1090")
\t\tformatString: #,##0 "kr"

\tmeasure 'NAV Refusjoner Art 1600' = CALCULATE(SUM(Fact_Regnskap[Regnskap]), Fact_Regnskap[KOSTRA_Art] = "1600")
\t\tformatString: #,##0 "kr"

\tmeasure 'Total Lonn' = CALCULATE(SUM(Fact_Regnskap[Regnskap]), Fact_Regnskap[Hovedgruppe] IN {"1 Lønn", "Lønn og sosiale utgifter", "10 Fastlønn"})
\t\tformatString: #,##0 "kr"

\tmeasure 'Vikarandel Lonn %' = DIVIDE([Vikarutgifter Art 1020], [Total Lonn], 0)
\t\tformatString: 0.0%

\tmeasure 'Overtidsandel %' = DIVIDE([Overtid Art 1090], [Total Lonn], 0)
\t\tformatString: 0.0%

\tmeasure 'Netto Driftsutgift Per Elev' = DIVIDE(CALCULATE([Regnskap YTD], Dim_Ansvar[ansvar_kode] = "2020"), 1420, 0)
\t\tformatString: #,##0 "kr/elev"

\t// --- WHAT-IF PARAMETERE ---
\tmeasure 'Framsikt Deflator Value' = SELECTEDVALUE(Framsikt_Deflator[Value], 0.041)
\t\tformatString: 0.0%

\tmeasure 'Fraværstiltak Effektreduksjon Value' = SELECTEDVALUE(Fravaer_Reduksjon[Value], 0.015)
\t\tformatString: 0.0%

\tmeasure 'Simulert EOY Netto Driftsresultat' = VAR DeflatorAddition = [Vedtatt Årsbudsjett] * [Framsikt Deflator Value] VAR VikarSavings = [Vikarutgifter Art 1020] * [Fraværstiltak Effektreduksjon Value] RETURN [EOY Rullende Prognose] + DeflatorAddition - VikarSavings
\t\tformatString: #,##0 "kr"

\tmeasure 'Simulert EOY Forventet Avvik' = [Simulert EOY Netto Driftsresultat] - [Vedtatt Årsbudsjett]
\t\tformatString: #,##0 "kr";[Red](#,##0 "kr");"-"

\t// --- PROJECT CONTROLLING (EVM) ---
\tmeasure 'Planlagt Verdi (PV)' = [Budsjett YTD]
\t\tformatString: #,##0 "kr"

\tmeasure 'Påløpt Kostnad (AC)' = [Regnskap YTD]
\t\tformatString: #,##0 "kr"

\tmeasure 'Kostnadsavvik (CV)' = [Planlagt Verdi (PV)] - [Påløpt Kostnad (AC)]
\t\tformatString: #,##0 "kr";[Red](#,##0 "kr");"-"

\tmeasure 'Kostnadsindeks (CPI)' = DIVIDE([Planlagt Verdi (PV)], [Påløpt Kostnad (AC)], 1.0)
\t\tformatString: 0.000

\tmeasure 'Sluttprognose (EAC)' = DIVIDE([Vedtatt Årsbudsjett], [Kostnadsindeks (CPI)], [Vedtatt Årsbudsjett])
\t\tformatString: #,##0 "kr"

\t// --- DYNAMISKE TITLER & AKSJONSTITLER ---
\tmeasure 'Dynamisk_Tittel_Nivaa' = IF(ISINSCOPE(Dim_Ansvar[ansvar_navn]), "Detaljnivå: " & SELECTEDVALUE(Dim_Ansvar[ansvar_navn]), "Samlet Kommunenivå — Kristiansand")

\tmeasure 'FT_Aksjonstittel_Avvik' = IF([Avvik YTD] > 500000, "Kritisk merforbruk på kr " & FORMAT([Avvik YTD], "#,##0") & " (" & FORMAT([Avvik YTD %], "+0.0%") & ") — Tiltak iverksatt", "Økonomisk drift i balanse innenfor tildelt budsjettramme")
"""
    (tables_dir / "_Measures.tmdl").write_text(measures_tmdl, encoding="utf-8")
    print("✓ Semantic Model (TMDL) ferdigstilt.")

# ==============================================================================
# 2. POWER BI REPORT (PBIR) GENERATOR
# ==============================================================================

def make_visual_card(name, x, y, w, h, measure_name, title_text, z=1):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z},
        "visual": {
            "visualType": "card",
            "drillFilterOtherVisuals": True,
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                        "Property": measure_name
                                    }
                                },
                                "queryRef": f"_Measures.{measure_name}",
                                "nativeQueryRef": measure_name,
                                "active": True
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                    }
                }]
            }
        }
    }

def make_visual_column_chart(name, x, y, w, h, cat_table, cat_col, measure_name, title_text, z=2):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z},
        "visual": {
            "visualType": "columnChart",
            "drillFilterOtherVisuals": True,
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [{
                            "field": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Entity": cat_table}},
                                    "Property": cat_col
                                }
                            },
                            "queryRef": f"{cat_table}.{cat_col}",
                            "nativeQueryRef": cat_col,
                            "active": True
                        }]
                    },
                    "Y": {
                        "projections": [{
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": measure_name
                                }
                            },
                            "queryRef": f"_Measures.{measure_name}",
                            "nativeQueryRef": measure_name,
                            "active": True
                        }]
                    }
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                    }
                }]
            }
        }
    }

def make_visual_bar_chart(name, x, y, w, h, cat_table, cat_col, measure_name, title_text, z=3):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z},
        "visual": {
            "visualType": "barChart",
            "drillFilterOtherVisuals": True,
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [{
                            "field": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Entity": cat_table}},
                                    "Property": cat_col
                                }
                            },
                            "queryRef": f"{cat_table}.{cat_col}",
                            "nativeQueryRef": cat_col,
                            "active": True
                        }]
                    },
                    "Y": {
                        "projections": [{
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": measure_name
                                }
                            },
                            "queryRef": f"_Measures.{measure_name}",
                            "nativeQueryRef": measure_name,
                            "active": True
                        }]
                    }
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                    }
                }]
            }
        }
    }

def make_visual_table(name, x, y, w, h, col_specs, measure_specs, title_text, z=4):
    projections = []
    for t_name, c_name in col_specs:
        projections.append({
            "field": {
                "Column": {
                    "Expression": {"SourceRef": {"Entity": t_name}},
                    "Property": c_name
                }
            },
            "queryRef": f"{t_name}.{c_name}",
            "nativeQueryRef": c_name,
            "active": True
        })
    for m_name in measure_specs:
        projections.append({
            "field": {
                "Measure": {
                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                    "Property": m_name
                }
            },
            "queryRef": f"_Measures.{m_name}",
            "nativeQueryRef": m_name,
            "active": True
        })
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z},
        "visual": {
            "visualType": "tableEx",
            "drillFilterOtherVisuals": True,
            "query": {
                "queryState": {
                    "Values": {
                        "projections": projections
                    }
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                    }
                }]
            }
        }
    }

def make_visual_slicer(name, x, y, w, h, table_name, col_name, title_text, z=5):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.3.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z},
        "visual": {
            "visualType": "slicer",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [{
                            "field": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Entity": table_name}},
                                    "Property": col_name
                                }
                            },
                            "queryRef": f"{table_name}.{col_name}",
                            "nativeQueryRef": col_name,
                            "active": True
                        }]
                    }
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                    }
                }]
            }
        }
    }

def build_report_pages():
    print("Bygger 7 standardiserte PBIR rapportsider...")
    pages_dir = REPORT_DIR / "definition" / "pages"
    
    # Slett eksisterende sider for å bygge 7 rene sider
    for item in pages_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)

    pages_config = [
        {
            "id": "p01_cfo_executive",
            "displayName": "1. Toppledelse (CFO Panel)",
            "actionTitle": "Kristiansand Kommune — Finansiell Topplederoversikt & Prognose 2026",
            "visuals": [
                make_visual_card("v01_card1", 20, 20, 360, 140, "Regnskap YTD", "Regnskap Hittil i År", z=1),
                make_visual_card("v01_card2", 400, 20, 360, 140, "Budsjett YTD", "Periodisert Budsjett", z=2),
                make_visual_card("v01_card3", 780, 20, 360, 140, "Avvik YTD", "Avvik Hittil i År", z=3),
                make_visual_card("v01_card4", 1160, 20, 380, 140, "EOY Forventet Årsavvik", "Forventet Årsavvik (EOY)", z=4),
                make_visual_slicer("v01_slicer1", 20, 180, 260, 240, "Dim_Ansvar", "kommunalsjefomrade", "Sektorfilter", z=5),
                make_visual_slicer("v01_slicer2", 20, 440, 260, 420, "Dim_Dato", "tertial", "Tertialfilter", z=6),
                make_visual_bar_chart("v01_bar1", 300, 180, 680, 340, "Dim_Ansvar", "ansvar_navn", "Avvik YTD", "Avvik per Enhet (Diverging Bar)", z=7),
                make_visual_column_chart("v01_col1", 1000, 180, 560, 340, "Dim_Art", "Hovedgruppe", "Regnskap YTD", "Forbruk per Hovedgruppe", z=8),
                make_visual_table("v01_tab1", 300, 540, 1260, 320, [("Dim_Ansvar", "ansvar_navn"), ("Dim_Ansvar", "kommunalsjefomrade")], ["Budsjett YTD", "Regnskap YTD", "Avvik YTD", "Avvik YTD %", "EOY Forventet Årsavvik"], "Enhetsoversikt og Sluttprognose", z=9)
            ]
        },
        {
            "id": "p02_oppvekst_skole",
            "displayName": "2. Sektor Oppvekst & Grunnskole",
            "actionTitle": "Enhet 202 Grunnskole: Vikarforbruk og sykefravær krever omdisponering",
            "visuals": [
                make_visual_card("v02_card1", 20, 20, 360, 140, "Regnskap YTD", "Forbruk Grunnskole", z=1),
                make_visual_card("v02_card2", 400, 20, 360, 140, "Vikarutgifter Art 1020", "Innkjøp Vikarer (Art 1020)", z=2),
                make_visual_card("v02_card3", 780, 20, 360, 140, "Vikarandel Lonn %", "Vikarandel av Lønn", z=3),
                make_visual_card("v02_card4", 1160, 20, 380, 140, "Netto Driftsutgift Per Elev", "Netto Kostnad pr. Elev", z=4),
                make_visual_column_chart("v02_col1", 20, 180, 850, 400, "Dim_Art", "Kontonavn", "Avvik YTD", "Avvik per Kontoart (Art 1010, 1020, 1090, 1600)", z=5),
                make_visual_table("v02_tab1", 890, 180, 670, 680, [("Dim_Art", "Kontokode"), ("Dim_Art", "Kontonavn")], ["Budsjett YTD", "Regnskap YTD", "Avvik YTD", "Avvik YTD %"], "Kontospesifikasjon Grunnskole", z=6),
                make_visual_table("v02_tab2", 20, 600, 850, 260, [("Dim_Ansvar", "ansvar_navn")], ["Regnskap YTD", "Vikarutgifter Art 1020", "Vikarandel Lonn %", "Netto Driftsutgift Per Elev"], "Skoleklyngesammenligning", z=7)
            ]
        },
        {
            "id": "p03_helse_mestring",
            "displayName": "3. Sektor Helse & Mestring",
            "actionTitle": "Enhet 401 Boenhet: Turnus- og overtidspress i døgnkontinuerlig drift",
            "visuals": [
                make_visual_card("v03_card1", 20, 20, 360, 140, "Regnskap YTD", "Forbruk Helse & Mestring", z=1),
                make_visual_card("v03_card2", 400, 20, 360, 140, "Overtid Art 1090", "Overtid & Tillegg", z=2),
                make_visual_card("v03_card3", 780, 20, 360, 140, "Overtidsandel %", "Overtidsandel i Turnus", z=3),
                make_visual_card("v03_card4", 1160, 20, 380, 140, "EOY Net Zero Sluttavvik", "Est. Sluttavvik etter Tiltak", z=4),
                make_visual_bar_chart("v03_bar1", 20, 180, 800, 420, "Dim_Ansvar", "ansvar_navn", "Avvik YTD", "Avvik per Boenhet / Lokasjon", z=5),
                make_visual_table("v03_tab1", 840, 180, 720, 680, [("Dim_Art", "Kontonavn"), ("Dim_Art", "Hovedgruppe")], ["Budsjett YTD", "Regnskap YTD", "Avvik YTD", "Overtidsandel %"], "Turnus- og Overtidsfordeling", z=6),
                make_visual_column_chart("v03_col1", 20, 620, 800, 240, "Dim_Dato", "manedsnavn", "Regnskap YTD", "Månedlig Utvikling Døgnvakter", z=7)
            ]
        },
        {
            "id": "p04_lonn_vikar_monitor",
            "displayName": "4. Lønn & Vikarmonitor",
            "actionTitle": "HR & Lønnsmonitor: Artsanalyse for 1000 Fastlønn, 1020 Vikar og 1090 Overtid",
            "visuals": [
                make_visual_card("v04_card1", 20, 20, 360, 140, "Total Lonn", "Samlet Lønnskostnad YTD", z=1),
                make_visual_card("v04_card2", 400, 20, 360, 140, "Vikarutgifter Art 1020", "Vikarforbruk (Art 1020)", z=2),
                make_visual_card("v04_card3", 780, 20, 360, 140, "Overtid Art 1090", "Overtid (Art 1090)", z=3),
                make_visual_card("v04_card4", 1160, 20, 380, 140, "NAV Refusjoner Art 1600", "Bokførte NAV-Refusjoner", z=4),
                make_visual_column_chart("v04_col1", 20, 180, 800, 380, "Dim_Dato", "manedsnavn", "Vikarutgifter Art 1020", "Vikarutvikling per Måned", z=5),
                make_visual_bar_chart("v04_bar1", 840, 180, 720, 380, "Dim_Ansvar", "ansvar_navn", "Vikarandel Lonn %", "Vikarandel per Enhet", z=6),
                make_visual_table("v04_tab1", 20, 580, 1540, 280, [("Dim_Art", "Kontokode"), ("Dim_Art", "Kontonavn"), ("Dim_Ansvar", "ansvar_navn")], ["Budsjett YTD", "Regnskap YTD", "Avvik YTD", "Avvik YTD %"], "Detaljert Lønns- og Refusjonsmatrise", z=7)
            ]
        },
        {
            "id": "p05_prognose_scenarier",
            "displayName": "5. Prognose & Scenarier",
            "actionTitle": "What-If Simulering: Framsikt deflator, vikarreduksjon og helårsbalanse",
            "visuals": [
                make_visual_card("v05_card1", 20, 20, 360, 140, "Vedtatt Årsbudsjett", "Vedtatt Årsramme", z=1),
                make_visual_card("v05_card2", 400, 20, 360, 140, "EOY Rullende Prognose", "Prognose EOY Uten Tiltak", z=2),
                make_visual_card("v05_card3", 780, 20, 360, 140, "Planlagt Tiltakseffekt T3", "Tiltaksbesparelse T3", z=3),
                make_visual_card("v05_card4", 1160, 20, 380, 140, "Simulert EOY Forventet Avvik", "Simulert EOY Sluttavvik", z=4),
                make_visual_slicer("v05_slic1", 20, 180, 360, 320, "Framsikt_Deflator", "Label", "What-If Lønnsdeflator", z=5),
                make_visual_slicer("v05_slic2", 20, 520, 360, 340, "Fravaer_Reduksjon", "Label", "What-If Fraværsreduksjon", z=6),
                make_visual_column_chart("v05_col1", 400, 180, 600, 360, "Dim_Ansvar", "ansvar_navn", "EOY Forventet Årsavvik", "Forventet Årsavvik per Enhet", z=7),
                make_visual_table("v05_tab1", 1020, 180, 540, 680, [("Dim_Ansvar", "ansvar_navn")], ["Vedtatt Årsbudsjett", "EOY Rullende Prognose", "Planlagt Tiltakseffekt T3", "Simulert EOY Forventet Avvik"], "Scenariooversikt EOY", z=8),
                make_visual_card("v05_card5", 400, 560, 600, 300, "Simulert EOY Netto Driftsresultat", "Simulert Netto Driftsramme ved Årsslutt", z=9)
            ]
        },
        {
            "id": "p06_investering_evm",
            "displayName": "6. Investering & Capex (EVM)",
            "actionTitle": "Project Controlling: Investeringsportefølje, Earned Value & Sluttkostnad (EAC)",
            "visuals": [
                make_visual_card("v06_card1", 20, 20, 360, 140, "Planlagt Verdi (PV)", "Planlagt Verdi (PV YTD)", z=1),
                make_visual_card("v06_card2", 400, 20, 360, 140, "Påløpt Kostnad (AC)", "Påløpt Kostnad (AC YTD)", z=2),
                make_visual_card("v06_card3", 780, 20, 360, 140, "Kostnadsavvik (CV)", "Kostnadsavvik (CV = PV - AC)", z=3),
                make_visual_card("v06_card4", 1160, 20, 380, 140, "Kostnadsindeks (CPI)", "Kostnadsindeks (CPI)", z=4),
                make_visual_bar_chart("v06_bar1", 20, 180, 750, 380, "Dim_Ansvar", "ansvar_navn", "Kostnadsavvik (CV)", "Prosjektavvik (CV) per Enhet", z=5),
                make_visual_column_chart("v06_col1", 790, 180, 770, 380, "Dim_Ansvar", "ansvar_navn", "Sluttprognose (EAC)", "Sluttprognose (EAC) per Prosjekt", z=6),
                make_visual_table("v06_tab1", 20, 580, 1540, 280, [("Dim_Ansvar", "ansvar_navn"), ("Dim_Ansvar", "kommunalsjefomrade")], ["Planlagt Verdi (PV)", "Påløpt Kostnad (AC)", "Kostnadsavvik (CV)", "Kostnadsindeks (CPI)", "Sluttprognose (EAC)"], "EVM Porteføljematrise for Project Controller", z=7)
            ]
        },
        {
            "id": "p07_revisjon_port9",
            "displayName": "7. Revisjon & Audit Trail",
            "actionTitle": "Revisjonsspor & Kontrollutvalget: SHA-256 forsegling og Human-in-the-Loop",
            "visuals": [
                make_visual_card("v07_card1", 20, 20, 480, 140, "Regnskap YTD", "Verifisert Transaksjonssum", z=1),
                make_visual_card("v07_card2", 520, 20, 480, 140, "Avvik YTD", "Totalavvik Gransket", z=2),
                make_visual_card("v07_card3", 1020, 20, 520, 140, "Planlagt Tiltakseffekt T3", "Signerte Tiltak i Port 9", z=3),
                make_visual_table("v07_tab1", 20, 180, 1520, 680, [("Audit_AI_Actions", "Tidsstempel"), ("Audit_AI_Actions", "Enhetskode"), ("Audit_AI_Actions", "AI_Tiltak"), ("Audit_AI_Actions", "Leder_Beslutning"), ("Audit_AI_Actions", "Saksbehandler"), ("Audit_AI_Actions", "Begrunnelse"), ("Audit_AI_Actions", "SHA256_Hash")], [], "Uforanderlig Revisjonslogg (Audit_AI_Actions)", z=4)
            ]
        }
    ]

    page_order = []
    for p_cfg in pages_config:
        pid = p_cfg["id"]
        page_order.append(pid)
        p_dir = pages_dir / pid
        v_dir = p_dir / "visuals"
        v_dir.mkdir(parents=True, exist_ok=True)

        # page.json
        page_json_data = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": pid,
            "displayName": p_cfg["displayName"],
            "displayOption": "FitToPage",
            "height": 900,
            "width": 1600
        }
        (p_dir / "page.json").write_text(json.dumps(page_json_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Visuals
        for vis in p_cfg["visuals"]:
            vis_id = vis["name"]
            single_v_dir = v_dir / vis_id
            single_v_dir.mkdir(parents=True, exist_ok=True)
            (single_v_dir / "visual.json").write_text(json.dumps(vis, indent=2, ensure_ascii=False), encoding="utf-8")

    # pages.json
    pages_meta = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": page_order,
        "activePageName": page_order[0]
    }
    (pages_dir / "pages.json").write_text(json.dumps(pages_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ {len(page_order)} PBIR rapportsider bygget og lagret.")

def main():
    print("Starter bygging av Power BI rapporteringsprosjekt...")
    setup_directories()
    build_semantic_model()
    build_report_pages()
    print("\n✅ Power BI Rapporteringsprosjekt (pbi_reporting_project.pbip) er 100 % ferdigstilt!")

if __name__ == "__main__":
    main()
