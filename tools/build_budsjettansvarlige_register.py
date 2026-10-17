#!/usr/bin/env python3
"""
Generator for Register over Budsjettansvarlige, Delegeringsfullmakter og Skjemaflyt
Kristiansand Kommune — Økonomi og Virksomhetsstyring
"""

import sys
import json
import csv
import sqlite3
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
ERP_DIR = ROOT_DIR / "erp_data"
DB_PATH = ERP_DIR / "kommune_golden_record.db"

REGISTER = [
    # =========================================================================
    # NIVÅ 1: TOPPLEDELSE (KOMMUNEDIREKTØR & KOMMUNALSJEFER)
    # =========================================================================
    {
        "ansvar_id": "0000-KOMMDIR",
        "navn": "Camilla Dunsæd",
        "tittel": "Kommunedirektør",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Toppledelse",
        "sektor_kode": "KONSERN",
        "sektor_navn": "Konsernledelsen / Bystyret",
        "enhet_navn": "Kommunedirektørens stab",
        "kostra_funksjon": "100 Politisk styring og konsernledelse",
        "epost": "camilla.dunsaed@kristiansand.kommune.no",
        "telefon": "+47 38 00 70 01",
        "kontorsted": "Rådhuset, Rådhusgata 18, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 100000000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Bystyrets Tertialrapport (T1/T2), Årsregnskap, Rammereguleringsnotat § 14-5, Beredskapsrapport",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNEDIREKTOR.docx",
        "returkanal": "bystyret.postmottak@kristiansand.kommune.no / Public 360",
        "returfrist": "M+12 virkedag kl. 16:00"
    },
    {
        "ansvar_id": "5000-SJEF-HELSE",
        "navn": "Brede Skeie",
        "tittel": "Kommunalsjef Helse og mestring",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Kommunalsjef",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Kommunalsjefens fagstab Helse",
        "kostra_funksjon": "241/253/254 Helse og omsorg",
        "epost": "brede.skeie@kristiansand.kommune.no",
        "telefon": "+47 38 00 71 10",
        "kontorsted": "Kvartal 35, Tollbodgata 22, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 25000000,
        "controller_navn": "Frank Ellingsen / Marianne Tellefsen",
        "controller_epost": "okonomi.helse@kristiansand.kommune.no",
        "utsendte_rapporter": "Sektorrapport Helse M9/M10, Porteføljerapport HTA § 4 Langvakter, Søknad toppfinansiering ressurskrevende",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no / Websak 26/08940",
        "returfrist": "M+8 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "4000-SJEF-OPPV",
        "navn": "Kristin Eidet Robstad",
        "tittel": "Kommunalsjef Oppvekst og utdanning",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Kommunalsjef",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Kommunalsjefens fagstab Oppvekst",
        "kostra_funksjon": "202/211/222 Grunnskole og barnehage",
        "epost": "kristin.robstad@kristiansand.kommune.no",
        "telefon": "+47 38 00 72 10",
        "kontorsted": "Kvartal 35, Tollbodgata 22, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 25000000,
        "controller_navn": "Frank Ellingsen / Erik Halvorsen",
        "controller_epost": "okonomi.oppvekst@kristiansand.kommune.no",
        "utsendte_rapporter": "Sektorrapport Oppvekst M9/M10, Lærernormoppfølging § 8-2, Barnehagetilskudd § 19, Vikarrammeavvik",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no / Websak 26/08940",
        "returfrist": "M+8 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "3000-SJEF-BYUTV",
        "navn": "Ragnar Evensen",
        "tittel": "Kommunalsjef By- og stedsutvikling",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Kommunalsjef",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "Kommunalsjefens stab Byutvikling",
        "kostra_funksjon": "301/340/345 Plan, VAR og samferdsel",
        "epost": "ragnar.evensen@kristiansand.kommune.no",
        "telefon": "+47 38 00 73 10",
        "kontorsted": "Tangen 8, 4608 Kristiansand",
        "delegeringsfullmakt_nok": 20000000,
        "controller_navn": "Knut Arild Vike",
        "controller_epost": "okonomi.byutvikling@kristiansand.kommune.no",
        "utsendte_rapporter": "VAR Selvkostrapport (5-års fond), Capex KS2 Investeringsoppfølging, Gebyrregulativ 2027",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.byutvikling@kristiansand.kommune.no / Websak",
        "returfrist": "M+8 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "2000-SJEF-KULTUR",
        "navn": "Camilla Jarlsby",
        "tittel": "Kommunalsjef Kultur og innbyggerdialog",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Kommunalsjef",
        "sektor_kode": "KULTUR",
        "sektor_navn": "Kultur og innbyggerdialog",
        "enhet_navn": "Kommunalsjefens stab Kultur",
        "kostra_funksjon": "380/383/385 Idrett, bibliotek og kulturhus",
        "epost": "camilla.jarlsby@kristiansand.kommune.no",
        "telefon": "+47 38 00 74 10",
        "kontorsted": "Gyldenløves gate 23, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 15000000,
        "controller_navn": "Silje Mæland",
        "controller_epost": "okonomi.kultur@kristiansand.kommune.no",
        "utsendte_rapporter": "Sektorrapport Kultur M9/M10, Folkebibliotektilbud jf. Lov § 1, Idrettsanlegg energiutligning",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.kultur@kristiansand.kommune.no / Websak",
        "returfrist": "M+8 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "1000-SJEF-ORGTEK",
        "navn": "Geir A. Askvik",
        "tittel": "Kommunalsjef Organisasjon og teknologi",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Kommunalsjef",
        "sektor_kode": "ORG_TEK",
        "sektor_navn": "Organisasjon og teknologi",
        "enhet_navn": "Kommunalsjefens stab Org & Tek",
        "kostra_funksjon": "120/130 IKT, digitalisering og fellestjenester",
        "epost": "geir.askvik@kristiansand.kommune.no",
        "telefon": "+47 38 00 75 10",
        "kontorsted": "Rådhuskvartalet, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 15000000,
        "controller_navn": "Silje Mæland / Frank Ellingsen",
        "controller_epost": "okonomi.orgtek@kristiansand.kommune.no",
        "utsendte_rapporter": "FinOps SaaS Lisensrapport, Konsulentreduksjonsplan (art 11950), AI Risikovurdering (FRIA/DPIA)",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.orgtek@kristiansand.kommune.no / Websak",
        "returfrist": "M+8 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "6000-DIR-OKONOMI",
        "navn": "Terje Fjellvang",
        "tittel": "Økonomidirektør",
        "niva": "NIVA1",
        "niva_tekst": "Nivå 1: Økonomidirektør",
        "sektor_kode": "OKONOMI",
        "sektor_navn": "Økonomi og virksomhetsstyring",
        "enhet_navn": "Sentral økonomistab",
        "kostra_funksjon": "170/180/190 Finansforvaltning og konsernregnskap",
        "epost": "terje.fjellvang@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 10",
        "kontorsted": "Rådhuset, Torvet 1, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 50000000,
        "controller_navn": "Frank Ellingsen (Senior Controller)",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Konsern Finans- og Gjeldsrapport, Likviditetsprognose, Pensjonspremieavvik (7 år), Handlingsregel Disposisjonsfond",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNEDIREKTOR.docx",
        "returkanal": "konsernokonomi@kristiansand.kommune.no / Websak",
        "returfrist": "M+9 virkedag kl. 12:00"
    },

    # =========================================================================
    # NIVÅ 2: AVDELINGSDIREKTØRER / OMRÅDELEDERE
    # =========================================================================
    {
        "ansvar_id": "5100-OMR-SYKEHJEM",
        "navn": "Mette Syvertsen",
        "tittel": "Områdeleder Institusjon & Døgnpleie",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Døgnomsorg og Sykehjem",
        "kostra_funksjon": "254 Kommunale sykehjem og heldøgnspleie",
        "epost": "mette.syvertsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 71 20",
        "kontorsted": "Kvartal 35, Tollbodgata 22",
        "delegeringsfullmakt_nok": 10000000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Samlet Institusjonsrapport M9/M10, Turnusoversikt GAT, Vikarbyråforbruk (art 10200)",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "5200-OMR-HJEMME",
        "navn": "Arve Sætre",
        "tittel": "Områdeleder Hjemmebaserte Tjenester",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Hjemmetjenester og rehabilitering",
        "kostra_funksjon": "253 Pleie og omsorg i hjemmet",
        "epost": "arve.saetre@kristiansand.kommune.no",
        "telefon": "+47 38 00 71 30",
        "kontorsted": "Lund Helsehus, Marviksveien 20",
        "delegeringsfullmakt_nok": 8000000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Kjørerute- og bemanningsavvik, Velferdsteknologieffekt, Overtidslogg art 10900",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "4100-OMR-SKOLE",
        "navn": "Svein Tore Kvernes",
        "tittel": "Skolesjef Grunnskole",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Grunnskoleavdelingen (28 skoler)",
        "kostra_funksjon": "202 Grunnskoleopplæring",
        "epost": "svein.tore.kvernes@kristiansand.kommune.no",
        "telefon": "+47 38 00 72 20",
        "kontorsted": "Kvartal 35, Tollbodgata 22",
        "delegeringsfullmakt_nok": 10000000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Konsolidert Skolerapport M9/M10, Felles Vikarring Status, Lærertetthetskontroll",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "4200-OMR-BHG",
        "navn": "Anne Lise Tønnessen",
        "tittel": "Barnehagesjef",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Barnehageavdelingen (54 barnehager)",
        "kostra_funksjon": "211 Styrket barnehagetilbud",
        "epost": "anne.lise.tonnessen@kristiansand.kommune.no",
        "telefon": "+47 38 00 72 30",
        "kontorsted": "Kvartal 35, Tollbodgata 22",
        "delegeringsfullmakt_nok": 8000000,
        "controller_navn": "Erik Halvorsen",
        "controller_epost": "erik.halvorsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Barnehagetilskudd Privat vs Kommunal, Bemanningsnormrapport, Vikarforbruk",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "3100-DIR-VAR",
        "navn": "Helge Møller",
        "tittel": "VA-sjef & Kommunalteknisk Direktør",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "Ingeniørvesenet (Vann, Avløp & Renovasjon)",
        "kostra_funksjon": "340/345 Vann og avløp selvkost",
        "epost": "helge.moller@kristiansand.kommune.no",
        "telefon": "+47 38 00 73 30",
        "kontorsted": "Rigetjønnveien 18, 4626 Kristiansand",
        "delegeringsfullmakt_nok": 10000000,
        "controller_navn": "Knut Arild Vike",
        "controller_epost": "knut.arild.vike@kristiansand.kommune.no",
        "utsendte_rapporter": "Selvkostberegning M9, Capex Hovedledning Framdriftsrapport, Investeringsplan 2026–2030",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.byutvikling@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "3200-DIR-PLAN",
        "navn": "Einar Jørgensen",
        "tittel": "Områdeleder Byplan & Byggesak",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "Plan- og bygningsetaten",
        "kostra_funksjon": "301/302 Plan og byggesak",
        "epost": "einar.jorgensen@kristiansand.kommune.no",
        "telefon": "+47 38 00 73 20",
        "kontorsted": "Tangen 8, 4608 Kristiansand",
        "delegeringsfullmakt_nok": 6000000,
        "controller_navn": "Knut Arild Vike",
        "controller_epost": "knut.arild.vike@kristiansand.kommune.no",
        "utsendte_rapporter": "Gebyrsituasjon Byggesak, Reguleringsplan portefølje, Selvkost 3-årskontroll",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.byutvikling@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "1100-DIR-IKT",
        "navn": "Siri Bentsen",
        "tittel": "IKT- og Digitaliseringsdirektør",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "ORG_TEK",
        "sektor_navn": "Organisasjon og teknologi",
        "enhet_navn": "Digitaliseringsavdelingen",
        "kostra_funksjon": "130 IKT og fellesløsninger",
        "epost": "siri.bentsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 75 20",
        "kontorsted": "Rådhuskvartalet, Tollbodgata 22",
        "delegeringsfullmakt_nok": 8000000,
        "controller_navn": "Silje Mæland / Frank Ellingsen",
        "controller_epost": "okonomi.orgtek@kristiansand.kommune.no",
        "utsendte_rapporter": "M365 & SaaS Lisenssanering, Konsulentavtaler art 11950, IT Sikkerhetsstatus",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.orgtek@kristiansand.kommune.no",
        "returfrist": "M+7 virkedag kl. 14:00"
    },
    {
        "ansvar_id": "6100-DIR-REGNSKAP",
        "navn": "Bente Gundersen",
        "tittel": "Konsernregnskapssjef",
        "niva": "NIVA2",
        "niva_tekst": "Nivå 2: Områdedirektør",
        "sektor_kode": "OKONOMI",
        "sektor_navn": "Økonomi og virksomhetsstyring",
        "enhet_navn": "Konsernregnskap og Lønnssentral",
        "kostra_funksjon": "100/170 Konsernregnskap og oppgjør",
        "epost": "bente.gundersen@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 20",
        "kontorsted": "Rådhuset, Torvet 1",
        "delegeringsfullmakt_nok": 10000000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavstemmingsinstruks, MVA-kompensasjonsstatus, Periodelukkingsprotokoll",
        "tilknyttet_mal": "templates/MAL_PERIODELUKKING_OG_AVSTEMMING.docx",
        "returkanal": "konsernokonomi@kristiansand.kommune.no",
        "returfrist": "M+5 virkedag kl. 15:00"
    },

    # =========================================================================
    # NIVÅ 3: ENHETSLEDERE / VIRKSOMHETSLEDERE (KOSTRA-ANSVAR)
    # =========================================================================
    {
        "ansvar_id": "5200-ENH-401",
        "navn": "Solveig Grimstad",
        "tittel": "Enhetsleder Strai Sykehjem",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Enhet 401: Strai Sykehjem & Omsorgsboliger",
        "kostra_funksjon": "254 Kommunal Boenhet og Sykehjem",
        "epost": "solveig.grimstad@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 01",
        "kontorsted": "Strai Helsehus, Setesdalsveien 320, 4618 Kristiansand",
        "delegeringsfullmakt_nok": 2000000,
        "controller_navn": "Frank Ellingsen / Marianne Tellefsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavviksrapport M10, Avviksnotat & Tiltaksplan Sykehjem, HTA § 4 Drøftingsprotokoll (Langvakter)",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "5210-ENH-402",
        "navn": "Berit Olsen",
        "tittel": "Enhetsleder Hjemmetjeneste Vågsbygd",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Enhet 402: Hjemmetjenesten Vågsbygd",
        "kostra_funksjon": "253 Pleie og omsorg i hjemmet",
        "epost": "berit.olsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 02",
        "kontorsted": "Kirsten Flagstads vei 28, 4621 Kristiansand",
        "delegeringsfullmakt_nok": 1500000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Hjemmetjeneste, Overtidsnotat art 10900, Kjøreplanoptimalisering",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "5220-ENH-403",
        "navn": "Christian Holte",
        "tittel": "Enhetsleder Bo- og Miljøtjenester",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Enhet 403: Sørlandsparken Bo- og Miljøtjeneste",
        "kostra_funksjon": "254 Heldøgns omsorgsbolig",
        "epost": "christian.holte@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 03",
        "kontorsted": "Skibåsen 12, 4636 Kristiansand",
        "delegeringsfullmakt_nok": 1800000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Bo og Miljø, To-pleier bemanningsoppfølging, IA-sykefraværsplan",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "5230-ENH-404",
        "navn": "Kari Vesterhus",
        "tittel": "Enhetsleder Presteheia Omsorgssenter",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Enhet 404: Presteheia Omsorgssenter",
        "kostra_funksjon": "254 Sykehjem korttidsplasser",
        "epost": "kari.vesterhus@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 04",
        "kontorsted": "Presteheia 1, 4633 Kristiansand",
        "delegeringsfullmakt_nok": 1500000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsrapport Korttidsbelegg, Samhandlingsavvik overliggerdøgn jf. § 11-2",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "2020",
        "navn": "Trond Jensen",
        "tittel": "Rektor / Enhetsleder Kommunal Skole 2020",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder / Rektor",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Kommunal Skole Enhet 2020",
        "kostra_funksjon": "202 Grunnskole 1.–10. trinn",
        "epost": "trond.jensen@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 20",
        "kontorsted": "Lovisenlev Skolevei 4, 4633 Kristiansand",
        "delegeringsfullmakt_nok": 2000000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Skole, Avviksnotat & Tiltaksplan Vikarer (art 10200), NAV Refusjonspurring (art 16000)",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "2540",
        "navn": "Christian Holte",
        "tittel": "Enhetsleder Kommunal Boenhet 2540",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Kommunal Boenhet 2540",
        "kostra_funksjon": "254 Heldøgns omsorgsbolig",
        "epost": "christian.holte@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 40",
        "kontorsted": "Skibåsen 12, 4636 Kristiansand",
        "delegeringsfullmakt_nok": 2000000,
        "controller_navn": "Frank Ellingsen / Marianne Tellefsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Bo og Miljø, To-pleier bemanningsoppfølging, IA-sykefraværsplan",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "4100-ENH-202",
        "navn": "Trond Jensen",
        "tittel": "Rektor / Enhetsleder Lovisenlev Skole",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder / Rektor",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Enhet 202: Lovisenlev Skole",
        "kostra_funksjon": "202 Grunnskole 1.–7. trinn",
        "epost": "trond.jensen@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 02",
        "kontorsted": "Lovisenlev Skolevei 4, 4633 Kristiansand",
        "delegeringsfullmakt_nok": 2000000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Skole, Avviksnotat & Tiltaksplan Vikarer (art 10200), NAV Refusjonspurring (art 16000)",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "4101-ENH-203",
        "navn": "Mona Lindstrøm",
        "tittel": "Rektor Vågsbygd Skole",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder / Rektor",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Enhet 203: Vågsbygd Skole",
        "kostra_funksjon": "202 Grunnskole 1.–10. trinn",
        "epost": "mona.lindstrom@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 03",
        "kontorsted": "Kirsten Flagstads vei 30, 4621 Kristiansand",
        "delegeringsfullmakt_nok": 1800000,
        "controller_navn": "Erik Halvorsen",
        "controller_epost": "erik.halvorsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Skole, Overtid lærere art 10900, Felles vikarring deltakelse",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "4102-ENH-204",
        "navn": "Espen Birkeland",
        "tittel": "Rektor Grim Ungdomsskole",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder / Rektor",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Enhet 204: Grim Ungdomsskole",
        "kostra_funksjon": "202 Grunnskole 8.–10. trinn",
        "epost": "espen.birkeland@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 04",
        "kontorsted": "Møllevannsveien 48, 4617 Kristiansand",
        "delegeringsfullmakt_nok": 1800000,
        "controller_navn": "Erik Halvorsen",
        "controller_epost": "erik.halvorsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Ungdomsskole, Realfagsvikarer, Valgfagsbudsjett",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "4210-ENH-211",
        "navn": "Grete Hovden",
        "tittel": "Styrer Lund Barnehage",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Styrer Barnehage",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Enhet 211: Lund Kommunale Barnehage",
        "kostra_funksjon": "211 Kommunal barnehage",
        "epost": "grete.hovden@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 11",
        "kontorsted": "Marviksveien 45, 4632 Kristiansand",
        "delegeringsfullmakt_nok": 1200000,
        "controller_navn": "Erik Halvorsen",
        "controller_epost": "erik.halvorsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Bemanningsnorm M9, Vikarkostnader assistenter, Kostpenger avstemming",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "3300-ENH-301",
        "navn": "Hans Petter Vik",
        "tittel": "Enhetsleder Byggesak & Tilsyn",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "Enhet 301: Byggesak og Tilsyn",
        "kostra_funksjon": "301/302 Byggesak og reguleringsplan",
        "epost": "hans.petter.vik@kristiansand.kommune.no",
        "telefon": "+47 38 00 83 01",
        "kontorsted": "Tangen 8, 4608 Kristiansand",
        "delegeringsfullmakt_nok": 1500000,
        "controller_navn": "Knut Arild Vike",
        "controller_epost": "knut.arild.vike@kristiansand.kommune.no",
        "utsendte_rapporter": "Gebyravvik art 1620, Saksmengdestatistikk, Selvkostgrad M9",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.byutvikling@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "3100-ENH-302",
        "navn": "Inger Johanne Foss",
        "tittel": "Enhetsleder VAR Ingeniørvesen",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "Enhet 302: Vann, Avløp og Renovasjon",
        "kostra_funksjon": "340/345 Selvkost Vann og Avløp",
        "epost": "inger.foss@kristiansand.kommune.no",
        "telefon": "+47 38 00 83 02",
        "kontorsted": "Rigetjønnveien 18, 4626 Kristiansand",
        "delegeringsfullmakt_nok": 3000000,
        "controller_navn": "Knut Arild Vike",
        "controller_epost": "knut.arild.vike@kristiansand.kommune.no",
        "utsendte_rapporter": "Selvkostfond Avregning M9, NS 8407 Totalentreprise Avvik, Investeringsframdrift",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.byutvikling@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "2200-ENH-101",
        "navn": "Hege Gabrielsen",
        "tittel": "Biblioteksjef",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder / Biblioteksjef",
        "sektor_kode": "KULTUR",
        "sektor_navn": "Kultur og innbyggerdialog",
        "enhet_navn": "Enhet 101: Kristiansand Folkebibliotek",
        "kostra_funksjon": "385 Folkebibliotek",
        "epost": "hege.gabrielsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 81 01",
        "kontorsted": "Gyldenløves gate 23, 4611 Kristiansand",
        "delegeringsfullmakt_nok": 1000000,
        "controller_navn": "Silje Mæland",
        "controller_epost": "silje.maeland@kristiansand.kommune.no",
        "utsendte_rapporter": "Kvelds- og helgetillegg M9, Bokkjøp og lisenser, Arrangementsbudsjett",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.kultur@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "1110-ENH-501",
        "navn": "Kenneth Dale",
        "tittel": "IKT Driftssjef",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Enhetsleder",
        "sektor_kode": "ORG_TEK",
        "sektor_navn": "Organisasjon og teknologi",
        "enhet_navn": "Enhet 501: IKT Drift & Brukerstøtte",
        "kostra_funksjon": "130 Felles IKT-infrastruktur",
        "epost": "kenneth.dale@kristiansand.kommune.no",
        "telefon": "+47 38 00 85 01",
        "kontorsted": "Rådhuskvartalet, Tollbodgata 22",
        "delegeringsfullmakt_nok": 2500000,
        "controller_navn": "Silje Mæland / Frank Ellingsen",
        "controller_epost": "okonomi.orgtek@kristiansand.kommune.no",
        "utsendte_rapporter": "FinOps Lisenssanering, Konsulenttimer art 11950, Server- og skydriftskostnader",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.orgtek@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "6200-ENH-601",
        "navn": "Knut Ingebrigtsen",
        "tittel": "Finans- og Gjeldsforvalter",
        "niva": "NIVA3",
        "niva_tekst": "Nivå 3: Avdelingsleder Finans",
        "sektor_kode": "OKONOMI",
        "sektor_navn": "Økonomi og virksomhetsstyring",
        "enhet_navn": "Enhet 601: Finans- og Likviditetsforvaltning",
        "kostra_funksjon": "180/190 Renter og gjeldsforvaltning",
        "epost": "knut.ingebrigtsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 86 01",
        "kontorsted": "Rådhuset, Torvet 1",
        "delegeringsfullmakt_nok": 5000000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Rentesikringsrapport (58 % fast), Likviditetsrenteinntekter, Pensjonspremieavvik",
        "tilknyttet_mal": "templates/MAL_PERIODELUKKING_OG_AVSTEMMING.docx",
        "returkanal": "konsernokonomi@kristiansand.kommune.no",
        "returfrist": "M+5 virkedag kl. 14:00"
    },

    # =========================================================================
    # NIVÅ 4: AVDELINGSLEDERE / SEKSJONSLEDERE / TURNUSLEDERE
    # =========================================================================
    {
        "ansvar_id": "5201-SEK-DEMENS",
        "navn": "Tone Røyseland",
        "tittel": "Avdelingsleder Demensavdelingen",
        "niva": "NIVA4",
        "niva_tekst": "Nivå 4: Avdelingsleder / Turnus",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Strai Sykehjem — Avd. Demens",
        "kostra_funksjon": "254 Skjermet enhet demens",
        "epost": "tone.royseland@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 11",
        "kontorsted": "Strai Helsehus, 2. etasje",
        "delegeringsfullmakt_nok": 250000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Gat Turnusliste M10, Overtidsattestasjon art 10900, Vikarforespørsel helg",
        "tilknyttet_mal": "templates/RAPPORTMAL_AVDELINGSLEDER.docx",
        "returkanal": "solveig.grimstad@kristiansand.kommune.no (Enhetsleder)",
        "returfrist": "M+3 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "5202-SEK-KORTTID",
        "navn": "Lars Klev",
        "tittel": "Avdelingsleder Somatikk & Korttid",
        "niva": "NIVA4",
        "niva_tekst": "Nivå 4: Avdelingsleder / Turnus",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Strai Sykehjem — Somatisk Korttidsavd.",
        "kostra_funksjon": "254 Somatisk pleie",
        "epost": "lars.klev@kristiansand.kommune.no",
        "telefon": "+47 38 00 84 12",
        "kontorsted": "Strai Helsehus, 1. etasje",
        "delegeringsfullmakt_nok": 250000,
        "controller_navn": "Marianne Tellefsen",
        "controller_epost": "marianne.tellefsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Turnusavvik, Medisinsk forbruksmateriell, Helgebemanning",
        "tilknyttet_mal": "templates/RAPPORTMAL_AVDELINGSLEDER.docx",
        "returkanal": "solveig.grimstad@kristiansand.kommune.no",
        "returfrist": "M+3 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "4103-SEK-SFO",
        "navn": "Cathrine Solberg",
        "tittel": "Avdelingsleder SFO Lovisenlev",
        "niva": "NIVA4",
        "niva_tekst": "Nivå 4: Avdelingsleder SFO",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Lovisenlev Skole — Skolefritidsordning",
        "kostra_funksjon": "202 Skolefritidsordning (SFO)",
        "epost": "cathrine.solberg@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 12",
        "kontorsted": "Lovisenlev Skole, Bygg B",
        "delegeringsfullmakt_nok": 150000,
        "controller_navn": "Erik Halvorsen",
        "controller_epost": "erik.halvorsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Assistenttimer SFO, Foreldrebetaling avstemming, Matinnkjøp",
        "tilknyttet_mal": "templates/RAPPORTMAL_AVDELINGSLEDER.docx",
        "returkanal": "trond.jensen@kristiansand.kommune.no (Rektor)",
        "returfrist": "M+3 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "4104-SEK-INSP",
        "navn": "Bjarne Wiig",
        "tittel": "Inspektør 1.–4. trinn",
        "niva": "NIVA4",
        "niva_tekst": "Nivå 4: Trinnleder / Inspektør",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Lovisenlev Skole — Småtrinnet",
        "kostra_funksjon": "202 Undervisning småtrinn",
        "epost": "bjarne.wiig@kristiansand.kommune.no",
        "telefon": "+47 38 00 82 13",
        "kontorsted": "Lovisenlev Skole, Administrasjonsfløy",
        "delegeringsfullmakt_nok": 200000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Vikarrekvisisjoner timelærere, Korttidsfravær logg, Lærernormsjekk",
        "tilknyttet_mal": "templates/RAPPORTMAL_AVDELINGSLEDER.docx",
        "returkanal": "trond.jensen@kristiansand.kommune.no (Rektor)",
        "returfrist": "M+3 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "3101-SEK-AVLOP",
        "navn": "Vidar Aanensen",
        "tittel": "Seksjonsleder Lund Renseanlegg",
        "niva": "NIVA4",
        "niva_tekst": "Nivå 4: Seksjonsleder drift",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "VAR Ingeniørvesenet — Renseanlegg Lund",
        "kostra_funksjon": "345 Avløpsrensing",
        "epost": "vidar.aanensen@kristiansand.kommune.no",
        "telefon": "+47 38 00 83 11",
        "kontorsted": "Marviksveien 120, 4632 Kristiansand",
        "delegeringsfullmakt_nok": 350000,
        "controller_navn": "Knut Arild Vike",
        "controller_epost": "knut.arild.vike@kristiansand.kommune.no",
        "utsendte_rapporter": "Driftsavvik kjemikalier art 11150, Slamtransportfakturaer, Beredskapsvakt",
        "tilknyttet_mal": "templates/RAPPORTMAL_AVDELINGSLEDER.docx",
        "returkanal": "inger.foss@kristiansand.kommune.no",
        "returfrist": "M+3 virkedag kl. 12:00"
    },
    {
        "ansvar_id": "1111-SEK-FINOPS",
        "navn": "Thomas Berge",
        "tittel": "Seksjonsleder Skyløsninger & FinOps",
        "niva": "NIVA4",
        "niva_tekst": "Nivå 4: Seksjonsleder IKT",
        "sektor_kode": "ORG_TEK",
        "sektor_navn": "Organisasjon og teknologi",
        "enhet_navn": "IKT Drift — Cloud & FinOps",
        "kostra_funksjon": "130 IT Cloud Operations",
        "epost": "thomas.berge@kristiansand.kommune.no",
        "telefon": "+47 38 00 85 11",
        "kontorsted": "Rådhuskvartalet, 3. etasje",
        "delegeringsfullmakt_nok": 300000,
        "controller_navn": "Silje Mæland",
        "controller_epost": "silje.maeland@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedlig Azure/M365 ressursforbruk, Ubrukte lisensallokeringer, Konsulenttimer",
        "tilknyttet_mal": "templates/RAPPORTMAL_AVDELINGSLEDER.docx",
        "returkanal": "kenneth.dale@kristiansand.kommune.no",
        "returfrist": "M+3 virkedag kl. 12:00"
    },

    # =========================================================================
    # CONTROLLERTEAMET (SPARREPARTNERE, RETURMOTTAKERE OG SERVICE)
    # =========================================================================
    {
        "ansvar_id": "6001-CTRL-FRANK",
        "navn": "Frank Ellingsen",
        "tittel": "Senior Financial Controller & Project Controller",
        "niva": "CONTROLLER",
        "niva_tekst": "Økonomirådgiver / Fagansvarlig",
        "sektor_kode": "KONSERN",
        "sektor_navn": "Konsern, Helse & Oppvekst",
        "enhet_navn": "Sentrale Økonomitjenester / Hub Koordinator",
        "kostra_funksjon": "100 Økonomistyring, EPM & AI Hub",
        "epost": "frank.ellingsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 50",
        "kontorsted": "Rådhuset, Torvet 1, Rom 214",
        "delegeringsfullmakt_nok": 1000000,
        "controller_navn": "Terje Fjellvang (Økonomidirektør)",
        "controller_epost": "terje.fjellvang@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedspakker M1–M12, Monte Carlo EOY P10/P50/P90, Stage-Gate Port 9 Revisjon, FAST Excel Modell",
        "tilknyttet_mal": "templates/RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.docx",
        "returkanal": "frank.ellingsen@kristiansand.kommune.no / AI Hub API",
        "returfrist": "Løpende oppfølging"
    },
    {
        "ansvar_id": "6002-CTRL-MARIANNE",
        "navn": "Marianne Tellefsen",
        "tittel": "Sektorcontroller Helse og Mestring",
        "niva": "CONTROLLER",
        "niva_tekst": "Økonomirådgiver Sektor",
        "sektor_kode": "HELSE",
        "sektor_navn": "Helse og mestring",
        "enhet_navn": "Økonomitjenesten Helse",
        "kostra_funksjon": "241/253/254 Helseøkonomi",
        "epost": "marianne.tellefsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 51",
        "kontorsted": "Kvartal 35, 4. etasje",
        "delegeringsfullmakt_nok": 500000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Helse, Turnusavstemming GAT, HTA § 4 Saksforberedelse",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.helse@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 16:00"
    },
    {
        "ansvar_id": "6003-CTRL-ERIK",
        "navn": "Erik Halvorsen",
        "tittel": "Sektorcontroller Oppvekst og Utdanning",
        "niva": "CONTROLLER",
        "niva_tekst": "Økonomirådgiver Sektor",
        "sektor_kode": "OPPVEKST",
        "sektor_navn": "Oppvekst og utdanning",
        "enhet_navn": "Økonomitjenesten Oppvekst",
        "kostra_funksjon": "202/211 Skole- og barnehageøkonomi",
        "epost": "erik.halvorsen@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 52",
        "kontorsted": "Kvartal 35, 4. etasje",
        "delegeringsfullmakt_nok": 500000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "Månedsavvik Skole, Lærernormberegninger, Barnehagetilskudd",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.oppvekst@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 16:00"
    },
    {
        "ansvar_id": "6004-CTRL-KNUT",
        "navn": "Knut Arild Vike",
        "tittel": "Sektorcontroller Byutvikling & Selvkost",
        "niva": "CONTROLLER",
        "niva_tekst": "Økonomirådgiver Sektor",
        "sektor_kode": "BYUTVIKLING",
        "sektor_navn": "By- og stedsutvikling",
        "enhet_navn": "Økonomitjenesten Byutvikling",
        "kostra_funksjon": "301/340/345 VAR og Byggesaksøkonomi",
        "epost": "knut.arild.vike@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 53",
        "kontorsted": "Tangen 8, 3. etasje",
        "delegeringsfullmakt_nok": 500000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "VAR Selvkostregnskap, Capex Framdriftsrapportering, Gebyrkalkyler",
        "tilknyttet_mal": "templates/RAPPORTMAL_KOMMUNALSJEF.docx",
        "returkanal": "okonomi.byutvikling@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 16:00"
    },
    {
        "ansvar_id": "6005-CTRL-SILJE",
        "navn": "Silje Mæland",
        "tittel": "Sektorcontroller Kultur, Dialog & Fellestjenester",
        "niva": "CONTROLLER",
        "niva_tekst": "Økonomirådgiver Sektor",
        "sektor_kode": "KULTUR",
        "sektor_navn": "Kultur, Dialog, Org & Teknologi",
        "enhet_navn": "Økonomitjenesten Kultur & Felles",
        "kostra_funksjon": "130/380/385 Kultur- og IKT-økonomi",
        "epost": "silje.maeland@kristiansand.kommune.no",
        "telefon": "+47 38 00 76 54",
        "kontorsted": "Gyldenløves gate 23",
        "delegeringsfullmakt_nok": 500000,
        "controller_navn": "Frank Ellingsen",
        "controller_epost": "frank.ellingsen@kristiansand.kommune.no",
        "utsendte_rapporter": "FinOps Kostnadsallokering, Bibliotek- og idrettsanalyser",
        "tilknyttet_mal": "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
        "returkanal": "okonomi.kultur@kristiansand.kommune.no",
        "returfrist": "M+6 virkedag kl. 16:00"
    }
]

def build_security_rls_register(register):
    """
    Bygger Sikkerhets- og RLS-register tilpasset Power BI og Microsoft Teams.
    Nivåhierarki:
      NIVA0_CONTROLLER: Frank Ellingsen (Senior Controller), Camilla Dunsæd, Terje Fjellvang
      NIVA1_KOMMUNALSJEF: Kristin Robstad (Oppvekst), Brede Skeie (Helse), Ragnar Evensen (Byutv), etc.
      NIVA2_OMRADELEDER: Svein Tore Kvernes (Skole), Mette Syvertsen (Institusjon), Helge Møller (VAR), etc.
      NIVA3_ENHETSLEDER: Trond Jensen (2020), Christian Holte (2540), Solveig Grimstad (401), etc.
    """
    sektor_map = {
        "KONSERN": "Konsern",
        "OPPVEKST": "Oppvekst",
        "HELSE": "Helse og mestring",
        "BYUTVIKLING": "By- og stedsutvikling",
        "KULTUR": "Kultur og innbyggerdialog",
        "ORG_TEK": "Organisasjon og teknologi",
        "OKONOMI": "Økonomi og virksomhetsstyring"
    }

    teams_team_map = {
        "KONSERN": "Teams - Konsernledelse & Bystyret",
        "OPPVEKST": "Teams - Oppvekst og Utdanning",
        "HELSE": "Teams - Helse og Mestring",
        "BYUTVIKLING": "Teams - By- og Stedsutvikling",
        "KULTUR": "Teams - Kultur og Dialog",
        "ORG_TEK": "Teams - Organisasjon og Teknologi",
        "OKONOMI": "Teams - Økonomistab & Finans"
    }

    rows = []
    for r in register:
        upn = r["epost"].strip()
        aid = r["ansvar_id"].strip()
        niva = r["niva"].strip()
        sektor = r["sektor_kode"].strip()
        kom_omrade = sektor_map.get(sektor, "Konsern")

        # Frank Ellingsen og toppledelse har full tilgang (Showcase & Admin)
        is_frank = (upn == "frank.ellingsen@kristiansand.kommune.no")
        is_exec = upn in [
            "camilla.dunsaed@kristiansand.kommune.no",
            "terje.fjellvang@kristiansand.kommune.no"
        ]
        har_full_tilgang = 1 if (is_frank or is_exec) else 0

        # RLS Rolle-mapping
        if har_full_tilgang == 1:
            rls_rolle = "Controller_Admin"
        elif sektor == "OPPVEKST" and niva == "NIVA1":
            rls_rolle = "Kommunalsjef_Oppvekst"
        elif sektor == "HELSE" and niva == "NIVA1":
            rls_rolle = "Kommunalsjef_Helse"
        elif sektor == "BYUTVIKLING" and niva == "NIVA1":
            rls_rolle = "Kommunalsjef_Byutvikling"
        elif sektor == "KULTUR" and niva == "NIVA1":
            rls_rolle = "Kommunalsjef_Kultur"
        elif sektor == "ORG_TEK" and niva == "NIVA1":
            rls_rolle = "Kommunalsjef_OrgTek"
        elif aid in ["2020", "4100-ENH-202", "4101-ENH-203", "4102-ENH-204"]:
            rls_rolle = "Enhetsleder_Skole"
        elif aid in ["2540", "5200-ENH-401", "5210-ENH-402", "5220-ENH-403", "5230-ENH-404"]:
            rls_rolle = "Enhetsleder_Boenhet"
        else:
            rls_rolle = "Dynamisk_Budsjettansvarlig_RLS"

        # Teams teamnavn og kanalnavn
        teams_team = teams_team_map.get(sektor, "Teams - Kristiansand Kommune")
        if niva == "CONTROLLER":
            teams_kanal = "Controller Hub & EPM Monitor"
        elif niva == "NIVA1":
            teams_kanal = "Ledergruppe & Sektorstyring"
        elif niva == "NIVA2":
            if sektor == "OPPVEKST":
                teams_kanal = "Skole- og Barnehageledelse"
            elif sektor == "HELSE":
                teams_kanal = "Institusjons- og Omsorgsledelse"
            elif sektor == "BYUTVIKLING":
                teams_kanal = "VAR & Byplan Seksjon"
            elif sektor == "ORG_TEK":
                teams_kanal = "Digitalisering & Fellestjenester"
            else:
                teams_kanal = "Områdeledelse & Fagstyring"
        elif niva == "NIVA3":
            if sektor == "OPPVEKST":
                teams_kanal = "Enhetsledere Skole"
            elif sektor == "HELSE":
                teams_kanal = "Virksomhetsledere Omsorg"
            elif sektor == "BYUTVIKLING":
                teams_kanal = "Enhetsledere Teknisk"
            elif sektor == "KULTUR":
                teams_kanal = "Enhetsledere Kultur & Bibliotek"
            elif sektor == "ORG_TEK":
                teams_kanal = "Drift & IKT-ledere"
            else:
                teams_kanal = "Enhetsledere & Driftsrapportering"
        else:
            teams_kanal = "Avdelingsrapportering"

        teams_url = f"https://app.powerbi.com/groups/me/reports/pbi_reporting_project?filter=Dim_Ansvar/ansvar_kode%20eq%20'{aid}'"

        rows.append({
            "bruker_upn": upn,
            "navn": r["navn"],
            "tittel": r["tittel"],
            "niva": niva,
            "niva_tekst": r["niva_tekst"],
            "sektor_kode": sektor,
            "kommunalsjefomrade": kom_omrade,
            "ansvar_kode": aid,
            "enhet_navn": r["enhet_navn"],
            "har_full_tilgang": har_full_tilgang,
            "rls_rolle": rls_rolle,
            "teams_team_navn": teams_team,
            "teams_kanal": teams_kanal,
            "teams_rapport_fane": "Power BI Månedsrapport",
            "powerbi_teams_app_url": teams_url,
            "delegeringsfullmakt_nok": float(r["delegeringsfullmakt_nok"]),
            "controller_navn": r["controller_navn"],
            "controller_epost": r["controller_epost"]
        })
    return rows

def export_json(path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(REGISTER, f, indent=2, ensure_ascii=False)
    print(f"✓ Eksportert JSON ({len(REGISTER)} poster): {path}")

def export_csv(path: Path):
    if not REGISTER:
        return
    fieldnames = list(REGISTER[0].keys())
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(REGISTER)
    print(f"✓ Eksportert CSV ({len(REGISTER)} poster): {path}")

def export_security_csv(path: Path, security_rows: list):
    if not security_rows:
        return
    fieldnames = list(security_rows[0].keys())
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(security_rows)
    print(f"✓ Eksportert Sikkerhet & RLS CSV ({len(security_rows)} poster): {path}")

def update_database(db_path: Path, security_rows: list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Dim_Budsjettansvarlige
    cur.execute("DROP TABLE IF EXISTS Dim_Budsjettansvarlige")
    cur.execute("""
        CREATE TABLE Dim_Budsjettansvarlige (
            ansvar_id TEXT PRIMARY KEY,
            navn TEXT NOT NULL,
            tittel TEXT NOT NULL,
            niva TEXT NOT NULL,
            niva_tekst TEXT NOT NULL,
            sektor_kode TEXT NOT NULL,
            sektor_navn TEXT NOT NULL,
            enhet_navn TEXT NOT NULL,
            kostra_funksjon TEXT NOT NULL,
            epost TEXT NOT NULL,
            telefon TEXT NOT NULL,
            kontorsted TEXT NOT NULL,
            delegeringsfullmakt_nok REAL NOT NULL,
            controller_navn TEXT NOT NULL,
            controller_epost TEXT NOT NULL,
            utsendte_rapporter TEXT NOT NULL,
            tilknyttet_mal TEXT NOT NULL,
            returkanal TEXT NOT NULL,
            returfrist TEXT NOT NULL
        )
    """)

    for r in REGISTER:
        cur.execute("""
            INSERT INTO Dim_Budsjettansvarlige VALUES (
                :ansvar_id, :navn, :tittel, :niva, :niva_tekst,
                :sektor_kode, :sektor_navn, :enhet_navn, :kostra_funksjon,
                :epost, :telefon, :kontorsted, :delegeringsfullmakt_nok,
                :controller_navn, :controller_epost, :utsendte_rapporter,
                :tilknyttet_mal, :returkanal, :returfrist
            )
        """, r)

    # 2. Dim_Sikkerhet_RLS
    cur.execute("DROP TABLE IF EXISTS Dim_Sikkerhet_RLS")
    cur.execute("""
        CREATE TABLE Dim_Sikkerhet_RLS (
            bruker_upn TEXT NOT NULL,
            navn TEXT NOT NULL,
            tittel TEXT NOT NULL,
            niva TEXT NOT NULL,
            niva_tekst TEXT NOT NULL,
            sektor_kode TEXT NOT NULL,
            kommunalsjefomrade TEXT NOT NULL,
            ansvar_kode TEXT NOT NULL,
            enhet_navn TEXT NOT NULL,
            har_full_tilgang INTEGER NOT NULL,
            rls_rolle TEXT NOT NULL,
            teams_team_navn TEXT NOT NULL,
            teams_kanal TEXT NOT NULL,
            teams_rapport_fane TEXT NOT NULL,
            powerbi_teams_app_url TEXT NOT NULL,
            delegeringsfullmakt_nok REAL NOT NULL,
            controller_navn TEXT NOT NULL,
            controller_epost TEXT NOT NULL,
            PRIMARY KEY (bruker_upn, ansvar_kode)
        )
    """)

    for s in security_rows:
        cur.execute("""
            INSERT INTO Dim_Sikkerhet_RLS VALUES (
                :bruker_upn, :navn, :tittel, :niva, :niva_tekst,
                :sektor_kode, :kommunalsjefomrade, :ansvar_kode, :enhet_navn,
                :har_full_tilgang, :rls_rolle, :teams_team_navn, :teams_kanal,
                :teams_rapport_fane, :powerbi_teams_app_url, :delegeringsfullmakt_nok,
                :controller_navn, :controller_epost
            )
        """, s)

    # 3. Sikre at Dim_Ansvar inneholder alle enheter
    existing_ansvar = set(r[0] for r in cur.execute("SELECT ansvar_kode FROM Dim_Ansvar").fetchall())
    for r in REGISTER:
        aid = r["ansvar_id"]
        if aid not in existing_ansvar:
            cur.execute("""
                INSERT OR IGNORE INTO Dim_Ansvar (ansvar_kode, enhet_navn, sektor, leder_stilling)
                VALUES (?, ?, ?, ?)
            """, (aid, r["enhet_navn"], r["sektor_navn"], r["tittel"]))

    conn.commit()
    count_b = cur.execute("SELECT COUNT(*) FROM Dim_Budsjettansvarlige").fetchone()[0]
    count_s = cur.execute("SELECT COUNT(*) FROM Dim_Sikkerhet_RLS").fetchone()[0]
    count_a = cur.execute("SELECT COUNT(*) FROM Dim_Ansvar").fetchone()[0]
    conn.close()
    print(f"✓ Opprettet tabell Dim_Budsjettansvarlige ({count_b} rader) og Dim_Sikkerhet_RLS ({count_s} rader), Dim_Ansvar har {count_a} rader.")

def main():
    json_path = ERP_DIR / "budsjettansvarlige_register.json"
    csv_path = ERP_DIR / "budsjettansvarlige_register.csv"
    sec_csv_path = ERP_DIR / "Dim_Sikkerhet_RLS.csv"

    security_rows = build_security_rls_register(REGISTER)

    export_json(json_path)
    export_csv(csv_path)
    export_security_csv(sec_csv_path, security_rows)

    if DB_PATH.exists():
        update_database(DB_PATH, security_rows)

if __name__ == "__main__":
    main()
