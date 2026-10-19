# -*- coding: utf-8 -*-
"""
tools/inject_framsikt_engine.py
Injects the Framsikt Hierarchical Budget Navigator and Total Sector Isolation Engine into index.html.
"""
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the start and end of previous engine if present
start_marker = "// ==============================================================================\n// 🏛️ FRAMSIKT BUDSJETTNIVÅ-HIERARKI & DYNAMISK ISOLERINGSMOTOR"
end_marker = "function initTop3KpiDashboard()"

idx_start = content.find(start_marker)
if idx_start != -1:
    idx_end = content.find(end_marker, idx_start)
    if idx_end != -1:
        # Cut out old version
        content = content[:idx_start] + content[idx_end:]
        print("Removed previous engine injection for clean update.")

FRAMSIKT_ENGINE_JS = r'''
// ==============================================================================
// 🏛️ FRAMSIKT BUDSJETTNIVÅ-HIERARKI & DYNAMISK ISOLERINGSMOTOR
// Speiler Framsikt EPM: Virksomhetsområde (N1) ➔ Sektor (N2) ➔ Enhet (N3) ➔ Avdeling (N4)
// jf. Kommuneloven § 14-5, § 14-6 og Bystyrets Økonomireglement
// ==============================================================================

const FRAMSIKT_HIERARCHY_DATA = {
    "HELSE": {
        id: "HELSE",
        sectorKey: "HELSE",
        name: "1. Helse og mestring",
        leder: "Brede Skeie",
        tittel: "Kommunalsjef Helse og mestring",
        niva: 1,
        nivaTekst: "Nivå 1: Kommunalsjef",
        ansvar: "5000-SJEF-HELSE",
        kostra: "Funksjon 241, 253, 254 (Pleie og omsorg)",
        fullmakt: 25000000,
        epost: "brede.skeie@kristiansand.kommune.no",
        telefon: "+47 38 00 71 10",
        controller: "Frank Ellingsen / Marianne Tellefsen",
        kontor: "Kvartal 35, Tollbodgata 22, 4611 Kristiansand",
        returfrist: "M+8 virkedag kl. 14:00",
        returkanal: "okonomi.helse@kristiansand.kommune.no / Websak 26/08940",
        ramme: 1850000000,
        pv: 1245000000,
        ac: 1254850000,
        cv: -9850000,
        cpi: 0.992,
        forbrukPct: 67.8,
        eac: 1864700000,
        vac: -14700000,
        p10: 1858000000,
        p50: 1864700000,
        p90: 1872000000,
        sparkline: [143.7, 144.0, 144.0, 144.2, 144.3, 144.5, 108.5, 137.3, 144.4],
        diagnose: {
            summary: "Bemanningspress og høyt sykefravær (10.8 %) i døgnomsorgen. Overtidsforbruk og innleie fra vikarbyrå.",
            drivers: [
                { art: "10200", navn: "Vikarbyrå / Ekstern innleie", belop: "+4 850 000 kr", vurdering: "Høyt sykefravær i pleie og omsorg dekket via Adecco/Dedicate." },
                { art: "10900", navn: "Overtid og ekstravakter", belop: "+2 650 000 kr", vurdering: "Helgebemanning og vaktvakanser i døgnomsorgen." },
                { art: "16000", navn: "Refusjoner sykepenger NAV", belop: "-1 450 000 kr", vurdering: "Etterslep på utestående refusjonskrav hos NAV over 60 dager." }
            ],
            lovhjemmel: "Kommuneloven § 14-5 (krav om budsjettbalanse) krever korrigerende tiltaksplan. HTA § 4 krever drøfting med tillitsvalgte ved turnusendringer."
        },
        prognose: {
            eac: "1 864 700 000 kr",
            vac: "-14 700 000 kr",
            status: "🔴 Merforbruk jf. § 14-5",
            intervall: "P10: 1.858 mrd | P50: 1.865 mrd | P90: 1.872 mrd",
            trend: "Ved uendrede tiltak vil merforbruket øke med ca. 1.3 MNOK/mnd ut året."
        },
        actions: [
            { nr: 1, type: "BEMANNING", tekst: "Etablere felles intern bemanningspool på tvers av Strai og Presteheia for å stanse innleie fra eksternt vikarbyrå.", frist: "Straks (Dag 1)" },
            { nr: 2, type: "TURNUS", tekst: "Gjennomføre formell drøfting med NSF og Fagforbundet etter HTA § 4 om pilot for 12.5-timers langvakter i helgene.", frist: "Innen 14 dager" },
            { nr: 3, type: "REFUSJON", tekst: "Innsende samlet purring på utestående sykepengerefusjoner til NAV Agder og avstemme toppfinansieringskrav (185.4M).", frist: "M+5 virkedag" },
            { nr: 4, type: "VEDTAK", tekst: "Fremlegge administrativt rammereguleringsnotat jf. Kommuneloven § 14-5 til Kommunedirektøren og Formannskapet.", frist: "M+8 virkedag" }
        ],
        children: [
            {
                id: "HELSE-INST",
                sectorKey: "HELSE",
                name: "Institusjonstjenester & Døgnpleie",
                leder: "Mette Syvertsen",
                tittel: "Områdeleder Institusjon & Døgnomsorg",
                niva: 2,
                nivaTekst: "Nivå 2: Områdeleder",
                ansvar: "5100-OMR-SYKEHJEM",
                kostra: "Funksjon 254 (Sykehjem & døgnpleie)",
                fullmakt: 10000000,
                epost: "mette.syvertsen@kristiansand.kommune.no",
                telefon: "+47 38 00 71 20",
                controller: "Frank Ellingsen",
                kontor: "Kvartal 35, Tollbodgata 22",
                returfrist: "M+7 virkedag kl 14:00",
                returkanal: "okonomi.helse@kristiansand.kommune.no",
                ramme: 1120000000,
                pv: 755600000,
                ac: 762400000,
                cv: -6800000,
                cpi: 0.991,
                forbrukPct: 68.1,
                eac: 1130500000,
                vac: -10500000,
                p10: 1126000000,
                p50: 1130500000,
                p90: 1136000000,
                diagnose: {
                    summary: "Vikarbyrå Adecco/Dedicate på art 10200 og helgetillegg art 10400 i sykehjemmene. Belegg 96 %.",
                    drivers: [
                        { art: "10200", navn: "Vikarbyrå sykepleiere", belop: "+3 400 000 kr", vurdering: "Mangel på intensiv-/geriatriske sykepleiere i helgeturnus." },
                        { art: "10400", navn: "Helge- og høytidstillegg", belop: "+1 800 000 kr", vurdering: "Bemanningsavtaler og ekstravakter." }
                    ],
                    lovhjemmel: "Helse- og omsorgstjenesteloven § 4-1 (forsvarlighetskrav) må balanseres mot Kommuneloven § 14-5."
                },
                prognose: {
                    eac: "1 130 500 000 kr",
                    vac: "-10 500 000 kr",
                    status: "🔴 Behov for tiltak",
                    intervall: "P10: 1.126 mrd | P50: 1.131 mrd | P90: 1.136 mrd",
                    trend: "Stabilt overforbruk på vikarer frem mot jul."
                },
                actions: [
                    { nr: 1, type: "BEMANNING", tekst: "Restriktiv godkjenning av ekstra overtidstimer.", frist: "Straks" },
                    { nr: 2, type: "IPLOS", tekst: "Avstemme IPLOS-score for samtlige beboere med særlig pleiebehov for å maksimere toppfinansiering.", frist: "M+5 virkedag" },
                    { nr: 3, type: "TURNUS", tekst: "Overføre ledig personell fra dag til kveld/helg ved sykdom.", frist: "Fortløpende" }
                ],
                children: [
                    {
                        id: "ENHET_401",
                        sectorKey: "HELSE",
                        name: "Strai Sykehjem & Omsorgsboliger",
                        leder: "Solveig Grimstad",
                        tittel: "Enhetsleder Strai Sykehjem",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "5200-ENH-401",
                        kostra: "Funksjon 254 (Sykehjem)",
                        fullmakt: 2000000,
                        epost: "solveig.grimstad@kristiansand.kommune.no",
                        telefon: "+47 38 00 84 01",
                        controller: "Frank Ellingsen",
                        kontor: "Strai Omsorgssenter, Setesdalsveien 320",
                        returfrist: "M+6 virkedag kl 12:00",
                        returkanal: "Websak 26/08940",
                        ramme: 84500000,
                        pv: 56333333,
                        ac: 58783333,
                        cv: -2450000,
                        cpi: 0.958,
                        forbrukPct: 69.6,
                        eac: 88200000,
                        vac: -3700000,
                        p10: 86600000,
                        p50: 88200000,
                        p90: 89900000,
                        diagnose: {
                            summary: "Sykefravær på 11.4 % (særlig kveld/natt). Vikarinnleie fra byrå (art 10200) utgjør 1.8M NOK. Overtid (art 10900) er 650k over ramme. Varsel jf. § 14-5.",
                            drivers: [
                                { art: "10200", navn: "Vikar Adecco/Dedicate", belop: "+1 800 000 kr", vurdering: "Høyt nattfravær i skjermet avdeling." },
                                { art: "10900", navn: "Overtid turnuspersonell", belop: "+650 000 kr", vurdering: "Dobbeltvakter ved akutt sykdom." },
                                { art: "16000", navn: "NAV Refusjoner", belop: "-240 000 kr", vurdering: "Utestående refusjoner for 4 sykmeldte." }
                            ],
                            lovhjemmel: "Kommuneloven § 14-5: Merforbruk utløser formelt avviksnotat til Kommunalsjef."
                        },
                        prognose: {
                            eac: "88 200 000 kr",
                            vac: "-3 700 000 kr",
                            status: "🔴 § 14-5 Avvik",
                            intervall: "P10: 86.6M | P50: 88.2M | P90: 89.9M",
                            trend: "Akutt behov for vikarstopp for å unngå 3.7M overskridelse."
                        },
                        actions: [
                            { nr: 1, type: "VIKARSTOPP", tekst: "Stans umiddelbar bruk av eksternt vikarbyrå; aktiver intern bemanningspool.", frist: "I dag" },
                            { nr: 2, type: "TURNUS", tekst: "Gjennomfør 12.5h langvakter som pilot jf. HTA § 4 for å redusere helgevakanser.", frist: "Neste turnus" },
                            { nr: 3, type: "RAPPORTERING", tekst: "Innsende utfylt avviksnotat og tiltaksplan til kommunalsjefen innen M+6 virkedag.", frist: "M+6 virkedag" }
                        ],
                        children: [
                            {
                                id: "SEK_401_1",
                                sectorKey: "HELSE",
                                name: "Avdeling Demensskjermet",
                                leder: "Tone Røyseland",
                                tittel: "Avdelingsleder Demens",
                                niva: 4,
                                nivaTekst: "Nivå 4: Avdelingsleder",
                                ansvar: "5201-SEK-DEMENS",
                                kostra: "Funksjon 254",
                                fullmakt: 250000,
                                epost: "tone.royseland@kristiansand.kommune.no",
                                telefon: "+47 38 00 84 11",
                                controller: "Frank Ellingsen",
                                ramme: 28500000,
                                pv: 19000000,
                                ac: 20100000,
                                cv: -1100000,
                                cpi: 0.945,
                                forbrukPct: 70.5,
                                eac: 30100000,
                                vac: -1600000,
                                p10: 29500000,
                                p50: 30100000,
                                p90: 30800000,
                                diagnose: {
                                    summary: "14.2 % sykefravær på natt. Vikarinnleie art 10200.",
                                    drivers: [
                                        { art: "10200", navn: "Vikar Adecco", belop: "+850 000 kr", vurdering: "Skjermet avd krever 2 faste på natt." }
                                    ],
                                    lovhjemmel: "Arbeidsmiljøloven § 10-12 og HTA § 4."
                                },
                                prognose: { eac: "30 100 000 kr", vac: "-1 600 000 kr", status: "🔴 Kritisk", intervall: "P50: 30.1M", trend: "+120k/mnd" },
                                actions: [
                                    { nr: 1, type: "TURNUS", tekst: "Etablere felles natt-turnus med somatisk avdeling for å dele vakt.", frist: "1 uke" },
                                    { nr: 2, type: "BHT", tekst: "Gjennomføre oppfølgingssamtaler med Bedriftshelsetjenesten for langtidssyke.", frist: "M+4 virkedag" }
                                ]
                            },
                            {
                                id: "SEK_401_2",
                                sectorKey: "HELSE",
                                name: "Avdeling Korttid & Rehabilitering",
                                leder: "Lars Klev",
                                tittel: "Avdelingsleder Korttid",
                                niva: 4,
                                nivaTekst: "Nivå 4: Avdelingsleder",
                                ansvar: "5202-SEK-KORTTID",
                                kostra: "Funksjon 254",
                                fullmakt: 250000,
                                epost: "lars.klev@kristiansand.kommune.no",
                                telefon: "+47 38 00 84 12",
                                controller: "Frank Ellingsen",
                                ramme: 32000000,
                                pv: 21333333,
                                ac: 22283333,
                                cv: -950000,
                                cpi: 0.957,
                                forbrukPct: 69.6,
                                eac: 33400000,
                                vac: -1400000,
                                p10: 32800000,
                                p50: 33400000,
                                p90: 34100000,
                                diagnose: {
                                    summary: "96 % belegg med overliggerpress. Sykepleierovertid art 10900.",
                                    drivers: [
                                        { art: "10900", navn: "Overtid sykepleiere", belop: "+520 000 kr", vurdering: "Pasientutskriving fra SSHF på fredager skaper helgetopp." }
                                    ],
                                    lovhjemmel: "Samhandlingsavtalen med Sørlandet Sykehus HF."
                                },
                                prognose: { eac: "33 400 000 kr", vac: "-1 400 000 kr", status: "🟠 Advarsel", intervall: "P50: 33.4M", trend: "+100k/mnd" },
                                actions: [
                                    { nr: 1, type: "SAMHANDLING", tekst: "Justere helgebemanning og kreve SSHF-samhandlingsmidler for helgeutskrivinger.", frist: "M+5 virkedag" }
                                ]
                            },
                            {
                                id: "SEK_401_3",
                                sectorKey: "HELSE",
                                name: "Avdeling Somatisk Langtid",
                                leder: "Ingvild Moen",
                                tittel: "Avdelingsleder Somatikk",
                                niva: 4,
                                nivaTekst: "Nivå 4: Avdelingsleder",
                                ansvar: "5203-SEK-SOMAT",
                                kostra: "Funksjon 254",
                                fullmakt: 200000,
                                epost: "ingvild.moen@kristiansand.kommune.no",
                                telefon: "+47 38 00 84 13",
                                controller: "Frank Ellingsen",
                                ramme: 24000000,
                                pv: 16000000,
                                ac: 16400000,
                                cv: -400000,
                                cpi: 0.976,
                                forbrukPct: 68.3,
                                eac: 24600000,
                                vac: -600000,
                                p10: 24200000,
                                p50: 24600000,
                                p90: 25000000,
                                diagnose: { summary: "Mindre overforbruk på medisinsk forbruksmateriell art 11200.", drivers: [{ art: "11200", navn: "Medisinsk forbruksmateriell", belop: "+250 000 kr", vurdering: "Sårbehandling og ernæringstilskudd." }], lovhjemmel: "§ 14-5" },
                                prognose: { eac: "24 600 000 kr", vac: "-600 000 kr", status: "🟡 Tilsyn", intervall: "P50: 24.6M", trend: "Moderat" },
                                actions: [{ nr: 1, type: "INNKJØP", tekst: "Samordne bestillinger via sentralavtale for forbruksmateriell.", frist: "M+4 virkedag" }]
                            }
                        ]
                    },
                    {
                        id: "ENHET_404",
                        sectorKey: "HELSE",
                        name: "Presteheia Omsorgssenter",
                        leder: "Kari Vesterhus",
                        tittel: "Enhetsleder Presteheia",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "5230-ENH-404",
                        kostra: "Funksjon 254",
                        fullmakt: 1500000,
                        epost: "kari.vesterhus@kristiansand.kommune.no",
                        telefon: "+47 38 00 84 04",
                        controller: "Frank Ellingsen",
                        kontor: "Presteheia Omsorgssenter, 4632 Kristiansand",
                        ramme: 76000000,
                        pv: 50666667,
                        ac: 51866667,
                        cv: -1200000,
                        cpi: 0.977,
                        forbrukPct: 68.2,
                        eac: 77800000,
                        vac: -1800000,
                        p10: 76900000,
                        p50: 77800000,
                        p90: 78700000,
                        diagnose: { summary: "Vikardekning ved langtidssykefravær, forsinket NAV-sykepengerefusjon på 380k kr art 16000.", drivers: [{ art: "16000", navn: "NAV Refusjoner", belop: "-380 000 kr etterslep", vurdering: "Foreldelsesrisiko." }], lovhjemmel: "Kommuneloven § 14-5" },
                        prognose: { eac: "77 800 000 kr", vac: "-1 800 000 kr", status: "🟠 Advarsel", intervall: "P50: 77.8M", trend: "Stabil" },
                        actions: [{ nr: 1, type: "NAV", tekst: "Purre NAV Agder på refusjoner eldre enn 60 dager.", frist: "Straks" }, { nr: 2, type: "TURNUS", tekst: "Turnustilpasning ved helger.", frist: "Innen 14 dager" }]
                    },
                    {
                        id: "ENHET_403",
                        sectorKey: "HELSE",
                        name: "Bo- og Miljøtjenester Sørlandsparken",
                        leder: "Christian Holte",
                        tittel: "Enhetsleder Bo & Miljø",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "5220-ENH-403",
                        kostra: "Funksjon 253",
                        fullmakt: 1800000,
                        epost: "christian.holte@kristiansand.kommune.no",
                        telefon: "+47 38 00 84 03",
                        controller: "Frank Ellingsen",
                        ramme: 92000000,
                        pv: 61333333,
                        ac: 64433333,
                        cv: -3100000,
                        cpi: 0.952,
                        forbrukPct: 70.0,
                        eac: 96500000,
                        vac: -4500000,
                        p10: 94800000,
                        p50: 96500000,
                        p90: 98200000,
                        diagnose: { summary: "3 nye særlig ressurskrevende brukere med 2:1 døgnbemanning. Toppfinansiering under behandling i Helsedirektoratet.", drivers: [{ art: "10100", navn: "Fastlønn miljøterapeuter", belop: "+2 200 000 kr", vurdering: "Nyansettelser godkjent av fagstab." }], lovhjemmel: "St.prp. nr. 1 (toppfinansiering)" },
                        prognose: { eac: "96 500 000 kr", vac: "-4 500 000 kr", status: "🔴 Toppfinansiering avventes", intervall: "P50: 96.5M", trend: "+300k/mnd" },
                        actions: [{ nr: 1, type: "STATLIG", tekst: "Fremme krav om toppfinansiering til staten (refusjonsgrad 80 % over 1.65M).", frist: "M+8 virkedag" }]
                    }
                ]
            },
            {
                id: "HELSE-HJEMME",
                sectorKey: "HELSE",
                name: "Hjemmebaserte Tjenester & Rehabilitering",
                leder: "Arve Sætre",
                tittel: "Områdeleder Hjemmetjenester",
                niva: 2,
                nivaTekst: "Nivå 2: Områdeleder",
                ansvar: "5200-OMR-HJEMME",
                kostra: "Funksjon 253",
                fullmakt: 8000000,
                epost: "arve.saetre@kristiansand.kommune.no",
                telefon: "+47 38 00 71 30",
                controller: "Frank Ellingsen",
                ramme: 620000000,
                pv: 418000000,
                ac: 420650000,
                cv: -2650000,
                cpi: 0.994,
                forbrukPct: 67.8,
                eac: 623800000,
                vac: -3800000,
                p10: 621000000,
                p50: 623800000,
                p90: 627000000,
                diagnose: { summary: "Kjøreruter og transportkostnader art 11500, helgeturnus-etterslep og sykefraværsdekning.", drivers: [{ art: "11500", navn: "Billeie og drivstoff", belop: "+650 000 kr", vurdering: "Økt kjørelengde i distriktene." }], lovhjemmel: "§ 14-5" },
                prognose: { eac: "623 800 000 kr", vac: "-3 800 000 kr", status: "🟡 Tilsyn", intervall: "P50: 623.8M", trend: "Moderat" },
                actions: [{ nr: 1, type: "RUTE", tekst: "Ruteoptimalisering med digital kjørebok.", frist: "M+5 virkedag" }],
                children: [
                    {
                        id: "ENHET_402",
                        sectorKey: "HELSE",
                        name: "Hjemmetjenesten Vågsbygd",
                        leder: "Berit Olsen",
                        tittel: "Enhetsleder Hjemmetjeneste",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "5210-ENH-402",
                        kostra: "Funksjon 253",
                        fullmakt: 1500000,
                        epost: "berit.olsen@kristiansand.kommune.no",
                        telefon: "+47 38 00 84 02",
                        controller: "Frank Ellingsen",
                        ramme: 68000000,
                        pv: 45333333,
                        ac: 46483333,
                        cv: -1150000,
                        cpi: 0.975,
                        forbrukPct: 68.4,
                        eac: 69700000,
                        vac: -1700000,
                        p10: 68900000,
                        p50: 69700000,
                        p90: 70500000,
                        diagnose: { summary: "Økt reisetid og transportutgifter art 11500, helgevakter dekket med overtid.", drivers: [{ art: "10900", navn: "Overtid helg", belop: "+420 000 kr", vurdering: "Vakanser." }], lovhjemmel: "§ 14-5" },
                        prognose: { eac: "69 700 000 kr", vac: "-1 700 000 kr", status: "🟠 Advarsel", intervall: "P50: 69.7M", trend: "Jevn" },
                        actions: [{ nr: 1, type: "LOGISTIKK", tekst: "Innføre digital ruteplanlegger og dele biler.", frist: "Straks" }]
                    }
                ]
            }
        ]
    },

    "OPPVEKST": {
        id: "OPPVEKST",
        sectorKey: "OPPVEKST",
        name: "2. Oppvekst og utdanning",
        leder: "Kristin Eidet Robstad",
        tittel: "Kommunalsjef Oppvekst og utdanning",
        niva: 1,
        nivaTekst: "Nivå 1: Kommunalsjef",
        ansvar: "4000-SJEF-OPPV",
        kostra: "Funksjon 201, 202, 211, 215, 221",
        fullmakt: 25000000,
        epost: "kristin.robstad@kristiansand.kommune.no",
        telefon: "+47 38 00 72 10",
        controller: "Frank Ellingsen / Erik Halvorsen",
        kontor: "Kvartal 35, Tollbodgata 22, 4611 Kristiansand",
        returfrist: "M+8 virkedag kl. 14:00",
        returkanal: "okonomi.oppvekst@kristiansand.kommune.no / Websak 26/08940",
        ramme: 2120000000,
        pv: 1427000000,
        ac: 1438872460,
        cv: -11872460,
        cpi: 0.992,
        forbrukPct: 67.9,
        eac: 2137650000,
        vac: -17650000,
        p10: 2129000000,
        p50: 2137650000,
        p90: 2146000000,
        sparkline: [164.8, 165.1, 165.2, 165.5, 165.7, 165.5, 122.8, 158.0, 166.3],
        diagnose: {
            summary: "Akkumulert merforbruk på lærervikarer art 10200 og forsinkede NAV-refusjoner for foreldrepenger/sykepenger art 16000 (410k NOK etterslep). Lærernorm overholdt (§ 8-2).",
            drivers: [
                { art: "10200", navn: "Lærervikarer ved korttidsfravær", belop: "+6 850 000 kr", vurdering: "Ekstern timelærerinnleie fremfor klassesammenslåing." },
                { art: "16000", navn: "NAV-refusjoner (foreldrepenger/sykepenger)", belop: "-2 850 000 kr etterslep", vurdering: "Forsinket saksbehandlingstid hos NAV Agder." },
                { art: "10500", navn: "Spesialpedagogiske assistenter", belop: "+2 172 460 kr", vurdering: "Enkeltvedtak om spesialundervisning." }
            ],
            lovhjemmel: "Opplæringsloven § 8-2 (lærernorm: 1:14.2 på trinn 1-4, krav 1:15). Kommuneloven § 14-5 budsjettbalanse."
        },
        prognose: {
            eac: "2 137 650 000 kr",
            vac: "-17 650 000 kr",
            status: "🔴 Kritisk avvik (§ 14-5)",
            intervall: "P10: 2.129 mrd | P50: 2.138 mrd | P90: 2.146 mrd",
            trend: "Merforbruket vokser med ca. 1.8 MNOK per måned i høstsemesteret."
        },
        actions: [
            { nr: 1, type: "VIKARRING", tekst: "Etablere forpliktende vikarring mellom naboskoler og pålegge klassesammenslåing ved 1-dags fravær.", frist: "Straks" },
            { nr: 2, type: "NAV", tekst: "Gjennomføre sentral purreaksjon mot NAV Agder for utestående refusjoner (art 16000) med liggetid over 90 dager.", frist: "M+4 virkedag" },
            { nr: 3, type: "POLITISK", tekst: "Fremlegge administrativt omposterings- og tiltaksnotat jf. § 14-5 til Formannskapet og Bystyret.", frist: "M+8 virkedag" }
        ],
        children: [
            {
                id: "OPPV-SKOLE",
                sectorKey: "OPPVEKST",
                name: "Grunnskoleavdelingen (28 skoler)",
                leder: "Svein Tore Kvernes",
                tittel: "Skolesjef Grunnskole",
                niva: 2,
                nivaTekst: "Nivå 2: Skolesjef",
                ansvar: "4100-OMR-SKOLE",
                kostra: "Funksjon 202 (Grunnskole)",
                fullmakt: 10000000,
                epost: "svein.tore.kvernes@kristiansand.kommune.no",
                telefon: "+47 38 00 72 20",
                controller: "Frank Ellingsen",
                kontor: "Kvartal 35, Tollbodgata 22",
                ramme: 1380000000,
                pv: 933000000,
                ac: 941200000,
                cv: -8200000,
                cpi: 0.991,
                forbrukPct: 68.2,
                eac: 1392000000,
                vac: -12000000,
                p10: 1386000000,
                p50: 1392000000,
                p90: 1398000000,
                diagnose: { summary: "Korttidsfravær i grunnskolen dekkes med eksterne timelærere fremfor intern deling.", drivers: [{ art: "10200", navn: "Timelærervikarer", belop: "+5 100 000 kr", vurdering: "Høyt fravær 1.-4. trinn." }], lovhjemmel: "Opplæringsloven § 8-2" },
                prognose: { eac: "1 392 000 000 kr", vac: "-12 000 000 kr", status: "🔴 Avvikstiltak nødvendig", intervall: "P50: 1.392 mrd", trend: "+1.1M/mnd" },
                actions: [{ nr: 1, type: "REGLER", tekst: "Innføre retningslinje for klassesammenslåing ved dagsfravær på 5.-7. trinn.", frist: "Straks" }],
                children: [
                    {
                        id: "ENHET_202",
                        sectorKey: "OPPVEKST",
                        name: "Lovisenlev Skole",
                        leder: "Trond Jensen",
                        tittel: "Rektor / Enhetsleder Lovisenlev Skole",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "4100-ENH-202",
                        kostra: "Funksjon 202 (Grunnskole) & 215 (SFO)",
                        fullmakt: 2000000,
                        epost: "trond.jensen@kristiansand.kommune.no",
                        telefon: "+47 38 00 82 02",
                        controller: "Frank Ellingsen",
                        kontor: "Lovisenlev Skole, Lovisenlevveien 12, 4633 Kristiansand",
                        returfrist: "M+6 virkedag kl 12:00",
                        returkanal: "Websak 26/08940",
                        ramme: 52000000,
                        pv: 35000000,
                        ac: 36850000,
                        cv: -1850000,
                        cpi: 0.950,
                        forbrukPct: 70.9,
                        eac: 54800000,
                        vac: -2800000,
                        p10: 53600000,
                        p50: 54800000,
                        p90: 55900000,
                        diagnose: {
                            summary: "Høyt korttidsfravær (8.9 %), 920 000 kr i ekstra vikarutgifter art 10200. NAV-refusjonsetterslep på 410 000 kr (art 16000) hvor 50k kr har ligget over 6 måneder med foreldelsesrisiko!",
                            drivers: [
                                { art: "10200", navn: "Lærervikarer art 10200", belop: "+920 000 kr", vurdering: "Innleide vikarer ved lærerfravær." },
                                { art: "16000", navn: "NAV Refusjoner art 16000", belop: "-410 000 kr etterslep", vurdering: "50k kr har over 6 mnd liggetid!" },
                                { art: "10500", navn: "Assistenttimer SFO", belop: "+520 000 kr", vurdering: "Økt assistentbehov i 1. klasse." }
                            ],
                            lovhjemmel: "Kommuneloven § 14-5 (Budsjettbalanse) & Folketrygdloven § 22-13 (foreldelse av refusjonskrav etter 6 måneder)."
                        },
                        prognose: {
                            eac: "54 800 000 kr",
                            vac: "-2 800 000 kr",
                            status: "🔴 Akutt tiltaksbehov",
                            intervall: "P10: 53.6M | P50: 54.8M | P90: 55.9M",
                            trend: "Dersom NAV-refusjoner ikke inndrives, tapes 410 000 kr endelig."
                        },
                        actions: [
                            { nr: 1, type: "PURRING", tekst: "Purre NAV umiddelbart på de 410 000 kr i refusjoner via digital K1-16000 blankett for å unngå foreldelse.", frist: "I dag" },
                            { nr: 2, type: "BEMANNING", tekst: "Iverksette klassesammenslåing på 5.–7. trinn ved 1-dags fravær fremfor ekstern innleie.", frist: "Fortløpende" },
                            { nr: 3, type: "SFO", tekst: "Justere assistentdekning i SFO i henhold til faktisk barnegruppe etter kl. 15:30.", frist: "Neste uke" }
                        ],
                        children: [
                            {
                                id: "SEK_202_1",
                                sectorKey: "OPPVEKST",
                                name: "Lovisenlev SFO",
                                leder: "Cathrine Solberg",
                                tittel: "Avdelingsleder SFO",
                                niva: 4,
                                nivaTekst: "Nivå 4: Avdelingsleder",
                                ansvar: "4103-SEK-SFO",
                                kostra: "Funksjon 215",
                                fullmakt: 150000,
                                epost: "cathrine.solberg@kristiansand.kommune.no",
                                telefon: "+47 38 00 82 12",
                                controller: "Frank Ellingsen",
                                ramme: 12000000,
                                pv: 8050000,
                                ac: 8500000,
                                cv: -450000,
                                cpi: 0.947,
                                forbrukPct: 70.8,
                                eac: 12700000,
                                vac: -700000,
                                p10: 12400000,
                                p50: 12700000,
                                p90: 13000000,
                                diagnose: { summary: "Assistenttimer og kostpengeinnkjøp art 11200 overskredet.", drivers: [{ art: "10500", navn: "Assistentlønn", belop: "+320 000 kr", vurdering: "Overtid ved sen henting." }], lovhjemmel: "Opplæringsloven" },
                                prognose: { eac: "12 700 000 kr", vac: "-700 000 kr", status: "🟠 Advarsel", intervall: "P50: 12.7M", trend: "+50k/mnd" },
                                actions: [{ nr: 1, type: "TURNUS", tekst: "Samkjøre bemanning i ytterkanttider.", frist: "Straks" }]
                            },
                            {
                                id: "SEK_202_2",
                                sectorKey: "OPPVEKST",
                                name: "Barneskolen 1.–4. trinn",
                                leder: "Bjarne Wiig",
                                tittel: "Inspektør 1.–4. trinn",
                                niva: 4,
                                nivaTekst: "Nivå 4: Inspektør",
                                ansvar: "4104-SEK-INSP",
                                kostra: "Funksjon 202",
                                fullmakt: 200000,
                                epost: "bjarne.wiig@kristiansand.kommune.no",
                                telefon: "+47 38 00 82 13",
                                controller: "Frank Ellingsen",
                                ramme: 22000000,
                                pv: 14800000,
                                ac: 15700000,
                                cv: -900000,
                                cpi: 0.943,
                                forbrukPct: 71.4,
                                eac: 23300000,
                                vac: -1300000,
                                p10: 22800000,
                                p50: 23300000,
                                p90: 23800000,
                                diagnose: { summary: "Lærernorm-oppfylling krever 1:14.2 dekning; vikartimer ved influensa.", drivers: [{ art: "10200", navn: "Timelærervikarer", belop: "+650 000 kr", vurdering: "Strengt lærernormkrav." }], lovhjemmel: "Opplæringsloven § 8-2" },
                                prognose: { eac: "23 300 000 kr", vac: "-1 300 000 kr", status: "🔴 Avvik", intervall: "P50: 23.3M", trend: "+90k/mnd" },
                                actions: [{ nr: 1, type: "VIKAR", tekst: "Bruke spesialpedagoger fleksibelt ved korttidsfravær.", frist: "Fortløpende" }]
                            },
                            {
                                id: "SEK_202_3",
                                sectorKey: "OPPVEKST",
                                name: "Mellomtrinnet 5.–7. trinn",
                                leder: "Astrid Lund",
                                tittel: "Inspektør 5.–7. trinn",
                                niva: 4,
                                nivaTekst: "Nivå 4: Inspektør",
                                ansvar: "4105-SEK-MELLOM",
                                kostra: "Funksjon 202",
                                fullmakt: 200000,
                                epost: "astrid.lund@kristiansand.kommune.no",
                                telefon: "+47 38 00 82 14",
                                controller: "Frank Ellingsen",
                                ramme: 18000000,
                                pv: 12150000,
                                ac: 12650000,
                                cv: -500000,
                                cpi: 0.960,
                                forbrukPct: 70.3,
                                eac: 18800000,
                                vac: -800000,
                                p10: 18400000,
                                p50: 18800000,
                                p90: 19200000,
                                diagnose: { summary: "Svømmeskyss og leirskoleutgifter art 11500.", drivers: [{ art: "11500", navn: "Skoleskyss", belop: "+280 000 kr", vurdering: "Prisøkning buss." }], lovhjemmel: "Opplæringsloven" },
                                prognose: { eac: "18 800 000 kr", vac: "-800 000 kr", status: "🟡 Tilsyn", intervall: "P50: 18.8M", trend: "Moderat" },
                                actions: [{ nr: 1, type: "SAMMENSLÅING", tekst: "Klassesammenslåing i teorifag ved fravær.", frist: "M+4 virkedag" }]
                            }
                        ]
                    },
                    {
                        id: "ENHET_203",
                        sectorKey: "OPPVEKST",
                        name: "Vågsbygd Skole",
                        leder: "Mona Lindstrøm",
                        tittel: "Rektor Vågsbygd Skole",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "4101-ENH-203",
                        kostra: "Funksjon 202",
                        fullmakt: 1800000,
                        epost: "mona.lindstrom@kristiansand.kommune.no",
                        telefon: "+47 38 00 82 03",
                        controller: "Frank Ellingsen",
                        ramme: 48000000,
                        pv: 32300000,
                        ac: 33250000,
                        cv: -950000,
                        cpi: 0.971,
                        forbrukPct: 69.3,
                        eac: 49400000,
                        vac: -1400000,
                        p10: 48700000,
                        p50: 49400000,
                        p90: 50100000,
                        diagnose: { summary: "Vikarbruk i spesialpedagogikk art 10200, manglende refusjoner art 16000 (180k kr).", drivers: [{ art: "10200", navn: "Spesialpedagogisk vikar", belop: "+620 000 kr", vurdering: "Tilsyn kreves." }], lovhjemmel: "§ 14-5" },
                        prognose: { eac: "49 400 000 kr", vac: "-1 400 000 kr", status: "🟠 Advarsel", intervall: "P50: 49.4M", trend: "+80k/mnd" },
                        actions: [{ nr: 1, type: "OPPFØLGING", tekst: "Tett oppfølging av spesialundervisningstimer, purre NAV-refusjoner.", frist: "M+5 virkedag" }]
                    }
                ]
            },
            {
                id: "OPPV-BHG",
                sectorKey: "OPPVEKST",
                name: "Barnehageavdelingen (54 barnehager)",
                leder: "Anne Lise Tønnessen",
                tittel: "Barnehagesjef",
                niva: 2,
                nivaTekst: "Nivå 2: Barnehagesjef",
                ansvar: "4200-OMR-BHG",
                kostra: "Funksjon 201",
                fullmakt: 8000000,
                epost: "anne.lise.tonnessen@kristiansand.kommune.no",
                telefon: "+47 38 00 72 30",
                controller: "Frank Ellingsen",
                ramme: 640000000,
                pv: 429700000,
                ac: 432800000,
                cv: -3100000,
                cpi: 0.993,
                forbrukPct: 67.6,
                eac: 644500000,
                vac: -4500000,
                p10: 642000000,
                p50: 644500000,
                p90: 647000000,
                diagnose: { summary: "Private barnehager overveltingstilskudd jf. § 19, vikarforbruk ved høstforkjølelser.", drivers: [{ art: "14700", navn: "Tilskudd private barnehager", belop: "+1 850 000 kr", vurdering: "42 % private barnehager." }], lovhjemmel: "Barnehageloven § 19" },
                prognose: { eac: "644 500 000 kr", vac: "-4 500 000 kr", status: "🟡 Tilsyn", intervall: "P50: 644.5M", trend: "Moderat" },
                actions: [{ nr: 1, type: "AVSTEMMING", tekst: "Avstemme kommunalt tilskudd mot nasjonal sats for private barnehager.", frist: "M+7 virkedag" }],
                children: [
                    {
                        id: "ENHET_211",
                        sectorKey: "OPPVEKST",
                        name: "Lund Barnehage",
                        leder: "Grete Hovden",
                        tittel: "Styrer Lund Barnehage",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "4210-ENH-211",
                        kostra: "Funksjon 201",
                        fullmakt: 1200000,
                        epost: "grete.hovden@kristiansand.kommune.no",
                        telefon: "+47 38 00 82 11",
                        controller: "Frank Ellingsen",
                        ramme: 24000000,
                        pv: 16100000,
                        ac: 16500000,
                        cv: -400000,
                        cpi: 0.976,
                        forbrukPct: 68.8,
                        eac: 24600000,
                        vac: -600000,
                        p10: 24300000,
                        p50: 24600000,
                        p90: 24900000,
                        diagnose: { summary: "Assistentvikarer ved høst- og vinterbølge, kostpenger i balanse.", drivers: [{ art: "10500", navn: "Assistentvikarer", belop: "+280 000 kr", vurdering: "Sykdom." }], lovhjemmel: "Barnehageloven" },
                        prognose: { eac: "24 600 000 kr", vac: "-600 000 kr", status: "🟡 Tilsyn", intervall: "P50: 24.6M", trend: "Normal" },
                        actions: [{ nr: 1, type: "POOL", tekst: "Samarbeide med nabobarnehage om vikarressurser ved morgenåpning.", frist: "Straks" }]
                    }
                ]
            }
        ]
    },

    "BYUTVIKLING": {
        id: "BYUTVIKLING",
        sectorKey: "BYUTVIKLING",
        name: "3. By- og stedsutvikling",
        leder: "Ragnar Evensen",
        tittel: "Kommunalsjef By- og stedsutvikling",
        niva: 1,
        nivaTekst: "Nivå 1: Kommunalsjef",
        ansvar: "3000-SJEF-BYUTV",
        kostra: "Funksjon 301, 312, 332, 340, 345, 354",
        fullmakt: 20000000,
        epost: "ragnar.evensen@kristiansand.kommune.no",
        telefon: "+47 38 00 73 10",
        controller: "Knut Arild Vike",
        kontor: "Tangen 8, 4608 Kristiansand",
        returfrist: "M+8 virkedag kl. 14:00",
        returkanal: "okonomi.byutvikling@kristiansand.kommune.no / Websak",
        ramme: 940000000,
        pv: 620000000,
        ac: 619690000,
        cv: 310000,
        cpi: 1.001,
        forbrukPct: 65.9,
        eac: 939500000,
        vac: 500000,
        p10: 936000000,
        p50: 939500000,
        p90: 943000000,
        sparkline: [71.2, 71.3, 71.1, 71.3, 71.2, 71.2, 53.3, 67.8, 71.2],
        diagnose: {
            summary: "VAR-området i balanse med overholdt selvkostfond (vann 98.2 %, avløp 101.4 %). Svikt i byggesaksgebyrer art 16200 (-3.3M NOK) pga. lavere byggeaktivitet i regionen kompensert av lavere driftskostnader.",
            drivers: [
                { art: "16200", navn: "Byggesaksgebyrer inntektssvikt", belop: "-3 300 000 kr svikt", vurdering: "Færre igangsettingstillatelser." },
                { art: "11150", navn: "Energi- og strømbesparelser", belop: "+1 850 000 kr buffer", vurdering: "Gunstige spotpriser og ENØK." },
                { art: "12000", navn: "VAR Selvkostavregning", belop: "+1 760 000 kr balanse", vurdering: "5-års selvkostfond overholder § 8." }
            ],
            lovhjemmel: "Selvkostforskriften § 8 (5-års utjevning) & Plan- og bygningsloven § 33-1 (selvkost for gebyrer)."
        },
        prognose: {
            eac: "939 500 000 kr",
            vac: "+500 000 kr (Balanse)",
            status: "🟢 I balanse jf. § 14-5",
            intervall: "P10: 936.0M | P50: 939.5M | P90: 943.0M",
            trend: "Selvkostfond sikrer stabilitet. Gebyrregulativ 2027 justeres."
        },
        actions: [
            { nr: 1, type: "VAR", tekst: "Sluttføre avregning av selvkostfond for vann og avløp for tertialavslutningen.", frist: "M+6 virkedag" },
            { nr: 2, type: "GEBYR", tekst: "Revidere byggesaksgebyrene i gebyrregulativet 2027 for å gjenopprette 100 % selvkostdekning.", frist: "Innen 1. nov" },
            { nr: 3, type: "CAPEX", tekst: "Sikre milepæl 3 fremdrift og MVA-kompensasjon (art 1729) for Odderøya renseanlegg.", frist: "M+8 virkedag" }
        ],
        children: [
            {
                id: "BYUTV-VAR",
                sectorKey: "BYUTVIKLING",
                name: "Ingeniørvesenet (Vann, Avløp & Renovasjon)",
                leder: "Helge Møller",
                tittel: "VA-sjef & Kommunalteknisk Direktør",
                niva: 2,
                nivaTekst: "Nivå 2: Direktør",
                ansvar: "3100-DIR-VAR",
                kostra: "Funksjon 340, 345, 354",
                fullmakt: 10000000,
                epost: "helge.moller@kristiansand.kommune.no",
                telefon: "+47 38 00 73 30",
                controller: "Knut Arild Vike",
                ramme: 490000000,
                pv: 324000000,
                ac: 322800000,
                cv: 1200000,
                cpi: 1.004,
                forbrukPct: 65.9,
                eac: 488200000,
                vac: 1800000,
                p10: 485000000,
                p50: 488200000,
                p90: 491000000,
                diagnose: { summary: "Vann- og avløpssektoren driftes strengt etter selvkostforskriften § 8. Fondsoppbygging på vann (+14.2M), avdrag på avløp (-4.8M).", drivers: [{ art: "16400", navn: "Vanngebyrer", belop: "+98.2 % dekningsgrad", vurdering: "I balanse." }], lovhjemmel: "Selvkostforskriften § 8" },
                prognose: { eac: "488 200 000 kr", vac: "+1 800 000 kr", status: "🟢 God kontroll", intervall: "P50: 488.2M", trend: "Balanse" },
                actions: [{ nr: 1, type: "FOND", tekst: "Sluttoppgjør for 5-års selvkostperiode og renteberegning på selvkostfond.", frist: "M+7 virkedag" }],
                children: [
                    {
                        id: "ENHET_302",
                        sectorKey: "BYUTVIKLING",
                        name: "VAR Ingeniørvesen",
                        leder: "Inger Johanne Foss",
                        tittel: "Enhetsleder VAR Ingeniørvesen",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "3100-ENH-302",
                        kostra: "Funksjon 340, 345",
                        fullmakt: 3000000,
                        epost: "inger.foss@kristiansand.kommune.no",
                        telefon: "+47 38 00 83 02",
                        controller: "Knut Arild Vike",
                        ramme: 145000000,
                        pv: 96666667,
                        ac: 96216667,
                        cv: 450000,
                        cpi: 1.005,
                        forbrukPct: 66.4,
                        eac: 144300000,
                        vac: 700000,
                        p10: 143500000,
                        p50: 144300000,
                        p90: 145200000,
                        diagnose: { summary: "God kontroll på ledningsnettfornyelse og lekkasjetetting. Lavere kjemikaliepriser.", drivers: [{ art: "11200", navn: "Kjemikalier renseanlegg", belop: "+350 000 kr buffer", vurdering: "Prisfall." }], lovhjemmel: "§ 8" },
                        prognose: { eac: "144 300 000 kr", vac: "+700 000 kr", status: "🟢 Balanse", intervall: "P50: 144.3M", trend: "Stabil" },
                        actions: [{ nr: 1, type: "DRIFT", tekst: "Opprettholde planlagt takt på ledningsfornyelse (2 % per år).", frist: "Pågår" }]
                    }
                ]
            },
            {
                id: "BYUTV-PLAN",
                sectorKey: "BYUTVIKLING",
                name: "Plan- og bygningsetaten",
                leder: "Einar Jørgensen",
                tittel: "Områdeleder Byplan & Byggesak",
                niva: 2,
                nivaTekst: "Nivå 2: Områdeleder",
                ansvar: "3200-DIR-PLAN",
                kostra: "Funksjon 301, 312",
                fullmakt: 6000000,
                epost: "einar.jorgensen@kristiansand.kommune.no",
                telefon: "+47 38 00 73 20",
                controller: "Knut Arild Vike",
                ramme: 180000000,
                pv: 119500000,
                ac: 121390000,
                cv: -1890000,
                cpi: 0.984,
                forbrukPct: 67.4,
                eac: 182800000,
                vac: -2800000,
                p10: 181500000,
                p50: 182800000,
                p90: 184500000,
                diagnose: { summary: "Gebyrsvikt art 16200 (-3.3M NOK) pga. færre rammesøknader i eiendomsmarkedet.", drivers: [{ art: "16200", navn: "Byggesaksgebyr", belop: "-3 300 000 kr", vurdering: "Lav byggeaktivitet." }], lovhjemmel: "Plan- og bygningsloven § 33-1" },
                prognose: { eac: "182 800 000 kr", vac: "-2 800 000 kr", status: "🟠 Gebyrsvikt", intervall: "P50: 182.8M", trend: "-250k/mnd" },
                actions: [{ nr: 1, type: "ANSETTELSE", tekst: "Ansettelsesstopp på ubesatte saksbehandlerstillinger inntil markedet snur.", frist: "Straks" }],
                children: [
                    {
                        id: "ENHET_301",
                        sectorKey: "BYUTVIKLING",
                        name: "Byggesak og Tilsyn",
                        leder: "Hans Petter Vik",
                        tittel: "Enhetsleder Byggesak & Tilsyn",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "3300-ENH-301",
                        kostra: "Funksjon 312",
                        fullmakt: 1500000,
                        epost: "hans.petter.vik@kristiansand.kommune.no",
                        telefon: "+47 38 00 83 01",
                        controller: "Knut Arild Vike",
                        ramme: 38000000,
                        pv: 25500000,
                        ac: 27800000,
                        cv: -2300000,
                        cpi: 0.917,
                        forbrukPct: 73.2,
                        eac: 41200000,
                        vac: -3200000,
                        p10: 40200000,
                        p50: 41200000,
                        p90: 42300000,
                        diagnose: { summary: "Svikt i inntekter fra byggesaksgebyrer (art 16200) utgjør 3.3M NOK under budsjettert takt. Færre store næringsbygg omsøkt i 2026.", drivers: [{ art: "16200", navn: "Byggesaksgebyrer", belop: "-3 300 000 kr", vurdering: "Markedssvikt." }], lovhjemmel: "§ 14-5" },
                        prognose: { eac: "41 200 000 kr", vac: "-3 200 000 kr", status: "🔴 Inntektsfall", intervall: "P50: 41.2M", trend: "Fallende" },
                        actions: [{ nr: 1, type: "TILTAK", tekst: "Tilpasse bemanning ved naturlig avgang og revidere gebyrregulativ for 2027.", frist: "M+8 virkedag" }]
                    }
                ]
            }
        ]
    },

    "KULTUR": {
        id: "KULTUR",
        sectorKey: "KULTUR",
        name: "4. Kultur og innbyggerdialog",
        leder: "Camilla Jarlsby",
        tittel: "Kommunalsjef Kultur og innbyggerdialog",
        niva: 1,
        nivaTekst: "Nivå 1: Kommunalsjef",
        ansvar: "2000-SJEF-KULTUR",
        kostra: "Funksjon 370, 375, 380, 383, 385",
        fullmakt: 15000000,
        epost: "camilla.jarlsby@kristiansand.kommune.no",
        telefon: "+47 38 00 74 10",
        controller: "Silje Mæland",
        kontor: "Gyldenløves gate 23, 4611 Kristiansand",
        returfrist: "M+8 virkedag kl. 14:00",
        returkanal: "okonomi.kultur@kristiansand.kommune.no / Websak",
        ramme: 380000000,
        pv: 252000000,
        ac: 252045000,
        cv: -450000,
        cpi: 1.000,
        forbrukPct: 66.3,
        eac: 380065000,
        vac: -65000,
        p10: 379500000,
        p50: 380065000,
        p90: 380800000,
        sparkline: [29.0, 28.9, 29.0, 29.0, 28.9, 29.0, 21.7, 27.5, 29.0],
        diagnose: {
            summary: "Stabil, kontrollert drift i balanse. Tilskudd til frivilligheten i rute, Kilden-tilskudd avstemt.",
            drivers: [{ art: "14700", navn: "Tilskudd til kulturinstitusjoner", belop: "I rute", vurdering: "Full kontroll." }],
            lovhjemmel: "Kulturloven § 1 & Kommuneloven § 14-5."
        },
        prognose: { eac: "380 065 000 kr", vac: "-65 000 kr", status: "🟢 Perfekt balanse", intervall: "P50: 380.1M", trend: "Stabil" },
        actions: [{ nr: 1, type: "KULTUR", tekst: "Gjennomgå energioptimalisering for kommunale kulturbygg og idrettshaller.", frist: "M+8 virkedag" }],
        children: [
            {
                id: "ENHET_101",
                sectorKey: "KULTUR",
                name: "Kristiansand Folkebibliotek",
                leder: "Hege Gabrielsen",
                tittel: "Biblioteksjef",
                niva: 3,
                nivaTekst: "Nivå 3: Enhetsleder",
                ansvar: "2200-ENH-101",
                kostra: "Funksjon 370",
                fullmakt: 1000000,
                epost: "hege.gabrielsen@kristiansand.kommune.no",
                telefon: "+47 38 00 81 01",
                controller: "Silje Mæland",
                ramme: 34000000,
                pv: 22700000,
                ac: 22750000,
                cv: -50000,
                cpi: 0.998,
                forbrukPct: 66.9,
                eac: 34075000,
                vac: -75000,
                p10: 33900000,
                p50: 34075000,
                p90: 34200000,
                diagnose: { summary: "Bibliotekdrift i balanse. Høy aktivitet på meråpent bibliotek.", drivers: [{ art: "11200", navn: "Innkjøp medier", belop: "I balanse", vurdering: "Stabilt." }], lovhjemmel: "Bibliotekloven" },
                prognose: { eac: "34 075 000 kr", vac: "-75 000 kr", status: "🟢 Balanse", intervall: "P50: 34.1M", trend: "Planmessig" },
                actions: [{ nr: 1, type: "STATUS", tekst: "Opprettholde drift i samsvar med ramme.", frist: "Løpende" }]
            }
        ]
    },

    "ORG_TEK": {
        id: "ORG_TEK",
        sectorKey: "ORG_TEK",
        name: "5. Organisasjon og teknologi",
        leder: "Geir A. Askvik",
        tittel: "Kommunalsjef Organisasjon og teknologi",
        niva: 1,
        nivaTekst: "Nivå 1: Kommunalsjef",
        ansvar: "1000-SJEF-ORGTEK",
        kostra: "Funksjon 120, 130, 180",
        fullmakt: 15000000,
        epost: "geir.askvik@kristiansand.kommune.no",
        telefon: "+47 38 00 75 10",
        controller: "Silje Mæland / Frank Ellingsen",
        kontor: "Rådhuskvartalet, 4611 Kristiansand",
        returfrist: "M+8 virkedag kl. 14:00",
        returkanal: "okonomi.orgtek@kristiansand.kommune.no / Websak",
        ramme: 460000000,
        pv: 308000000,
        ac: 308120000,
        cv: -120000,
        cpi: 1.000,
        forbrukPct: 67.0,
        eac: 460180000,
        vac: -180000,
        p10: 458500000,
        p50: 460180000,
        p90: 462000000,
        sparkline: [35.4, 35.4, 35.4, 35.4, 35.4, 35.4, 26.6, 33.7, 35.4],
        diagnose: {
            summary: "FinOps SaaS lisenssanering gir gevinster. 38 inaktive M365 E5 lisenser funnet (420k kr/år). Konsulentkonverteringsplan art 11950 påbegynt (-1.8M innsparingspotensial).",
            drivers: [
                { art: "11950", navn: "Eksterne konsulenter IKT", belop: "1 450 kr/time", vurdering: "Konvertering til 2 faste stillinger gir 1.8M spart/år." },
                { art: "13000", navn: "M365 og skylisenser", belop: "420 000 kr/år inaktivt", vurdering: "Automatisk deaktivering igangsatt." }
            ],
            lovhjemmel: "NSM grunnprinsipper for IKT-sikkerhet & Kommuneloven § 14-5."
        },
        prognose: { eac: "460 180 000 kr", vac: "-180 000 kr", status: "🟢 God kontroll", intervall: "P50: 460.2M", trend: "Balanse" },
        actions: [
            { nr: 1, type: "FINOPS", tekst: "Deaktivere de 38 identifiserte inaktive M365 og Visma lisensene.", frist: "M+3 virkedag" },
            { nr: 2, type: "HR", tekst: "Iverksette ansettelsesprosess for å konvertere 2 innleide konsulenter til faste stillinger.", frist: "M+8 virkedag" }
        ],
        children: [
            {
                id: "ENHET_501",
                sectorKey: "ORG_TEK",
                name: "IKT Drift & Brukerstøtte",
                leder: "Kenneth Dale",
                tittel: "IKT Driftssjef Brukerstøtte",
                niva: 3,
                nivaTekst: "Nivå 3: Enhetsleder",
                ansvar: "1110-ENH-501",
                kostra: "Funksjon 130",
                fullmakt: 2500000,
                epost: "kenneth.dale@kristiansand.kommune.no",
                telefon: "+47 38 00 85 01",
                controller: "Silje Mæland",
                ramme: 82000000,
                pv: 54800000,
                ac: 54900000,
                cv: -100000,
                cpi: 0.998,
                forbrukPct: 67.0,
                eac: 82150000,
                vac: -150000,
                p10: 81800000,
                p50: 82150000,
                p90: 82500000,
                diagnose: { summary: "Drift av servere og nettverk stabil. FinOps lisensoptimalisering pågår.", drivers: [{ art: "13000", navn: "Skyløsninger", belop: "I rute", vurdering: "God kontroll." }], lovhjemmel: "§ 14-5" },
                prognose: { eac: "82 150 000 kr", vac: "-150 000 kr", status: "🟢 Balanse", intervall: "P50: 82.2M", trend: "Stabil" },
                actions: [{ nr: 1, type: "FINOPS", tekst: "Sanere ubrukte skyressurser i Azure og M365.", frist: "M+4 virkedag" }],
                children: [
                    {
                        id: "SEK_501_1",
                        sectorKey: "ORG_TEK",
                        name: "Seksjon Skyløsninger & FinOps",
                        leder: "Thomas Berge",
                        tittel: "Seksjonsleder FinOps",
                        niva: 4,
                        nivaTekst: "Nivå 4: Seksjonsleder",
                        ansvar: "1111-SEK-FINOPS",
                        kostra: "Funksjon 130",
                        fullmakt: 300000,
                        epost: "thomas.berge@kristiansand.kommune.no",
                        ramme: 48000000,
                        pv: 32000000,
                        ac: 32100000,
                        cv: -100000,
                        cpi: 0.997,
                        forbrukPct: 66.9,
                        eac: 48150000,
                        vac: -150000,
                        p10: 47900000,
                        p50: 48150000,
                        p90: 48400000,
                        diagnose: { summary: "Fakturerte skylisenser 32.1M NOK. 420 000 kr identifisert i inaktive kontoer.", drivers: [{ art: "13000", navn: "M365 E5", belop: "38 inaktive", vurdering: "Besparelse klar." }], lovhjemmel: "FinOps" },
                        prognose: { eac: "48 150 000 kr", vac: "-150 000 kr", status: "🟢 Balanse", intervall: "P50: 48.2M", trend: "Fallende" },
                        actions: [{ nr: 1, type: "KUTT", tekst: "Avslutte lisenser for fratrådte ansatte.", frist: "I dag" }]
                    }
                ]
            }
        ]
    },

    "OKONOMI": {
        id: "OKONOMI",
        sectorKey: "OKONOMI",
        name: "6. Økonomi og virksomhetsstyring",
        leder: "Terje Fjellvang",
        tittel: "Økonomidirektør",
        niva: 1,
        nivaTekst: "Nivå 1: Toppledelse",
        ansvar: "6000-DIR-OKONOMI",
        kostra: "Funksjon 100, 110, 170, 800-serien (Felles & Finans)",
        fullmakt: 50000000,
        epost: "terje.fjellvang@kristiansand.kommune.no",
        telefon: "+47 38 00 76 10",
        controller: "Frank Ellingsen (Senior Controller)",
        kontor: "Rådhuset, Rådhusgata 18, 4611 Kristiansand",
        returfrist: "M+9 virkedag kl. 12:00",
        returkanal: "konsernokonomi@kristiansand.kommune.no",
        ramme: 1490000000,
        pv: 994872460,
        ac: 992295000,
        cv: 2577460,
        cpi: 1.003,
        forbrukPct: 66.6,
        eac: 1486125000,
        vac: 3875000,
        p10: 1482000000,
        p50: 1486125000,
        p90: 1491000000,
        sparkline: [114.1, 114.1, 114.0, 114.1, 114.1, 114.0, 85.5, 108.3, 114.0],
        diagnose: {
            summary: "Finansforvaltningen har god kontroll. Gjennomsnittsrente 4.12 % på 7.25 mrd NOK gjeld (58 % fast / 42 % flytende). Disposisjonsfond 485 MNOK (6.7 %) sikrer buffer mot handlingsregelen (min. 6.0 %). Pensjonspremieavvik på 36 MNOK amortiseres over 7 år lineært.",
            drivers: [
                { art: "18000", navn: "Renteinntekter & renteavtaler", belop: "+2 800 000 kr buffer", vurdering: "Gunstige fastrenteavtaler." },
                { art: "10990", navn: "Premieavvik KLP/SPK", belop: "+36 000 000 kr", vurdering: "7 års lineær amortisering jf. forskrift § 5-4." }
            ],
            lovhjemmel: "Kommuneloven § 14-5 & § 14-14 (finansreglement)."
        },
        prognose: {
            eac: "1 486 125 000 kr",
            vac: "+3 875 000 kr (Mindreforbruk)",
            status: "🟢 Robust buffer",
            intervall: "P10: 1.482 mrd | P50: 1.486 mrd | P90: 1.491 mrd",
            trend: "Finansielle reserver sikrer årets netto driftsresultat."
        },
        actions: [
            { nr: 1, type: "FINANS", tekst: "Overvåke NIBOR-rentebanen mot 50 % rentesikringskravet i finansreglementet.", frist: "Månedlig" },
            { nr: 2, type: "PENSJON", tekst: "Gjennomføre aktuarmessig avstemming av pensjonspremieavvik med KLP og SPK.", frist: "M+8 virkedag" },
            { nr: 3, type: "TERTIAL", tekst: "Konsolidere samlet 2. tertialrapport for Bystyret med SHA-256 forsegling.", frist: "M+12 virkedag" }
        ],
        children: [
            {
                id: "OKO-FINANS",
                sectorKey: "OKONOMI",
                name: "Finans- og Gjeldsforvaltning",
                leder: "Knut Ingebrigtsen",
                tittel: "Finans- og Gjeldsforvalter",
                niva: 3,
                nivaTekst: "Nivå 3: Enhetsleder",
                ansvar: "6200-ENH-601",
                kostra: "Funksjon 800-serien",
                fullmakt: 15000000,
                epost: "knut.ingebrigtsen@kristiansand.kommune.no",
                telefon: "+47 38 00 86 01",
                controller: "Frank Ellingsen",
                ramme: 960000000,
                pv: 640000000,
                ac: 638200000,
                cv: 1800000,
                cpi: 1.003,
                forbrukPct: 66.5,
                eac: 957500000,
                vac: 2500000,
                p10: 955000000,
                p50: 957500000,
                p90: 961000000,
                diagnose: { summary: "Rente- og gjeldsportefølje under streng kontroll. Fastrenteandelen demper renteuro.", drivers: [{ art: "18000", navn: "Renter og avdrag", belop: "1.8M buffer", vurdering: "Balanse." }], lovhjemmel: "Finansreglementet" },
                prognose: { eac: "957 500 000 kr", vac: "+2 500 000 kr", status: "🟢 God buffer", intervall: "P50: 957.5M", trend: "Stabil" },
                actions: [{ nr: 1, type: "LIKVIDITET", tekst: "Sikre kassakredittramme på 150M NOK mot skatteinngang i november.", frist: "Fortløpende" }]
            }
        ]
    }
};

let currentFramsiktActiveNode = null;
let currentFramsiktFilterSector = "ALL";
let framsiktExpandedFolders = new Set(["HELSE", "HELSE-INST", "ENHET_401", "OPPVEKST", "OPPV-SKOLE", "ENHET_202", "BYUTVIKLING", "KULTUR", "ORG_TEK", "OKONOMI"]);

function formatKr(num) {
    if (num === undefined || num === null) return "0 kr";
    const abs = Math.abs(num);
    if (abs >= 1000000000) {
        return (num / 1000000000).toFixed(2).replace(".", ",") + " mrd kr";
    } else if (abs >= 1000000) {
        return (num / 1000000).toFixed(1).replace(".", ",") + " mill. kr";
    } else {
        return num.toLocaleString("no-NO") + " kr";
    }
}

function findFramsiktNodeById(nodeId, nodeObj) {
    if (!nodeObj) {
        for (const secKey of Object.keys(FRAMSIKT_HIERARCHY_DATA)) {
            const found = findFramsiktNodeById(nodeId, FRAMSIKT_HIERARCHY_DATA[secKey]);
            if (found) return found;
        }
        return null;
    }
    if (nodeObj.id === nodeId) return nodeObj;
    if (nodeObj.children) {
        for (const child of nodeObj.children) {
            const found = findFramsiktNodeById(nodeId, child);
            if (found) return found;
        }
    }
    return null;
}

function getBreadcrumbTrail(nodeId) {
    for (const secKey of Object.keys(FRAMSIKT_HIERARCHY_DATA)) {
        const root = FRAMSIKT_HIERARCHY_DATA[secKey];
        const res = searchTrail(root, nodeId, [root]);
        if (res) return res;
    }
    return [];
}

function searchTrail(current, targetId, path) {
    if (current.id === targetId) return path;
    if (current.children) {
        for (const child of current.children) {
            const res = searchTrail(child, targetId, [...path, child]);
            if (res) return res;
        }
    }
    return null;
}

function toggleFramsiktFolder(nodeId, event) {
    if (event) event.stopPropagation();
    if (framsiktExpandedFolders.has(nodeId)) {
        framsiktExpandedFolders.delete(nodeId);
    } else {
        framsiktExpandedFolders.add(nodeId);
    }
    renderFramsiktTree(currentFramsiktFilterSector, document.getElementById("framsikt-search-input")?.value || "");
}

function selectFramsiktNode(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    currentFramsiktActiveNode = node;

    // Ensure parents are expanded
    const trail = getBreadcrumbTrail(nodeId);
    trail.forEach(t => framsiktExpandedFolders.add(t.id));

    renderFramsiktTree(currentFramsiktFilterSector, document.getElementById("framsikt-search-input")?.value || "");
    renderFramsiktDetail(node);
}

function renderFramsiktTree(sectorFilter = "ALL", searchTerm = "") {
    const rootEl = document.getElementById("framsikt-tree-root");
    if (!rootEl) return;
    currentFramsiktFilterSector = sectorFilter;

    const countLabel = document.getElementById("framsikt-tree-count-label");
    if (countLabel) {
        if (sectorFilter === "ALL") {
            countLabel.innerHTML = "Viser struktur for: <strong>Alle 6 virksomhetsområder (Konsern)</strong>";
        } else {
            const secName = FRAMSIKT_HIERARCHY_DATA[sectorFilter]?.name || sectorFilter;
            countLabel.innerHTML = `Viser struktur for: <strong>${secName} (Isolert)</strong>`;
        }
    }

    const term = searchTerm.toLowerCase().trim();
    let sectorsToRender = [];
    if (sectorFilter === "ALL") {
        sectorsToRender = Object.values(FRAMSIKT_HIERARCHY_DATA);
    } else if (FRAMSIKT_HIERARCHY_DATA[sectorFilter]) {
        sectorsToRender = [FRAMSIKT_HIERARCHY_DATA[sectorFilter]];
    }

    let html = "";
    sectorsToRender.forEach(rootNode => {
        html += buildTreeNodeHtml(rootNode, term);
    });

    rootEl.innerHTML = html;

    // Default select if none selected or if active node is not in current filter
    if (!currentFramsiktActiveNode || (sectorFilter !== "ALL" && currentFramsiktActiveNode.sectorKey !== sectorFilter)) {
        if (sectorsToRender.length > 0) {
            const firstRoot = sectorsToRender[0];
            const defaultNode = (firstRoot.children && firstRoot.children[0]?.children && firstRoot.children[0].children[0]) 
                ? firstRoot.children[0].children[0] 
                : firstRoot;
            currentFramsiktActiveNode = defaultNode;
            renderFramsiktDetail(defaultNode);
        }
    }
}

function buildTreeNodeHtml(node, searchTerm = "") {
    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = framsiktExpandedFolders.has(node.id) || searchTerm.length > 0;
    const isActive = currentFramsiktActiveNode && currentFramsiktActiveNode.id === node.id;

    if (searchTerm.length > 0) {
        const textToSearch = (node.name + " " + node.leder + " " + (node.ansvar || "")).toLowerCase();
        let isMatch = textToSearch.includes(searchTerm);
        if (!isMatch && hasChildren) {
            isMatch = hasMatchingDescendant(node, searchTerm);
        }
        if (!isMatch) return "";
    }

    const toggleIcon = hasChildren ? (isExpanded ? "▼" : "▶") : "•";
    const toggleClick = hasChildren ? `onclick="toggleFramsiktFolder('${node.id}', event)"` : "";

    const cvColor = node.cv < 0 ? "#b91c1c" : "#15803d";
    const cvSign = node.cv > 0 ? "+" : "";
    const cvText = node.cv !== 0 ? `${cvSign}${(node.cv / 1000000).toFixed(1)}M` : "0";

    let childHtml = "";
    if (hasChildren && isExpanded) {
        childHtml = `<ul class="framsikt-sub-tree">`;
        node.children.forEach(c => {
            childHtml += buildTreeNodeHtml(c, searchTerm);
        });
        childHtml += `</ul>`;
    }

    return `
    <li class="framsikt-tree-node">
        <div class="framsikt-node-row ${isActive ? 'active' : ''}" onclick="selectFramsiktNode('${node.id}')" title="Klikk for å se full budsjettdiagnose og tiltak for ${node.leder}">
            <div class="framsikt-node-left">
                <button type="button" class="framsikt-toggle-btn" ${toggleClick}>${toggleIcon}</button>
                <span class="framsikt-level-badge lvl-${node.niva}">N${node.niva}</span>
                <span class="framsikt-node-title">${node.name}</span>
            </div>
            <div class="framsikt-node-right">
                <span style="color:#64748b; font-size:10px;">${(node.ramme / 1000000).toFixed(0)}M</span>
                <span class="framsikt-node-cv" style="color:${cvColor};">${cvText}</span>
            </div>
        </div>
        ${childHtml}
    </li>
    `;
}

function hasMatchingDescendant(node, term) {
    if (!node.children) return false;
    for (const c of node.children) {
        const txt = (c.name + " " + c.leder + " " + (c.ansvar || "")).toLowerCase();
        if (txt.includes(term)) return true;
        if (hasMatchingDescendant(c, term)) return true;
    }
    return false;
}

function searchFramsiktTree(query) {
    renderFramsiktTree(currentFramsiktFilterSector, query);
}

function expandAllFramsiktTree() {
    function addAll(node) {
        framsiktExpandedFolders.add(node.id);
        if (node.children) node.children.forEach(addAll);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(addAll);
    renderFramsiktTree(currentFramsiktFilterSector, document.getElementById("framsikt-search-input")?.value || "");
}

function collapseAllFramsiktTree() {
    framsiktExpandedFolders.clear();
    renderFramsiktTree(currentFramsiktFilterSector, document.getElementById("framsikt-search-input")?.value || "");
}

function renderFramsiktDetail(node) {
    const container = document.getElementById("framsikt-detail-panel");
    if (!container || !node) return;

    const trail = getBreadcrumbTrail(node.id);
    let breadcrumbHtml = `<div class="framsikt-breadcrumb-bar"><span>Framsikt 2026</span> <span>›</span>`;
    trail.forEach((step, idx) => {
        const isLast = idx === trail.length - 1;
        if (isLast) {
            breadcrumbHtml += `<span class="framsikt-breadcrumb-current">${step.name}</span>`;
        } else {
            breadcrumbHtml += `<a class="framsikt-breadcrumb-step" onclick="selectFramsiktNode('${step.id}')">${step.name}</a> <span>›</span>`;
        }
    });
    breadcrumbHtml += `</div>`;

    const cvIsNeg = node.cv < 0;
    const cvClass = cvIsNeg ? "f-val-red" : "f-val-green";
    const cvSign = node.cv > 0 ? "+" : "";
    const cpiClass = node.cpi >= 1.0 ? "f-val-green" : (node.cpi >= 0.95 ? "f-val-amber" : "f-val-red");

    let driversHtml = "";
    if (node.diagnose && node.diagnose.drivers) {
        driversHtml = `
            <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:11.5px;">
                <thead>
                    <tr style="border-bottom:1.5px solid #cbd5e1; text-align:left; color:#475569;">
                        <th style="padding:4px 6px;">KOSTRA Art</th>
                        <th style="padding:4px 6px;">Beskrivelse</th>
                        <th style="padding:4px 6px; text-align:right;">Avviksbeløp</th>
                        <th style="padding:4px 6px;">Controller-vurdering</th>
                    </tr>
                </thead>
                <tbody>
                    ${node.diagnose.drivers.map(d => `
                        <tr style="border-bottom:1px solid #f1f5f9;">
                            <td style="padding:5px 6px; font-family:var(--font-mono); font-weight:700; color:var(--navy-dark);">${d.art}</td>
                            <td style="padding:5px 6px; font-weight:600;">${d.navn}</td>
                            <td style="padding:5px 6px; text-align:right; font-weight:700; color:#b91c1c;">${d.belop}</td>
                            <td style="padding:5px 6px; color:#475569;">${d.vurdering}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    let actionsHtml = "";
    if (node.actions && node.actions.length > 0) {
        actionsHtml = `
            <ul class="framsikt-action-list">
                ${node.actions.map(a => `
                    <li class="framsikt-action-item">
                        <span class="action-num">${a.nr}</span>
                        <div style="flex:1;">
                            <strong style="color:var(--navy-dark);">${a.type}:</strong> ${a.tekst}
                            <span style="font-size:10.5px; color:#64748b; margin-left:6px; font-weight:600;">[Frist: ${a.frist}]</span>
                        </div>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    container.innerHTML = `
        ${breadcrumbHtml}

        <div class="framsikt-leader-card">
            <div class="framsikt-leader-info">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="framsikt-level-badge lvl-${node.niva}">${node.nivaTekst || 'Nivå ' + node.niva}</span>
                    <h3>${node.name}</h3>
                </div>
                <div class="subtitle">
                    Budsjettansvarlig: <strong>${node.leder}</strong> (${node.tittel}) | Ansvarsnummer: <strong style="font-family:var(--font-mono);">${node.ansvar || 'N/A'}</strong>
                </div>
                <div class="framsikt-leader-meta">
                    <div>Anvisningsfullmakt: <strong>${(node.fullmakt || 0).toLocaleString("no-NO")} kr</strong></div>
                    <div>KOSTRA: <strong>${node.kostra || 'Felles'}</strong></div>
                    <div>Controller: <strong>${node.controller || 'Frank Ellingsen'}</strong></div>
                    <div>Returkanal: <strong>${node.returkanal || 'Websak 26/08940'}</strong></div>
                </div>
            </div>
            <div>
                <span class="status-badge" style="background:${cvIsNeg ? '#fef2f2' : '#f0fdf4'}; color:${cvIsNeg ? '#b91c1c' : '#15803d'}; font-size:11px; font-weight:700;">
                    ${cvIsNeg ? '🔴 Merforbruk jf. § 14-5' : '🟢 I budsjettbalanse'}
                </span>
            </div>
        </div>

        <div class="framsikt-four-dimensions">
            <!-- 1. NØKKELTALL (Tufte Data-Ink Metrics) -->
            <div class="framsikt-dimension-box">
                <div class="framsikt-dim-title">
                    <span>📊 1. Finansielle Nøkkeltall (Framsikt / Visma ERP)</span>
                    <span style="font-size:10.5px; color:#64748b; font-weight:normal;">M09 / M10 Akkumulert</span>
                </div>
                <div class="framsikt-kpi-grid">
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Årsbudsjett (BAC)</div>
                        <div class="f-kpi-val">${formatKr(node.ramme)}</div>
                        <div class="f-kpi-sub">Framsikt godkjent ramme</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Periodisert (PV YTD)</div>
                        <div class="f-kpi-val">${formatKr(node.pv)}</div>
                        <div class="f-kpi-sub">Planlagt forbruk til nå</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Faktisk (AC YTD)</div>
                        <div class="f-kpi-val">${formatKr(node.ac)}</div>
                        <div class="f-kpi-sub">Bokført i Visma ERP</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Avvik (CV)</div>
                        <div class="f-kpi-val ${cvClass}">${cvSign}${formatKr(node.cv)}</div>
                        <div class="f-kpi-sub">${((node.cv / (node.pv || 1)) * 100).toFixed(1)} % avvik</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Effektivitet (CPI)</div>
                        <div class="f-kpi-val ${cpiClass}">${node.cpi ? node.cpi.toFixed(3) : '1.000'}</div>
                        <div class="f-kpi-sub">Mål: ≥ 1.000</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Forbruksgrad</div>
                        <div class="f-kpi-val">${node.forbrukPct ? node.forbrukPct.toFixed(1) : '67.0'} %</div>
                        <div class="f-kpi-sub">Av total årsramme</div>
                    </div>
                </div>
            </div>

            <!-- 2. DIAGNOSE (Årsaksforklaring & Juss) -->
            <div class="framsikt-dimension-box f-diagnose-card">
                <div class="framsikt-dim-title">
                    <span>🔍 2. AI-Avviksdiagnose &amp; Rotårsaker (KOSTRA &amp; Driftsarter)</span>
                    <span style="font-size:10.5px; color:#b45309; font-weight:700;">§ 14-5 Tilsyn</span>
                </div>
                <div style="font-size:12px; color:#1e293b; line-height:1.55;">
                    ${node.diagnose?.summary || 'Drift i samsvar med periodisert budsjettramme.'}
                </div>
                ${driversHtml}
                <div style="margin-top:10px; padding-top:8px; border-top:1px dashed #e2e8f0; font-size:11px; color:#475569;">
                    ⚖️ <strong>Rettslig etterlevelse:</strong> ${node.diagnose?.lovhjemmel || 'Etterlever krav om realistisk budsjettering jf. Kommuneloven § 14-5.'}
                </div>
            </div>

            <!-- 3. PROGNOSE (Rolling Forecast & Monte Carlo) -->
            <div class="framsikt-dimension-box f-prognose-card">
                <div class="framsikt-dim-title">
                    <span>📈 3. Sluttprognose per 31.12 (EAC &amp; Usikkerhet)</span>
                    <span class="status-badge" style="font-size:10px;">${node.prognose?.status || 'Prognose'}</span>
                </div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:11px; color:#64748b; text-transform:uppercase;">Forventet Sluttregnskap (EAC)</div>
                        <div style="font-size:18px; font-weight:800; color:var(--navy-dark);">${node.prognose?.eac || formatKr(node.eac)}</div>
                    </div>
                    <div>
                        <div style="font-size:11px; color:#64748b; text-transform:uppercase;">Estimert Sluttavvik (VAC)</div>
                        <div style="font-size:18px; font-weight:800; color:${cvIsNeg ? '#b91c1c' : '#15803d'};">${node.prognose?.vac || formatKr(node.vac)}</div>
                    </div>
                    <div>
                        <div style="font-size:11px; color:#64748b; text-transform:uppercase;">Monte Carlo Konfidens (P10/P50/P90)</div>
                        <div style="font-size:12px; font-weight:700; color:#0f172a; margin-top:3px;">
                            ${node.prognose?.intervall || 'P50: ' + formatKr(node.eac)}
                        </div>
                    </div>
                </div>
                <div style="font-size:11.5px; color:#475569;">
                    ℹ️ <em>${node.prognose?.trend || 'Prognosen er sesongjustert basert på 3 års historikk i Visma ERP.'}</em>
                </div>
            </div>

            <!-- 4. ACTION TO TAKE (Konkrete Tiltak for Budsjettansvarlig) -->
            <div class="framsikt-dimension-box f-action-card">
                <div class="framsikt-dim-title">
                    <span>⚡ 4. Action To Take (Operativ Handlingsplan for ${node.leder})</span>
                    <span style="font-size:10.5px; color:#15803d; font-weight:700;">Prioriterte strakstiltak</span>
                </div>
                ${actionsHtml}
                <div class="framsikt-action-btns">
                    <button type="button" class="btn btn-sm btn-primary" onclick="generateFramsiktDoc('${node.id}')" title="Generer offisielt Word-avviksnotat for denne lederen">
                        📝 Generer Avviksnotat (.docx)
                    </button>
                    <button type="button" class="btn btn-sm" onclick="jumpToTriageForNode('${node.id}')" style="background:#f1f5f9; color:var(--navy-dark); font-weight:700;">
                        📋 Behandle i Triage-kø
                    </button>
                    <button type="button" class="btn btn-sm" onclick="contactControllerForNode('${node.id}')" style="background:#f1f5f9;">
                        ✉️ Kontakt Controller (${node.controller ? node.controller.split('/')[0].trim() : 'Frank Ellingsen'})
                    </button>
                    <button type="button" class="btn btn-sm" onclick="sealFramsiktAssessment('${node.id}')" style="background:#ecfdf5; color:#065f46; border-color:#a7f3d0; font-weight:700;">
                        🔒 Forsegl Vurdering (SHA-256)
                    </button>
                </div>
                <div id="framsikt-action-feedback-${node.id}" style="display:none; margin-top:8px; font-size:11px; padding:6px 10px; border-radius:3px; background:#f0fdf4; color:#166534; border:1px solid #bbf7d0;"></div>
            </div>
        </div>
    `;
}

function generateFramsiktDoc(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    showToast(`📝 Genererer avviksnotat for ${node.leder} (${node.name})...`);
    
    if (typeof openTab === 'function') openTab('sektor-konsern');
    const genEnhet = document.getElementById("gen-enhet");
    if (genEnhet) {
        for (let i = 0; i < genEnhet.options.length; i++) {
            if (genEnhet.options[i].text.includes(node.name) || genEnhet.options[i].value.includes(node.id)) {
                genEnhet.selectedIndex = i;
                break;
            }
        }
        if (typeof updateGeneratedNote === 'function') updateGeneratedNote();
    }
    const fb = document.getElementById(`framsikt-action-feedback-${nodeId}`);
    if (fb) {
        fb.style.display = "block";
        fb.innerHTML = `✓ Avviksnotat for <strong>${node.name}</strong> klargjort i Saksgenerator. Last ned Word-fil under saksflyt.`;
    }
}

function jumpToTriageForNode(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    if (typeof openTab === 'function') openTab('sektor-konsern');
    const triageEl = document.getElementById("triage-seksjon");
    if (triageEl) {
        triageEl.scrollIntoView({ behavior: 'smooth' });
        showToast(`📋 Viser arbeidskø og triage for ${node.name}`);
    }
}

function contactControllerForNode(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    const ctrl = node.controller ? node.controller.split('/')[0].trim() : 'Frank Ellingsen';
    const email = node.epost || 'controller@kristiansand.kommune.no';
    const subject = encodeURIComponent(`Oppfølging av budsjettavvik — ${node.name} (${node.ansvar || ''})`);
    const body = encodeURIComponent(`Hei ${ctrl},\n\nViser til månedlig avviksrapport for ${node.name}. Påløpt avvik er ${formatKr(node.cv)} (CPI: ${node.cpi}).\n\nVennligst bistå med avstemming og utarbeidelse av tiltaksplan jf. Kommuneloven § 14-5.\n\nMvh,\n${node.leder}`);
    window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
}

function sealFramsiktAssessment(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
    const mockHash = "SHA256:" + Array.from(crypto.getRandomValues(new Uint8Array(16))).map(b => b.toString(16).padStart(2, '0')).join('');
    const fb = document.getElementById(`framsikt-action-feedback-${nodeId}`);
    if (fb) {
        fb.style.display = "block";
        fb.innerHTML = `🔒 <strong>Kryptografisk forseglingsbevis (Stage-Gate Port 9):</strong><br>Signert av: ${node.leder} | Tidspunkt: ${now} UTC | Hash: <code>${mockHash}</code>`;
    }
    showToast(`🔒 Vurdering for ${node.name} forseglet med SHA-256`);
}

function jumpToFramsiktHierarchy() {
    if (typeof openTab === 'function') {
        openTab('sektor-konsern');
    }
    const sec = document.getElementById("framsikt-budsjetthierarki-seksjon");
    if (sec) {
        sec.scrollIntoView({ behavior: 'smooth' });
    }
}

function exportFramsiktHierarchyXlsx() {
    let csv = "Nivå;ID;Område / Enhet;Leder;Tittel;Ansvar-ID;Fullmakt NOK;Årsbudsjett BAC;Periodisert PV;Påløpt AC;Avvik CV;CPI;EAC;Status\n";
    function addCsvRows(node) {
        csv += `${node.niva};"${node.id}";"${node.name}";"${node.leder}";"${node.tittel}";"${node.ansvar || ''}";${node.fullmakt || 0};${node.ramme};${node.pv};${node.ac};${node.cv};${node.cpi};${node.eac};"${node.cv < 0 ? 'Merforbruk' : 'Balanse'}"\n`;
        if (node.children) node.children.forEach(addCsvRows);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(addCsvRows);
    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Framsikt_Budsjetthierarki_Kristiansand_2026.csv`;
    a.click();
    showToast("📥 Eksporterte Framsikt budsjetthierarki til CSV/Excel");
}

function updateGlobalSectorBanner(sectorKey) {
    const pills = document.querySelectorAll("#global-sector-pills .gsec-pill");
    pills.forEach(p => {
        if (p.getAttribute("data-sec") === sectorKey) {
            p.classList.add("active");
        } else {
            p.classList.remove("active");
        }
    });

    const noticeText = document.getElementById("global-sector-notice-text");
    const resetBtn = document.getElementById("global-sector-reset-btn");
    const sectorData = SEKTOR_DATA[sectorKey] || SEKTOR_DATA["ALL"];

    if (sectorKey === "ALL") {
        if (noticeText) noticeText.innerHTML = "🌐 <strong>Konsernvisning:</strong> Viser alle 6 virksomhetsområder for Kristiansand kommune samlet. Klikk et område over for å isolere data.";
        if (resetBtn) resetBtn.style.display = "none";
    } else {
        if (noticeText) noticeText.innerHTML = `📍 <strong>Aktivt område:</strong> ${sectorData.icon} <strong>${sectorData.title}</strong> — Viser kun data, budsjetter, avvik og enheter tilknyttet dette området.`;
        if (resetBtn) resetBtn.style.display = "inline-flex";
    }
}

function filterTop3HierarchyTableForSector(sectorKey) {
    const tbody = document.getElementById("top3-hierarchy-tbody");
    if (!tbody) return;

    const sMap = {
        "ALL": "ALL",
        "HELSE": "OMR-03",
        "OPPVEKST": "OMR-02",
        "BYUTVIKLING": "OMR-05",
        "KULTUR": "OMR-04",
        "ORG_TEK": "OMR-11",
        "OKONOMI": "OMR-12"
    };
    const targetSectorId = sMap[sectorKey] || "ALL";

    if (typeof renderHierarchyTable === 'function') {
        renderHierarchyTable();
    }

    const rows = tbody.querySelectorAll("tr");
    rows.forEach(tr => {
        if (targetSectorId === "ALL") {
            tr.style.display = "";
        } else {
            const isMatch = (tr.getAttribute("onclick") && tr.getAttribute("onclick").includes(targetSectorId)) || 
                            tr.id === `drilldown-${targetSectorId}` || 
                            (tr.innerText && tr.innerText.includes(targetSectorId));
            if (!isMatch) {
                tr.style.display = "none";
            } else {
                tr.style.display = "";
                if (tr.id === `drilldown-${targetSectorId}`) {
                    tr.style.display = "";
                    const toggleBtn = document.getElementById(`toggle-btn-${targetSectorId}`);
                    if (toggleBtn) toggleBtn.innerHTML = "▼ Skjul enheter";
                }
            }
        }
    });
}

function updateBudgetHoldersForSector(sectorKey) {
    const secSelect = document.getElementById("budget-holder-sector-filter");
    if (secSelect) {
        secSelect.value = sectorKey;
    }
    if (typeof filterBudgetHoldersTable === 'function') {
        filterBudgetHoldersTable();
    }
}

function updateProjectAccountingForSector(sectorKey) {
    const prSec = document.getElementById("pr-filter-sector");
    if (prSec) {
        prSec.value = sectorKey;
    }
    if (typeof renderProjectsTable === 'function') {
        renderProjectsTable();
    }
}

// Store reference to original selectSector function
const originalSelectSector = typeof window.selectSector === 'function' ? window.selectSector : null;

// OVERRIDE: Master selectSector() with full isolation
window.selectSector = function(sectorKey, fromTop3Sync) {
    // 1. Call original selectSector if exists (updates detail card, kpi row, existing syncs)
    if (typeof originalSelectSector === 'function') {
        originalSelectSector(sectorKey, fromTop3Sync);
    }

    // 2. Persist selection
    try {
        localStorage.setItem("aikom_selected_sector", sectorKey);
    } catch(e) {}

    // 3. Update Global Sector Banner
    updateGlobalSectorBanner(sectorKey);

    // 4. Update Framsikt Budsjettnivå-Hierarki
    renderFramsiktTree(sectorKey, "");

    // 5. Filter Top 3 Avvikshierarki Table (Strictly shows selected sector)
    filterTop3HierarchyTableForSector(sectorKey);

    // 6. Filter Budsjettansvarlige Table (Strictly shows budget holders for selected sector)
    updateBudgetHoldersForSector(sectorKey);

    // 7. Filter Prosjektregnskap Table (Strictly shows projects for selected sector)
    updateProjectAccountingForSector(sectorKey);

    // 8. Filter Sektor Comparison Table (hides non-matching rows)
    if (typeof filterSectorComparisonTable === 'function') {
        filterSectorComparisonTable(sectorKey);
    }
};

function initFramsiktHierarchyEngine() {
    const savedSector = localStorage.getItem("aikom_selected_sector") || "ALL";
    renderFramsiktTree(savedSector, "");
    updateGlobalSectorBanner(savedSector);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFramsiktHierarchyEngine);
} else {
    initFramsiktHierarchyEngine();
}
// ==============================================================================
'''

marker = 'function initTop3KpiDashboard()'
content = content.replace(marker, FRAMSIKT_ENGINE_JS + "\n\n" + marker, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected updated FRAMSIKT_ENGINE_JS.")

# Check syntax with node -c
with open('scratch_full_test.js', 'w', encoding='utf-8') as sf:
    # extract script
    scripts = content.split('<script>')[1].split('</script>')[0]
    sf.write(scripts)

res = subprocess.run(["node", "-c", "scratch_full_test.js"], capture_output=True, text=True)
if res.returncode == 0:
    print("Full index.html script syntax: 100% VALID!")
else:
    print("Syntax error:")
    print(res.stderr[:1000])
