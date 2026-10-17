"""
Ingest Municipal Advisor Knowledge Chunks into Golden Record and RAG Store.
Beriker vektordatabasen og Golden Record med kjerneveiledere og lovverk
for rollen som Kommunal Økonomirådgiver i Kristiansand kommune.
"""

import json
import sqlite3
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GOLDEN_DB_PATH = BASE_DIR / "erp_data" / "kommune_golden_record.db"
RAG_DB_PATH = BASE_DIR / "kommune-ai-guardrails" / "data" / "db" / "kommune_rag_store.db"
JSON_CHUNKS_PATH = BASE_DIR / "erp_data" / "municipal_advisor_knowledge_chunks.json"

ADVISOR_KNOWLEDGE_CHUNKS = [
    # -------------------------------------------------------------------------
    # 1. DELEGERING & FULLMAKTER I KRISTIANSAND KOMMUNE
    # -------------------------------------------------------------------------
    {
        "source_file": "bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md",
        "category": "Delegering & Fullmakter",
        "section_ref": "Delegeringsreglementet Kap. 2",
        "title": "Enhetsleders fullmakt til budsjettomdisponering innenfor egen ramme",
        "content": (
            "Enhetsledere i Kristiansand kommune (skoler, sykehjem, barnehager, VAR) har delegert budsjettdisponeringsmyndighet "
            "innenfor tildelt nettobudsjettramme. Enhetsleder kan fritt omdisponere driftsmidler mellom ulike driftsarter "
            "(f.eks. fra art 1150/1200 forbruksmateriell til art 1020 vikarer eller art 1050 ubekvemstillegg) forutsatt at: "
            "1) Enhetens samlede årsbudsjett overholdes, 2) Tiltaket ikke medfører varige driftskonsekvenser for påfølgende økonomiplanperiode, "
            "og 3) Faste stillingshjemler ikke opprettes uten godkjenning fra kommunalsjef jf. HTA § 4. "
            "Omdisponeringer registreres i Framsikt EPM i månedlige prognoserunder."
        )
    },
    {
        "source_file": "bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md",
        "category": "Delegering & Fullmakter",
        "section_ref": "Delegeringsreglementet Kap. 3",
        "title": "Anvisningsmyndighet og beløpsgrenser for fakturagodkjenning",
        "content": (
            "Anvisning av fakturaer og forpliktelser i Visma Enterprise følger Kristiansand kommunes beløpshierarki: "
            "1) Avdelingsleder / fagleder: Inntil 50 000 NOK (krever skriftlig fullmakt fra enhetsleder). "
            "2) Enhetsleder (rektor, styrer, virksomhetsleder): Inntil 500 000 NOK innenfor godkjent budsjettpost. "
            "3) Kommunalsjef / direktør for virksomhetsområde: Inntil 5 000 000 NOK. "
            "4) Kommunedirektør: Inntil 20 000 000 NOK innenfor vedtatt årsbudsjett og rammer. "
            "5) Bystyret / Formannskapet: Alle forpliktelser over 20 mill NOK eller anskaffelser som krever tilleggsbevilgning jf. Kommuneloven § 14-5. "
            "Ingen kan anvise egne utgiftsrefusjoner eller reiseruter (fire-øyne-prinsippet)."
        )
    },
    {
        "source_file": "bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md",
        "category": "Delegering & Fullmakter",
        "section_ref": "Økonomireglementet § 7",
        "title": "Prosedyre ved merforbruk og plikt til å fremme avviksnotat",
        "content": (
            "Dersom en enhet styrer mot et merforbruk over 250 000 NOK eller 3 % av årsbudsjettet ved månedsslutt eller tertialrapportering, "
            "plikter enhetsleder umiddelbart å utarbeide et standardisert 'Avviksnotat og tiltaksplan' til økonomirådgiver og kommunalsjef. "
            "Tiltaksplanen skal angi: 1) Rotårsak (sykefravær, elevtall, strøm, prisvekst), 2) Korrigerende tiltak (ansettelsesstopp, sammenslåing av grupper, "
            "reduksjon av overtid), 3) Forventet innsparingseffekt i NOK, og 4) Revidert prognose (EOY). "
            "Kommunalsjef vurderer om merforbruket kan avregnes mot sektorens omstillingsreserve eller om sak må fremmes for kommunedirektøren."
        )
    },
    {
        "source_file": "bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md",
        "category": "Delegering & Fullmakter",
        "section_ref": "Finansreglementet § 4",
        "title": "Kristiansand Finansreglement: Gjeldsgrenser og rentebinding",
        "content": (
            "Kristiansand kommunes finansreglement (vedtatt av Bystyret juni 2025) setter strenge finansielle styringsparametere: "
            "1) Netto lånegjeld som andel av brutto driftsinntekter skal ikke overstige 78 % (måltall jf. bystyrevedtak). "
            "2) Rentebindingsandel: Mellom 50 % og 70 % av kommunens samlede låneportefølje skal ha fast rente med løpetid over 1 år for å dempe rentevolatilitet. "
            "3) Motpartsrisiko: Finansielle plasseringer og derivater (renteswapper) kan kun inngås med finansinstitusjoner med minimum kredittrating A/A2. "
            "4) Likviditetsreserve: Kommunen skal til enhver tid ha en trekkrettighet / kassakredittramme på minimum 150 mill NOK."
        )
    },

    # -------------------------------------------------------------------------
    # 2. FRAMSIKT EPM & LØNNSBUDSJETTERING
    # -------------------------------------------------------------------------
    {
        "source_file": "budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md",
        "category": "Framsikt & Lønn",
        "section_ref": "Framsikt Veileder Kap. 1",
        "title": "Stillingshjemler og lønnsberegning i Framsikt (Stillingsmodulen)",
        "content": (
            "I Framsikt budsjetteres personalkostnader på stillingsnivå knyttet til stillingskode, stillingsprosent og ansiennitetstrinn. "
            "Grunnlønn konteres på art 1010 (fast lønn). Framsikt beregner automatisk: "
            "1) Arbeidsgiveravgift (AGA) på 14,1 % for Kristiansand kommune (Sone 1). "
            "2) Pensjonspremie til KLP (Kommunal Landspensjonskasse) med 14,5 % for ordinære ansatte og sykepleiere. "
            "3) Pensjonspremie til SPK (Statens pensjonskasse) med 11,2 % for lærere og pedagogisk personell i grunnskolen. "
            "4) Gruppelivs- og yrkesskadeforsikring på ca. 0,4 %. "
            "Totalt påslag for sosiale kostnader er ca. 29,0–30,5 % av brutto grunnlønn."
        )
    },
    {
        "source_file": "budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md",
        "category": "Framsikt & Lønn",
        "section_ref": "Framsikt Veileder Kap. 2",
        "title": "Vikarer, ekstravakter og overtid: Artskoder og budsjettering",
        "content": (
            "Variable personalkostnader skal budsjetteres spesifikt på egne driftsarter i Framsikt: "
            "• Art 1020: Vikarer ved sykdom, permisjoner og ferie (timelønnede vikarer og korttidsengasjementer). "
            "• Art 1040: Overtid (pålagt overtid etter AML § 10-6 med 50 % eller 100 % overtidstillegg). "
            "• Art 1050: Ubekvemstillegg (faste og variable kvelds-, natt- og helgetillegg jf. HTA kap. 1 § 5). "
            "• Art 1090: Andre godtgjørelser og kortere oppdrag. "
            "• Art 1270: Kjøp av tjenester fra eksterne vikarbyråer (Adecco, Dedicare, Randstad). "
            "Vikarbyråfakturaer skal ALDRI føres på art 1020, men på art 1270 fordi de faktureres som tjenestekjøp med moms."
        )
    },
    {
        "source_file": "budsjett-framsikt/FRAMSIKT_OMDISPONERING_OG_RAMMEREGULERING_VEILEDER.md",
        "category": "Framsikt & Lønn",
        "section_ref": "Framsikt Veileder Kap. 3",
        "title": "Håndtering av sykefraværsrefusjon fra NAV (Art 1700/1710) og bruttoprinsippet",
        "content": (
            "Kommuneloven § 14-6 fjerde ledd krever streng bruttoføring. Ved sykefravær skal: "
            "1) Lønn til sykmeldt ansatt føres som normalt på art 1010 (fast lønn). "
            "2) Vikarutgifter føres brutto på art 1020 (vikar) eller art 1040 (overtid). "
            "3) Refusjon av sykepenger og foreldrepenger fra NAV inntektsføres på art 1700 / 1710 (Refusjon fra trygdeetaten/NAV). "
            "Det er STRENGT FORBUDT å motregne NAV-refusjon direkte mot vikarutgiftene (nettoføring). "
            "Rådgiver-tips: Gjennomsnittlig saksbehandlingstid hos NAV er 4–8 uker; økonomirådgiver må månedlig avstemme "
            "ubetalte refusjonskrav i Visma mot NAV-portalen for å hindre likviditetslekkasje."
        )
    },
    {
        "source_file": "budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md",
        "category": "Framsikt & Lønn",
        "section_ref": "Periodiseringsrutine",
        "title": "Periodisering av driftsbudsjett i Framsikt gjennom året",
        "content": (
            "For å oppnå korrekt månedlig avviksanalyse må budsjettet i Framsikt periodiseres realistisk: "
            "• Lønn art 1010: Periodiseres jevnt med 1/12 hver måned (feriepenger utbetales i juni, men periodiseres jevnt regnskapsmessig). "
            "• Overtid og vikarer art 1020/1040: Vektet mot historiske fraværstoppe (januar-mars influensatopp, mai/juni eksamenstopp, høstsesong). "
            "• Strøm og oppvarming art 1160: Vektet mot fyringssesong (høy i jan-mars og nov-des, lav mai-august). "
            "• Gebyrinntekter art 1600–1640: Kvartalsvis eller månedlig fakturering jf. innkrevingssyklus."
        )
    },

    # -------------------------------------------------------------------------
    # 3. KOMMUNELOVEN & JURIDISKE RAMMER
    # -------------------------------------------------------------------------
    {
        "source_file": "budsjett-framsikt/budsjettering-kristiansand-kommune.md",
        "category": "Kommuneloven & Regelverk",
        "section_ref": "Kommuneloven § 14-5",
        "title": "Realistisk budsjettbalanse og økonomisk handleplikt ved merforbruk",
        "content": (
            "Kommuneloven § 14-5 fastslår kravet om et realistisk årsbudsjett i balanse. "
            "Dersom det i løpet av året oppstår vesentlige uforutsette avvik, merforbruk eller inntektssvikt som truer budsjettbalansen, "
            "har kommunedirektøren en lovpålagt plikt til uten ugrunnet opphold å fremme sak om endring av årsbudsjettet for Bystyret. "
            "Bystyret må enten: 1) Vedta kompenserende innsparingstiltak, 2) Omdisponere fra andre sektorer, eller "
            "3) Dekke inn merforbruket ved bruk av disposisjonsfond jf. § 14-10. "
            "Å videreføre et udekket merforbruk inn i neste år uten vedtatt inndekningsplan er lovstridig og utløser ROBEK-fare jf. § 14-28."
        )
    },
    {
        "source_file": "budsjett-framsikt/budsjettering-kristiansand-kommune.md",
        "category": "Kommuneloven & Regelverk",
        "section_ref": "Kommuneloven § 14-6",
        "title": "Bruttoprinsippet og forbud mot nettoføring i kommunale oppstillinger",
        "content": (
            "Kommuneloven § 14-6 fjerde ledd lovfester bruttoprinsippet for kommunale budsjetter og regnskaper. "
            "Alle utgifter og inntekter skal budsjetteres og føres med sitt fulle bruttobeløp. "
            "Fradrag for tilskudd, refusjoner, salgsinntekter eller gebyrer kan ikke trekkes fra utgiftsposten. "
            "Unntak gjelder kun for eksplisitt lovhjemlede oppstillinger (som netto driftsresultat i bevilgningsoversikten). "
            "Dette sikrer demokratisk transparens og kontroll med kommunens reelle ressursbruk."
        )
    },
    {
        "source_file": "budsjett-framsikt/budsjettering-kristiansand-kommune.md",
        "category": "Kommuneloven & Regelverk",
        "section_ref": "Kommuneloven § 14-10",
        "title": "Avsetninger til og bruk av disposisjonsfond og bundne fond",
        "content": (
            "Disposisjonsfond (§ 14-10) er kommunens frie reservekapital opparbeidet gjennom positive netto driftsresultater. "
            "Bystyret har enerett til å disponere over disposisjonsfondet. Fondet kan brukes til å dekke uforutsette merforbruk i drift "
            "eller finansiere egenkapital i investeringsprosjekter. "
            "Bundne driftsfond (§ 14-10 annet ledd) er midler som etter lov, forskrift eller bindende avtaler er øremerket spesifikke formål "
            "(f.eks. selvkostfond for vann/avløp, statlige prosjekttilskudd, legatmidler) og kan ALDRI brukes til å dekke generelt driftsmerforbruk."
        )
    },
    {
        "source_file": "budsjett-framsikt/budsjettering-kristiansand-kommune.md",
        "category": "Kommuneloven & Regelverk",
        "section_ref": "Kommuneloven § 14-15",
        "title": "Låneopptak, låneramme og gjeldsforvaltning i kommunen",
        "content": (
            "Kommuneloven § 14-15 gir kommunen rett til å ta opp lån til finansiering av egne varige driftsmidler (investeringer i bygg, anlegg, infrastruktur), "
            "refinansiering av eksisterende gjeld, og konvertering av kortsiktig gjeld. "
            "Det er ULOVLIG å ta opp lån for å finansiere løpende driftsutgifter. "
            "Kommunen plikter å betale et årlig minimumsavdrag på sin samlede gjeld jf. § 14-18, beregnet etter veid gjennomsnittlig levetid for anleggsmidlene. "
            "I Kristiansand kommune forvaltes låneopptak sentralt av finansseksjonen."
        )
    },
    {
        "source_file": "budsjett-framsikt/budsjettering-kristiansand-kommune.md",
        "category": "Kommuneloven & Regelverk",
        "section_ref": "Budsjett- og regnskapsforskriften § 3-4",
        "title": "Premieavvik pensjon og 7-års amortiseringsregel",
        "content": (
            "Etter forskrift om økonomiplan, årsbudsjett og årsregnskap § 3-4 skal differansen mellom faktisk innbetalt pensjonspremie "
            "(forfallspremie til KLP/SPK) og den aktuarmessig beregnede pensjonskostnaden regnskapsføres som et premieavvik. "
            "Positivt premieavvik (innbetalt premie > pensjonskostnad) utgiftsføres i balansen og inntektsføres i driftsregnskapet. "
            "Akkumulert premieavvik skal amortiseres (avskrives) lineært over maksimalt 7 år i driftsregnskapet. "
            "Dette jevner ut voldsomme pensjonssjokk over tid for kommunens driftsenheter."
        )
    },

    # -------------------------------------------------------------------------
    # 4. MOMSKOMPENSASJON & KONTO 2130 (JUSTERINGSREGLER)
    # -------------------------------------------------------------------------
    {
        "source_file": "revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md",
        "category": "MVA & Momskompensasjon",
        "section_ref": "Momskompensasjonsloven § 4",
        "title": "Rett til kompensasjon for merverdiavgift i kommunale enheter",
        "content": (
            "Kommuner har rett til kompensasjon for inngående merverdiavgift på anskaffelser av varer og tjenester etter momskompensasjonsloven § 4. "
            "Formålet er nøytralitet slik at kommunen ikke favoriserer egenproduksjon fremfor kjøp fra private aktører. "
            "Kompensasjon ytes for lovpålagte kjerneoppgaver: Grunnskole, barnehage, helse og omsorg, barnevern, administrasjon, brannvesen. "
            "Vilkår: Faktura må være stilet til Kristiansand kommune med spesifisert mva-beløp og organisasjonsnummer."
        )
    },
    {
        "source_file": "revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md",
        "category": "MVA & Momskompensasjon",
        "section_ref": "Momskompensasjonsloven § 4 annet ledd",
        "title": "Unntak fra kompensasjonsretten: Konkurranse og avgiftsplikt",
        "content": (
            "Momskompensasjonsloven § 4 annet ledd oppstiller strenge unntak der det IKKE foreligger rett til momskompensasjon: "
            "1) Virksomhet som kommunen driver som ledd i næringsvirksomhet eller som er avgiftspliktig etter merverdiavgiftsloven (f.eks. parkering, utleie av lokaler). "
            "2) Økonomisk aktivitet i konkurranse med ikke-kompensasjonsberettigede private aktører (f.eks. kommunal kafé, catering, treningssenter). "
            "3) Ytelser til privat bruk eller boligformål for ansatte. "
            "Dersom en enhet benytter et bygg til både kompensasjonsberettiget formål (skoleundervisning) og utleie til private næringsdrivende på kveldstid, "
            "må mva-kompensasjonen avkortes forholdsmessig etter areal- eller tidsbrøk."
        )
    },
    {
        "source_file": "reports/test_mva_balanse_2130_rapport.md",
        "category": "MVA & Momskompensasjon",
        "section_ref": "Momskompensasjonsloven § 7 & Mval kap. 9",
        "title": "Justeringsregler for fast eiendom over 10 år og Balansekonto 2130",
        "content": (
            "Ved nybygg, påbygging eller ombygging av fast eiendom der inngående merverdiavgift overstiger 100 000 NOK, "
            "gjelder en 10-årig justeringsperiode etter momskompensasjonsloven § 7 og merverdiavgiftsloven kapittel 9. "
            "Dersom bygget endrer formål innen 10 år (f.eks. en kommunal skolefløy leies ut til en privat aktør eller barnehage selges), "
            "utløses plikt til å tilbakebetale kompensert merverdiavgift til Skatteetaten for gjenværende tiendedeler. "
            "Balansekonto 2130 benyttes som oppgjørskonto mot Skatteetaten for løpende mva-kompensasjon (6 terminer per år). "
            "Konto 2130 må månedlig avstemmes mot innleverte mva-meldinger for å sikre at kommunen ikke har uoppgjorte mellomværender."
        )
    },

    # -------------------------------------------------------------------------
    # 5. SELVKOST (VANN, AVLØP, RENOVASJON & BYGGESAK)
    # -------------------------------------------------------------------------
    {
        "source_file": "budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md",
        "category": "Selvkost & VAR",
        "section_ref": "Selvkostforskriften § 3",
        "title": "Selvkostprinsippet og direkte vs. indirekte henførbare kostnader",
        "content": (
            "Forskrift om beregning av selvkost regulerer kommunale gebyrområder (vann, avløp, renovasjon, feiing, byggesak, oppmåling, feiegebyr). "
            "Gebyrinntektene kan ikke overstige kommunens faktiske kostnader ved å yte tjenesten (100 % selvkost). "
            "Selvkostkalkylen består av: "
            "1) Direkte driftskostnader (lønninger, vedlikehold av ledningsnett, kjemikalier, slamhåndtering, renovasjonsavtaler). "
            "2) Indirekte henførbare kostnader (forholdsmessig andel av rådhusleie, IT-systemer, HR, sentral økonomi- og arkivfunksjon etter fordelingsnøkkel). "
            "3) Kapitalkostnader: Avskrivninger på VAR-infrastruktur pluss kalkulatoriske rentekostnader."
        )
    },
    {
        "source_file": "budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md",
        "category": "Selvkost & VAR",
        "section_ref": "Selvkostforskriften § 5",
        "title": "Kalkylerente og beregning av kapitalkostnader i selvkost",
        "content": (
            "Etter selvkostforskriften § 5 fastsettes kalkylerenten for anleggsmidler og selvkostfond som: "
            "Gjennomsnittlig 5-årig swaprente i budsjettåret med et tillegg på 0,5 prosentpoeng (1/2 prosentpoeng). "
            "Renten beregnes av gjennomsnittlig restverdi på anleggsmidlene gjennom året. "
            "Renten på bundne selvkostfond godskrives fondet dersom fondet er positivt, og belastes selvkostområdet dersom fondet har et akkumulert underskudd. "
            "Dette sikrer at innbyggerne verken over- eller underbelastes for kommunens kapitalbinding."
        )
    },
    {
        "source_file": "budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md",
        "category": "Selvkost & VAR",
        "section_ref": "Selvkostforskriften § 7",
        "title": "Selvkostfond og 5-års fremføringsregel for overskudd og underskudd",
        "content": (
            "Årlige avvik mellom gebyrinntekter og faktiske selvkostutgifter avsettes til eller dekkes fra bundne selvkostfond. "
            "Etter selvkostforskriften § 7 gjelder en streng 5-års fremføringsregel: "
            "Et fremført underskudd må dekkes inn innen 5 år gjennom justering av gebyrene. "
            "Et akkumulert overskudd på selvkostfondet skal tilbakeføres til abonnentene i form av lavere gebyrer innen maksimalt 5 år. "
            "Dersom selvkostfondet vokser utover forventet reinvesteringsbehov, plikter kommunedirektøren å foreslå gebyrreduksjon i neste års gebyrregulativ."
        )
    },

    # -------------------------------------------------------------------------
    # 6. STATLIGE TILSKUDD & REFUSJONSORDNINGER
    # -------------------------------------------------------------------------
    {
        "source_file": "budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md",
        "category": "Statlige Tilskudd",
        "section_ref": "IMDi Integreringstilskudd",
        "title": "IMDi tilskudd ved bosetting av flyktninger: År 1–5 og kontering",
        "content": (
            "Integrerings- og mangfoldsdirektoratet (IMDi) yter integreringstilskudd for bosetting av personer med flyktningstatus: "
            "• Tilskudd 1 (voksne og barn): Utbetales årlig i 5 år (år 1 høyest, avtrappende år 2–5). "
            "• Tilskudd for enslige mindreårige flyktninger (EM): Særskilt forhøyet tilskudd for å dekke døgnbemannede bofellesskap. "
            "• Barnehagetilskudd og norskopplæringstilskudd for voksne innvandrere. "
            "Kontering i Kristiansand: "
            "Inntektsføres på funksjon 234 (Aktivisering og bosetting av flyktninger) under art 1700 (Statlige tilskudd). "
            "Midler som ikke er forbrukt ved årsslutt kan settes av til bundet driftsfond dersom de knytter seg til konkrete vedtatte integreringstiltak."
        )
    },
    {
        "source_file": "budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md",
        "category": "Statlige Tilskudd",
        "section_ref": "Helsedirektoratet Tilskudd",
        "title": "Helsedirektoratets tilskuddsordninger til helse, omsorg og rus",
        "content": (
            "Helsedirektoratet forvalter øremerkede tilskudd som kommunale enheter kan søke på: "
            "1) Tilskudd til styrking av helsestasjons- og skolehelsetjenesten: Konteres på funksjon 232/233 art 1700. Krever dokumentert stillingsøkning. "
            "2) Kompetanse- og innovasjonstilskudd for helse- og omsorgstjenesten: Midler til etterutdanning, sykepleieropplæring og velferdsteknologi. "
            "3) Tilskudd til kommunalt rus- og psykisk helsearbeid: Stillingsstøtte og oppsøkende virksomhet. "
            "Rapporteringskrav: Regnskapsrapport attestert av kommunerevisjonen innen 1. april påfølgende år. "
            "Ubenyttede midler må tilbakebetales til staten dersom forlengelse ikke innvilges."
        )
    },
    {
        "source_file": "budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md",
        "category": "Statlige Tilskudd",
        "section_ref": "Udir Tilskudd",
        "title": "Utdanningsdirektoratet (Udir): DeKomp, ReKomp og tilrettelegging",
        "content": (
            "Utdanningsdirektoratet yter tilskudd til grunnskoler og barnehager: "
            "• DeKomp (Desentralisert ordning for lokal kompetanseutvikling i skolen): Tildeles gjennom samarbeidsforum med Universitetet i Agder (UiA). "
            "• ReKomp (Regional ordning for barnehagekompetanse). "
            "• Tilskudd til svømmeopplæring i barnehage/skole og tilretteleggingstilskudd for minoritetselever. "
            "Konteres på funksjon 202/211 under art 1700. Økonomirådgiver må sikre at midlene ikke blandes sammen med skolens ordinære rammetildeling."
        )
    },
    {
        "source_file": "budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md",
        "category": "Statlige Tilskudd",
        "section_ref": "Husbanken & ENOVA",
        "title": "Husbanken Startlån og ENOVA energieffektiviseringstilskudd",
        "content": (
            "• Husbanken Startlån: Låneramme tildeles Kristiansand kommune for videreutlån til vanskeligstilte (funksjon 283/art 1920/1930). "
            "Kommunen plikter å sette av midler til tapsfond for startlån (bundet fond) for å dekke eventuelle mislighold. "
            "• ENOVA-tilskudd: Støtte til energi- og klimatiltak i eksisterende formålsbygg (ventilasjon, varmepumper, solceller, SD-anlegg). "
            "Kompensasjon utbetales etter ferdigattest og tredjepartsverifisering av oppnådd kWh-reduksjon. Føres i investeringsregnskapet art 2700."
        )
    },

    # -------------------------------------------------------------------------
    # 7. DRIFT VS. INVESTERING (KRS 1 & KRS 4)
    # -------------------------------------------------------------------------
    {
        "source_file": "revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md",
        "category": "Drift vs Investering",
        "section_ref": "KRS 4 Avgrensning",
        "title": "KRS 4: Avgrensning mellom drift og investering (vedlikehold vs påkostning)",
        "content": (
            "God kommunal regnskapsskikk (KRS 4) trekker et strengt skille mellom driftsutgifter og investeringsutgifter: "
            "1) Løpende vedlikehold (Drift art 1230): Utgifter for å opprettholde anlegget i dets opprinnelige standard og funksjon "
            "(f.eks. maling av fasade, utskifting av slitte gulvbelegg, rutinemessig takreparasjon). "
            "2) Påkostning / Rehabilitering (Investering art 2300): Utgifter som hever anleggets standard, øker levetiden vesentlig utover opprinnelig prosjektert levetid, "
            "eller endrer byggets funksjon (f.eks. etterisolering med energiklasseheving, installasjon av heis, ombygging fra kontor til klasserom). "
            "Å belaste lånefinansiert investeringsregnskap med ordinært vedlikehold er lovstridig jf. Kommuneloven § 14-9 og § 14-15!"
        )
    },
    {
        "source_file": "revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md",
        "category": "Drift vs Investering",
        "section_ref": "KRS 1 Anleggsmidler",
        "title": "KRS 1: Aktiveringskriterier og avskrivningsregler for anleggsmidler",
        "content": (
            "Etter KRS 1 og kommuneloven skal et formuesgode aktiveres i investeringsregnskapet og balansen dersom det: "
            "1) Har en vesentlig anskaffelseskostnad: I Kristiansand kommune er nedre aktiveringsgrense 100 000 NOK (ekskl. mva). "
            "2) Har en forventet økonomisk levetid på minst 3 år. "
            "Innkjøp under 100 000 NOK skal utgiftsføres direkte i driftsregnskapet som inventar/utstyr (art 1120/1200) selv om levetiden er lang. "
            "Aktiverte anleggsmidler skal avskrives lineært i driftsregnskapet over levetiden (f.eks. 5 år for IKT, 20 år for biler/maskiner, 40-50 år for formålsbygg)."
        )
    },

    # -------------------------------------------------------------------------
    # 8. PARTSSAMARBEID, HTA § 4 & ARBEIDSMILJØLOVEN (TURNUS)
    # -------------------------------------------------------------------------
    {
        "source_file": "reports/budsjettansvarlige_arkiv/5210-ENH-402/03_Saksdokumenter_og_Maler/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md",
        "category": "Arbeidsrett & Turnus",
        "section_ref": "HTA § 4",
        "title": "Hovedtariffavtalen (HTA) § 4: Arbeidsgivers drøftingsplikt ved bemanningsgrep",
        "content": (
            "Før arbeidsgiver iverksetter tiltak som har vesentlig betydning for bemanning, arbeidsmiljø eller organisering, "
            "har arbeidsgiver en ubetinget drøftingsplikt med de tillitsvalgte etter HTA § 4 og Hovedavtalen del B § 3. "
            "Typiske situasjoner for økonomirådgiver og leder: "
            "• Ansettelsesstopp eller vikarstopp for å hente inn merforbruk. "
            "• Omlegging av turnusplaner, fjerning av faste vakter, eller sammenslåing av avdelinger. "
            "• Endring i oppgaver og stillingsbrøker. "
            "Det skal skrives formell drøftingsprotokoll med de tillitsvalgte (Fagforbundet, NSF, Delta) FØR vedtak fattes. "
            "Manglende drøfting medfører tariffbrudd og kan stoppe tiltakene juridisk."
        )
    },
    {
        "source_file": "reports/budsjettansvarlige_arkiv/5210-ENH-402/03_Saksdokumenter_og_Maler/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md",
        "category": "Arbeidsrett & Turnus",
        "section_ref": "AML § 10-12 & Langvakter",
        "title": "AML § 10-12 og langvakter (12,5 timer) i helseturnus: Økonomiske effekter",
        "content": (
            "I døgntjenester (sykehjem, bo- og omsorgssentre, bofellesskap) har innføring av langvakter (12,5 timer i helger) "
            "betydelige økonomiske og faglige effekter: "
            "1) Juridisk hjemmel: Arbeid utover 10 timer i døgnet krever skriftlig avtale med tillitsvalgte etter Arbeidsmiljøloven § 10-12 fjerde ledd. "
            "2) Økonomisk virkning: Færre vaktbytter per helg reduserer overleveringstid, kutter overtid (art 1040) og reduserer behovet for helgevikarer (art 1020). "
            "3) Kostnadskomponenter: Krever ofte helgetillegg eller lønnskompensasjon jf. lokal særavtale. "
            "Økonomirådgiveren må lage What-If kalkyle på helårseffekt før avtale inngås."
        )
    },

    # -------------------------------------------------------------------------
    # 9. ANSKAFFELSER & INNKJØP (ANSKAFFELSESSTRATEGI 2026–2030)
    # -------------------------------------------------------------------------
    {
        "source_file": "bruker-guides/BUDSJETTANSVARLIGE_OG_DELEGERINGSKATALOG_2026.md",
        "category": "Anskaffelser & Innkjøp",
        "section_ref": "Anskaffelsesstrategi 2026-2030",
        "title": "Terskelverdier for innkjøp og obligatorisk bruk av kommunale rammeavtaler",
        "content": (
            "Alle innkjøp i Kristiansand kommune skal skje i henhold til Lov om offentlige anskaffelser (LOA) og kommunens innkjøpsreglement: "
            "1) Rammeavtaler: Dersom kommunen har inngått rammeavtale (forbruksmateriell, PC-utstyr, møbler, håndverkertjenester, vikarbyrå), "
            "er samtlige enheter FORPLIKTET til å handle fra avtalepartneren i Visma Innkjøp. Lojalitetsbrudd medfører merkostnader og er tariff-/avtalebrudd. "
            "2) Terskler for enkeltanskaffelser uten rammeavtale: "
            "• Under 100 000 NOK: Direkte bestilling, men krever at leder sikrer markedsmessige betingelser (anbefalt 2-3 tilbud). "
            "• 100 000 – 1,4 mill NOK (nasjonal terskel): Forenklet tilbudskonkurranse kunngjort på Doffin. "
            "• Over 1,4 mill NOK (varer/tjenester) / Over 45 mill NOK (bygg/anlegg): EØS-kunngjøring. "
            "3) Miljøkrav (LOA § 5a): Obligatorisk minimum 30 % vekting på klima og miljø i alle anskaffelser."
        )
    },

    # -------------------------------------------------------------------------
    # 10. POLITISK SAKSFREMLEGG & ÅRSHJUL FOR RÅDGIVERE
    # -------------------------------------------------------------------------
    {
        "source_file": "templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.md",
        "category": "Politisk Saksfremlegg",
        "section_ref": "Kommuneloven § 13-1",
        "title": "Krav til politiske saksfremlegg om budsjettendring og tertialrapportering",
        "content": (
            "Saksfremlegg til Bystyret og Formannskapet jf. Kommuneloven § 13-1 om budsjettjusteringer skal ha fast oppbygging: "
            "1) 'Forslag til vedtak': Konsise vedtakspunkter med bevilgninger spesifisert i hele 1 000 NOK per sektor/ansvarssted. "
            "2) 'Bakgrunn og faktagrunnlag': Regnskapstall per M04/M08, avviksanalyse og underliggende drivere. "
            "3) 'Vurdering og økonomiske konsekvenser': Konsekvens for netto driftsresultat, disposisjonsfond og lånegjeld. "
            "4) 'Inndekningsplan': Hvor skal pengene tas fra (kutt i andre sektorer, økte skatteinntekter eller disposisjonsfond). "
            "5) 'Klima- og miljøvurdering' og 'Medvirkning/partssamarbeid' jf. HTA § 4. "
            "Saken må være signert av kommunedirektøren før utsendelse til politisk behandling."
        )
    },
    {
        "source_file": "bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md",
        "category": "Styringskalender & Årshjul",
        "section_ref": "Styringskalender 2026",
        "title": "Månedshjul og milepæler for kommunale økonomirådgivere i Kristiansand",
        "content": (
            "Viktige milepæler i det kommunale styringsåret for økonomirådgiveren: "
            "• Januar/Februar: Årsavslutning, periodisering, avstemming av Balansekonto 2130 og oversendelse av årsregnskap til Kommunerevisjonen (frist 22. februar). "
            "• Mars/April: Behandling av årsregnskap i formannskapet. 1. tertialrapportering per 30. april (T1) med revidert helårsprognose i Framsikt. "
            "• Mai/Juni: Behandling av T1 i Bystyret. Start på Handlings- og økonomiplan (HØP 2027–2030) i enhetene. Lønnsoppgjør og regulering. "
            "• August/September: 2. tertialrapportering per 31. august (T2). Innlevering av budsjettinnspill fra enhetene i Framsikt. "
            "• Oktober/November: Kommunedirektørens forslag til HØP og årsbudsjett legges frem. Formannskapets innstilling. "
            "• Desember: Bystyrets endelige budsjettvedtak, tildeling av rammer til enhetene og oppstart av forberedelser til årsoppgjør."
        )
    }
]


def ingest_advisor_knowledge():
    print(f"==================================================================")
    print(f"Ingesting {len(ADVISOR_KNOWLEDGE_CHUNKS)} Municipal Advisor Knowledge Chunks...")
    print(f"==================================================================")

    # 1. Save JSON artifact
    with open(JSON_CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(ADVISOR_KNOWLEDGE_CHUNKS, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON chunks to: {JSON_CHUNKS_PATH}")

    # 2. Ingest into Golden Record DB
    if GOLDEN_DB_PATH.exists():
        conn = sqlite3.connect(str(GOLDEN_DB_PATH))
        cur = conn.cursor()

        # Ensure table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS legal_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                category TEXT NOT NULL,
                section_ref TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert or update
        inserted_count = 0
        for chunk in ADVISOR_KNOWLEDGE_CHUNKS:
            # Check if exists
            cur.execute(
                "SELECT id FROM legal_chunks WHERE title = ? AND category = ?",
                (chunk["title"], chunk["category"])
            )
            row = cur.fetchone()
            if not row:
                cur.execute(
                    """
                    INSERT INTO legal_chunks (source_file, category, section_ref, title, content)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (chunk["source_file"], chunk["category"], chunk["section_ref"], chunk["title"], chunk["content"])
                )
                inserted_count += 1
            else:
                cur.execute(
                    """
                    UPDATE legal_chunks
                    SET source_file = ?, section_ref = ?, content = ?
                    WHERE id = ?
                    """,
                    (chunk["source_file"], chunk["section_ref"], chunk["content"], row[0])
                )

        # Ensure FTS table exists in Golden DB
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS legal_fts USING fts5(
                title,
                content,
                category,
                section_ref,
                content='legal_chunks',
                content_rowid='id'
            )
        """)
        # Rebuild FTS
        cur.execute("INSERT INTO legal_fts(legal_fts) VALUES('rebuild')")

        conn.commit()
        total_chunks = cur.execute("SELECT count(*) FROM legal_chunks").fetchone()[0]
        conn.close()
        print(f"Golden Record ({GOLDEN_DB_PATH.name}): inserted {inserted_count} new chunks, total now: {total_chunks}")

    # 3. Ingest into RAG Store DB
    if RAG_DB_PATH.exists():
        conn = sqlite3.connect(str(RAG_DB_PATH))
        cur = conn.cursor()

        inserted_rag = 0
        for chunk in ADVISOR_KNOWLEDGE_CHUNKS:
            cur.execute(
                "SELECT id FROM legal_chunks WHERE title = ? AND category = ?",
                (chunk["title"], chunk["category"])
            )
            row = cur.fetchone()
            if not row:
                cur.execute(
                    """
                    INSERT INTO legal_chunks (source_file, category, section_ref, title, content)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (chunk["source_file"], chunk["category"], chunk["section_ref"], chunk["title"], chunk["content"])
                )
                inserted_rag += 1
            else:
                cur.execute(
                    """
                    UPDATE legal_chunks
                    SET source_file = ?, section_ref = ?, content = ?
                    WHERE id = ?
                    """,
                    (chunk["source_file"], chunk["section_ref"], chunk["content"], row[0])
                )

        # Rebuild FTS in RAG store
        try:
            cur.execute("INSERT INTO legal_fts(legal_fts) VALUES('rebuild')")
        except Exception as e:
            print("Note on RAG FTS rebuild:", e)

        conn.commit()
        total_rag = cur.execute("SELECT count(*) FROM legal_chunks").fetchone()[0]
        conn.close()
        print(f"RAG Store ({RAG_DB_PATH.name}): inserted {inserted_rag} new chunks, total now: {total_rag}")

    print("Knowledge Ingestion Completed Successfully!")


if __name__ == "__main__":
    ingest_advisor_knowledge()
