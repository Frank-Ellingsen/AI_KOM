# tools/inject_budsjett_js.py
# -*- coding: utf-8 -*-
"""
Injisering av JavaScript-kjerne og datamodeller for Budsjettmodulen i index.html.
"""

import sys

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    content = f.read()

JS_BLOCK = r"""
    /* ==========================================================================
       BUDSJETTMODUL: FRAMSIKT EPM, STILLINGS- OG LØNNSMOTOR, SELVKOST OG ÅRSHJUL
       Basert på Bystyrets økonomireglement og Framsikt-veilederne
       ========================================================================== */

    const BUDSJETT_POSITIONS_DATA = [
        { id: "ST-202-01", tittel: "Rektor / Enhetsleder", ansatt: "Knut O. Myhre", sektor: "Oppvekst", sektor_id: "OPPVEKST", pensjon: "SPK", brok: 100, fastlonn: 940000, sosiale: 284300 },
        { id: "ST-202-02", tittel: "Avdelingsleder / Lektor", ansatt: "Astrid Tveit", sektor: "Oppvekst", sektor_id: "OPPVEKST", pensjon: "SPK", brok: 100, fastlonn: 745000, sosiale: 225300 },
        { id: "ST-401-01", tittel: "Spesialsykepleier natt", ansatt: "Marit Solberg", sektor: "Helse og mestring", sektor_id: "HELSE", pensjon: "KLP", brok: 100, fastlonn: 665000, sosiale: 236800 },
        { id: "ST-401-02", tittel: "Helsefagarbeider turnus", ansatt: "Einar Løvås", sektor: "Helse og mestring", sektor_id: "HELSE", pensjon: "KLP", brok: 80, fastlonn: 432000, sosiale: 153800 },
        { id: "ST-501-01", tittel: "Overingeniør Vann & Avløp", ansatt: "Lars K. Strand", sektor: "By- og stedsutvikling", sektor_id: "BYUTVIKLING", pensjon: "KLP", brok: 100, fastlonn: 875000, sosiale: 311500 },
        { id: "ST-502-01", tittel: "Senior Saksbehandler Bygg", ansatt: "Ingrid Bakke", sektor: "By- og stedsutvikling", sektor_id: "BYUTVIKLING", pensjon: "KLP", brok: 100, fastlonn: 685000, sosiale: 243900 },
        { id: "ST-301-01", tittel: "Kulturkonsulent Kilden", ansatt: "Tone Lind", sektor: "Kultur og dialog", sektor_id: "KULTUR", pensjon: "KLP", brok: 100, fastlonn: 630000, sosiale: 224300 },
        { id: "ST-101-01", tittel: "Senior Controller Økonomi", ansatt: "Frank Ellingsen", sektor: "Økonomistyring", sektor_id: "OKONOMI", pensjon: "KLP", brok: 100, fastlonn: 895000, sosiale: 318600 }
    ];

    const SELVKOST_SERVICES_DATA = {
        "VANN": {
            tittel: "💧 Funksjon 3400: Vannforsyning — Drikkevann og Ledningsnett",
            direkte: 142500000,
            henforing: 8200000,
            avskrivning: 44800000,
            restverdi: 820000000,
            rente_sats: 0.040,
            inntekter: 4500000,
            gebyrinntekt: 223800000,
            fond_primo: 12400000,
            fremforing_ar: "År 2 av 5",
            lov: "Kommuneloven § 15-1 & Drikkevannsforskriften"
        },
        "AVLOEP": {
            tittel: "🚽 Funksjon 3450: Avløpshåndtering — Renseanlegg & Pumpestasjoner",
            direkte: 185200000,
            henforing: 11400000,
            avskrivning: 78500000,
            restverdi: 1950000000,
            rente_sats: 0.040,
            inntekter: 5100000,
            gebyrinntekt: 348000000,
            fond_primo: -14200000,
            fremforing_ar: "År 3 av 5 (Investeringsplan 2027–2030: 2 mrd kr)",
            lov: "Forurensningsloven & Kommuneloven § 15-1"
        },
        "RENOVASJON": {
            tittel: "♻️ Funksjon 3500: Renovasjon & Avfallshåndtering (Avfall Sør)",
            direkte: 128400000,
            henforing: 3600000,
            avskrivning: 9200000,
            restverdi: 95000000,
            rente_sats: 0.040,
            inntekter: 2100000,
            gebyrinntekt: 142900000,
            fond_primo: 4800000,
            fremforing_ar: "År 1 av 5",
            lov: "Forurensningsloven § 30 og § 34"
        },
        "BYGGESAK": {
            tittel: "📐 Funksjon 3600: Byggesak, Oppmåling og Geodata",
            direkte: 41200000,
            henforing: 4100000,
            avskrivning: 1800000,
            restverdi: 18000000,
            rente_sats: 0.040,
            inntekter: 900000,
            gebyrinntekt: 46920000,
            fond_primo: 1100000,
            fremforing_ar: "År 2 av 5",
            lov: "Plan- og bygningsloven § 33-1 & Eierseksjonsloven"
        }
    };

    const BUDSJETT_ARSHJUL_DATA = [
        {
            id: 1,
            periode: "Mai – Juni",
            tittel: "Rammeavklaringer & 1. Tertial",
            status: "Fullført",
            status_color: "var(--success-green)",
            rolle: "Kommunedirektørens ledergruppe & Bystyret",
            desc: "Avklaring av demografiberegninger for skole/barnehage og omsorg. Behandling av 1. tertialrapport og oppdatering av 4-årige HØP-rammer.",
            oppgaver: [
                "Demografifremskriving fra SSB analyseres per resultatenhet",
                "Kommunedirektørens retningslinjer for lønnsvekst og prisvekst fastsettes",
                "1. tertialrapport fremlegges for Bystyret med oppdaterte skatteprognoser"
            ],
            hjemmel: "Kommuneloven § 14-5 & § 14-10"
        },
        {
            id: 2,
            periode: "Primo August",
            tittel: "HR-Data Eksport til Framsikt",
            status: "Fullført",
            status_color: "var(--success-green)",
            rolle: "Lønnsavdeling & Økonomi",
            desc: "Oppdaterte person- og stillingsdata importeres fra Visma Enterprise / Unit4 til Framsikt Årsbudsjettmodul. Excel-maler klargjøres for utsending.",
            oppgaver: [
                "Avstemming av faste stillingshjemler mot faktisk ansattliste",
                "Verifisering av stillingskoder, ansiennitet og pensjonstilhørighet (SPK/KLP)",
                "Klargjøring og låsing av felles satser for AGA (14,1 %) og feriepenger"
            ],
            hjemmel: "Økonomireglement for Kristiansand kommune kap. 3"
        },
        {
            id: 3,
            periode: "25. August",
            tittel: "Utsending av Excel-Maler",
            status: "Fullført",
            status_color: "var(--success-green)",
            rolle: "Økonomirådgivere → Seksjonsledere",
            desc: "Excel-maler per seksjon og kostnadssted distribueres til seksjons- og enhetsledere sammen med tildelte budsjettrammer og retningslinjer.",
            oppgaver: [
                "Distribusjon av Excel bemanningsplan per resultatansvar",
                "Gjennomgang av krav til driftseffektivisering og omstillingskrav",
                "Veiledning om uforanderlige stillings-IDer ved senere gjeninnlesing"
            ],
            hjemmel: "Delegeringsreglement Kristiansand kommune"
        },
        {
            id: 4,
            periode: "10. September",
            tittel: "Seksjonsledernes Frist",
            status: "Fullført",
            status_color: "var(--success-green)",
            rolle: "Seksjonsledere",
            desc: "Frist for seksjonsledere til å ferdigstille neste års stillings- og bemanningsplan, registrere vikar-/overtidspotter og lese inn i Framsikt.",
            oppgaver: [
                "Planlagte fødsels- og utdanningspermisjoner registreres med startmåned",
                "Vakanser og nyrekrutteringer bekreftes med måned for tilsetting",
                "Innlesing av oppdatert Excel-mal i Framsikt og kontroll av summer"
            ],
            hjemmel: "Kommuneloven § 13-1 (Enhetsleders ansvar)"
        },
        {
            id: 5,
            periode: "20. September",
            tittel: "Enhetsledernes Godkjenning",
            status: "Fullført",
            status_color: "var(--success-green)",
            rolle: "Enhetsledere / Rektorer",
            desc: "Enhetsledere avstemmer hele enhetens budsjett i Framsikt, kontrollerer at rammen holder, og godkjenner i systemet.",
            oppgaver: [
                "Kvalitetskontroll av at sum lønn, varekjøp og refusjoner er i balanse",
                "Avsjekk av bruttoføring: vikarutgifter (1020) ikke nettet mot NAV-refusjon (1690)",
                "Formell godkjenning av enhetsbudsjett i Framsikt (Stage-Gate Port 4)"
            ],
            hjemmel: "Kommuneloven § 14-5 (Budsjettbalanse)"
        },
        {
            id: 6,
            periode: "30. September",
            tittel: "Kommunalsjefens Godkjenning",
            status: "Fullført",
            status_color: "var(--success-green)",
            rolle: "Direktører / Kommunalsjefer",
            desc: "Kommunalsjefene ferdigstiller sitt samlede virksomhetsområde. Kvalitetssikring av selvkostkalkyler (Vann, avløp, renovasjon, byggesak) og investeringer.",
            oppgaver: [
                "Konsolidering av kommunalområdets enheter i Framsikt",
                "Avstemming av selvkostkalkyler og regulering av bundet fond (1530/1930)",
                "Samordning av 4-årig investeringsbudsjett opp mot lånetaket (8,8 mrd kr)"
            ],
            hjemmel: "Selvkostforskriften § 6 & Kommuneloven § 14-6"
        },
        {
            id: 7,
            periode: "Ultimo Oktober",
            tittel: "HØP & Årsbudsjett Offentliggjøres",
            status: "AKTIV NÅ",
            status_color: "#0284c7",
            rolle: "Kommunedirektøren",
            desc: "Siste kvalitetssikring i Kommunedirektørens ledergruppe. Kommunedirektørens forslag til Handlings- og økonomiplan (HØP 2027–2030) og årsbudsjett legges frem 25. oktober.",
            oppgaver: [
                "Sluttbehandling i Kommunedirektørens ledergruppe (KDLG)",
                "Offentlig publisering av HØP-dokument, saksfremlegg og Framsikt-portal",
                "Presseorientering og oversendelse til de folkevalgte organene"
            ],
            hjemmel: "Kommuneloven § 14-3 & § 14-4"
        },
        {
            id: 8,
            periode: "Nov – Desember",
            tittel: "Politisk Behandling & Bystyrevedtak",
            status: "Kommende",
            status_color: "var(--text-muted)",
            rolle: "Formannskap, Fagutvalg & Bystyret",
            desc: "Fagutvalg og formannskap behandler forslaget. Midten av desember fatter Bystyret endelig vedtak. Budsjettet registreres i Unit4 innen 31. desember.",
            oppgaver: [
                "Primo nov: Orientering for formannskapet og høring i fagutvalgene",
                "Primo des: Formannskapet avgir endelig innstilling",
                "Midtdesember: Bystyret fatter bindende budsjettvedtak, skatter og gebyrer",
                "31. des: Endelig budsjett lastes over til regnskapssystemet Unit4 for neste regnskapsår"
            ],
            hjemmel: "Kommuneloven § 14-3, § 14-4 og § 14-6"
        }
    ];

    const KOSTRA_DRIFTSARTER_DATA = [
        { art: "1010", navn: "Fast lønn / fastlønn", cat: "LONN", modul: "Stillingsoversikt", desc: "Bruttolønn for faste stillinger og faste engasjementer. Beregnes automatisk per stilling/ansatt i Framsikt.", typisk: "Lærere, sykepleiere, ingeniører, saksbehandlere", regel: "Hovedregel for faste årsverk. Sykefravær skal ALDRI redusere Art 1010." },
        { art: "1020", navn: "Lønn til vikarer", cat: "LONN", modul: "Konto / Pot", desc: "Lønn til timelønte sykevikarer og kortere vikariater ved fravær. Budskjetteres som kronepott per ansvar.", typisk: "Lærervikarer, pleievikarer ved korttidsfravær", regel: "Må ALDRI nettføres mot fastlønn eller mot NAV-refusjon (1690)." },
        { art: "1030", navn: "Lønn til ekstrahjelp", cat: "LONN", modul: "Konto / Pot", desc: "Timelønte ekstrahjelper ved sesongtopper, snøbrøyting, prosjekter eller uforutsett arbeidsmengde.", typisk: "Badevakter, sommerhjelper, sesongarbeidere park", regel: "Genererer feriepenger (12%) og AGA (14,1%)." },
        { art: "1040", navn: "Lønn til lærlinger", cat: "LONN", modul: "Stilling / Pot", desc: "Lønn og godtgjørelse til lærlinger etter gjeldende læretekst og lærlingelønnssatser.", typisk: "Helsefaglærlinger, IKT-lærlinger, barne- og ungdomsarbeidere", regel: "Knyttes mot sentral tilskuddsordning for lærlinger." },
        { art: "1050", navn: "Annen lønn og godtgjørelser", cat: "LONN", modul: "Stilling / Pot", desc: "Trekkpliktige uregelmessige tillegg, utrykningstillegg, klesgodtgjørelse og stasjonsvakter.", typisk: "Klesgodtgjørelse, utrykning brann/legevakt, telefonkompensasjon", regel: "Inngår i grunnlag for feriepenger og AGA." },
        { art: "1090", navn: "Overtid og ubekvem tid", cat: "LONN", modul: "Konto / Pot", desc: "Overtidsbetaling jf. HTA, samt turnustillegg (kvelds-, natt- og helgetillegg, lørdag/søndag).", typisk: "Kveldstillegg hjemmesykepleie, beredskapsvakt VAR, helgetillegg omsorg", regel: "Turnustillegg må baseres på godkjente bemanningsplaner i Visma." },
        { art: "1099", navn: "Påløpt feriepengeavsetning", cat: "LONN", modul: "Automatisk (System)", desc: "Regnskapsmessig avsetning for opptjente feriepenger (12,0 % under 60 år / 14,3 % over 60 år).", typisk: "Lovpålagt feriepengeavsetning for alle kommunalt ansatte", regel: "Framsikt beregner automatisk AGA (14,1 %) av feriepengeavsetningen." },
        { art: "1200", navn: "Pensjonsinnskudd (KLP/SPK)", cat: "LONN", modul: "Automatisk (Stilling)", desc: "Arbeidsgivers lovpålagte pensjonspremie. Framsikt beregner ut fra pensjonskassetilhørighet.", typisk: "SPK for lærere/pedagoger, KLP for helse, teknisk og administrasjon", regel: "Premiesatser fastsettes sentralt (SPK ~13,8 %, KLP ~15,2 %)." },
        { art: "1210", navn: "Arbeidsgiveravgift (AGA)", cat: "LONN", modul: "Automatisk (System)", desc: "AGA av lønn, tillegg og pensjon. Beregnes ut fra kommunens sone (14,1 % / Sone 1 for Kristiansand).", typisk: "Statlig arbeidsgiveravgift på alle lønns- og pensjonsutgifter", regel: "Beregnes av (Lønn 1010-1090 + Feriepenger 1099 + Pensjon 1200)." },
        { art: "1220", navn: "Yrkesskade / gruppeliv", cat: "LONN", modul: "Automatisk (Stilling)", desc: "Lovpålagte personalforsikringer og gruppelivsordninger for kommunalt ansatte.", typisk: "Ulykkesforsikring, yrkesskadeforsikring gjennom KLP Skade", regel: "Periodiseres månedlig i Framsikt." },
        { art: "1100", navn: "Kontormateriell og trykksaker", cat: "VARE", modul: "Detaljbudsjett", desc: "Standard rekvisita, papir, trykking av brosjyrer og profilmateriell.", typisk: "Kopipapir, toner, trykking av utvalgspapirer til bystyret", regel: "Følger felles innkjøpsavtale via Agder Innkjøpssamarbeid." },
        { art: "1115", navn: "Undervisningsmateriell", cat: "VARE", modul: "Detaljbudsjett", desc: "Lærebøker, digitale læremidler, forbruksmateriell i skoler og barnehager.", typisk: "Skolebøker, NEON elevlisenser, formingsrekvisita, musikkutstyr", regel: "Brukes utelukkende under funksjon 2010–2220 i Oppvekst." },
        { art: "1120", navn: "Møbler, inventar og utstyr", cat: "VARE", modul: "Detaljbudsjett", desc: "Løsøre, møbler og utstyr under aktiveringsgrensen for investering (under 100 000 kr).", typisk: "Kontorstoler, heve/senk-pulter, sykehjemssenger, elevpulter", regel: "Kjøp over 100 000 kr med levetid >3 år skal vurderes for investering (klasse 2)." },
        { art: "1130", navn: "Telefoni og datakommunikasjon", cat: "VARE", modul: "Detaljbudsjett", desc: "Mobiltelefoner, linjeleie, bredbånd og fasttelefoni for kommunale lokasjoner.", typisk: "Tjenestemobiler, fiberlinjer til omsorgssentre og skoler", regel: "Telenor-rammeavtale forvaltes av IKT-avdelingen." },
        { art: "1140", navn: "Annonser og informasjon", cat: "VARE", modul: "Detaljbudsjett", desc: "Offentlige kunngjøringer, annonsering av reguleringsplaner, stillingsutlysninger.", typisk: "Stillingsutlysninger på Finn, kunngjøring av planhøringer i Fædrelandsvennen", regel: "Gebyrpliktige planannonser henføres til selvkost funksjon 3600." },
        { art: "1150", navn: "Opplæring og kompetanseheving", cat: "VARE", modul: "Detaljbudsjett", desc: "Kursavgifter, etterutdanning, seminarer og sertifiseringer for ansatte.", typisk: "Videreutdanning sykepleiere, Framsikt-opplæring, HMS-kurs", regel: "Kompensasjon for tapt fritid føres på lønnsart 1050, ikke 1150." },
        { art: "1160", navn: "Skyss- og reiseutgifter (oppg.pl.)", cat: "VARE", modul: "Detaljbudsjett", desc: "Oppgavepliktig kilometergodtgjørelse ved bruk av privat bil i tjenesten.", typisk: "Kjøregodtgjørelse for hjemmesykepleiere, tilsynsførere, feltinspektører", regel: "Føres etter statens satser i Visma Lønn." },
        { art: "1170", navn: "Reiseutgifter (ikke oppg.pl.)", cat: "VARE", modul: "Detaljbudsjett", desc: "Tog, fly, overnatting, offentlig transport og diett ved tjenestereiser.", typisk: "Deltakelse på KS-konferanser, nasjonale fagsamlinger, revisjonskurs", regel: "Kommunens reisepolicy krever tog på strekningen Kr.sand–Oslo/Stavanger." },
        { art: "1180", navn: "Energi, strøm og fjernvarme", cat: "VARE", modul: "Detaljbudsjett", desc: "Elektrisk kraft, nettleie, brensel og fjernvarme for kommunale formålsbygg.", typisk: "Strøm til rådhus, omsorgssentre, skoler, idrettshaller, gatelys", regel: "Avstemmes mot Eiendomsavdelingens volumprognoser (kWh)." },
        { art: "1190", navn: "Husleie og leie av lokaler", cat: "VARE", modul: "Detaljbudsjett", desc: "Ekstern leie av formålsbygg, kontorlokaler, moduler og idrettsanlegg.", typisk: "Leie av eksterne barnehagelokaler, legesentre, midlertidige skolepaviljonger", regel: "Må skilles fra intern husleieavregning." },
        { art: "1200", navn: "Forbruksmateriell og råvarer", cat: "VARE", modul: "Detaljbudsjett", desc: "Innsatsfaktorer til drift, helseartikler, kjemikalier og matvarer.", typisk: "Medisinsk forbruksmateriell, kjemikalier til vannverk, strøsand for vei", regel: "Inngår i direkte driftsutgifter på selvkostområdene (VAR)." },
        { art: "1220", navn: "Vedlikehold av maskiner/utstyr", cat: "VARE", modul: "Detaljbudsjett", desc: "Service, reparasjon og vedlikehold av teknisk utstyr og kjøretøypark.", typisk: "Service på legevaktbiler, brøyteutstyr, heiser, medisinsk-teknisk utstyr", regel: "Årlige servicekontrakter periodiseres jevnt." },
        { art: "1230", navn: "Vedlikeholdstjenester bygg", cat: "VARE", modul: "Detaljbudsjett", desc: "Løpende bygningsmessig vedlikehold utført av eksterne håndverkere.", typisk: "Rørlegger-, elektriker- og malertjenester i skoler og sykehjem", regel: "Større oppgraderinger som forlenger levetid vurderes for klasse 2." },
        { art: "1240", navn: "Serviceavtaler, IT-lisenser & SaaS", cat: "VARE", modul: "Detaljbudsjett", desc: "Årlige skytjenestelisenser, IT-vedlikehold og programvareavtaler.", typisk: "Lisenser for Framsikt, Visma Enterprise, Microsoft 365, Agresso", regel: "Felleslisenser henføres delvis til selvkost som indirekte kostnader." },
        { art: "1250", navn: "Konsulenttjenester og revisjon", cat: "VARE", modul: "Detaljbudsjett", desc: "Kjøp av ekstern spesialistkompetanse, prosjektering, juridisk bistand og revisjon.", typisk: "Advokatbistand, arkitekt, Agder Kommunerevisjon IKS", regel: "Konsulentkjøp krever særskilt begrunnelse jf. innkjøpsreglementet." },
        { art: "1260", navn: "Renhold og vaskeritjenester", cat: "VARE", modul: "Detaljbudsjett", desc: "Renholdstjenester kjøpt fra eksterne samt vask av tøy/tekstiler.", typisk: "Eksternt vaskeri for sykehjemstøy, vindusvask, spesialrenhold", regel: "Avstemmes mot renholdskontrakter per bygg." },
        { art: "1270", navn: "Andre kjøp av driftstjenester", cat: "VARE", modul: "Detaljbudsjett", desc: "Øvrige driftsavtaler, vakthold, snøbrøyting, renovasjonsfrakt og vektertjenester.", typisk: "Vintervedlikehold/brøyting veinett, vektertjenester rådhus og skoler", regel: "Vinterdrift budsjetteres med normalårskostnad." },
        { art: "1300", navn: "Kjøp av tjenester fra staten", cat: "OVERFORING", modul: "Overføringer", desc: "Betaling for statlige spesialisttjenester eller institusjonsplasser.", typisk: "Barnevernsinstitusjoner (Bufetat), statlige oppholdsbetalinger", regel: "Statlige satser legges til grunn i budsjettet." },
        { art: "1350", navn: "Kjøp fra andre kommuner", cat: "OVERFORING", modul: "Overføringer", desc: "Vertskommunesamarbeid, legevaktsamarbeid og gjesteelevsoppgjør.", typisk: "Gjesteelever i Vennesla/Lillesand, felles IKT-tjenester", regel: "Avstemmes mot nabokommunenes fakturagrunnlag." },
        { art: "1370", navn: "Tilskudd til private og ideelle", cat: "OVERFORING", modul: "Overføringer", desc: "Lovpålagte driftstilskudd til private barnehager, private skoler og frivillighet.", typisk: "Tilskudd til private barnehager (ca. 450 mill kr), idrettslag, Kilden", regel: "Beregnes etter nasjonale satser og historiske kommunale kostnader." },
        { art: "1380", navn: "Kjøp fra KOSTRA-konsernet", cat: "OVERFORING", modul: "Konsern", desc: "Kjøp av tjenester fra kommunale foretak (KF) eller interkommunale selskaper (IKS).", typisk: "Avfallsbehandling kjøpt fra Avfall Sør, havnetjenester", regel: "Må motsvares av konsernselskapets salgsinntekt på art 1780." },
        { art: "1400", navn: "Direkte overføringer innbyggere", cat: "OVERFORING", modul: "Overføringer", desc: "Utbetaling av økonomisk sosialhjelp, bostøtte og kommunale stipend.", typisk: "Livsopphold og husleiestøtte via NAV, TT-kort forflytningshemmede", regel: "Sosialhjelp er en lovpålagt rettighet og kan ikke rammebegrenses." },
        { art: "1480", navn: "Overføringer til konsernenheter", cat: "OVERFORING", modul: "Konsern", desc: "Driftstilskudd til IKS og KF (Kristiansandsregionen brann og redning - KBR).", typisk: "Driftstilskudd til KBR brann og redning IKS, Agder Renovasjon IKS", regel: "Eierbrøk fastsatt i selskapsavtale legges til grunn." },
        { art: "1530", navn: "Avsetning til selvkostfond", cat: "FINANS", modul: "Selvkost", desc: "Avsetning av årets overskudd på selvkostområdene (Vann, avløp, renovasjon, byggesak).", typisk: "Overskytende gebyrinntekter som må tilbakeføres innbyggerne", regel: "Bundet fond. Må tilbakeføres til abonnentene innen 5 år." },
        { art: "1590", navn: "Avskrivninger", cat: "FINANS", modul: "Kapitalkostnader", desc: "Regnskapsmessig lineær avskrivning av kommunens anleggsmidler.", typisk: "Avskrivning av vann- og avløpsledninger, renseanlegg, skolebygg", regel: "Inngår som kapitalkostnad i selvkostberegninger." },
        { art: "1600", navn: "Bruker- og foreldrebetaling", cat: "INNTEKT", modul: "Konto / Pot", desc: "Betaling for opphold i barnehage, SFO, kulturskole og institusjonsplass.", typisk: "Foreldrebetaling SFO, egenandeler korttidsopphold sykehjem", regel: "Følger nasjonal makspris for barnehage og SFO." },
        { art: "1620", navn: "Gebyrinntekter (Selvkost)", cat: "INNTEKT", modul: "Selvkost", desc: "Gebyrer for vann, avløp, renovasjon, feiing og byggesaksbehandling.", typisk: "Vanngebyr, kloakkgebyr, tømmegebyr avfall, byggesaksgebyr", regel: "Skal dekke 100 % av beregnet gebyrgrunnlag over en 5-årsperiode." },
        { art: "1690", navn: "Sykelønnsrefusjon fra NAV", cat: "INNTEKT", modul: "Konto / Pot", desc: "Refusjon av sykepenger og foreldrepenger etter arbeidsgiverperioden (16 dager).", typisk: "Refusjonskrav sendt NAV for langtidssykmeldte ansatte", regel: "Må føres BRUTTO som inntekt. Må ALDRI motregnes mot lønnskonto 1010/1020." },
        { art: "1700", navn: "Refusjon fra staten", cat: "INNTEKT", modul: "Konto / Pot", desc: "Øremerkede tilskudd og refusjoner fra statlige etater (Udir, Helsedirektoratet).", typisk: "Statlig helsestasjonsmidler, lærernormstilskudd, legetilskudd", regel: "Krever dokumentasjon på at vilkårene for tilskuddet er oppfylt." },
        { art: "1850", navn: "Integreringstilskudd fra IMDi", cat: "STAT", modul: "Konto / Pot", desc: "Statlige tilskudd ved bosetting av flyktninger og introduksjonsprogram.", typisk: "År 1–5 integreringstilskudd for bosatte flyktninger", regel: "Forvaltes av Nav og Næring (Virksomhetsområde 6)." },
        { art: "1930", navn: "Bruk av bundet selvkostfond", cat: "STAT", modul: "Selvkost", desc: "Bruk av tidligere avsatt overskudd for å dekke årets underskudd i selvkost.", typisk: "Dekning av økte driftskostnader på vann og avløp uten gebyrøkning", regel: "Fondets saldo tilføres kalkulatorisk rente." }
    ];

    let currentSelvkostKey = "VANN";
    let currentBudsjettPhaseId = 7; // Aktiv fase nå: Ultimo Oktober

    function switchBudsjettModulTab(tabKey) {
        const tabs = ["lonn", "selvkost", "arshjul", "kostra", "qa"];
        tabs.forEach(t => {
            const btn = document.getElementById("bm-btn-" + t);
            const pane = document.getElementById("bm-pane-" + t);
            if (btn) btn.classList.remove("active");
            if (pane) pane.classList.remove("active");
        });

        const activeKey = tabKey.toLowerCase();
        const activeBtn = document.getElementById("bm-btn-" + activeKey);
        const activePane = document.getElementById("bm-pane-" + activeKey);

        if (activeBtn) activeBtn.classList.add("active");
        if (activePane) activePane.classList.add("active");

        // Spesiell init for faner
        if (activeKey === "lonn") {
            recalcSalaryBudsjett();
            renderBmPositionsTable();
        } else if (activeKey === "selvkost") {
            switchSelvkostService(currentSelvkostKey);
        } else if (activeKey === "arshjul") {
            renderBmYearStepper();
            selectBudsjettPhase(currentBudsjettPhaseId);
        } else if (activeKey === "kostra") {
            filterKostraDriftsarter();
        } else if (activeKey === "qa") {
            updateBmQaStatus();
        }
    }

    function onBmSectorChange() {
        const sec = document.getElementById("bm-calc-sector").value;
        const titleSelect = document.getElementById("bm-calc-title");
        const pensionSelect = document.getElementById("bm-calc-pension");

        if (sec === "OPPVEKST") {
            titleSelect.value = "LEKTOR";
            pensionSelect.value = "SPK";
            document.getElementById("bm-calc-salary").value = 680000;
        } else if (sec === "HELSE") {
            titleSelect.value = "SYKEPLEIER";
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 640000;
        } else if (sec === "BYUTVIKLING") {
            titleSelect.value = "INGENIOR";
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 850000;
        } else if (sec === "KULTUR") {
            titleSelect.value = "KONSULENT";
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 630000;
        } else {
            pensionSelect.value = "KLP";
        }
        recalcSalaryBudsjett();
    }

    function onBmTitleChange() {
        const title = document.getElementById("bm-calc-title").value;
        const pensionSelect = document.getElementById("bm-calc-pension");

        if (title === "LEKTOR") {
            pensionSelect.value = "SPK";
            document.getElementById("bm-calc-salary").value = 680000;
        } else if (title === "SYKEPLEIER") {
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 640000;
        } else if (title === "FAGARBEIDER") {
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 510000;
        } else if (title === "INGENIOR") {
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 850000;
        } else if (title === "SAKSBEHANDLER") {
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 670000;
        } else if (title === "KONSULENT") {
            pensionSelect.value = "KLP";
            document.getElementById("bm-calc-salary").value = 620000;
        }
        recalcSalaryBudsjett();
    }

    function recalcSalaryBudsjett() {
        const grunnlonn = parseFloat(document.getElementById("bm-calc-salary").value) || 0;
        const brok = parseFloat(document.getElementById("bm-calc-fraction").value) || 100;
        const alder = document.getElementById("bm-calc-age").value;
        const pensjonKasse = document.getElementById("bm-calc-pension").value;
        const tillegg = parseFloat(document.getElementById("bm-calc-shifts").value) || 0;
        const vikar = parseFloat(document.getElementById("bm-calc-substitute").value) || 0;
        const navRefusjon = parseFloat(document.getElementById("bm-calc-refund").value) || 0;

        // 1. Beregn Fast Lønn (Art 1010)
        const fastlonn = Math.round(grunnlonn * (brok / 100));

        // 2. Feriepenger (Art 1099): 12,0 % under 60 år, 14,3 % ved 60+
        const ferieRate = (alder === "OVER60") ? 0.143 : 0.120;
        const feriepenger = Math.round(fastlonn * ferieRate);

        // 3. Pensjonspremie (Art 1200): SPK (13,8 %) for lærere, KLP (15,2 %) for øvrige
        const pensjonRate = (pensjonKasse === "SPK") ? 0.138 : 0.152;
        const pensjon = Math.round(fastlonn * pensjonRate);

        // 4. Arbeidsgiveravgift (Art 1210): 14,1 % (Sone 1 - Kristiansand) av (Lønn + Feriepenger + Pensjon)
        const agaRate = 0.141;
        const agaFast = Math.round((fastlonn + feriepenger + pensjon) * agaRate);

        // 5. Variable tillegg og vikarer
        // Tillegg genererer feriepenger og AGA
        const ferieTillegg = Math.round(tillegg * ferieRate);
        const agaTillegg = Math.round((tillegg + ferieTillegg) * agaRate);
        const sumTilleggTot = tillegg + ferieTillegg + agaTillegg;

        // Vikarer genererer feriepenger og AGA
        const ferieVikar = Math.round(vikar * ferieRate);
        const agaVikar = Math.round((vikar + ferieVikar) * agaRate);
        const sumVikarTot = vikar + ferieVikar + agaVikar;

        // Samlet Brutto og Netto
        const bruttoTot = fastlonn + feriepenger + pensjon + agaFast + sumTilleggTot + sumVikarTot;
        const nettoTot = bruttoTot - navRefusjon;

        // Oppdater DOM
        const fmt = num => num.toLocaleString('nb-NO') + " kr";
        document.getElementById("bm-res-fastlonn").innerText = fmt(fastlonn);
        document.getElementById("bm-res-ferie-rate").innerText = (ferieRate * 100).toFixed(1) + " %";
        document.getElementById("bm-res-feriepenger").innerText = fmt(feriepenger);
        document.getElementById("bm-res-pensjon-org").innerText = `${pensjonKasse} ${(pensjonRate * 100).toFixed(1)} %`;
        document.getElementById("bm-res-pensjon").innerText = fmt(pensjon);
        document.getElementById("bm-res-aga-fast").innerText = fmt(agaFast);
        document.getElementById("bm-res-tillegg-tot").innerText = fmt(sumTilleggTot);
        document.getElementById("bm-res-vikar-tot").innerText = fmt(sumVikarTot);
        document.getElementById("bm-res-refusjon").innerText = "-" + fmt(navRefusjon);
        document.getElementById("bm-res-brutto-tot").innerText = fmt(bruttoTot);
        document.getElementById("bm-res-netto-tot").innerText = fmt(nettoTot);

        // Render KOSTRA Konteringsmatrise
        renderBmKostraSplit({
            fastlonn,
            feriepenger,
            pensjon,
            agaFast,
            tillegg,
            ferieTillegg,
            agaTillegg,
            vikar,
            ferieVikar,
            agaVikar,
            navRefusjon,
            bruttoTot,
            nettoTot,
            pensjonKasse
        });
    }

    function renderBmKostraSplit(data) {
        const tbody = document.getElementById("bm-kostra-tbody");
        if (!tbody) return;

        const fmt = n => n.toLocaleString('nb-NO');
        const rows = [
            { art: "1010", navn: "Fast lønn / stilling", debet: fmt(data.fastlonn), kredit: "-", modul: "Stilling", merknad: "Grunnlønn stillingshjemmel" },
            { art: "1099", navn: "Feriepengeavsetning", debet: fmt(data.feriepenger), kredit: "-", modul: "System", merknad: "Påløpt feriepengeforpliktelse" },
            { art: "1200", navn: `Pensjonsinnskudd (${data.pensjonKasse})`, debet: fmt(data.pensjon), kredit: "-", modul: "Stilling", merknad: "Arbeidsgivers premieandel" },
            { art: "1210", navn: "Arbeidsgiveravgift (AGA)", debet: fmt(data.agaFast + data.agaTillegg + data.agaVikar), kredit: "-", modul: "System", merknad: "14,1 % Sone 1 av lønn+ferie+pensjon" },
            { art: "1050/1090", navn: "Turnus- og overtidstillegg", debet: fmt(data.tillegg), kredit: "-", modul: "Konto/Pot", merknad: "Ubekvem arbeidstid / helgetillegg" },
            { art: "1020", navn: "Lønn til vikarer", debet: fmt(data.vikar), kredit: "-", modul: "Konto/Pot", merknad: "Syke- og fraværsvikarpott" },
            { art: "1690", navn: "Sykelønnsrefusjon fra NAV", debet: "-", kredit: fmt(data.navRefusjon), modul: "Inntekt", merknad: "Forventet refundert etter 16 dager" },
            { art: "SUM", navn: "Netto Kommunal Kostnad", debet: fmt(data.nettoTot), kredit: "-", modul: "Framsikt HØP", merknad: "Belastes enhetens driftsramme" }
        ];

        let html = "";
        rows.forEach(r => {
            const isSum = r.art === "SUM";
            html += `
                <tr style="${isSum ? 'font-weight:700; border-top:1.5px solid var(--navy-dark); border-bottom:2px solid var(--navy-dark); background:#f8fafc;' : ''}">
                    <td style="font-family:var(--font-mono); font-weight:600;">${r.art}</td>
                    <td>${r.navn}</td>
                    <td class="num" style="font-family:var(--font-mono);">${r.debet}</td>
                    <td class="num" style="font-family:var(--font-mono);">${r.kredit}</td>
                    <td style="font-size:11px; color:var(--text-secondary);">${r.merknad}</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }

    function resetSalaryCalc() {
        document.getElementById("bm-calc-salary").value = 620000;
        document.getElementById("bm-calc-fraction").value = 100;
        document.getElementById("bm-calc-age").value = "UNDER60";
        document.getElementById("bm-calc-pension").value = "KLP";
        document.getElementById("bm-calc-shifts").value = 35000;
        document.getElementById("bm-calc-substitute").value = 45000;
        document.getElementById("bm-calc-refund").value = 30000;
        recalcSalaryBudsjett();
        showToast("↺ Lønnskalkulator nullstilt til standardparametere");
    }

    function copySalaryAccounting() {
        const text = `KRISTIANSAND KOMMUNE — KOSTRA LØNNSKONTERINGSBILAG (FRAMSIKT)
Fastlønn (Art 1010): ${document.getElementById("bm-res-fastlonn").innerText}
Feriepenger (Art 1099): ${document.getElementById("bm-res-feriepenger").innerText}
Pensjon (Art 1200): ${document.getElementById("bm-res-pensjon").innerText}
AGA Sone 1 (Art 1210): ${document.getElementById("bm-res-aga-fast").innerText}
Variable tillegg (Art 1050/1090): ${document.getElementById("bm-res-tillegg-tot").innerText}
Vikarpott (Art 1020): ${document.getElementById("bm-res-vikar-tot").innerText}
NAV Sykelønnsrefusjon (Art 1690 Inntekt): ${document.getElementById("bm-res-refusjon").innerText}
SAMLET BRUTTO LØNNSKOSTNAD: ${document.getElementById("bm-res-brutto-tot").innerText}
NETTO KOMMUNAL KOSTNAD: ${document.getElementById("bm-res-netto-tot").innerText}
Kilde: Framsikt EPM & Visma Golden Record | Kommuneloven § 14-6`;

        navigator.clipboard.writeText(text).then(() => {
            showToast("✓ KOSTRA Konteringssplitt kopiert til utklippstavlen!");
        });
    }

    function renderBmPositionsTable() {
        const tbody = document.getElementById("bm-positions-tbody");
        if (!tbody) return;

        let html = "";
        BUDSJETT_POSITIONS_DATA.forEach(pos => {
            const sumTot = pos.fastlonn + pos.sosiale;
            html += `
                <tr>
                    <td style="font-family:var(--font-mono); font-weight:700;">${pos.id}</td>
                    <td><strong>${pos.tittel}</strong></td>
                    <td>${pos.ansatt}</td>
                    <td>${pos.sektor}</td>
                    <td><span class="bm-badge bm-badge-primary">${pos.pensjon}</span></td>
                    <td class="num">${pos.brok} %</td>
                    <td class="num">${pos.fastlonn.toLocaleString('nb-NO')} kr</td>
                    <td class="num">${pos.sosiale.toLocaleString('nb-NO')} kr</td>
                    <td class="num" style="font-weight:700; color:var(--navy-dark);">${sumTot.toLocaleString('nb-NO')} kr</td>
                    <td style="text-align:center;">
                        <button type="button" class="btn btn-sm" onclick="loadPositionIntoCalc('${pos.id}')" title="Last denne stillingen inn i lønnskalkulatoren">
                            ⚡ Regn
                        </button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }

    function loadPositionIntoCalc(posId) {
        const pos = BUDSJETT_POSITIONS_DATA.find(p => p.id === posId);
        if (!pos) return;

        document.getElementById("bm-calc-salary").value = pos.fastlonn;
        document.getElementById("bm-calc-fraction").value = pos.brok;
        document.getElementById("bm-calc-pension").value = pos.pensjon;

        if (pos.sektor_id) {
            const secSel = document.getElementById("bm-calc-sector");
            if (secSel) secSel.value = pos.sektor_id;
        }

        recalcSalaryBudsjett();
        showToast(`⚡ Lastet ${pos.tittel} (${pos.ansatt}) inn i Framsikt-kalkulatoren`);
        const el = document.getElementById("bm-pane-lonn");
        if (el) el.scrollIntoView({ behavior: "smooth" });
    }

    /* --- SELVKOSTKALKULATOR LOGIKK --- */
    function switchSelvkostService(svcKey) {
        currentSelvkostKey = svcKey;
        const keys = ["vann", "avloep", "renovasjon", "byggesak"];
        keys.forEach(k => {
            const btn = document.getElementById("btn-sk-" + k);
            if (btn) btn.classList.remove("active");
        });

        const activeBtn = document.getElementById("btn-sk-" + svcKey.toLowerCase());
        if (activeBtn) activeBtn.classList.add("active");

        const data = SELVKOST_SERVICES_DATA[svcKey];
        if (!data) return;

        document.getElementById("bm-sk-title").innerText = data.tittel;
        document.getElementById("bm-sk-direkte").value = data.direkte;
        document.getElementById("bm-sk-henforing").value = data.henforing;
        document.getElementById("bm-sk-avskrivning").value = data.avskrivning;
        document.getElementById("bm-sk-restverdi").value = data.restverdi;
        document.getElementById("bm-sk-inntekter").value = data.inntekter;
        document.getElementById("bm-sk-gebyr").value = data.gebyrinntekt;
        document.getElementById("bm-sk-fond-saldo").value = data.fond_primo;
        document.getElementById("bm-sk-fremforing-ar").innerText = data.fremforing_ar;

        recalcSelvkost();
    }

    function recalcSelvkost() {
        const direkte = parseFloat(document.getElementById("bm-sk-direkte").value) || 0;
        const henforing = parseFloat(document.getElementById("bm-sk-henforing").value) || 0;
        const avskrivning = parseFloat(document.getElementById("bm-sk-avskrivning").value) || 0;
        const restverdi = parseFloat(document.getElementById("bm-sk-restverdi").value) || 0;
        const inntekter = parseFloat(document.getElementById("bm-sk-inntekter").value) || 0;
        const gebyr = parseFloat(document.getElementById("bm-sk-gebyr").value) || 0;
        const fondPrimo = parseFloat(document.getElementById("bm-sk-fond-saldo").value) || 0;

        // Kalkulatorisk rente (5-årig statsobligasjon 3,25 % + 0,75 % = 4,00 %)
        const renteSats = 0.040;
        const kalkRente = Math.round(restverdi * renteSats);

        // Full Selvkost (Kalkulert Gebyrgrunnlag)
        const gebyrgrunnlag = Math.round(direkte + henforing + avskrivning + kalkRente - inntekter);

        // Selvkostresultat (Avvik i året)
        const resultat = Math.round(gebyr - gebyrgrunnlag);

        // Dekningsgrad
        const dekningsgrad = gebyrgrunnlag > 0 ? ((gebyr / gebyrgrunnlag) * 100) : 100;

        // Fond ultimo estimat
        const renteFond = Math.round(fondPrimo * renteSats);
        const fondUltimo = Math.round(fondPrimo + resultat + renteFond);

        const fmt = n => n.toLocaleString('nb-NO') + " kr";
        document.getElementById("bm-res-sk-direkte").innerText = fmt(direkte);
        document.getElementById("bm-res-sk-henforing").innerText = fmt(henforing);
        document.getElementById("bm-res-sk-avskrivning").innerText = fmt(avskrivning);
        document.getElementById("bm-res-sk-rente").innerText = fmt(kalkRente);
        document.getElementById("bm-res-sk-inntekt").innerText = "-" + fmt(inntekter);
        document.getElementById("bm-res-sk-gebyrgrunnlag").innerText = fmt(gebyrgrunnlag);
        document.getElementById("bm-res-sk-gebyrinntekt").innerText = fmt(gebyr);

        const resEl = document.getElementById("bm-res-sk-resultat");
        const badgeEl = document.getElementById("bm-sk-status-badge");
        const dgEl = document.getElementById("bm-res-sk-dekningsgrad");
        const forklaringEl = document.getElementById("bm-sk-fond-forklaring");

        dgEl.innerText = dekningsgrad.toFixed(1) + " %";
        document.getElementById("bm-sk-fond-ultimo").innerText = fmt(fondUltimo);

        if (Math.abs(resultat) < 50000) {
            resEl.innerText = fmt(resultat) + " (I balanse)";
            resEl.style.color = "var(--success-green)";
            badgeEl.innerText = "I Balanse (100 %)";
            badgeEl.className = "bm-badge bm-badge-success";
            dgEl.style.color = "var(--success-green)";
            forklaringEl.innerHTML = "Gebyret dekker nøyaktig selvkost. Ingen vesentlig avsetning til Art 1530 eller bruk av Art 1930 jf. <strong>Kommuneloven § 15-1</strong>.";
        } else if (resultat > 0) {
            resEl.innerText = "+" + fmt(resultat) + " (Overskudd)";
            resEl.style.color = "var(--navy-dark)";
            badgeEl.innerText = `Overskudd (+${((dekningsgrad - 100)).toFixed(1)} %)`;
            badgeEl.className = "bm-badge bm-badge-primary";
            dgEl.style.color = "var(--navy-dark)";
            forklaringEl.innerHTML = `Gebyret overstiger årets selvkost med <strong>${fmt(resultat)}</strong>. Beløpet må avsettes til <strong>Bundet Selvkostfond (Art 1530)</strong> og tilbakeføres abonnentene gjennom lavere gebyrer innen maksimalt <strong>5 år</strong> jf. Selvkostforskriften § 6.`;
        } else {
            resEl.innerText = fmt(resultat) + " (Underskudd)";
            resEl.style.color = "var(--alert-amber)";
            badgeEl.innerText = `Underskudd (${dekningsgrad.toFixed(1)} %)`;
            badgeEl.className = "bm-badge";
            badgeEl.style.background = "#fef3c7";
            badgeEl.style.color = "#92400e";
            dgEl.style.color = "var(--alert-amber)";
            forklaringEl.innerHTML = `Gebyret er lavere enn årets selvkost med <strong>${fmt(Math.abs(resultat))}</strong>. Underskuddet må dekkes ved <strong>Bruk av Bundet Selvkostfond (Art 1930)</strong> eller innarbeides i fremtidige gebyrsatser innen 5-årsfristen.`;
        }
    }

    function resetSelvkostValues() {
        switchSelvkostService(currentSelvkostKey);
        showToast("↺ Selvkostparametere tilbakestilt til Framsikt-grunndata");
    }

    function exportSelvkostNote() {
        const svc = SELVKOST_SERVICES_DATA[currentSelvkostKey];
        const direkte = document.getElementById("bm-res-sk-direkte").innerText;
        const henforing = document.getElementById("bm-res-sk-henforing").innerText;
        const avskrivning = document.getElementById("bm-res-sk-avskrivning").innerText;
        const rente = document.getElementById("bm-res-sk-rente").innerText;
        const gebyrgrunnlag = document.getElementById("bm-res-sk-gebyrgrunnlag").innerText;
        const gebyr = document.getElementById("bm-res-sk-gebyrinntekt").innerText;
        const resultat = document.getElementById("bm-res-sk-resultat").innerText;
        const dg = document.getElementById("bm-res-sk-dekningsgrad").innerText;
        const fondUltimo = document.getElementById("bm-sk-fond-ultimo").innerText;

        const note = `KRISTIANSAND KOMMUNE — SELVKOSTNOTAT FOR BYSTYRET
Tjeneste: ${svc.tittel}
Rettslig grunnlag: ${svc.lov}
Kalkulatorisk rente: 4,00 % (Årsgjennomsnitt 5-årig statsobligasjon + 0,75 %-poeng)

1. Direkte driftsutgifter (Art 1000–1270): ${direkte}
2. Indirekte henføring fellestjenester: ${henforing}
3. Avskrivninger på anleggsmidler (Art 1590): ${avskrivning}
4. Kalkulatorisk rente på anleggsmidler: ${rente}
SUM KALKULERT GEBYRGRUNNLAG: ${gebyrgrunnlag}

5. Budsjettert gebyrinntekt (Art 1620): ${gebyr}
ÅRETS SELVKOSTRESULTAT: ${resultat}
DEKNINGSGRAD: ${dg}
Estimert fondssaldo ultimo (Art 1530/1930): ${fondUltimo}
5-årsregel: Fremført saldo må avvikles innen 5 år jf. Selvkostforskriften § 6.
Kilde: Framsikt Selvkostmodul | Senior Controller Frank Ellingsen`;

        navigator.clipboard.writeText(note).then(() => {
            showToast("✓ Selvkostnotat kopiert til utklippstavlen!");
        });
    }

    /* --- BUDSJETT-ÅRSHJUL LOGIKK --- */
    function renderBmYearStepper() {
        const container = document.getElementById("bm-year-stepper-container");
        if (!container) return;

        let html = "";
        BUDSJETT_ARSHJUL_DATA.forEach(phase => {
            const isActive = phase.id === currentBudsjettPhaseId;
            html += `
                <div class="bm-step-card ${isActive ? 'active-phase' : ''}" onclick="selectBudsjettPhase(${phase.id})">
                    <div class="bm-step-period" style="display:flex; justify-content:space-between;">
                        <span>${phase.periode}</span>
                        <span style="color:${phase.status_color}; font-size:10px;">● ${phase.status}</span>
                    </div>
                    <div class="bm-step-title">${phase.id}. ${phase.tittel}</div>
                    <div class="bm-step-desc">${phase.desc}</div>
                    <span class="bm-step-role">👤 Ansvarlig: ${phase.rolle}</span>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function selectBudsjettPhase(phaseId) {
        currentBudsjettPhaseId = phaseId;
        renderBmYearStepper();

        const phase = BUDSJETT_ARSHJUL_DATA.find(p => p.id === phaseId);
        const card = document.getElementById("bm-phase-detail-card");
        if (!phase || !card) return;

        let oppgaverHtml = "";
        phase.oppgaver.forEach(op => {
            oppgaverHtml += `<li style="padding:4px 0; color:var(--text-primary); font-size:12.5px;">✓ ${op}</li>`;
        });

        card.innerHTML = `
            <div class="bm-box-title">
                <span>📍 Detaljert Arbeidspakke: Fase ${phase.id} — ${phase.tittel} (${phase.periode})</span>
                <span class="bm-badge" style="background:${phase.status === 'AKTIV NÅ' ? '#0284c7' : 'var(--navy-dark)'}; color:#fff;">
                    ${phase.status}
                </span>
            </div>
            <p style="font-size:13px; color:var(--text-secondary); margin-bottom:12px; line-height:1.55;">
                ${phase.desc}
            </p>
            <div style="background:#f8fafc; border:1px solid var(--border-light); padding:12px 16px; border-radius:3px; margin-bottom:12px;">
                <div style="font-size:11.5px; font-weight:700; color:var(--navy-dark); text-transform:uppercase; margin-bottom:6px;">
                    Obligatoriske Oppgaver & Leveranser:
                </div>
                <ul style="list-style:none; padding-left:0;">
                    ${oppgaverHtml}
                </ul>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:11.5px; color:var(--text-muted); border-top:1px solid var(--border-subtle); padding-top:8px;">
                <span>⚖️ Hjemmel: <strong>${phase.hjemmel}</strong></span>
                <span>👤 Nøkkelrolle: <strong>${phase.rolle}</strong></span>
            </div>
        `;
    }

    /* --- KOSTRA KONTOPLAN FILTER LOGIKK --- */
    function filterKostraDriftsarter() {
        const query = (document.getElementById("bm-kostra-search")?.value || "").toLowerCase().trim();
        const cat = document.getElementById("bm-kostra-cat-filter")?.value || "ALL";
        const tbody = document.getElementById("bm-kostra-full-tbody");
        if (!tbody) return;

        const filtered = KOSTRA_DRIFTSARTER_DATA.filter(item => {
            const matchesCat = (cat === "ALL" || item.cat === cat);
            const matchesQuery = !query || 
                item.art.includes(query) || 
                item.navn.toLowerCase().includes(query) || 
                item.desc.toLowerCase().includes(query) || 
                item.typisk.toLowerCase().includes(query) ||
                item.regel.toLowerCase().includes(query);
            return matchesCat && matchesQuery;
        });

        if (filtered.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; color:var(--text-muted);">Ingen KOSTRA-arter matcher søket "${query}".</td></tr>`;
            return;
        }

        let html = "";
        filtered.forEach(item => {
            html += `
                <tr>
                    <td style="font-family:var(--font-mono); font-weight:700; color:var(--navy-dark);">${item.art}</td>
                    <td><strong>${item.navn}</strong></td>
                    <td><span class="bm-badge bm-badge-primary">${item.modul}</span></td>
                    <td style="font-size:12px; line-height:1.45;">${item.desc}</td>
                    <td style="font-size:11.5px; color:var(--text-secondary);">${item.typisk}</td>
                    <td style="font-size:11.5px; color:#92400e; font-weight:500;">${item.regel}</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }

    function resetKostraFilter() {
        const s = document.getElementById("bm-kostra-search");
        const c = document.getElementById("bm-kostra-cat-filter");
        if (s) s.value = "";
        if (c) c.value = "ALL";
        filterKostraDriftsarter();
    }

    /* --- FRAMSIKT EXCEL QA VALIDERINGS LOGIKK --- */
    function updateBmQaStatus() {
        let checkedCount = 0;
        for (let i = 1; i <= 8; i++) {
            const chk = document.getElementById("bm-qa-" + i);
            if (chk && chk.checked) checkedCount++;
        }
        const badge = document.getElementById("bm-qa-checked-count");
        if (badge) {
            badge.innerText = `${checkedCount} av 8 Bekreftet`;
            if (checkedCount === 8) {
                badge.className = "bm-badge bm-badge-success";
            } else {
                badge.className = "bm-badge";
                badge.style.background = "#fef3c7";
                badge.style.color = "#92400e";
            }
        }
    }

    function toggleAllBmQa(checkAll) {
        for (let i = 1; i <= 8; i++) {
            const chk = document.getElementById("bm-qa-" + i);
            if (chk) chk.checked = checkAll;
        }
        updateBmQaStatus();
    }

    function runSimulatedFramsiktQA() {
        let checkedCount = 0;
        let uncheckedItems = [];
        const checkTitles = [
            "Uforanderlige ID-er i Excel",
            "Månedsoppdeling og oppstart",
            "AGA 14,1 % Sone 1 på lønn, ferie og pensjon",
            "Pensjonskassetilhørighet (SPK vs KLP)",
            "Bruttoføring av vikarer (1020) og NAV-refusjon (1690)",
            "Selvkost og 5-årsfond (VAR/Byggesak)",
            "Konsernavstemming (KBR IKS & Avfall Sør)",
            "Finansielle måltall (Netto driftsresultat ≥ 1,0 %)"
        ];

        for (let i = 1; i <= 8; i++) {
            const chk = document.getElementById("bm-qa-" + i);
            if (chk && chk.checked) {
                checkedCount++;
            } else {
                uncheckedItems.push(checkTitles[i - 1]);
            }
        }

        const now = new Date();
        const dateStr = now.toLocaleDateString('nb-NO') + " kl. " + now.toLocaleTimeString('nb-NO');
        const sha256 = "6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c";

        let reportText = "";
        if (checkedCount === 8) {
            reportText = `========================================================================
KRISTIANSAND KOMMUNE — KONTROLL OG GODKJENNING AV BUDSJETTGRUNNLAG
FRAMSIKT EPM ÅRSBUDSJETT & HANDLINGS- OG ØKONOMIPLAN 2027–2030
========================================================================
Tidspunkt: ${dateStr}
Saksbehandler / Lead Controller: Frank Ellingsen
Organisasjon: Kristiansand Kommune (81 resultatenheter / 6 virksomhetsområder)
Revisjonsstandard: Kommuneloven kapittel 14 & Selvkostforskriften
Stage-Gate: Port 9 HITL (Human-in-the-Loop) Formell Godkjenning

VERIFIKASJONSSTATUS: FULLT GODKJENT (8 av 8 sjekkpunkter bestått)
------------------------------------------------------------------------
[✓] 1. Unike stillings- og ansatt-ID-er intakt ved Excel-import
[✓] 2. Oppstartsdatoer og stillingsbrøker periodisert per måned
[✓] 3. Sone 1 AGA (14,1 %) beregnet av Lønn, Feriepenger og Pensjon
[✓] 4. Pensjonskassetilhørighet verifisert: SPK for lærere, KLP for øvrige
[✓] 5. Bruttoføring jf. § 14-6: Ingen ulovlig netting av vikar mot refusjon
[✓] 6. Selvkostkalkyler (Vann, avløp, renovasjon, byggesak) 100 % dekningsgrad
[✓] 7. Konsernavstemming fullført: KBR brann IKS og Avfall Sør avstemt
[✓] 8. Finansielle måltall overholdt: Korrigert driftsresultat ≥ 1,0 %

KRYPTOGRAFISK FORSEGLING (SHA-256):
${sha256}

Dette dokumentet er godkjent for oversendelse til Kommunedirektøren og
videre politisk behandling i Formannskapet og Bystyret.
========================================================================`;
            document.getElementById("bm-qa-attest-badge").innerText = "Verifisert (100 %)";
            document.getElementById("bm-qa-attest-badge").className = "bm-badge bm-badge-success";
            showToast("✓ Framsikt QA fullstendig godkjent med SHA-256 stempel!");
        } else {
            reportText = `========================================================================
KRISTIANSAND KOMMUNE — AVVIK I BUDSJETTVALIDERING (FRAMSIKT QA)
========================================================================
Tidspunkt: ${dateStr}
Kontrollør: Frank Ellingsen
STATUS: AVVIST / KREVER RETTING (${checkedCount} av 8 sjekkpunkter godkjent)

FØLGENDE PUNKTER ER IKKE BEKREFTET:
${uncheckedItems.map(item => `[!] ${item}`).join('\n')}

ADVARSEL: Budsjettrammen kan ikke låses i Framsikt før alle 8 punkter er 
verifisert jf. Kommuneloven § 14-5 og Kristiansand kommunes økonomireglement.
========================================================================`;
            document.getElementById("bm-qa-attest-badge").innerText = `Avvik (${checkedCount}/8)`;
            document.getElementById("bm-qa-attest-badge").className = "bm-badge";
            document.getElementById("bm-qa-attest-badge").style.background = "#fee2e2";
            document.getElementById("bm-qa-attest-badge").style.color = "#991b1b";
            showToast("⚠️ Framsikt QA har uavklarte sjekkpunkter!");
        }

        const out = document.getElementById("bm-qa-attest-output");
        if (out) out.innerText = reportText;
    }

    function copyBmQaAttest() {
        const text = document.getElementById("bm-qa-attest-output").innerText;
        navigator.clipboard.writeText(text).then(() => {
            showToast("✓ QA-attest kopiert til utklippstavlen!");
        });
    }

    function downloadBmQaReport() {
        const text = document.getElementById("bm-qa-attest-output").innerText;
        const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "Framsikt_Budsjett_QA_Attest_2026.txt";
        a.click();
        showToast("📥 Lastet ned Framsikt QA Valideringsrapport (.txt)");
    }

    // Init-kall for Budsjettmodul
    if (typeof recalcSalaryBudsjett === 'function') {
        recalcSalaryBudsjett();
        renderBmPositionsTable();
        recalcSelvkost();
        renderBmYearStepper();
        selectBudsjettPhase(7);
        filterKostraDriftsarter();
        updateBmQaStatus();
    }
"""

# Insertion: before </script>
TARGET_SCRIPT_ANCHOR = "</script>"

if "/* BUDSJETTMODUL: FRAMSIKT EPM" not in content:
    content = content.replace(TARGET_SCRIPT_ANCHOR, JS_BLOCK + "\n" + TARGET_SCRIPT_ANCHOR, 1)
    print("Inserted JS_BLOCK before </script>")
else:
    print("JS_BLOCK already present.")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("Stage 3 complete: JavaScript logic injected.")
