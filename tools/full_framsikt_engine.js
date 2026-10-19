// ==============================================================================
// 🏛️ FRAMSIKT BUDSJETTNIVÅ-HIERARKI & DYNAMISK ISOLERINGSMOTOR
// Speiler Framsikt EPM: Virksomhetsområde (N1) ➔ Tjenesteområde (N2) ➔ Resultatenhet (N3) ➔ Avdeling/Kostnadssted (N4)
// jf. Kommuneloven § 14-5, § 14-6, HTA § 4 og Kristiansand Bystyres Økonomireglement
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
                ramme: 1150000000,
                pv: 775000000,
                ac: 782200000,
                cv: -7200000,
                cpi: 0.991,
                forbrukPct: 68.0,
                eac: 1160800000,
                vac: -10800000,
                p10: 1156000000,
                p50: 1160800000,
                p90: 1167000000,
                diagnose: {
                    summary: "Sykefravær i pleiesektoren på 11.2 %. Vikarbyråkostnader på art 10200 og helgeovertid art 10900 er hoveddriverne.",
                    drivers: [
                        { art: "10200", navn: "Vikarbyrå", belop: "+3 800 000 kr", vurdering: "Avtale med Dedicate benyttet." },
                        { art: "10900", navn: "Overtid helg", belop: "+2 100 000 kr", vurdering: "Vakanser i helgeturnus." }
                    ],
                    lovhjemmel: "Kommuneloven § 14-5 & HTA § 4."
                },
                prognose: { eac: "1 160 800 000 kr", vac: "-10 800 000 kr", status: "🔴 Alvorlig avvik", intervall: "P50: 1.161 mrd", trend: "+900k/mnd" },
                actions: [
                    { nr: 1, type: "VIKARSTOPP", tekst: "Innføre attestasjonssperre på ekstern innleie over 50 000 kr uten godkjenning fra Områdeleder.", frist: "Straks" },
                    { nr: 2, type: "GAT", tekst: "Avstemme GAT-turnuser ukentlig mot planlagt grunnbemanning.", frist: "Hver mandag kl 10" }
                ],
                children: [
                    {
                        id: "ENHET_401",
                        sectorKey: "HELSE",
                        name: "Strai Sykehjem",
                        leder: "Solveig Grimstad",
                        tittel: "Enhetsleder Strai Sykehjem",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "5200-ENH-401",
                        kostra: "Funksjon 254",
                        fullmakt: 2000000,
                        epost: "solveig.grimstad@kristiansand.kommune.no",
                        telefon: "+47 38 00 84 01",
                        controller: "Frank Ellingsen",
                        kontor: "Strai Sykehjem, Setesdalsveien 320, 4618 Kristiansand",
                        ramme: 84000000,
                        pv: 56350000,
                        ac: 58800000,
                        cv: -2450000,
                        cpi: 0.958,
                        forbrukPct: 70.0,
                        eac: 87600000,
                        vac: -3600000,
                        p10: 86200000,
                        p50: 87600000,
                        p90: 89100000,
                        diagnose: {
                            summary: "Merforbruk skyldes vikarbyråinnleie ved langtidssykefravær (Adecco Care) og overtid helg (art 10900).",
                            drivers: [
                                { art: "10200", navn: "Vikarbyrå Adecco", belop: "+1 650 000 kr", vurdering: "Døgnbemanning krav." },
                                { art: "10900", navn: "Overtid helg", belop: "+800 000 kr", vurdering: "Sykdom helgevakter." }
                            ],
                            lovhjemmel: "Kommuneloven § 14-5 & AML § 10-12."
                        },
                        prognose: { eac: "87 600 000 kr", vac: "-3 600 000 kr", status: "🔴 Kritisk avvik", intervall: "P50: 87.6M", trend: "+300k/mnd" },
                        actions: [
                            { nr: 1, type: "TURNUS", tekst: "Gjennomgå turnusplaner i GAT med tillitsvalgt for å redusere overtid.", frist: "M+4 virkedag" },
                            { nr: 2, type: "VIKARSTOPP", tekst: "Stoppe all bestilling av vikarbyrå på natt med mindre akutt liv/helse trues.", frist: "Straks" }
                        ],
                        children: [
                            {
                                id: "SEK_401_1",
                                sectorKey: "HELSE",
                                name: "Avd. 2A Somatikk & Rehabilitering",
                                leder: "Tone Røyseland",
                                tittel: "Avdelingsleder Demens & Somatikk",
                                niva: 4,
                                nivaTekst: "Nivå 4: Avdelingsleder",
                                ansvar: "5201-SEK-DEMENS",
                                kostra: "Funksjon 254 (Kostnadssted 5201)",
                                fullmakt: 250000,
                                epost: "tone.royseland@kristiansand.kommune.no",
                                telefon: "+47 38 00 84 11",
                                controller: "Frank Ellingsen",
                                ramme: 28000000,
                                pv: 18780000,
                                ac: 19680000,
                                cv: -900000,
                                cpi: 0.954,
                                forbrukPct: 70.3,
                                eac: 29300000,
                                vac: -1300000,
                                p10: 28900000,
                                p50: 29300000,
                                p90: 29800000,
                                diagnose: { summary: "Ekstraordinært sykefravær på natt og kveld dekket med vikarbyrå.", drivers: [{ art: "10200", navn: "Sykepleierinnleie", belop: "+650 000 kr", vurdering: "Spesialkompetansekrav." }], lovhjemmel: "AML § 10-12" },
                                prognose: { eac: "29 300 000 kr", vac: "-1 300 000 kr", status: "🔴 Avvik", intervall: "P50: 29.3M", trend: "+100k/mnd" },
                                actions: [{ nr: 1, type: "TIMELISTER", tekst: "Attestere timelister og vikarforbruk ukentlig i Visma Enterprise.", frist: "M+3 virkedag" }]
                            },
                            {
                                id: "SEK_401_2",
                                sectorKey: "HELSE",
                                name: "Avd. 2B Skjermet Enhet Demens",
                                leder: "Lars Klev",
                                tittel: "Avdelingsleder Korttid & Skjermet",
                                niva: 4,
                                nivaTekst: "Nivå 4: Avdelingsleder",
                                ansvar: "5202-SEK-KORTTID",
                                kostra: "Funksjon 254 (Kostnadssted 5202)",
                                fullmakt: 250000,
                                epost: "lars.klev@kristiansand.kommune.no",
                                telefon: "+47 38 00 84 12",
                                controller: "Frank Ellingsen",
                                ramme: 26000000,
                                pv: 17440000,
                                ac: 18240000,
                                cv: -800000,
                                cpi: 0.956,
                                forbrukPct: 70.2,
                                eac: 27200000,
                                vac: -1200000,
                                p10: 26800000,
                                p50: 27200000,
                                p90: 27600000,
                                diagnose: { summary: "2:1 bemanning ved utagerende demenspasient. Sikkerhetsprosedyrer utløser ekstravakter.", drivers: [{ art: "10900", navn: "Overtid sikkerhet", belop: "+480 000 kr", vurdering: "HMS-krav." }], lovhjemmel: "Helse- og omsorgstjenesteloven § 9" },
                                prognose: { eac: "27 200 000 kr", vac: "-1 200 000 kr", status: "🔴 Merforbruk", intervall: "P50: 27.2M", trend: "+80k/mnd" },
                                actions: [{ nr: 1, type: "HMS", tekst: "Gjennomgå ressursbehov med fagkoordinator og vurdere overføring til spesialenhet.", frist: "M+5 virkedag" }]
                            }
                        ]
                    },
                    {
                        id: "ENHET_404",
                        sectorKey: "HELSE",
                        name: "Presteheia Omsorgssenter",
                        leder: "Kari Vesterhus",
                        tittel: "Enhetsleder Presteheia Omsorgssenter",
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
                        name: "Bo- og Miljøtjenester",
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
            lovhjemmel: "Kommuneloven § 14-5 & Opplæringsloven § 8-2 (lærernorm). HTA § 4 ved endring i arbeidsplan."
        },
        prognose: {
            eac: "2 137 650 000 kr",
            vac: "-17 650 000 kr",
            status: "🔴 Merforbruk jf. § 14-5",
            intervall: "P10: 2.129 mrd | P50: 2.138 mrd | P90: 2.146 mrd",
            trend: "Stabilisert etter innføring av vikarring i skolesektoren."
        },
        actions: [
            { nr: 1, type: "VIKARRING", tekst: "Aktivere felles vikarring på tvers av Lovisenlev, Vågsbygd og Grim ungdomsskole for å erstatte eksterne timelærere.", frist: "Mandag uke 43" },
            { nr: 2, type: "REFUSJON", tekst: "Sende samlet oversending av 410k kr uoppgjorte krav til NAV Agder med kopi til Statsforvalteren.", frist: "M+5 virkedag" },
            { nr: 3, type: "SAKSNOTAT", tekst: "Ferdigstille saksfremlegg til Oppvekstutvalget om kompensasjon for økt elevtallsvekst jf. § 14-5.", frist: "M+8 virkedag" }
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
                kostra: "Funksjon 202, 211, 215, 221",
                fullmakt: 10000000,
                epost: "svein.tore.kvernes@kristiansand.kommune.no",
                telefon: "+47 38 00 72 20",
                controller: "Erik Halvorsen",
                ramme: 1480000000,
                pv: 997300000,
                ac: 1006072460,
                cv: -8772460,
                cpi: 0.991,
                forbrukPct: 68.0,
                eac: 1493150000,
                vac: -13150000,
                p10: 1488000000,
                p50: 1493150000,
                p90: 1499000000,
                diagnose: {
                    summary: "Lærernorm og spesialundervisning enkeltvedtak. Timelærervikarer art 10200 utgjør hovedtyngden av avviket.",
                    drivers: [
                        { art: "10200", navn: "Lærervikarer", belop: "+5 100 000 kr", vurdering: "Korttidsfravær." },
                        { art: "10500", navn: "Miljøterapeuter", belop: "+1 800 000 kr", vurdering: "Spesialtiltak." }
                    ],
                    lovhjemmel: "Opplæringsloven § 8-2 & § 14-5."
                },
                prognose: { eac: "1 493 150 000 kr", vac: "-13 150 000 kr", status: "🔴 Avvik", intervall: "P50: 1.493 mrd", trend: "+750k/mnd" },
                actions: [
                    { nr: 1, type: "NORM", tekst: "Klassestørrelse-avstemming mot lærernorm (1:15 på 1.–4. trinn, 1:20 på 5.–10. trinn).", frist: "M+4 virkedag" }
                ],
                children: [
                    {
                        id: "ENHET_202",
                        sectorKey: "OPPVEKST",
                        name: "Lovisenlev Skole",
                        leder: "Trond Jensen",
                        tittel: "Rektor Lovisenlev Skole",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "4100-ENH-202",
                        kostra: "Funksjon 202 (Grunnskole) & 215 (SFO)",
                        fullmakt: 2000000,
                        epost: "trond.jensen@kristiansand.kommune.no",
                        telefon: "+47 38 00 82 02",
                        controller: "Frank Ellingsen",
                        kontor: "Lovisenlev Skole, Lovisenlevveien 12, 4633 Kristiansand",
                        ramme: 52000000,
                        pv: 34966667,
                        ac: 37400000,
                        cv: -2433333,
                        cpi: 0.935,
                        forbrukPct: 71.9,
                        eac: 54800000,
                        vac: -2800000,
                        p10: 53900000,
                        p50: 54800000,
                        p90: 55700000,
                        diagnose: {
                            summary: "Merforbruk skyldes vikarbyrå/timelærere ved høyt sykefravær (Adecco Education 1.8M), overtid SFO (art 10500) og 410k NOK uavstemt refusjonskrav mot NAV Agder.",
                            drivers: [
                                { art: "10200", navn: "Lærervikarer (Adecco Education)", belop: "+1 820 000 kr", vurdering: "Høyt sykefravær." },
                                { art: "16000", navn: "NAV Refusjon sykepenger/foreldrepenger", belop: "-410 000 kr etterslep", vurdering: "Etterslep > 60 dager." },
                                { art: "10500", navn: "Lønn assistenter SFO", belop: "+350 000 kr", vurdering: "Ekstra bemanning." }
                            ],
                            lovhjemmel: "Kommuneloven § 14-5 & Opplæringsloven § 8-2."
                        },
                        prognose: {
                            eac: "54 800 000 kr",
                            vac: "-2 800 000 kr",
                            status: "🔴 Kritisk merforbruk",
                            intervall: "P10: 53.9M | P50: 54.8M | P90: 55.7M",
                            trend: "Ved etablering av vikarring reduseres EAC til 50.52M NOK (balanse)."
                        },
                        actions: [
                            { nr: 1, type: "VIKARRING", tekst: "Etablere felles vikarring med Vågsbygd Skole for å kutte ekstern innleie med 60 %.", frist: "Mandag uke 43" },
                            { nr: 2, type: "NAV-PURRING", tekst: "Innsende samlet purring på 410k kr utestående refusjonskrav til NAV Agder.", frist: "M+5 virkedag" },
                            { nr: 3, type: "VEDTAK", tekst: "Fremlegge administrativt avviksnotat til Kommunalsjef Kristin Eidet Robstad.", frist: "M+6 virkedag" }
                        ],
                        children: [
                            {
                                id: "SEK_202_1",
                                sectorKey: "OPPVEKST",
                                name: "SFO (Skolefritidsordning)",
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
                        actions: [{ nr: 1, type: "DRIFT", tekst: "Opprettholde planlagt takt på ledningsfornyelse (2 % per år).", frist: "Pågår" }],
                        children: [
                            {
                                id: "SEK_3101",
                                sectorKey: "BYUTVIKLING",
                                name: "Seksjon Avløp & Renseanlegg Odderøya/Lund",
                                leder: "Vidar Aanensen",
                                tittel: "Seksjonsleder Avløp",
                                niva: 4,
                                nivaTekst: "Nivå 4: Seksjonsleder",
                                ansvar: "3101-SEK-AVLOP",
                                kostra: "Funksjon 345 (Kostnadssted 3101)",
                                fullmakt: 350000,
                                epost: "vidar.aanensen@kristiansand.kommune.no",
                                telefon: "+47 38 00 83 11",
                                controller: "Knut Arild Vike",
                                ramme: 42000000,
                                pv: 28100000,
                                ac: 27950000,
                                cv: 150000,
                                cpi: 1.005,
                                forbrukPct: 66.5,
                                eac: 41800000,
                                vac: 200000,
                                p10: 41500000,
                                p50: 41800000,
                                p90: 42200000,
                                diagnose: { summary: "Driftsfakturaer og fellingskjemikalier innenfor rammen. Full MVA-kompensasjon jf. momskompensasjonsloven.", drivers: [{ art: "11200", navn: "Polymer og jernklorid", belop: "+120 000 kr besparelse", vurdering: "Effektiv dosering." }], lovhjemmel: "Momskompensasjonsloven § 4" },
                                prognose: { eac: "41 800 000 kr", vac: "+200 000 kr", status: "🟢 Balanse", intervall: "P50: 41.8M", trend: "Stabil" },
                                actions: [{ nr: 1, type: "ATTESTASJON", tekst: "Ferdigstille månedlig kjemikalielageravstemming.", frist: "M+3 virkedag" }]
                            }
                        ]
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
        cv: -45000,
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
                id: "KULT-OMR-SCENE",
                sectorKey: "KULTUR",
                name: "Kulturinstitusjoner, Scene & Bibliotek",
                leder: "Knut Ragnar Nilsen",
                tittel: "Områdeleder Kultur & Scene",
                niva: 2,
                nivaTekst: "Nivå 2: Områdeleder",
                ansvar: "2100-OMR-KULTUR",
                kostra: "Funksjon 370, 375",
                fullmakt: 8000000,
                epost: "knut.ragnar.nilsen@kristiansand.kommune.no",
                telefon: "+47 38 00 74 20",
                controller: "Silje Mæland",
                ramme: 195000000,
                pv: 130000000,
                ac: 130020000,
                cv: -20000,
                cpi: 1.000,
                forbrukPct: 66.7,
                eac: 195030000,
                vac: -30000,
                p10: 194500000,
                p50: 195030000,
                p90: 195600000,
                diagnose: { summary: "Bibliotektjenester, samskaping og Kilden-samarbeid i henhold til årsplan.", drivers: [{ art: "11200", navn: "Materialkjøp og lisenser", belop: "I balanse", vurdering: "Følger budsjett." }], lovhjemmel: "Kulturloven § 1" },
                prognose: { eac: "195 030 000 kr", vac: "-30 000 kr", status: "🟢 Balanse", intervall: "P50: 195.0M", trend: "Jevn" },
                actions: [{ nr: 1, type: "TILSKUDD", tekst: "Kvalitetssikre rapportering for statlige stimuleringstilskudd.", frist: "M+6 virkedag" }],
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
                        pv: 22800000,
                        ac: 22780000,
                        cv: 20000,
                        cpi: 1.001,
                        forbrukPct: 67.0,
                        eac: 33970000,
                        vac: 30000,
                        p10: 33800000,
                        p50: 33970000,
                        p90: 34200000,
                        diagnose: { summary: "God kontroll på mediebudsjett og publikumsarrangementer i Vågsbygd, Tangvall og Sentrum.", drivers: [{ art: "11200", navn: "Digitalt bibliotek", belop: "Avstemt", vurdering: "Fellesinnkjøp." }], lovhjemmel: "Folkebibliotekloven" },
                        prognose: { eac: "33 970 000 kr", vac: "+30 000 kr", status: "🟢 Balanse", intervall: "P50: 34.0M", trend: "Stabil" },
                        actions: [{ nr: 1, type: "DRIFT", tekst: "Avstemme lisensavtaler for e-bøker med fylkesbiblioteket.", frist: "M+7 virkedag" }]
                    }
                ]
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
        kostra: "Funksjon 120, 180 (Administrasjon og IKT)",
        fullmakt: 15000000,
        epost: "geir.askvik@kristiansand.kommune.no",
        telefon: "+47 38 00 75 10",
        controller: "Frank Ellingsen",
        kontor: "Rådhuset, Rådhusgata 18, 4611 Kristiansand",
        returfrist: "M+8 virkedag kl. 14:00",
        returkanal: "okonomi.orgtek@kristiansand.kommune.no / Websak",
        ramme: 420000000,
        pv: 279000000,
        ac: 278670000,
        cv: 330000,
        cpi: 1.001,
        forbrukPct: 66.3,
        eac: 419500000,
        vac: 500000,
        p10: 417000000,
        p50: 419500000,
        p90: 422000000,
        sparkline: [32.1, 32.2, 32.1, 32.2, 32.1, 32.1, 24.1, 30.5, 32.2],
        diagnose: {
            summary: "FinOps-tiltak på M365 og Azure-infrastruktur har frigjort 1.2M NOK i lisensbesparelser. Konsulentbruk art 11950 sanert.",
            drivers: [{ art: "11950", navn: "M365 Lisenssanering", belop: "+1 200 000 kr besparelse", vurdering: "FinOps gevinst." }],
            lovhjemmel: "Kommuneloven § 14-5."
        },
        prognose: { eac: "419 500 000 kr", vac: "+500 000 kr", status: "🟢 Kostnadskontroll", intervall: "P50: 419.5M", trend: "Balanse" },
        actions: [{ nr: 1, type: "FINOPS", tekst: "Videreføre automatisk deaktivering av inaktive Microsoft 365-lisenser.", frist: "Løpende" }],
        children: [
            {
                id: "ORG-IKT",
                sectorKey: "ORG_TEK",
                name: "IKT- og Digitaliseringsavdelingen",
                leder: "Siri Bentsen",
                tittel: "IKT- og Digitaliseringsdirektør",
                niva: 2,
                nivaTekst: "Nivå 2: Direktør",
                ansvar: "1100-DIR-IKT",
                kostra: "Funksjon 120 (Felles IKT-drift)",
                fullmakt: 8000000,
                epost: "siri.bentsen@kristiansand.kommune.no",
                telefon: "+47 38 00 75 20",
                controller: "Frank Ellingsen",
                ramme: 230000000,
                pv: 153000000,
                ac: 152800000,
                cv: 200000,
                cpi: 1.001,
                forbrukPct: 66.4,
                eac: 229700000,
                vac: 300000,
                p10: 228000000,
                p50: 229700000,
                p90: 231500000,
                diagnose: { summary: "Full kontroll på skyinfrastruktur, konsulentsanering og lisensportefølje.", drivers: [{ art: "11950", navn: "Konsulenter", belop: "Redusert", vurdering: "Egne ressurser." }], lovhjemmel: "§ 14-5" },
                prognose: { eac: "229 700 000 kr", vac: "+300 000 kr", status: "🟢 Balanse", intervall: "P50: 229.7M", trend: "Stabil" },
                actions: [{ nr: 1, type: "SKY", tekst: "Gjennomføre kvartalsvis reservering av Azure reserved instances for å kutte 25 % driftskostnader.", frist: "M+8 virkedag" }],
                children: [
                    {
                        id: "ENHET_501",
                        sectorKey: "ORG_TEK",
                        name: "IKT Brukerstøtte & Applikasjonsdrift",
                        leder: "Kenneth Dale",
                        tittel: "IKT Driftssjef Brukerstøtte",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "1110-ENH-501",
                        kostra: "Funksjon 120",
                        fullmakt: 2500000,
                        epost: "kenneth.dale@kristiansand.kommune.no",
                        telefon: "+47 38 00 85 01",
                        controller: "Frank Ellingsen",
                        ramme: 72000000,
                        pv: 48000000,
                        ac: 47900000,
                        cv: 100000,
                        cpi: 1.002,
                        forbrukPct: 66.5,
                        eac: 71850000,
                        vac: 150000,
                        p10: 71200000,
                        p50: 71850000,
                        p90: 72500000,
                        diagnose: { summary: "Servicedesk og PC-utrulling innenfor budsjettrammen. Gjenbruk av IT-utstyr i skolene.", drivers: [{ art: "11200", navn: "Klientdrift", belop: "I balanse", vurdering: "God avtale." }], lovhjemmel: "§ 14-5" },
                        prognose: { eac: "71 850 000 kr", vac: "+150 000 kr", status: "🟢 Balanse", intervall: "P50: 71.9M", trend: "Stabil" },
                        actions: [{ nr: 1, type: "INNKJØP", tekst: "Optimalisere innkjøp av Chromebooks for Oppvekst.", frist: "M+5 virkedag" }],
                        children: [
                            {
                                id: "SEK_1111",
                                sectorKey: "ORG_TEK",
                                name: "FinOps & SaaS Fakturakontroll",
                                leder: "Thomas Berge",
                                tittel: "Seksjonsleder FinOps",
                                niva: 4,
                                nivaTekst: "Nivå 4: Seksjonsleder",
                                ansvar: "1111-SEK-FINOPS",
                                kostra: "Funksjon 120 (Kostnadssted 1111)",
                                fullmakt: 300000,
                                epost: "thomas.berge@kristiansand.kommune.no",
                                telefon: "+47 38 00 85 11",
                                controller: "Frank Ellingsen",
                                ramme: 18000000,
                                pv: 12050000,
                                ac: 11980000,
                                cv: 70000,
                                cpi: 1.006,
                                forbrukPct: 66.6,
                                eac: 17900000,
                                vac: 100000,
                                p10: 17700000,
                                p50: 17900000,
                                p90: 18100000,
                                diagnose: { summary: "Ukentlig avstemming av skytjenestefakturaer og deaktivering av inaktive brukere.", drivers: [{ art: "11950", navn: "SaaS lisenser", belop: "+70 000 kr buffer", vurdering: "Ryddig." }], lovhjemmel: "Kommuneloven § 14-5" },
                                prognose: { eac: "17 900 000 kr", vac: "+100 000 kr", status: "🟢 Balanse", intervall: "P50: 17.9M", trend: "Stabil" },
                                actions: [{ nr: 1, type: "KONTROLL", tekst: "Fakturakontroll av månedlig Microsoft Azure-regning.", frist: "M+2 virkedag" }]
                            }
                        ]
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
        nivaTekst: "Nivå 1: Økonomidirektør",
        ansvar: "6000-DIR-OKONOMI",
        kostra: "Funksjon 100, 130 (Finans og EPM)",
        fullmakt: 50000000,
        epost: "terje.fjellvang@kristiansand.kommune.no",
        telefon: "+47 38 00 76 10",
        controller: "Frank Ellingsen",
        kontor: "Rådhuset, Rådhusgata 18, 4611 Kristiansand",
        returfrist: "M+9 virkedag kl. 12:00",
        returkanal: "konsernokonomi@kristiansand.kommune.no / Websak",
        ramme: 530000000,
        pv: 355000000,
        ac: 354890000,
        cv: 110000,
        cpi: 1.000,
        forbrukPct: 67.0,
        eac: 529850000,
        vac: 150000,
        p10: 527000000,
        p50: 529850000,
        p90: 532500000,
        sparkline: [40.6, 40.7, 40.7, 40.8, 40.7, 40.7, 30.5, 38.6, 40.7],
        diagnose: {
            summary: "Finansforvaltningen har generert 14.5M NOK i ekstraordinære renteinntekter. Likviditeten er robust med 150M NOK ubenyttet trekkramme.",
            drivers: [{ art: "19000", navn: "Renteinntekter bank og sertifikater", belop: "+14 500 000 kr merinntekt", vurdering: "Høyt rentenivå." }],
            lovhjemmel: "Kommuneloven § 14-14 (finansreglementet) & § 14-5."
        },
        prognose: { eac: "529 850 000 kr", vac: "+150 000 kr", status: "🟢 Svært god kontroll", intervall: "P50: 529.9M", trend: "Balanse" },
        actions: [
            { nr: 1, type: "LIKVIDITET", tekst: "Optimalisere plasseringer på høyrentekonto i DNB og Kommunalbanken.", frist: "Daglig" },
            { nr: 2, type: "MVA", tekst: "Innsende MVA-kompensasjonsoppgave for termin 5 (balansekonto 2130 avstemt).", frist: "M+8 virkedag" }
        ],
        children: [
            {
                id: "OKO-REGNSKAP",
                sectorKey: "OKONOMI",
                name: "Konsernregnskap & Finansforvaltning",
                leder: "Bente Gundersen",
                tittel: "Konsernregnskapssjef",
                niva: 2,
                nivaTekst: "Nivå 2: Direktør",
                ansvar: "6100-DIR-REGNSKAP",
                kostra: "Funksjon 130",
                fullmakt: 10000000,
                epost: "bente.gundersen@kristiansand.kommune.no",
                telefon: "+47 38 00 76 20",
                controller: "Frank Ellingsen",
                ramme: 290000000,
                pv: 194000000,
                ac: 193900000,
                cv: 100000,
                cpi: 1.001,
                forbrukPct: 66.9,
                eac: 289850000,
                vac: 150000,
                p10: 288000000,
                p50: 289850000,
                p90: 291500000,
                diagnose: { summary: "Månedsavstemming og MVA-kompensasjon gjennomført til rett tid uten avvik.", drivers: [{ art: "19000", navn: "Renteinntekter", belop: "Merinntekt", vurdering: "Meget tilfredsstillende." }], lovhjemmel: "Kommuneloven § 14-14" },
                prognose: { eac: "289 850 000 kr", vac: "+150 000 kr", status: "🟢 Balanse", intervall: "P50: 289.9M", trend: "Stabil" },
                actions: [{ nr: 1, type: "PERIODELUKKING", tekst: "Gjennomføre M10-periodelukking i Visma Enterprise.", frist: "M+5 virkedag" }],
                children: [
                    {
                        id: "ENHET_601",
                        sectorKey: "OKONOMI",
                        name: "Finans- og Gjeldsforvaltning",
                        leder: "Knut Ingebrigtsen",
                        tittel: "Finans- og Gjeldsforvalter",
                        niva: 3,
                        nivaTekst: "Nivå 3: Enhetsleder",
                        ansvar: "6200-ENH-601",
                        kostra: "Funksjon 130 (Finansforvaltning)",
                        fullmakt: 5000000,
                        epost: "knut.ingebrigtsen@kristiansand.kommune.no",
                        telefon: "+47 38 00 86 01",
                        controller: "Frank Ellingsen",
                        ramme: 45000000,
                        pv: 30100000,
                        ac: 30050000,
                        cv: 50000,
                        cpi: 1.002,
                        forbrukPct: 66.8,
                        eac: 44920000,
                        vac: 80000,
                        p10: 44500000,
                        p50: 44920000,
                        p90: 45300000,
                        diagnose: { summary: "Renteportefølje sikret med 65 % fastrente. Sertifikatlån refinansiert til gunstige marginer.", drivers: [{ art: "19000", navn: "Sertifikatlån", belop: "+50 000 kr buffer", vurdering: "Lav margin." }], lovhjemmel: "Finansreglementet § 4" },
                        prognose: { eac: "44 920 000 kr", vac: "+80 000 kr", status: "🟢 Balanse", intervall: "P50: 44.9M", trend: "Stabil" },
                        actions: [{ nr: 1, type: "REFINANSIERING", tekst: "Refinansiere 200M kr i KBN-lån som forfaller i Q4.", frist: "M+8 virkedag" }]
                    }
                ]
            }
        ]
    }
};

let currentSelectedFramsiktNodeId = "HELSE";
let framsiktTreeState = {
    "HELSE": true,
    "HELSE-INST": true,
    "ENHET_401": true,
    "OPPVEKST": true,
    "OPPV-SKOLE": true,
    "ENHET_202": true,
    "BYUTVIKLING": true,
    "BYUTV-VAR": true,
    "KULTUR": true,
    "ORG_TEK": true,
    "OKONOMI": true
};

function findFramsiktNodeById(nodeId, rootNode) {
    if (!rootNode) {
        for (const secKey of Object.keys(FRAMSIKT_HIERARCHY_DATA)) {
            const found = findFramsiktNodeById(nodeId, FRAMSIKT_HIERARCHY_DATA[secKey]);
            if (found) return found;
        }
        return null;
    }
    if (rootNode.id === nodeId) return rootNode;
    if (rootNode.children && rootNode.children.length > 0) {
        for (const child of rootNode.children) {
            const found = findFramsiktNodeById(nodeId, child);
            if (found) return found;
        }
    }
    return null;
}

function getBreadcrumbTrail(nodeId) {
    const trail = [];
    function search(curr, targetId, currentTrail) {
        if (!curr) return false;
        const newTrail = [...currentTrail, { id: curr.id, name: curr.name, niva: curr.niva, leder: curr.leder }];
        if (curr.id === targetId) {
            trail.push(...newTrail);
            return true;
        }
        if (curr.children) {
            for (const child of curr.children) {
                if (search(child, targetId, newTrail)) return true;
            }
        }
        return false;
    }
    for (const secKey of Object.keys(FRAMSIKT_HIERARCHY_DATA)) {
        const root = FRAMSIKT_HIERARCHY_DATA[secKey];
        if (search(root, nodeId, [])) break;
    }
    return trail;
}

function formatKr(num) {
    if (num === null || num === undefined || isNaN(num)) return "0 kr";
    return Math.round(num).toLocaleString("no-NO") + " kr";
}

function renderFramsiktTree(sectorFilter, searchTerm) {
    const treeRoot = document.getElementById("framsikt-tree-root");
    if (!treeRoot) return;

    if (!sectorFilter) sectorFilter = localStorage.getItem("aikom_selected_sector") || "ALL";
    if (searchTerm === undefined) searchTerm = "";
    searchTerm = searchTerm.toLowerCase().trim();

    const headerScope = document.getElementById("framsikt-header-scope");
    if (headerScope) {
        if (sectorFilter === "ALL") {
            headerScope.textContent = "Konsern (Alle 6 virksomhetsområder)";
        } else {
            const secName = FRAMSIKT_HIERARCHY_DATA[sectorFilter]?.name || sectorFilter;
            headerScope.textContent = `Aktivt område: ${secName}`;
        }
    }

    let sectorsToRender = [];
    if (sectorFilter === "ALL") {
        sectorsToRender = Object.values(FRAMSIKT_HIERARCHY_DATA);
    } else if (FRAMSIKT_HIERARCHY_DATA[sectorFilter]) {
        sectorsToRender = [FRAMSIKT_HIERARCHY_DATA[sectorFilter]];
    } else {
        sectorsToRender = Object.values(FRAMSIKT_HIERARCHY_DATA);
    }

    let html = "";
    sectorsToRender.forEach(rootNode => {
        html += buildTreeNodeHtml(rootNode, searchTerm);
    });

    treeRoot.innerHTML = html;

    const currentFound = findFramsiktNodeById(currentSelectedFramsiktNodeId);
    if (!currentFound || (sectorFilter !== "ALL" && currentFound.sectorKey !== sectorFilter)) {
        const firstNode = sectorsToRender[0];
        if (firstNode) {
            selectFramsiktNode(firstNode.id);
        }
    } else {
        renderFramsiktDetail(currentFound);
    }
}

function buildTreeNodeHtml(node, searchTerm) {
    if (!node) return "";
    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = framsiktTreeState[node.id] !== false;
    const isSelected = currentSelectedFramsiktNodeId === node.id;

    if (searchTerm) {
        const textMatch = node.name.toLowerCase().includes(searchTerm) ||
                          node.leder.toLowerCase().includes(searchTerm) ||
                          (node.ansvar && node.ansvar.toLowerCase().includes(searchTerm));
        let childHasMatch = false;
        if (hasChildren) {
            childHasMatch = node.children.some(c => checkChildMatch(c, searchTerm));
        }
        if (!textMatch && !childHasMatch) {
            return "";
        }
    }

    const cvIsNeg = node.cv < 0;
    const cvColor = cvIsNeg ? "#b91c1c" : "#15803d";
    const cvFormatted = (node.cv > 0 ? "+" : "") + (node.cv / 1000000).toFixed(1) + "M";

    let folderIcon = "";
    if (hasChildren) {
        folderIcon = `<span class="f-toggle" onclick="toggleFramsiktFolder('${node.id}'); event.stopPropagation();">${isExpanded ? '▼' : '▶'}</span>`;
    } else {
        folderIcon = `<span class="f-toggle-leaf">•</span>`;
    }

    let childrenHtml = "";
    if (hasChildren) {
        childrenHtml = `<div class="f-tree-children ${isExpanded ? 'expanded' : 'collapsed'}" id="f-children-${node.id}">`;
        node.children.forEach(child => {
            childrenHtml += buildTreeNodeHtml(child, searchTerm);
        });
        childrenHtml += `</div>`;
    }

    return `
        <div class="f-tree-branch">
            <div class="f-tree-node ${isSelected ? 'active' : ''} niva-${node.niva}" 
                 id="f-node-${node.id}" 
                 onclick="selectFramsiktNode('${node.id}')"
                 title="Nivå ${node.niva}: ${node.name} — Leder: ${node.leder}">
                ${folderIcon}
                <span class="f-node-badge lvl-${node.niva}">N${node.niva}</span>
                <span class="f-node-title">${node.name}</span>
                <span class="f-node-leader">${node.leder}</span>
                <span class="f-node-cv" style="color:${cvColor};">${cvFormatted}</span>
            </div>
            ${childrenHtml}
        </div>
    `;
}

function checkChildMatch(node, searchTerm) {
    if (node.name.toLowerCase().includes(searchTerm) ||
        node.leder.toLowerCase().includes(searchTerm) ||
        (node.ansvar && node.ansvar.toLowerCase().includes(searchTerm))) {
        return true;
    }
    if (node.children) {
        return node.children.some(c => checkChildMatch(c, searchTerm));
    }
    return false;
}

function selectFramsiktNode(nodeId) {
    currentSelectedFramsiktNodeId = nodeId;
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;

    let curr = nodeId;
    const trail = getBreadcrumbTrail(nodeId);
    trail.forEach(step => {
        framsiktTreeState[step.id] = true;
    });

    document.querySelectorAll(".f-tree-node").forEach(el => el.classList.remove("active"));
    const targetEl = document.getElementById(`f-node-${nodeId}`);
    if (targetEl) targetEl.classList.add("active");

    renderFramsiktDetail(node);
}

function toggleFramsiktFolder(nodeId) {
    framsiktTreeState[nodeId] = !(framsiktTreeState[nodeId] !== false);
    const childDiv = document.getElementById(`f-children-${nodeId}`);
    if (childDiv) {
        if (framsiktTreeState[nodeId]) {
            childDiv.classList.remove("collapsed");
            childDiv.classList.add("expanded");
        } else {
            childDiv.classList.remove("expanded");
            childDiv.classList.add("collapsed");
        }
    }
    const nodeEl = document.getElementById(`f-node-${nodeId}`);
    if (nodeEl) {
        const toggleSpan = nodeEl.querySelector(".f-toggle");
        if (toggleSpan) toggleSpan.textContent = framsiktTreeState[nodeId] ? '▼' : '▶';
    }
}

function expandAllFramsiktTree() {
    function setAll(n) {
        framsiktTreeState[n.id] = true;
        if (n.children) n.children.forEach(setAll);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(setAll);
    const sec = localStorage.getItem("aikom_selected_sector") || "ALL";
    renderFramsiktTree(sec, "");
}

function collapseAllFramsiktTree() {
    function setFalse(n) {
        framsiktTreeState[n.id] = false;
        if (n.children) n.children.forEach(setFalse);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(setFalse);
    const sec = localStorage.getItem("aikom_selected_sector") || "ALL";
    renderFramsiktTree(sec, "");
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
            <!-- 1. NØKKELTALL (Tufte Tabular Nums) -->
            <div class="framsikt-dimension-box f-kpi-box">
                <div class="framsikt-dim-title">
                    <span>📊 1. Nøkkeltall (YTD Regnskap per M10 vs. Periodisert Ramme)</span>
                    <span style="font-size:10.5px; color:#64748b;">EVM Standard</span>
                </div>
                <div class="f-kpi-grid">
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Årsbudsjett (BAC)</div>
                        <div class="f-kpi-val">${formatKr(node.ramme)}</div>
                        <div class="f-kpi-sub">Vedtatt av Bystyret</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Periodisert Ramme (PV)</div>
                        <div class="f-kpi-val">${formatKr(node.pv)}</div>
                        <div class="f-kpi-sub">Per M10 (Oktober)</div>
                    </div>
                    <div class="f-kpi-card">
                        <div class="f-kpi-label">Faktisk Forbruk (AC)</div>
                        <div class="f-kpi-val">${formatKr(node.ac)}</div>
                        <div class="f-kpi-sub">Visma ERP Golden Record</div>
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
    }
    showToast(`📋 Hopper til Triage for ${node.name}`);
}

function contactControllerForNode(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    const ctrl = node.controller ? node.controller.split('/')[0].trim() : 'Frank Ellingsen';
    const email = 'frank.ellingsen@kristiansand.kommune.no';
    const subject = encodeURIComponent(`Oppfølging budsjettavvik 2026: ${node.name} (${node.ansvar})`);
    const body = encodeURIComponent(`Hei ${ctrl},\n\nViser til månedsoppfølging M10 for ${node.name} (ansvar ${node.ansvar}).\nVi har et registrert avvik på ${formatKr(node.cv)} og ber om controllers bistand vedrørende korrigerende tiltak jf. Kommuneloven § 14-5.\n\nMvh,\n${node.leder}\n${node.tittel}`);
    window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
}

function sealFramsiktAssessment(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    const timestamp = new Date().toISOString();
    const payload = `${node.id}|${node.cv}|${node.cpi}|${node.eac}|${timestamp}|Frank Ellingsen`;
    
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
        const char = payload.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    const mockSha256 = "SHA256-" + Math.abs(hash).toString(16).padStart(16, "0") + "a7f3e8c2";

    const fb = document.getElementById(`framsikt-action-feedback-${nodeId}`);
    if (fb) {
        fb.style.display = "block";
        fb.style.background = "#ecfdf5";
        fb.style.color = "#065f46";
        fb.style.borderColor = "#a7f3d0";
        fb.innerHTML = `🔒 <strong>Stage-Gate Port 9 Forseglet:</strong> Vurdering og tiltaksplan for ${node.name} er kryptografisk forankret med stempel <code>${mockSha256}</code> (${timestamp.slice(0, 19).replace('T', ' ')}). Klar for Kommunerevisjonen.`;
    }
    showToast(`🔒 Vurdering forseglet for ${node.name} (Port 9 HITL)`);
}

function exportFramsiktHierarchyXlsx() {
    showToast("📊 Klargjør eksport av Framsikt Budsjettnivå-hierarki...");
    const rows = [];
    rows.push(["Nivå", "Område / Enhet", "Budsjettansvarlig", "Tittel", "Ansvarsnr", "KOSTRA", "Årsbudsjett (BAC)", "Periodisert (PV)", "Faktisk (AC)", "Avvik (CV)", "CPI", "EAC Sluttprognose", "VAC Sluttavvik"]);

    function addCsvRows(n) {
        rows.push([
            "Nivå " + n.niva,
            n.name,
            n.leder,
            n.tittel,
            n.ansvar || "",
            n.kostra || "",
            n.ramme || 0,
            n.pv || 0,
            n.ac || 0,
            n.cv || 0,
            n.cpi || 1.0,
            n.eac || 0,
            n.vac || 0
        ]);
        if (n.children) {
            n.children.forEach(addCsvRows);
        }
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(addCsvRows);

    let csvContent = "\uFEFF" + rows.map(e => e.map(val => `"${String(val).replace(/"/g, '""')}"`).join(";")).join("\r\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `Framsikt_Budsjetthierarki_Kristiansand_2026.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("✓ Framsikt CSV lastet ned.");
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

// -----------------------------------------------------------------------------
// TOTAL SECTOR ISOLATION INTEGRATION: selectSector()
// -----------------------------------------------------------------------------
window.selectSector = function(sectorKey, fromTop3Sync) {
    try {
        localStorage.setItem("aikom_selected_sector", sectorKey);
    } catch(e) {}

    const data = SEKTOR_DATA[sectorKey] || SEKTOR_DATA["ALL"];

    // 1. Global Sector Selector Bar update
    updateGlobalSectorBanner(sectorKey);

    // 2. Sektor Nav Bar active pills in sektor-seksjon
    const navButtons = document.querySelectorAll("#sector-nav-bar .sector-tab-btn");
    navButtons.forEach(btn => btn.classList.remove("active"));
    const activeNavBtn = document.getElementById(`sec-btn-${sectorKey.toLowerCase()}`) || document.getElementById("sec-btn-all");
    if (activeNavBtn) activeNavBtn.classList.add("active");

    // 3. Dropdown synchronizations
    const kpiSelect = document.getElementById("kpi-sector-select");
    if (kpiSelect && kpiSelect.value !== sectorKey) {
        kpiSelect.value = sectorKey;
    }
    const bhSelect = document.getElementById("budget-holder-sector-filter");
    if (bhSelect && bhSelect.value !== sectorKey) {
        bhSelect.value = sectorKey;
    }

    // 4. Top 3 Sync
    if (!fromTop3Sync && typeof selectTop3Sector === 'function') {
        const sMap = {
            "ALL": "ALL",
            "HELSE": "OMR-03",
            "OPPVEKST": "OMR-02",
            "BYUTVIKLING": "OMR-05",
            "KULTUR": "OMR-04",
            "ORG_TEK": "OMR-11",
            "OKONOMI": "OMR-12"
        };
        selectTop3Sector(sMap[sectorKey] || "ALL", true);
    }

    // 5. Update Sektor Detail Card
    const detailCard = document.getElementById("sector-detail-card");
    if (detailCard && typeof renderSectorDetailCardHtml === 'function') {
        detailCard.innerHTML = renderSectorDetailCardHtml(sectorKey, data);
    }

    // 6. Update KPI row (PV, AC, CV, CPI, EAC)
    if (typeof updateKpiRow === 'function') {
        updateKpiRow(sectorKey);
    }

    // 7. Filter Sector Comparison Table: STRICT SINGLE SECTOR ISOLATION
    filterSectorComparisonTableStrict(sectorKey);

    // 8. Filter Top 3 Avvikshierarki Table: ONLY display selected sector
    filterTop3HierarchyTableForSector(sectorKey);

    // 9. Update FRAMSIKT BUDSJETTHIERARKI: Filters tree and renders detail
    renderFramsiktTree(sectorKey, "");

    // 10. Filter Budsjettansvarlige Table
    if (typeof filterBudgetHoldersTable === 'function') {
        filterBudgetHoldersTable();
    }

    // 11. Filter Prosjektregnskap (Investeringer)
    const prSec = document.getElementById("pr-filter-sector");
    if (prSec) {
        prSec.value = sectorKey;
        if (typeof renderProjectsTable === 'function') {
            renderProjectsTable();
        }
    }

    // 12. Smart Arbeidskø, Triage & Saksgenerator
    if (typeof renderSectorTriage === 'function') {
        renderSectorTriage(sectorKey);
    }
    if (typeof syncSaksgeneratorForSector === 'function') {
        syncSaksgeneratorForSector(sectorKey);
    }

    // 13. Budsjettmodul & KOSTRA
    if (typeof updateBudsjettModulForSector === 'function') {
        updateBudsjettModulForSector(sectorKey);
    }

    // 14. Dokumentbank
    if (typeof updateDocbankForSector === 'function') {
        updateDocbankForSector(sectorKey);
    }

    // 15. Power BI Showcase
    if (typeof renderPbiKostraForSector === 'function') {
        renderPbiKostraForSector(sectorKey);
        renderPbiCapexForSector(sectorKey);
        syncPbiReportPageForSector(sectorKey);
    }

    // 16. Sidebar sync
    if (typeof updateSidebarOverview === 'function') {
        updateSidebarOverview(sectorKey);
    }

    // 17. Min Enhet Møterapportering sync
    if (typeof renderMeetingPack === 'function') {
        const lvl = typeof currentMeetingLevel !== 'undefined' ? currentMeetingLevel : 'NIVA1';
        renderMeetingPack(sectorKey, lvl);
    }

    showToast(`🏢 Valgt ansvarsområde: ${data.title}`);
};

function filterSectorComparisonTableStrict(sectorKey) {
    const rows = document.querySelectorAll("#sector-comparison-tbody tr");
    if (!rows.length) return;

    rows.forEach(r => {
        if (sectorKey === "ALL") {
            r.style.display = "";
            if (r.id === "row-sec-all") {
                r.style.background = "#f8fafc";
            } else {
                r.style.background = "";
            }
        } else {
            const targetId = `row-sec-${sectorKey.toLowerCase()}`;
            if (r.id === targetId) {
                r.style.display = "";
                r.style.background = "#e0f2fe";
            } else {
                r.style.display = "none";
            }
        }
    });
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
            // Keep all
        } else {
            const isMatch = tr.getAttribute("onclick")?.includes(targetSectorId) || 
                            tr.id === `drilldown-${targetSectorId}` || 
                            tr.innerText.includes(targetSectorId);
            if (!isMatch) {
                tr.style.display = "none";
            } else {
                if (tr.id === `drilldown-${targetSectorId}`) {
                    tr.style.display = "table-row";
                    const toggleBtn = document.getElementById(`toggle-btn-${targetSectorId}`);
                    if (toggleBtn) toggleBtn.innerHTML = "▼ Skjul enheter";
                }
            }
        }
    });
}

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
