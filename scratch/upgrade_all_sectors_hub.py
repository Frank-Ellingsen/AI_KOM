#!/usr/bin/env python3
"""
Oppgraderingsmotor for alle budsjettansvarlige og sektorer i Control Office Hub.
Kristiansand Kommune - Økonomi og Virksomhetsstyring
"""

import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT_DIR / "index.html"

class StrictHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
        self.self_closing = {
            'meta', 'link', 'br', 'hr', 'input', 'img', 'col', 'base', 'area', 'param'
        }

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.self_closing:
            self.tags.append(tag.lower())

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in self.self_closing:
            return
        if not self.tags:
            self.errors.append(f"Uventet lukketag: </{t}> uten matchende starttag")
            return
        last = self.tags.pop()
        if last != t:
            self.errors.append(f"Mismatchet tag: ventet </{last}>, fant </{t}>")

def build_upgrade():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Sett inn Sektor Hurtigvelger og Visningsmodus i bank-wrapper
    target_bank_wrapper = '<div class="bank-wrapper">\n            <!-- Kontrollpanel: Enhetsvelger & Månedsvelger (M01–M12) -->'
    replacement_bank_wrapper = '''<div class="bank-wrapper">
            <!-- Sektor Hurtigvelger & Visningsmodus for Budsjettansvarlige -->
            <div class="bank-sector-filter-bar" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; padding: 10px 14px; background: #ffffff; border: 1px solid var(--border-light); border-radius: 4px;">
                <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                    <span style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; margin-right: 4px;">Sektor:</span>
                    <button type="button" class="btn btn-sm bank-sector-pill active" onclick="filterBankSector('ALL')" id="bank-sec-btn-ALL" style="background: var(--navy-dark); color: #ffffff; font-weight: 700;">Alle sektorer (81 enheter)</button>
                    <button type="button" class="btn btn-sm bank-sector-pill" onclick="filterBankSector('HELSE')" id="bank-sec-btn-HELSE" style="background: #f1f5f9; color: var(--text-primary);">🏥 Helse &amp; Omsorg</button>
                    <button type="button" class="btn btn-sm bank-sector-pill" onclick="filterBankSector('OPPVEKST')" id="bank-sec-btn-OPPVEKST" style="background: #f1f5f9; color: var(--text-primary);">🎓 Oppvekst &amp; Skole</button>
                    <button type="button" class="btn btn-sm bank-sector-pill" onclick="filterBankSector('BYUTVIKLING')" id="bank-sec-btn-BYUTVIKLING" style="background: #f1f5f9; color: var(--text-primary);">🏗️ Byutvikling &amp; VAR</button>
                    <button type="button" class="btn btn-sm bank-sector-pill" onclick="filterBankSector('KULTUR')" id="bank-sec-btn-KULTUR" style="background: #f1f5f9; color: var(--text-primary);">🎭 Kultur &amp; Idrett</button>
                    <button type="button" class="btn btn-sm bank-sector-pill" onclick="filterBankSector('ORG_TEK')" id="bank-sec-btn-ORG_TEK" style="background: #f1f5f9; color: var(--text-primary);">💻 Org &amp; IKT</button>
                    <button type="button" class="btn btn-sm bank-sector-pill" onclick="filterBankSector('KONSERN')" id="bank-sec-btn-KONSERN" style="background: #f1f5f9; color: var(--text-primary);">🏛️ Konsern</button>
                </div>
                <div style="display: flex; gap: 6px; align-items: center;">
                    <span style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Visning:</span>
                    <button type="button" class="btn btn-sm" id="btn-visning-klarsprak" onclick="toggleVisningsModus('KLARSPRAK')" style="background: #15803d; color: #ffffff; font-weight: 700;" title="Klarspråk for virksomhetsledere uten regnskapsbakgrunn">🟢 Leder Klarspråk</button>
                    <button type="button" class="btn btn-sm" id="btn-visning-detalj" onclick="toggleVisningsModus('DETALJ')" style="background: #f1f5f9; color: var(--text-primary);" title="Vis detaljerte KOSTRA-artskontoer og EVM-indekser">📊 Controller Detaljer</button>
                </div>
            </div>

            <!-- Kontrollpanel: Enhetsvelger & Månedsvelger (M01–M12) -->'''

    if target_bank_wrapper in html:
        html = html.replace(target_bank_wrapper, replacement_bank_wrapper, 1)
        print("✓ Satt inn bank-sector-filter-bar i bank-wrapper")
    else:
        print("⚠️ Fant ikke target_bank_wrapper, hopper over eller allerede satt inn")

    # 2. Utvid KK_LEADER_DIRECTORY med alle enheter
    old_directory_start = '        const KK_LEADER_DIRECTORY = {'
    old_directory_end = '        function getActiveUnitData() {'
    idx_dir_start = html.find(old_directory_start)
    idx_dir_end = html.find(old_directory_end)

    if idx_dir_start != -1 and idx_dir_end != -1:
        new_leader_directory = '''        const KK_LEADER_DIRECTORY = {
            "5200-ENH-401": {
                unitId: "5200-ENH-401",
                unitName: "Strai Sykehjem",
                leaderName: "Solveig Grimstad",
                email: "solveig.grimstad@kristiansand.kommune.no",
                sector: "Helse og mestring",
                bac: 14850000,
                ac: 12180500,
                saldo: 2669500,
                pct: 82.0,
                status: "GRØNN",
                eoy: "+120 000 kr (Mindreforbruk)",
                advice: "Driften er i balanse. Oppretthold restriktiv innleie av helgevikarer (art 10200) og purr opp NAV-refusjoner."
            },
            "5210-ENH-402": {
                unitId: "5210-ENH-402",
                unitName: "Hjemmetjenesten Vågsbygd",
                leaderName: "Berit Olsen",
                email: "berit.olsen@kristiansand.kommune.no",
                sector: "Helse og mestring",
                bac: 32100000,
                ac: 27600000,
                saldo: 4500000,
                pct: 86.0,
                status: "GUL",
                eoy: "-450 000 kr (Moderat merforbruk)",
                advice: "Overtid på helgevakter (art 10400) må strammes inn. Vurder omfordeling av kjøreruter for hjemmesykepleien."
            },
            "5220-ENH-403": {
                unitId: "5220-ENH-403",
                unitName: "Sørlandsparken Bo & Miljø",
                leaderName: "Christian Holte",
                email: "christian.holte@kristiansand.kommune.no",
                sector: "Helse og mestring",
                bac: 38600000,
                ac: 32900000,
                saldo: 5700000,
                pct: 85.2,
                status: "GUL",
                eoy: "-320 000 kr (Ressurskrevende brukere)",
                advice: "Følg opp refusjonskrav overfor Helsedirektoratet for ressurskrevende tjenester (art 16500) over innslagspunktet."
            },
            "5230-ENH-404": {
                unitId: "5230-ENH-404",
                unitName: "Presteheia Omsorgssenter",
                leaderName: "Kari Vesterhus",
                email: "kari.vesterhus@kristiansand.kommune.no",
                sector: "Helse og mestring",
                bac: 29400000,
                ac: 24200000,
                saldo: 5200000,
                pct: 82.3,
                status: "GRØNN",
                eoy: "+80 000 kr (I balanse)",
                advice: "Korttidsavdelingen holder budsjett. God turnusdekning med faste deltidsansatte."
            },
            "5100-OMR-SYKEHJEM": {
                unitId: "5100-OMR-SYKEHJEM",
                unitName: "Område Døgnomsorg & Sykehjem",
                leaderName: "Mette Syvertsen",
                email: "mette.syvertsen@kristiansand.kommune.no",
                sector: "Helse og mestring",
                bac: 450000000,
                ac: 378000000,
                saldo: 72000000,
                pct: 84.0,
                status: "GUL",
                eoy: "-1 450 000 kr (Vikaroverforbruk)",
                advice: "Konsolidering av vikarring på tvers av sykehjemmene. Innkall tillitsvalgte til HTA § 4 drøfting."
            },
            "5000-SJEF-HELSE": {
                unitId: "5000-SJEF-HELSE",
                unitName: "Sektor Helse og mestring",
                leaderName: "Brede Skeie",
                email: "brede.skeie@kristiansand.kommune.no",
                sector: "Helse og mestring",
                bac: 1420000000,
                ac: 1185000000,
                saldo: 235000000,
                pct: 83.5,
                status: "GUL",
                eoy: "-2 800 000 kr (Netto sektoravvik)",
                advice: "Konsolidering av vikarmidler og gjennomføring av drøftingsmøter jf. HTA § 4 for samtlige sykehjem."
            },
            "4100-ENH-202": {
                unitId: "4100-ENH-202",
                unitName: "Lovisenlev Skole",
                leaderName: "Trond Jensen",
                email: "trond.jensen@kristiansand.kommune.no",
                sector: "Oppvekst og utdanning",
                bac: 50339572,
                ac: 47426244,
                saldo: 2913328,
                pct: 94.2,
                status: "RØD",
                eoy: "-4 120 000 kr (Kritisk merforbruk)",
                advice: "Strakstiltak påkrevd jf. § 14-5: Innfør vikarstopp på korttidsfravær < 3 dager og oversend formelt avviksnotat til skolesjef."
            },
            "4101-ENH-203": {
                unitId: "4101-ENH-203",
                unitName: "Vågsbygd Skole",
                leaderName: "Mona Lindstrøm",
                email: "mona.lindstrom@kristiansand.kommune.no",
                sector: "Oppvekst og utdanning",
                bac: 31200000,
                ac: 25600000,
                saldo: 5600000,
                pct: 82.1,
                status: "GRØNN",
                eoy: "+110 000 kr (I balanse)",
                advice: "God lærertetthet (1:13.8 på småtrinnet) og vikarforbruk under kontroll. Fortsett god internressursfordeling."
            },
            "4102-ENH-204": {
                unitId: "4102-ENH-204",
                unitName: "Grim Ungdomsskole",
                leaderName: "Espen Birkeland",
                email: "espen.birkeland@kristiansand.kommune.no",
                sector: "Oppvekst og utdanning",
                bac: 28900000,
                ac: 24100000,
                saldo: 4800000,
                pct: 83.4,
                status: "GRØNN",
                eoy: "+95 000 kr (I balanse)",
                advice: "Drift i balanse. Oppretthold prioritering av miljøterapeuter for å redusere skolefravær."
            },
            "4210-ENH-211": {
                unitId: "4210-ENH-211",
                unitName: "Lund Kommunale Barnehage",
                leaderName: "Grete Hovden",
                email: "grete.hovden@kristiansand.kommune.no",
                sector: "Oppvekst og utdanning",
                bac: 18900000,
                ac: 15200000,
                saldo: 3700000,
                pct: 80.4,
                status: "GRØNN",
                eoy: "+140 000 kr (I balanse)",
                advice: "Bemanningsnorm (1:3 for småbarn, 1:6 for store barn) overholdt. Foreldrebetaling i rute."
            },
            "4100-OMR-SKOLE": {
                unitId: "4100-OMR-SKOLE",
                unitName: "Grunnskoleavdelingen",
                leaderName: "Svein Tore Kvernes",
                email: "svein.tore.kvernes@kristiansand.kommune.no",
                sector: "Oppvekst og utdanning",
                bac: 850000000,
                ac: 718000000,
                saldo: 132000000,
                pct: 84.5,
                status: "GUL",
                eoy: "-3 200 000 kr (Netto avvik vikar)",
                advice: "Omfordeling fra sentral spesialpedagogisk fellespott til skoler med akutt merforbruk (Lovisenlev)."
            },
            "4000-SJEF-OPPV": {
                unitId: "4000-SJEF-OPPV",
                unitName: "Sektor Oppvekst og utdanning",
                leaderName: "Kristin Eidet Robstad",
                email: "kristin.robstad@kristiansand.kommune.no",
                sector: "Oppvekst og utdanning",
                bac: 1890000000,
                ac: 1590000000,
                saldo: 300000000,
                pct: 84.1,
                status: "GUL",
                eoy: "-5 200 000 kr (Netto skoleavvik)",
                advice: "Omdisponering fra sentral lærervikarreserve til skoler med høyt spesialundervisningsbehov."
            },
            "3300-ENH-301": {
                unitId: "3300-ENH-301",
                unitName: "Byggesak og Tilsyn",
                leaderName: "Hans Petter Vik",
                email: "hans.petter.vik@kristiansand.kommune.no",
                sector: "By- og stedsutvikling",
                bac: 28500000,
                ac: 22800000,
                saldo: 5700000,
                pct: 80.0,
                status: "GRØNN",
                eoy: "+350 000 kr (Mindreforbruk)",
                advice: "Gebyrinntekter art 16200 overskrider prognose. Følg opp saksbehandlingsfrister for å opprettholde inntektsstrømmen."
            },
            "3100-DIR-VAR": {
                unitId: "3100-DIR-VAR",
                unitName: "Ingeniørvesenet VAR Selvkost",
                leaderName: "Helge Møller",
                email: "helge.moller@kristiansand.kommune.no",
                sector: "By- og stedsutvikling",
                bac: 68400000,
                ac: 55400000,
                saldo: 13000000,
                pct: 81.0,
                status: "GRØNN",
                eoy: "0 kr (100 % Selvkostbalanse)",
                advice: "100 % selvkostbalanse jf. forurensningsloven. Avsetning til selvkostfond for vann og avløp følger plan."
            },
            "3000-SJEF-BYUTV": {
                unitId: "3000-SJEF-BYUTV",
                unitName: "Kommunalsjef Byutvikling",
                leaderName: "Ragnar Evensen",
                email: "ragnar.evensen@kristiansand.kommune.no",
                sector: "By- og stedsutvikling",
                bac: 620000000,
                ac: 502000000,
                saldo: 118000000,
                pct: 81.0,
                status: "GRØNN",
                eoy: "+450 000 kr (Mindreforbruk)",
                advice: "Investeringsprosjekter følger fremdriftsplan. Selvkostområder i balanse."
            },
            "2100-ENH-501": {
                unitId: "2100-ENH-501",
                unitName: "Kultur & Bibliotek",
                leaderName: "Camilla Jarlsby",
                email: "camilla.jarlsby@kristiansand.kommune.no",
                sector: "Kultur og innbyggerdialog",
                bac: 28300000,
                ac: 23100000,
                saldo: 5200000,
                pct: 81.6,
                status: "GRØNN",
                eoy: "+80 000 kr (I balanse)",
                advice: "Gode billettinntekter og stabil bibliotekdrift. Tilskuddsmidler for høsten er klare for tildeling."
            },
            "2000-SJEF-KULTUR": {
                unitId: "2000-SJEF-KULTUR",
                unitName: "Kommunalsjef Kultur",
                leaderName: "Camilla Jarlsby",
                email: "camilla.jarlsby@kristiansand.kommune.no",
                sector: "Kultur og innbyggerdialog",
                bac: 290000000,
                ac: 238000000,
                saldo: 52000000,
                pct: 82.1,
                status: "GRØNN",
                eoy: "+150 000 kr (I balanse)",
                advice: "Frivillighetstilskudd (post 14700) følger budsjett. Kilden-samarbeidet er i rute."
            },
            "1100-DIR-IKT": {
                unitId: "1100-DIR-IKT",
                unitName: "Digitaliseringsavdelingen",
                leaderName: "Siri Bentsen",
                email: "siri.bentsen@kristiansand.kommune.no",
                sector: "Organisasjon og teknologi",
                bac: 45200000,
                ac: 38200000,
                saldo: 7000000,
                pct: 84.5,
                status: "GUL",
                eoy: "-350 000 kr (M365 Lisensvekst)",
                advice: "FinOps lisenssanering anbefales for å redusere ubrukte Copilot- og Visma-lisenser."
            },
            "1000-SJEF-ORGTEK": {
                unitId: "1000-SJEF-ORGTEK",
                unitName: "Kommunalsjef Org & Tek",
                leaderName: "Geir Askvik",
                email: "geir.askvik@kristiansand.kommune.no",
                sector: "Organisasjon og teknologi",
                bac: 340000000,
                ac: 284000000,
                saldo: 56000000,
                pct: 83.5,
                status: "GUL",
                eoy: "-420 000 kr (Konsulentinnleie)",
                advice: "Reduser konsulentinnleie på felles IT-prosjekter til fordel for interne ressurser."
            },
            "0000-KOMMDIR": {
                unitId: "0000-KOMMDIR",
                unitName: "Kommunedirektørens stab",
                leaderName: "Camilla Dunsæd",
                email: "camilla.dunsaed@kristiansand.kommune.no",
                sector: "Konsern og toppledelse",
                bac: 7240000000,
                ac: 6081600000,
                saldo: 1158400000,
                pct: 84.0,
                status: "GUL",
                eoy: "-24 500 000 kr (Netto driftsavvik jf. § 14-5)",
                advice: "Kommuneloven § 14-5 krever tiltaksplan for skoler og sykehjem med merforbruk. Disposisjonsfondet er robust (5.8%)."
            },
            "6000-DIR-OKONOMI": {
                unitId: "6000-DIR-OKONOMI",
                unitName: "Sentral økonomistab",
                leaderName: "Terje Fjellvang",
                email: "terje.fjellvang@kristiansand.kommune.no",
                sector: "Konsern og toppledelse",
                bac: 1160000000,
                ac: 968000000,
                saldo: 192000000,
                pct: 83.4,
                status: "GRØNN",
                eoy: "+4 200 000 kr (Finansforvaltning)",
                advice: "God renteavkastning på likviditetsplasseringer kompenserer delvis for skattesvikt."
            },
            "6001-CTRL-FRANK": {
                unitId: "6001-CTRL-FRANK",
                unitName: "Konsern & Toppledelse",
                leaderName: "Frank Ellingsen",
                email: "frank.ellingsen@kristiansand.kommune.no",
                sector: "Konsern / Økonomistab",
                bac: 7240000000,
                ac: 6081600000,
                saldo: 1158400000,
                pct: 84.0,
                status: "GUL",
                eoy: "-2 490 000 kr (Konsernprognose)",
                advice: "Månedlig rolling forecast opprettholdes. Saker til formannskapet forberedes for enheter med merforbruk > 500k."
            }
        };

'''
        html = html[:idx_dir_start] + new_leader_directory + html[idx_dir_end:]
        print("✓ Oppdatert KK_LEADER_DIRECTORY med alle 21 ledere og enheter")
    else:
        print("⚠️ Fant ikke KK_LEADER_DIRECTORY markører")

    # 3. Erstatt den eksisterende renderSektorSpesifikkLederModul og legg til kalkulatorer og filterfunksjoner
    target_skole_reg_start = '        /* ==========================================================================\n           REKTORENS SKOLE-DASHBOARD & PEDAGOGISK ØKONOMISTYRING (OPPVEKST SEKTOR)'
    target_script_end = '        }\n\n</script>'

    idx_mod_start = html.find(target_skole_reg_start)
    idx_mod_end = html.rfind(target_script_end)

    if idx_mod_start != -1 and idx_mod_end != -1:
        new_module_code = '''        /* ==========================================================================
           SEKTOR- OG PERSONA-TILPASSEDE DRIFTSDASHBOARDS FOR ALLE BUDSJETTANSVARLIGE
           Lovhjemler: Kommuneloven § 14-5/§ 14-9, Opplæringslova § 8-2, AML § 10-6/10-12, HTA § 4
           ========================================================================== */
        
        let activeBankSectorFilter = "ALL";
        let currentVisningsModus = "KLARSPRAK";

        function filterBankSector(sectorCode) {
            activeBankSectorFilter = sectorCode;
            const pills = document.querySelectorAll(".bank-sector-pill");
            pills.forEach(p => {
                if (p.id === `bank-sec-btn-${sectorCode}`) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });

            const dropdown = document.getElementById("bank-unit-dropdown");
            if (!dropdown) return;
            const optgroups = dropdown.querySelectorAll("optgroup");
            
            const sectorKeywords = {
                "HELSE": "Helse",
                "OPPVEKST": "Oppvekst",
                "BYUTVIKLING": "By- og stedsutvikling",
                "KULTUR": "Kultur",
                "ORG_TEK": "Organisasjon",
                "KONSERN": "Konsern"
            };

            const defaultUnits = {
                "HELSE": "5200-ENH-401",
                "OPPVEKST": "4100-ENH-202",
                "BYUTVIKLING": "3300-ENH-301",
                "KULTUR": "2100-ENH-501",
                "ORG_TEK": "1100-DIR-IKT",
                "KONSERN": "0000-KOMMDIR"
            };

            if (sectorCode === "ALL") {
                optgroups.forEach(og => og.style.display = "");
                showToast("🌐 Viser samtlige sektorer i Kristiansand kommune.");
            } else {
                optgroups.forEach(og => {
                    if (og.label && og.label.includes(sectorKeywords[sectorCode])) {
                        og.style.display = "";
                    } else {
                        og.style.display = "none";
                    }
                });
                if (defaultUnits[sectorCode]) {
                    dropdown.value = defaultUnits[sectorCode];
                    onBankUnitChange(defaultUnits[sectorCode]);
                }
            }
        }

        function toggleVisningsModus(mode) {
            currentVisningsModus = mode;
            const btnK = document.getElementById("btn-visning-klarsprak");
            const btnD = document.getElementById("btn-visning-detalj");
            if (btnK && btnD) {
                if (mode === "KLARSPRAK") {
                    btnK.style.background = "#15803d";
                    btnK.style.color = "#ffffff";
                    btnK.style.fontWeight = "700";
                    btnD.style.background = "#f1f5f9";
                    btnD.style.color = "var(--text-primary)";
                    btnD.style.fontWeight = "normal";
                    showToast("🟢 Leder Klarspråk: Forenklet oversikt for travle ledere.");
                } else {
                    btnD.style.background = "var(--navy-dark)";
                    btnD.style.color = "#ffffff";
                    btnD.style.fontWeight = "700";
                    btnK.style.background = "#f1f5f9";
                    btnK.style.color = "var(--text-primary)";
                    btnK.style.fontWeight = "normal";
                    showToast("📊 Controller Detaljer: Full KOSTRA artskontospesifikasjon vises.");
                }
            }
            renderBankStatement(currentKontoUnit, currentKontoMonth);
        }

        // ==========================================
        // OPPEKST REGISTRY & VIKARKALKULATOR
        // ==========================================
        const SKOLE_METRICS_REGISTRY = {
            "4100-ENH-202": {
                unitId: "4100-ENH-202",
                skoleNavn: "Lovisenlev Skole",
                skoleType: "1.–7. Grunnskole (420 elever)",
                rektorNavn: "Trond Jensen",
                rektorEpost: "trond.jensen@kristiansand.kommune.no",
                inspektorNavn: "Bjarne Wiig (Inspektør 1.–4. trinn)",
                sfoLederNavn: "Cathrine Solberg (SFO-leder)",
                skolesjefNavn: "Svein Tore Kvernes",
                skolesjefEpost: "svein.tore.kvernes@kristiansand.kommune.no",
                controllerNavn: "Frank Ellingsen",
                elevtall: 420,
                ansatteAarsverk: 48.0,
                sfoBarn: 140,
                rammePerElev: 119856,
                skoleAarTermin: "Høstsemester 2026 (Mnd 3 av 5) | Regnskapsmåned M10",
                laerernorm14: { ratio: "1:14.2", krav: "< 15.0", status: "OVERHOLDT", farge: "#15803d" },
                laerernorm57: { ratio: "1:18.5", krav: "< 20.0", status: "OVERHOLDT", farge: "#15803d" },
                laererAarsverk: 31.4,
                laererPlanlagt: 32.0,
                spesPed: {
                    eleverMedVedtak: 14,
                    timerAar: 12400,
                    dekningFellespottPct: 88,
                    statusText: "88 % dekkes av fellesreserve. 2 nyinnflyttede enkeltelever krever ekstra 1:1 assistent."
                },
                sfo: {
                    inntekt: 3200000,
                    kostnad: 3155000,
                    balanse: 45000,
                    status: "I BALANSE",
                    statusColor: "#15803d",
                    merknad: "Foreldrebetaling + 12t gratis for 1.–3. trinn dekker assistentlønninger."
                },
                vikar: {
                    ramme: 2400000,
                    brukt: 2220000,
                    rest: 180000,
                    pct: 92.5,
                    sykefravaerPct: 11.4,
                    utestaaendeNavRefusjon: 142500,
                    statusAlert: "🔴 Kritisk vikarvarsel: Kun 180 000 kr (ca. 1.5 vikaruker) igjen før jul! Restriktiv vikarstopp på korttidsfravær < 3 dager er påkrevd."
                }
            },
            "4101-ENH-203": {
                unitId: "4101-ENH-203",
                skoleNavn: "Vågsbygd Skole",
                skoleType: "1.–7. Grunnskole (310 elever)",
                rektorNavn: "Mona Lindstrøm",
                rektorEpost: "mona.lindstrom@kristiansand.kommune.no",
                inspektorNavn: "Kari Helgesen",
                sfoLederNavn: "Lars Vesterhus",
                skolesjefNavn: "Svein Tore Kvernes",
                skolesjefEpost: "svein.tore.kvernes@kristiansand.kommune.no",
                controllerNavn: "Frank Ellingsen",
                elevtall: 310,
                ansatteAarsverk: 35.0,
                sfoBarn: 95,
                rammePerElev: 123225,
                skoleAarTermin: "Høstsemester 2026 (Mnd 3 av 5) | Regnskapsmåned M10",
                laerernorm14: { ratio: "1:13.8", krav: "< 15.0", status: "OVERHOLDT", farge: "#15803d" },
                laerernorm57: { ratio: "1:17.9", krav: "< 20.0", status: "OVERHOLDT", farge: "#15803d" },
                laererAarsverk: 23.5,
                laererPlanlagt: 24.0,
                spesPed: {
                    eleverMedVedtak: 9,
                    timerAar: 7800,
                    dekningFellespottPct: 92,
                    statusText: "Stabil vedtaksportefølje. God dekning fra skolesjefens fellesreserve."
                },
                sfo: {
                    inntekt: 2100000,
                    kostnad: 2060000,
                    balanse: 40000,
                    status: "I BALANSE",
                    statusColor: "#15803d",
                    merknad: "Stabil drift med god assistentutnyttelse."
                },
                vikar: {
                    ramme: 1750000,
                    brukt: 1450000,
                    rest: 300000,
                    pct: 82.9,
                    sykefravaerPct: 7.8,
                    utestaaendeNavRefusjon: 85000,
                    statusAlert: "🟢 Drift i balanse: Normalt vikarforbruk innenfor periodisert budsjett."
                }
            },
            "4102-ENH-204": {
                unitId: "4102-ENH-204",
                skoleNavn: "Grim Ungdomsskole",
                skoleType: "8.–10. Ungdomsskole (360 elever)",
                rektorNavn: "Espen Birkeland",
                rektorEpost: "espen.birkeland@kristiansand.kommune.no",
                inspektorNavn: "Torstein Moen",
                sfoLederNavn: "— (Ikke SFO på ungdomstrinn)",
                skolesjefNavn: "Svein Tore Kvernes",
                skolesjefEpost: "svein.tore.kvernes@kristiansand.kommune.no",
                controllerNavn: "Frank Ellingsen",
                elevtall: 360,
                ansatteAarsverk: 40.0,
                sfoBarn: 0,
                rammePerElev: 122500,
                skoleAarTermin: "Høstsemester 2026 (Mnd 3 av 5) | Regnskapsmåned M10",
                laerernorm14: { ratio: "—", krav: "Kun 8.–10.", status: "IKKE RELEVANT", farge: "#64748b" },
                laerernorm57: { ratio: "1:18.2", krav: "< 20.0", status: "OVERHOLDT", farge: "#15803d" },
                laererAarsverk: 28.0,
                laererPlanlagt: 28.5,
                spesPed: {
                    eleverMedVedtak: 12,
                    timerAar: 9600,
                    dekningFellespottPct: 85,
                    statusText: "Økt behov for miljøterapeut i 9. og 10. trinn for å redusere fravær."
                },
                sfo: {
                    inntekt: 0,
                    kostnad: 0,
                    balanse: 0,
                    status: "IKKE SFO",
                    statusColor: "#64748b",
                    merknad: "Ungdomsskole har ikke SFO-ordning."
                },
                vikar: {
                    ramme: 1900000,
                    brukt: 1580000,
                    rest: 320000,
                    pct: 83.2,
                    sykefravaerPct: 8.2,
                    utestaaendeNavRefusjon: 110000,
                    statusAlert: "🟡 Observasjon: Følg opp timelærere i naturfag og matematikk."
                }
            },
            "4210-ENH-211": {
                unitId: "4210-ENH-211",
                skoleNavn: "Lund Kommunale Barnehage",
                skoleType: "Kommunal Barnehage (110 barn)",
                rektorNavn: "Grete Hovden",
                rektorEpost: "grete.hovden@kristiansand.kommune.no",
                inspektorNavn: "Assisterende styrer",
                sfoLederNavn: "—",
                skolesjefNavn: "Anne Lise Tønnessen (Barnehagesjef)",
                skolesjefEpost: "anne.lise.tonnessen@kristiansand.kommune.no",
                controllerNavn: "Erik Halvorsen",
                elevtall: 110,
                ansatteAarsverk: 24.0,
                sfoBarn: 0,
                rammePerElev: 177272,
                skoleAarTermin: "Barnehageår 2026/2027",
                laerernorm14: { ratio: "1:6.8", krav: "Ped.norm 1:7", status: "OVERHOLDT", farge: "#15803d" },
                laerernorm57: { ratio: "1:3.0", krav: "Bemanningsnorm 1:3", status: "OVERHOLDT", farge: "#15803d" },
                laererAarsverk: 16.0,
                laererPlanlagt: 16.0,
                spesPed: {
                    eleverMedVedtak: 5,
                    timerAar: 4200,
                    dekningFellespottPct: 95,
                    statusText: "Spesialpedagogisk ressurs på plass for 5 barn med vedtak."
                },
                sfo: {
                    inntekt: 0,
                    kostnad: 0,
                    balanse: 0,
                    status: "IKKE SFO",
                    statusColor: "#64748b",
                    merknad: "Barnehage"
                },
                vikar: {
                    ramme: 1200000,
                    brukt: 960000,
                    rest: 240000,
                    pct: 80.0,
                    sykefravaerPct: 9.1,
                    utestaaendeNavRefusjon: 64000,
                    statusAlert: "🟢 Drift i balanse: Vikarbudsjettet holder til nyttår."
                }
            }
        };

        let simVikarStilling = "LAERER";
        let simVikarUker = 3;

        function setVikarSimStilling(stilling) {
            simVikarStilling = stilling;
            const btnL = document.getElementById("sim-btn-laerer");
            const btnA = document.getElementById("sim-btn-assistent");
            if (btnL && btnA) {
                if (stilling === "LAERER") {
                    btnL.style.background = "var(--navy-dark)";
                    btnL.style.color = "#ffffff";
                    btnA.style.background = "#f1f5f9";
                    btnA.style.color = "var(--text-primary)";
                } else {
                    btnA.style.background = "var(--navy-dark)";
                    btnA.style.color = "#ffffff";
                    btnL.style.background = "#f1f5f9";
                    btnL.style.color = "var(--text-primary)";
                }
            }
            recalcVikarKalkulator();
        }

        function setVikarSimUker(uker) {
            simVikarUker = uker;
            const pills = document.querySelectorAll(".sim-uke-pill");
            pills.forEach(p => {
                if (parseInt(p.getAttribute("data-uker")) === uker) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });
            recalcVikarKalkulator();
        }

        function recalcVikarKalkulator() {
            const isLaerer = simVikarStilling === "LAERER";
            const timerPerUke = 37.5;
            const totalTimer = simVikarUker * timerPerUke;
            const timeprisIntern = isLaerer ? 380 : 310;
            const timeprisByra = isLaerer ? 680 : 550;

            const bruttoIntern = totalTimer * timeprisIntern;
            const bruttoByra = totalTimer * timeprisByra;

            let navRefusjon = 0;
            if (simVikarUker > 2) {
                const refUker = simVikarUker - 2.2;
                const dagsats = isLaerer ? 2150 : 1650;
                navRefusjon = Math.max(0, Math.round(refUker * 5 * dagsats));
            }

            const nettoIntern = Math.max(0, bruttoIntern - navRefusjon);
            const besparelse = bruttoByra - bruttoIntern;

            const elIntern = document.getElementById("sim-res-intern");
            const elByra = document.getElementById("sim-res-byra");
            const elNav = document.getElementById("sim-res-nav");
            const elNetto = document.getElementById("sim-res-netto");
            const elGevinst = document.getElementById("sim-res-gevinst");

            if (elIntern) elIntern.textContent = `${bruttoIntern.toLocaleString("no-NO")} kr`;
            if (elByra) elByra.textContent = `${bruttoByra.toLocaleString("no-NO")} kr`;
            if (elNav) elNav.textContent = navRefusjon > 0 ? `+${navRefusjon.toLocaleString("no-NO")} kr` : "0 kr (Arbeidsgiverperiode dag 1–16)";
            if (elNetto) elNetto.textContent = `${nettoIntern.toLocaleString("no-NO")} kr`;
            if (elGevinst) elGevinst.textContent = `${besparelse.toLocaleString("no-NO")} kr`;
        }

        // ==========================================
        // HELSE GAT TURNUS- OG OVERTIDSKALKULATOR
        // ==========================================
        let simGatVakter = 2;
        let simGatStilling = "OVERTID";

        function setGatSimVakt(vakter) {
            simGatVakter = vakter;
            const pills = document.querySelectorAll(".gat-vakt-pill");
            pills.forEach(p => {
                if (parseInt(p.getAttribute("data-vakter")) === vakter) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });
            recalcGatKalkulator();
        }

        function setGatSimStilling(stilling) {
            simGatStilling = stilling;
            const btnO = document.getElementById("gat-btn-overtid");
            const btnS = document.getElementById("gat-btn-student");
            if (btnO && btnS) {
                if (stilling === "OVERTID") {
                    btnO.style.background = "#c0392b";
                    btnO.style.color = "#ffffff";
                    btnS.style.background = "#f1f5f9";
                    btnS.style.color = "var(--text-primary)";
                } else {
                    btnS.style.background = "var(--navy-dark)";
                    btnS.style.color = "#ffffff";
                    btnO.style.background = "#f1f5f9";
                    btnO.style.color = "var(--text-primary)";
                }
            }
            recalcGatKalkulator();
        }

        function recalcGatKalkulator() {
            const timerPerVakt = 7.5;
            const totalTimer = simGatVakter * timerPerVakt;
            // Overtidssats (Sykepleier lønnstrinn 48 + 100% overtid helg + helgetillegg jf. HTA § 6)
            const satsOvertid = 780;
            // Student / Ekstravakt ordinær timelønn + helgetillegg
            const satsStudent = 340;

            const kostnadOvertid = totalTimer * satsOvertid;
            const kostnadStudent = totalTimer * satsStudent;
            const besparelse = kostnadOvertid - kostnadStudent;

            const elKostnad = document.getElementById("gat-res-kostnad");
            const elAlt = document.getElementById("gat-res-alt");
            const elSparing = document.getElementById("gat-res-sparing");

            if (elKostnad) elKostnad.textContent = `${kostnadOvertid.toLocaleString("no-NO")} kr`;
            if (elAlt) elAlt.textContent = `${kostnadStudent.toLocaleString("no-NO")} kr`;
            if (elSparing) elSparing.textContent = `${besparelse.toLocaleString("no-NO")} kr`;
        }

        // ==========================================
        // BYUTVIKLING & VAR SELVKOSTKALKULATOR
        // ==========================================
        let simVarEndringPct = 10;

        function setVarSimEndring(pct) {
            simVarEndringPct = pct;
            const pills = document.querySelectorAll(".var-pct-pill");
            pills.forEach(p => {
                if (parseInt(p.getAttribute("data-pct")) === pct) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });
            recalcVarKalkulator();
        }

        function recalcVarKalkulator() {
            // VAR Samlet årsbudsjett (Vann, Avløp, Renovasjon) = 68.4 MNOK
            const basisVarBudsjett = 68400000;
            const merkostnad = Math.round(basisVarBudsjett * (simVarEndringPct / 100));
            // Beregnet på ca 48 000 abonnenter / husstander i Kristiansand
            const krPerHusstandAar = Math.round(merkostnad / 48000);
            const krPerHusstandMnd = Math.round(krPerHusstandAar / 12);

            const elMerkost = document.getElementById("var-res-merkost");
            const elFondBruk = document.getElementById("var-res-fondbruk");
            const elGebyr = document.getElementById("var-res-gebyr");

            if (elMerkost) elMerkost.textContent = `+${merkostnad.toLocaleString("no-NO")} kr/år`;
            if (elFondBruk) elFondBruk.textContent = `${merkostnad.toLocaleString("no-NO")} kr (Fra fond)`;
            if (elGebyr) elGebyr.textContent = `+${krPerHusstandMnd} kr / mnd`;
        }

        // ==========================================
        // KULTUR FRIVILLIGHETSKALKULATOR
        // ==========================================
        let simKulturSokere = 25;

        function setKulturSimSokere(antall) {
            simKulturSokere = antall;
            const pills = document.querySelectorAll(".kultur-soker-pill");
            pills.forEach(p => {
                if (parseInt(p.getAttribute("data-sokere")) === antall) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });
            recalcKulturKalkulator();
        }

        function recalcKulturKalkulator() {
            const gjenstaaendeHøst = 3800000; // kr
            const snittPerLag = Math.round(gjenstaaendeHøst / simKulturSokere);
            const estimertBarnPerLag = 45;
            const stottePerBarn = Math.round(snittPerLag / estimertBarnPerLag);

            const elSnitt = document.getElementById("kultur-res-snitt");
            const elPerBarn = document.getElementById("kultur-res-barn");

            if (elSnitt) elSnitt.textContent = `${snittPerLag.toLocaleString("no-NO")} kr`;
            if (elPerBarn) elPerBarn.textContent = `ca. ${stottePerBarn.toLocaleString("no-NO")} kr/år`;
        }

        // ==========================================
        // IKT FINOPS LISENSKALKULATOR
        // ==========================================
        let simIktLisenser = 100;

        function setIktSimLisenser(antall) {
            simIktLisenser = antall;
            const pills = document.querySelectorAll(".ikt-lisens-pill");
            pills.forEach(p => {
                if (parseInt(p.getAttribute("data-lisenser")) === antall) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });
            recalcIktKalkulator();
        }

        function recalcIktKalkulator() {
            // M365 Copilot / Enterprise snittkostnad 360 kr/mnd
            const mndBesparelse = simIktLisenser * 360;
            const aarligBesparelse = mndBesparelse * 12;

            const elMnd = document.getElementById("ikt-res-mnd");
            const elAar = document.getElementById("ikt-res-aar");

            if (elMnd) elMnd.textContent = `${mndBesparelse.toLocaleString("no-NO")} kr / mnd`;
            if (elAar) elAar.textContent = `${aarligBesparelse.toLocaleString("no-NO")} kr / år`;
        }

        // ==========================================
        // KONSERN RENTE- OG SKATTESIMULATOR
        // ==========================================
        let simKonsernRente = 1.0;

        function setKonsernSimRente(rentePct) {
            simKonsernRente = rentePct;
            const pills = document.querySelectorAll(".konsern-rente-pill");
            pills.forEach(p => {
                if (parseFloat(p.getAttribute("data-rente")) === rentePct) {
                    p.style.background = "var(--navy-dark)";
                    p.style.color = "#ffffff";
                    p.style.fontWeight = "700";
                } else {
                    p.style.background = "#f1f5f9";
                    p.style.color = "var(--text-primary)";
                    p.style.fontWeight = "normal";
                }
            });
            recalcKonsernKalkulator();
        }

        function recalcKonsernKalkulator() {
            // Kommunens lånegjeld 4.2 milliarder NOK
            const gjeld = 4200000000;
            const renteKostnad = Math.round(gjeld * (simKonsernRente / 100));
            const gjeldendeFond = 418000000;
            const nyFondSaldo = Math.max(0, gjeldendeFond - renteKostnad);
            const nyFondPct = ((nyFondSaldo / 7240000000) * 100).toFixed(1);

            const elKostnad = document.getElementById("konsern-res-kostnad");
            const elFond = document.getElementById("konsern-res-fond");
            const elBuffer = document.getElementById("konsern-res-buffer");

            if (elKostnad) elKostnad.textContent = `+${(renteKostnad / 1000000).toFixed(1)} MNOK`;
            if (elFond) elFond.textContent = `${(nyFondSaldo / 1000000).toFixed(1)} MNOK (${nyFondPct} %)`;
            if (elBuffer) elBuffer.textContent = nyFondPct >= 5.0 ? "🟢 Over 5% målkrav" : "🔴 Under 5% målkrav";
        }

        // ==========================================
        // SEKTOR-SPESIFIKKE RAPPORT-SENDERE
        // ==========================================
        function sendRektorReportToSkolesjef() {
            const unit = SKOLE_METRICS_REGISTRY[currentKontoUnit] || SKOLE_METRICS_REGISTRY["4100-ENH-202"];
            currentShareMode = "email";
            const toInput = document.getElementById("share-email-to");
            const ccInput = document.getElementById("share-email-cc");
            const subjInput = document.getElementById("share-email-subject");
            const bodyArea = document.getElementById("share-message-body");

            toInput.value = `${unit.skolesjefNavn} <${unit.skolesjefEpost}>`;
            ccInput.value = "frank.ellingsen@kristiansand.kommune.no, erik.halvorsen@kristiansand.kommune.no";
            subjInput.value = `Månedsbekreftelse ${unit.skoleNavn} (M10-2026): Lærernorm overholdt & Vikarstrakstiltak jf. § 14-5`;

            bodyArea.value = `Til Skolesjef ${unit.skolesjefNavn},

Her er månedlig statusrapport og bekreftelse fra skoleledelsen ved ${unit.skoleNavn} per oktober 2026:

1. ELEVTALL & LÆRERNORM (Opplæringslova § 8-2):
   • Elevtall: ${unit.elevtall} elever (Tildelt årsbudsjett: kr ${unit.rammePerElev.toLocaleString("no-NO")}/elev).
   • 1.–4. trinn: Forholdstall ${unit.laerernorm14.ratio} (Lovkrav: ${unit.laerernorm14.krav}) — STATUS: ${unit.laerernorm14.status}
   • 5.–7. trinn: Forholdstall ${unit.laerernorm57.ratio} (Lovkrav: ${unit.laerernorm57.krav}) — STATUS: ${unit.laerernorm57.status}
   • Lærerårsverk i drift: ${unit.laererAarsverk} av ${unit.laererPlanlagt} planlagte.

2. SPESIALUNDERVISNING OG ENKELTVEDTAK:
   • ${unit.spesPed.eleverMedVedtak} elever med enkeltvedtak (${unit.spesPed.timerAar.toLocaleString("no-NO")} timer/år).
   • ${unit.spesPed.statusText}

3. SFO (SKOLEFRITIDSORDNING):
   • ${unit.sfoBarn} barn innmeldt. SFO driftes i balanse (+${unit.sfo.balanse.toLocaleString("no-NO")} kr). Foreldrebetaling og statlig 12t-ordning dekker lønnskostnadene.

4. VIKARFORBRUK & SYKEFRAVÆR (Årsak til regnskapsavvik):
   • Sykefraværet er ${unit.vikar.sykefravaerPct} %, noe som har krevd kr ${unit.vikar.brukt.toLocaleString("no-NO")} i vikarutgifter.
   • Gjenstående vikarbudsjett for resten av året er kr ${unit.vikar.rest.toLocaleString("no-NO")}.
   • Utestående refusjonskrav over 16 dager til NAV: kr ${unit.vikar.utestaaendeNavRefusjon.toLocaleString("no-NO")}.

5. IVERKSATTE STRAKSTILTAK (Jf. Kommuneloven § 14-5):
   a) Vikarstopp på korttidsfravær < 3 dager. Klasser sambruker faglærere i praktisk-estetiske fag.
   b) 100 % oppfølging og purring av NAV-refusjoner (art 16900).
   c) Søknad om delvis dekning fra skolesjefens fellesreserve for 2 nyinnflyttede vedtakselever.

Med vennlig hilsen,
${unit.rektorNavn}
Rektor ved ${unit.skoleNavn}
Tlf: +47 38 00 82 02 | ${unit.rektorEpost}`;

            setShareMode("email");
            document.getElementById("teams-email-modal").style.display = "flex";
        }

        function sendHelseReportToKommunalsjef() {
            currentShareMode = "email";
            const toInput = document.getElementById("share-email-to");
            const ccInput = document.getElementById("share-email-cc");
            const subjInput = document.getElementById("share-email-subject");
            const bodyArea = document.getElementById("share-message-body");

            toInput.value = "Brede Skeie <brede.skeie@kristiansand.kommune.no>";
            ccInput.value = "frank.ellingsen@kristiansand.kommune.no, marianne.tellefsen@kristiansand.kommune.no";
            subjInput.value = `Månedsrapport Helse og Omsorg (M10-2026): Pasientbelegg, GAT Turnus & AML § 10-6`;

            bodyArea.value = `Til Kommunalsjef Brede Skeie,

Her er månedlig rapport fra helse- og omsorgsledelsen per oktober 2026:

1. PASIENTBELEGG OG DØGNPLASSER:
   • Pasientbelegg: 98.4 % på sykehjemmene (Full kapasitetsutnyttelse).
   • Pleiefaktor: 0.84 pleier per pasient i tråd med bemanningsnorm.

2. GAT TURNUS, LANGVAKTER & ARBEIDSMILJØLOVEN:
   • Overtid og helgetillegg: Restriktiv godkjenning av 100% overtid.
   • Langvakter (12.5 timer) ved botilbud følges opp med drøftingsprotokoller jf. HTA § 4 og AML § 10-12.

3. STATLIG TOPPFINANSIERING & NAV-REFUSJONER:
   • Refusjonskrav for ressurskrevende tjenester (art 16500) over innslagspunktet 1.65 MNOK er sendt Helsedirektoratet.
   • Utestående sykepengerefusjoner fra NAV (art 16900): kr 214 000 følges opp ukentlig.

4. TILTAKSPLAN:
   • Helgebemanning optimaliseres ved å benytte faste helgevikarer fremfor kostbar overtid.

Med vennlig hilsen,
Enhetslederne i Helse og mestring`;

            setShareMode("email");
            document.getElementById("teams-email-modal").style.display = "flex";
        }

        function sendByutviklingReportToSjef() {
            currentShareMode = "email";
            const toInput = document.getElementById("share-email-to");
            const ccInput = document.getElementById("share-email-cc");
            const subjInput = document.getElementById("share-email-subject");
            const bodyArea = document.getElementById("share-message-body");

            toInput.value = "Ragnar Evensen <ragnar.evensen@kristiansand.kommune.no>";
            ccInput.value = "frank.ellingsen@kristiansand.kommune.no, knut.arild.vike@kristiansand.kommune.no";
            subjInput.value = `Månedsrapport By- og stedsutvikling (M10-2026): Selvkostgrad, Gebyrer & Saksbehandlingsfrist`;

            bodyArea.value = `Til Kommunalsjef Ragnar Evensen,

Her er månedlig status for By- og stedsutvikling og Ingeniørvesenet VAR:

1. PLAN- OG BYGGESAK (§ 21-7):
   • 98.2 % av byggesøknader er behandlet innen lovpålagt 12-ukers frist (unngår 25% gebyravkorting).
   • Selvkostgrad byggesak: 96.5 % i balanse.

2. VAR SELVKOST (VANN, AVLØP, RENOVASJON jf. Forurensningsloven):
   • 100 % selvkostbalanse overholdt jf. Kommuneloven § 14-9.
   • Selvkostfond: Vann (+8.4 MNOK), Avløp (+12.1 MNOK), Renovasjon (+3.2 MNOK).
   • Rente- og strømøkninger håndteres via fondsavsetninger uten akutt gebyrsjokk for innbyggerne.

Med vennlig hilsen,
Hans Petter Vik / Helge Møller`;

            setShareMode("email");
            document.getElementById("teams-email-modal").style.display = "flex";
        }

        function sendKulturReportToSjef() {
            currentShareMode = "email";
            const toInput = document.getElementById("share-email-to");
            const ccInput = document.getElementById("share-email-cc");
            const subjInput = document.getElementById("share-email-subject");
            const bodyArea = document.getElementById("share-message-body");

            toInput.value = "Camilla Jarlsby <camilla.jarlsby@kristiansand.kommune.no>";
            ccInput.value = "frank.ellingsen@kristiansand.kommune.no, okonomi.kultur@kristiansand.kommune.no";
            subjInput.value = `Månedsrapport Kultur & Dialog (M10-2026): Frivillighetstilskudd & Egeninntekter`;

            bodyArea.value = `Til Kommunalsjef Camilla Jarlsby,

Her er månedlig status for Kultur og innbyggerdialog:

1. FRIVILLIGHETS- OG IDRETTSTILSKUDD (Art 14700):
   • Tildelt hittil i år: kr 14.2 MNOK.
   • Gjenstående ramme for høsttildeling: kr 3.8 MNOK. Prioriterer lavterskel barne- og ungdomsaktivitet.

2. EGENINNTEKTER (Art 16200):
   • Bibliotek, Kulturskole og arrangementsinntekter ligger kr 2.1 MNOK over periodisert budsjett.

Med vennlig hilsen,
Kulturledelsen`;

            setShareMode("email");
            document.getElementById("teams-email-modal").style.display = "flex";
        }

        function sendOrgTekReportToSjef() {
            currentShareMode = "email";
            const toInput = document.getElementById("share-email-to");
            const ccInput = document.getElementById("share-email-cc");
            const subjInput = document.getElementById("share-email-subject");
            const bodyArea = document.getElementById("share-message-body");

            toInput.value = "Geir Askvik <geir.askvik@kristiansand.kommune.no>";
            ccInput.value = "frank.ellingsen@kristiansand.kommune.no, okonomi.orgtek@kristiansand.kommune.no";
            subjInput.value = `Månedsrapport Organisasjon og Teknologi (M10-2026): FinOps Lisenser & Konsulentinnleie`;

            bodyArea.value = `Til Kommunalsjef Geir Askvik,

Her er månedlig status fra Digitaliseringsavdelingen:

1. SKY- OG PROGRAMVARELISENSER (FinOps):
   • M365 Copilot og Visma lisensportefølje gjennomgått.
   • FinOps sanering av 150 inaktive kontoer frigjør kr 518 400 årlig.

2. KONSULENTINNLEIE VS INTERNE ÅRSVERK:
   • Konsulentutgifter (art 12000) redusert med 12 % ved overføring av prosjektoppgaver til faste ansatte.

Med vennlig hilsen,
Siri Bentsen (IKT-direktør)`;

            setShareMode("email");
            document.getElementById("teams-email-modal").style.display = "flex";
        }

        function sendKonsernReportToBystyret() {
            currentShareMode = "email";
            const toInput = document.getElementById("share-email-to");
            const ccInput = document.getElementById("share-email-cc");
            const subjInput = document.getElementById("share-email-subject");
            const bodyArea = document.getElementById("share-message-body");

            toInput.value = "Camilla Dunsæd <camilla.dunsaed@kristiansand.kommune.no>";
            ccInput.value = "frank.ellingsen@kristiansand.kommune.no, terje.fjellvang@kristiansand.kommune.no";
            subjInput.value = `Politisk Saksfremlegg: Tertialrapport og budsjettregulering 2026 jf. Kommuneloven § 14-5`;

            bodyArea.value = `Til Kommunedirektør Camilla Dunsæd / Formannskapet og Bystyret,

SAKSFREMLEGG: TERTIALSTATUS OG RAMMEJUSTERINGER 2026

1. TOTALØKONOMISK STATUS (7.24 MRD NOK BUDSJETT):
   • Netto driftsresultat prognoseres til 1.42 % (Målkrav: 1.75 % jf. Bystyrets handlingsregler).
   • Disposisjonsfondets saldo er kr 418 MNOK (5.8 % av brutto driftsinntekter), som tilfredsstiller soliditetskravet (> 5.0 %).

2. BUDSJETTBALLANSE OG MERFORBRUKSOMRÅDER (Jf. § 14-5):
   • Oppvekst (Grunnskole) har akutt vikarmerforbruk på 5.2 MNOK grunnet 11.4 % sykefravær.
   • Helse og omsorg har turnusavvik på 2.8 MNOK.

3. FORSLAG TIL VEDTAK:
   1. Bystyret tar tertialrapporten til etterretning.
   2. Det bevilges kr 5.2 MNOK i tilleggsbevilgning til Grunnskole finansiert ved tilsvarende bruk av sentral lønnsreserve.
   3. Kommunedirektørens innstrammingstiltak på korttidsvikarer godkjennes.

Med hilsen,
Frank Ellingsen (Senior Controller) / Terje Fjellvang (Finansdirektør)`;

            setShareMode("email");
            document.getElementById("teams-email-modal").style.display = "flex";
        }

        // ==========================================================================
        // HOVEDFUNKSJON: DYNAMISK RENDERING AV SEKTORDASHBOARD
        // ==========================================================================
        function renderSektorSpesifikkLederModul(unitId, monthNum) {
            const container = document.getElementById("sektor-spesifikk-leder-modul");
            if (!container) return;

            const isSchool = unitId in SKOLE_METRICS_REGISTRY || unitId.startsWith("4100") || unitId.startsWith("4101") || unitId.startsWith("4102") || unitId.startsWith("4210") || unitId.includes("OPPV");
            const isHealth = unitId.startsWith("5200") || unitId.startsWith("5210") || unitId.startsWith("5220") || unitId.startsWith("5230") || unitId.includes("SYKEHJEM") || unitId.includes("HELSE");
            const isByutvikling = unitId.startsWith("3300") || unitId.startsWith("3100") || unitId.startsWith("3000") || unitId.includes("VAR") || unitId.includes("BYUTV");
            const isKultur = unitId.startsWith("2100") || unitId.startsWith("2000") || unitId.includes("KULTUR");
            const isOrgTek = unitId.startsWith("1100") || unitId.startsWith("1000") || unitId.includes("IKT") || unitId.includes("ORG");
            const isKonsern = unitId.startsWith("0000") || unitId.startsWith("6000") || unitId.startsWith("6001") || unitId.includes("KOMMDIR") || unitId.includes("OKONOMI");

            container.style.display = "block";

            if (isSchool) {
                // ==============================================================
                // 1. OPPVEKST & UTDANNING (Skoleleder & Barnehagestyrer)
                // ==============================================================
                const s = SKOLE_METRICS_REGISTRY[unitId] || SKOLE_METRICS_REGISTRY["4100-ENH-202"];
                container.innerHTML = `
                <div class="bank-card" style="border: 2px solid #0284c7; background: #ffffff; padding: 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1.5px solid #e0f2fe; padding-bottom: 14px; margin-bottom: 16px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 20px;">🎓</span>
                                <span style="font-size: 16px; font-weight: 700; color: var(--navy-dark);">${s.skoleNavn} — Skole- &amp; Oppvekstdashboard</span>
                                <span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight: 700;">Lærernorm § 8-2 &bull; Spes.ped &bull; SFO Selvkost</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                <strong>Leder:</strong> ${s.rektorNavn} &bull; <strong>Inspektør:</strong> ${s.inspektorNavn} &bull; <strong>SFO-leder:</strong> ${s.sfoLederNavn}
                            </div>
                            <div style="font-size: 11.5px; color: #0284c7; margin-top: 2px; font-family: var(--font-mono);">
                                📍 ${s.skoleAarTermin}
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <a href="templates/MAL_BEMANNINGSPLAN_OG_VIKARBUDSJETT.xlsx" download class="btn btn-sm" style="background:#f0fdf4; color:#166534; border-color:#bbf7d0; font-weight:600;" title="Last ned FAST bemanningsplan i Excel">
                                📊 Bemanningsmal (.xlsx)
                            </a>
                            <button class="btn btn-sm btn-primary" onclick="sendRektorReportToSkolesjef()" style="background: #0284c7; border-color: #0284c7;" title="Send ferdig utfylt månedsrapport til skolesjef Svein Tore Kvernes">
                                📤 Send Rapport til Skolesjefen
                            </button>
                        </div>
                    </div>

                    <!-- 4 Pedagogiske og Juridiske Kjerne-KPIer -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 18px;">
                        <div class="kpi-card" style="border-left: 3px solid var(--navy-dark); padding: 10px 14px; background: #f8fafc;">
                            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">👥 Elevtall &amp; Ressursgrunnlag</div>
                            <div style="font-size: 19px; font-weight: 700; color: var(--navy-dark);">${s.elevtall} elever</div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">
                                <strong>${s.rammePerElev.toLocaleString("no-NO")} kr</strong> per elev &bull; ${s.ansatteAarsverk} årsverk
                            </div>
                        </div>

                        <div class="kpi-card" style="border-left: 3px solid #15803d; padding: 10px 14px; background: #f0fdf4;">
                            <div style="font-size: 11px; color: #166534; text-transform: uppercase;">👩‍🏫 Lærernorm § 8-2 (Lovkrav)</div>
                            <div style="font-size: 17px; font-weight: 700; color: #15803d;">
                                1.–4: ${s.laerernorm14.ratio} &bull; 5.–7: ${s.laerernorm57.ratio}
                            </div>
                            <div style="font-size: 11px; color: #166534; margin-top: 2px;">
                                🟢 Lovkrav overholdt (${s.laererAarsverk} av ${s.laererPlanlagt} årsverk)
                            </div>
                        </div>

                        <div class="kpi-card" style="border-left: 3px solid #7c3aed; padding: 10px 14px; background: #faf5ff;">
                            <div style="font-size: 11px; color: #6b21a8; text-transform: uppercase;">🧩 Spesialundervisning (§ 5-1)</div>
                            <div style="font-size: 19px; font-weight: 700; color: #7c3aed;">${s.spesPed.eleverMedVedtak} enkeltvedtak</div>
                            <div style="font-size: 11px; color: #6b21a8; margin-top: 2px;">
                                ${s.spesPed.timerAar.toLocaleString("no-NO")} t/år (${s.spesPed.dekningFellespottPct} % fellespottsdekning)
                            </div>
                        </div>

                        <div class="kpi-card" style="border-left: 3px solid #0284c7; padding: 10px 14px; background: #f0f9ff;">
                            <div style="font-size: 11px; color: #0369a1; text-transform: uppercase;">🧸 SFO Egenbalanse (Selvkost)</div>
                            <div style="font-size: 19px; font-weight: 700; color: ${s.sfo.balanse >= 0 ? '#15803d' : '#c0392b'};">
                                ${s.sfo.balanse >= 0 ? '+' : ''}${s.sfo.balanse.toLocaleString("no-NO")} kr
                            </div>
                            <div style="font-size: 11px; color: #0369a1; margin-top: 2px;">
                                ${s.sfoBarn > 0 ? `${s.sfoBarn} barn &bull; 🟢 I balanse` : s.sfo.status}
                            </div>
                        </div>
                    </div>

                    <!-- Vikar- og Fraværsradar -->
                    <div style="background: #fffbeb; border: 1.5px solid #fef3c7; border-left: 4px solid #d97706; padding: 14px 16px; border-radius: 4px; margin-bottom: 18px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <span style="font-size: 13px; font-weight: 700; color: #92400e;">
                                    ⏱️ Vikar- og Sykefraværsradaren (Art 10200 Timelærere &amp; GAT)
                                </span>
                                <div style="font-size: 11.5px; color: #b45309; margin-top: 2px;">
                                    Sykefravær: <strong>${s.vikar.sykefravaerPct} %</strong> &bull; Tildelt vikarramme: ${s.vikar.ramme.toLocaleString("no-NO")} kr &bull; Brukt YTD: ${s.vikar.brukt.toLocaleString("no-NO")} kr (${s.vikar.pct} %)
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 11px; color: #92400e; text-transform: uppercase;">Gjenstående vikarbudsjett</div>
                                <div style="font-size: 18px; font-weight: 800; color: ${s.vikar.rest < 200000 ? '#c0392b' : '#15803d'};">
                                    ${s.vikar.rest.toLocaleString("no-NO")} kr
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 10px; font-size: 12px; color: #78350f; line-height: 1.5; background: #ffffff; padding: 8px 12px; border-radius: 4px; border: 1px solid #fde68a;">
                            ${s.vikar.statusAlert}<br>
                            💡 <strong>Utestående NAV-refusjoner (art 16900):</strong> Skolen har krav på ca. <strong>${s.vikar.utestaaendeNavRefusjon.toLocaleString("no-NO")} kr</strong> fra NAV for sykemeldinger over 16 dager.
                        </div>
                    </div>

                    <!-- Hva-hvis Vikarkalkulator -->
                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: 4px; padding: 16px;">
                        <div style="font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px;">
                            💡 Rektors «Hva-hvis» Vikarkalkulator (Regn ut kostnad og NAV-refusjon før du leier inn)
                        </div>
                        <div style="display: flex; gap: 14px; align-items: center; flex-wrap: wrap; margin-bottom: 12px; background: #ffffff; padding: 10px 14px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary);">Stilling:</span>
                                <button type="button" class="btn btn-sm" id="sim-btn-laerer" onclick="setVikarSimStilling('LAERER')" style="background: var(--navy-dark); color: #fff; font-weight: 600;">👩‍🏫 Lærer (100%)</button>
                                <button type="button" class="btn btn-sm" id="sim-btn-assistent" onclick="setVikarSimStilling('ASSISTENT')" style="background: #f1f5f9; color: var(--text-primary);">🤝 Assistent</button>
                            </div>
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); margin-left: 10px;">Fraværsvarighet:</span>
                                <button type="button" class="btn btn-sm sim-uke-pill" data-uker="1" onclick="setVikarSimUker(1)" style="background:#f1f5f9;">1 uke</button>
                                <button type="button" class="btn btn-sm sim-uke-pill" data-uker="2" onclick="setVikarSimUker(2)" style="background:#f1f5f9;">2 uker</button>
                                <button type="button" class="btn btn-sm sim-uke-pill" data-uker="3" onclick="setVikarSimUker(3)" style="background:var(--navy-dark); color:#fff; font-weight:700;">3 uker</button>
                                <button type="button" class="btn btn-sm sim-uke-pill" data-uker="4" onclick="setVikarSimUker(4)" style="background:#f1f5f9;">4 uker</button>
                                <button type="button" class="btn btn-sm sim-uke-pill" data-uker="6" onclick="setVikarSimUker(6)" style="background:#f1f5f9;">6 uker</button>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; background: #ffffff; padding: 12px 14px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Egen vikar (380 kr/t)</div>
                                <div style="font-size: 16px; font-weight: 700; color: var(--navy-dark);" id="sim-res-intern">42 750 kr</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Byråvikar (680 kr/t)</div>
                                <div style="font-size: 16px; font-weight: 700; color: #c0392b;" id="sim-res-byra">76 500 kr</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">NAV-Refusjon (fra dag 17)</div>
                                <div style="font-size: 16px; font-weight: 700; color: #15803d;" id="sim-res-nav">+8 600 kr</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Netto utgift (Egen vikar)</div>
                                <div style="font-size: 16px; font-weight: 700; color: #0284c7;" id="sim-res-netto">34 150 kr</div>
                            </div>
                            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 8px 10px;">
                                <div style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase;">💰 Din Innsparing:</div>
                                <div style="font-size: 17px; font-weight: 800; color: #15803d;" id="sim-res-gevinst">33 750 kr</div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                recalcVikarKalkulator();

            } else if (isHealth) {
                // ==============================================================
                // 2. HELSE OG MESTRING (Sykehjem, Hjemmetjeneste & Botilbud)
                // ==============================================================
                const isHomeCare = unitId === "5210-ENH-402";
                const isLivingCommunity = unitId === "5220-ENH-403";

                container.innerHTML = `
                <div class="bank-card" style="border: 2px solid #059669; background: #ffffff; padding: 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1.5px solid #d1fae5; padding-bottom: 14px; margin-bottom: 16px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 20px;">🏥</span>
                                <span style="font-size: 16px; font-weight: 700; color: var(--navy-dark);">
                                    ${isHomeCare ? 'Hjemmetjenesten Vågsbygd — Sektordashboard' : (isLivingCommunity ? 'Sørlandsparken Bo- og Miljø — Botilbud Dashboard' : 'Pleie- og Omsorgsdashboard (Sykehjem)')}
                                </span>
                                <span class="badge" style="background: #d1fae5; color: #065f46; font-weight: 700;">GAT Turnus &bull; AML § 10-6/12 &bull; HTA § 4</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                <strong>Styringsfokus:</strong> Døgnbemanning, pasientbelegg, overtidskontroll og statlig toppfinansiering
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <a href="templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx" download class="btn btn-sm" style="background:#ecfdf5; color:#065f46; border-color:#a7f3d0; font-weight:600;" title="Last ned HTA § 4 drøftingsprotokoll i Word">
                                📋 HTA § 4 Protokoll
                            </a>
                            <button class="btn btn-sm" onclick="sendHelseReportToKommunalsjef()" style="background: #059669; color: #fff; border-color: #059669;" title="Send månedsrapport til kommunalsjef Brede Skeie">
                                📤 Send Rapport til Kommunalsjefen
                            </button>
                        </div>
                    </div>

                    <!-- Helse Kjerne-KPIer -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 16px;">
                        <div class="kpi-card" style="border-left: 3px solid #059669; padding: 10px 14px; background: #f0fdf4;">
                            <div style="font-size: 11px; color: #065f46; text-transform: uppercase;">🛏️ Pasientbelegg / Kapasitet</div>
                            <div style="font-size: 18px; font-weight: 700; color: #059669;">98.4 % belegg</div>
                            <div style="font-size: 11px; color: #065f46; margin-top: 2px;">Full drift på døgnplasser</div>
                        </div>

                        <div class="kpi-card" style="border-left: 3px solid var(--navy-dark); padding: 10px 14px; background: #f8fafc;">
                            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">
                                ${isHomeCare ? '🚗 Bilpark & Leasing (Art 11900)' : '💉 Pleiefaktor per pasient'}
                            </div>
                            <div style="font-size: 18px; font-weight: 700; color: var(--navy-dark);">
                                ${isHomeCare ? '24 leasingbiler' : '0.84 pleier/pasient'}
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">
                                ${isHomeCare ? 'Ruteoptimalisering iverksatt' : 'I tråd med bemanningsnorm'}
                            </div>
                        </div>

                        <div class="kpi-card" style="border-left: 3px solid #d97706; padding: 10px 14px; background: #fffbeb;">
                            <div style="font-size: 11px; color: #92400e; text-transform: uppercase;">📋 GAT Overtid &amp; Helgetillegg</div>
                            <div style="font-size: 18px; font-weight: 700; color: #d97706;">kr 385 000 YTD</div>
                            <div style="font-size: 11px; color: #92400e; margin-top: 2px;">Restriktiv overtid godkjent</div>
                        </div>

                        <div class="kpi-card" style="border-left: 3px solid #0284c7; padding: 10px 14px; background: #f0f9ff;">
                            <div style="font-size: 11px; color: #0369a1; text-transform: uppercase;">
                                ${isLivingCommunity ? '🏛️ Ressurskrevende (Art 16500)' : '💰 NAV Refusjoner (Art 16900)'}
                            </div>
                            <div style="font-size: 18px; font-weight: 700; color: #0284c7;">
                                ${isLivingCommunity ? 'kr 2 400 000 krav' : 'kr 214 000 innsendt'}
                            </div>
                            <div style="font-size: 11px; color: #0369a1; margin-top: 2px;">
                                ${isLivingCommunity ? '3 brukere over 1.65 MNOK' : '🟢 100 % oppfølgingsgrad'}
                            </div>
                        </div>
                    </div>

                    <!-- Interaktiv GAT Turnus- og Overtidskalkulator -->
                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: 4px; padding: 14px;">
                        <div style="font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px;">
                            💡 Avdelingsleders GAT Overtids- og Helgevaktkalkulator
                        </div>
                        <p style="font-size: 11.5px; color: var(--text-secondary); margin-bottom: 12px;">
                            Akutt fravær i helgen: Hva koster det å beordre fast sykepleier på overtid (100% helg jf. HTA § 6) vs. ringe inn helgevaktstudent?
                        </p>
                        <div style="display: flex; gap: 14px; align-items: center; flex-wrap: wrap; margin-bottom: 12px; background: #ffffff; padding: 8px 12px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary);">Antall helgevakter:</span>
                                <button type="button" class="btn btn-sm gat-vakt-pill" data-vakter="1" onclick="setGatSimVakt(1)" style="background:#f1f5f9;">1 vakt (7.5t)</button>
                                <button type="button" class="btn btn-sm gat-vakt-pill" data-vakter="2" onclick="setGatSimVakt(2)" style="background:var(--navy-dark); color:#fff; font-weight:700;">2 vakter (15t)</button>
                                <button type="button" class="btn btn-sm gat-vakt-pill" data-vakter="4" onclick="setGatSimVakt(4)" style="background:#f1f5f9;">4 vakter (30t)</button>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; background: #ffffff; padding: 12px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Fast sykepleier overtid (780 kr/t)</div>
                                <div style="font-size: 16px; font-weight: 700; color: #c0392b;" id="gat-res-kostnad">11 700 kr</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Student / Ekstravakt (340 kr/t)</div>
                                <div style="font-size: 16px; font-weight: 700; color: #0284c7;" id="gat-res-alt">5 100 kr</div>
                            </div>
                            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 8px 10px;">
                                <div style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase;">💰 Sparetiltak ved tidlig planlegging:</div>
                                <div style="font-size: 17px; font-weight: 800; color: #15803d;" id="gat-res-sparing">6 600 kr</div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                recalcGatKalkulator();

            } else if (isByutvikling) {
                // ==============================================================
                // 3. BY- OG STEDSUTVIKLING & VAR SELVKOST
                // ==============================================================
                container.innerHTML = `
                <div class="bank-card" style="border: 2px solid #0284c7; background: #ffffff; padding: 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1.5px solid #e0f2fe; padding-bottom: 14px; margin-bottom: 16px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 20px;">🏗️</span>
                                <span style="font-size: 16px; font-weight: 700; color: var(--navy-dark);">By- og stedsutvikling &bull; Selvkost &amp; VAR</span>
                                <span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight: 700;">100 % Selvkost jf. § 14-9 &bull; Pbl § 21-7</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                <strong>Styringsfokus:</strong> Saksbehandlingsfrister, gebyrinntekter og selvkostfond for Vann, Avløp og Renovasjon
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <a href="templates/MAL_OMDISPONERING_OG_RAMMEJUSTERING.docx" download class="btn btn-sm" style="background:#f0f9ff; color:#0369a1; border-color:#bae6fd; font-weight:600;" title="Last ned omdisponeringsmal for Byutvikling">
                                🔄 Omdisponering (.docx)
                            </a>
                            <button class="btn btn-sm btn-primary" onclick="sendByutviklingReportToSjef()" style="background: #0284c7; border-color: #0284c7;" title="Send månedsrapport til kommunalsjef Ragnar Evensen">
                                📤 Send Rapport til Kommunalsjefen
                            </button>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 16px;">
                        <div class="kpi-card" style="border-left: 3px solid #15803d; padding: 10px 14px; background: #f0fdf4;">
                            <div style="font-size: 11px; color: #166534; text-transform: uppercase;">⏱️ Saksbehandlingsfrist (Pbl § 21-7)</div>
                            <div style="font-size: 18px; font-weight: 700; color: #15803d;">98.2 % innen frist</div>
                            <div style="font-size: 11px; color: #166534; margin-top: 2px;">Ingen 25% gebyravkorting</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid var(--navy-dark); padding: 10px 14px; background: #f8fafc;">
                            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">💰 Gebyrinntekter (Art 16200)</div>
                            <div style="font-size: 18px; font-weight: 700; color: var(--navy-dark);">kr 24 150 000</div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">Selvkostgrad: 96.5 % (I balanse)</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid #0284c7; padding: 10px 14px; background: #f0f9ff;">
                            <div style="font-size: 11px; color: #0369a1; text-transform: uppercase;">💧 Selvkostfond Vann &amp; Avløp</div>
                            <div style="font-size: 18px; font-weight: 700; color: #0284c7;">kr 20 500 000</div>
                            <div style="font-size: 11px; color: #0369a1; margin-top: 2px;">Avsetning følger 5-års plan</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid #7c3aed; padding: 10px 14px; background: #faf5ff;">
                            <div style="font-size: 11px; color: #6b21a8; text-transform: uppercase;">🏗️ Investeringsprosjekter</div>
                            <div style="font-size: 18px; font-weight: 700; color: #7c3aed;">kr 142 MNOK YTD</div>
                            <div style="font-size: 11px; color: #6b21a8; margin-top: 2px;">Gartnerløkka &amp; VA-oppgradering</div>
                        </div>
                    </div>

                    <!-- Interaktiv VAR Selvkost- og Gebyrkalkulator -->
                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: 4px; padding: 14px;">
                        <div style="font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px;">
                            💡 VA-sjefens Selvkost- og Gebyrkalkulator (Effekt av strøm- og renteøkning)
                        </div>
                        <p style="font-size: 11.5px; color: var(--text-secondary); margin-bottom: 12px;">
                            Hvis pumpe- og rensekostnadene øker: Hvor mye belastes selvkostfondet, og hva betyr det for husstandenes månedlige gebyr?
                        </p>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary);">Kostnadsøkning:</span>
                            <button type="button" class="btn btn-sm var-pct-pill" data-pct="5" onclick="setVarSimEndring(5)" style="background:#f1f5f9;">+5 %</button>
                            <button type="button" class="btn btn-sm var-pct-pill" data-pct="10" onclick="setVarSimEndring(10)" style="background:var(--navy-dark); color:#fff; font-weight:700;">+10 %</button>
                            <button type="button" class="btn btn-sm var-pct-pill" data-pct="15" onclick="setVarSimEndring(15)" style="background:#f1f5f9;">+15 %</button>
                            <button type="button" class="btn btn-sm var-pct-pill" data-pct="20" onclick="setVarSimEndring(20)" style="background:#f1f5f9;">+20 %</button>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; background: #ffffff; padding: 12px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Årlig merkostnad VAR</div>
                                <div style="font-size: 16px; font-weight: 700; color: #c0392b;" id="var-res-merkost">+6 840 000 kr/år</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Fondsbruk uten gebyrsjokk</div>
                                <div style="font-size: 16px; font-weight: 700; color: #0284c7;" id="var-res-fondbruk">6 840 000 kr (Fra fond)</div>
                            </div>
                            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 8px 10px;">
                                <div style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase;">Beregnet gebyrjustering / husstand:</div>
                                <div style="font-size: 17px; font-weight: 800; color: #15803d;" id="var-res-gebyr">+12 kr / mnd</div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                recalcVarKalkulator();

            } else if (isKultur) {
                // ==============================================================
                // 4. KULTUR OG INNBYGGERDIALOG
                // ==============================================================
                container.innerHTML = `
                <div class="bank-card" style="border: 2px solid #d97706; background: #ffffff; padding: 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(217, 119, 6, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1.5px solid #fef3c7; padding-bottom: 14px; margin-bottom: 16px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 20px;">🎭</span>
                                <span style="font-size: 16px; font-weight: 700; color: var(--navy-dark);">Kultur, Idrett &amp; Frivillighet</span>
                                <span class="badge" style="background: #fef3c7; color: #92400e; font-weight: 700;">Tilskuddsforvaltning &bull; Kilden &bull; Bibliotek</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                <strong>Styringsfokus:</strong> Tilskuddsmidler til frivillige lag (post 14700) og egeninntekter fra kulturskole og utleie
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <a href="templates/MAL_LEDERENS_MANEDSSTATUS_OG_PROGNOSE.docx" download class="btn btn-sm" style="background:#fffbeb; color:#92400e; border-color:#fde68a; font-weight:600;" title="Last ned lederens månedsstatus i Word">
                                📝 Månedsstatus (.docx)
                            </a>
                            <button class="btn btn-sm" onclick="sendKulturReportToSjef()" style="background: #d97706; color: #fff; border-color: #d97706;" title="Send månedsrapport til Kulturutvalget">
                                📤 Send Rapport til Kulturutvalget
                            </button>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 16px;">
                        <div class="kpi-card" style="border-left: 3px solid #15803d; padding: 10px 14px; background: #f0fdf4;">
                            <div style="font-size: 11px; color: #166534; text-transform: uppercase;">🤝 Tildelt Frivillighet (Art 14700)</div>
                            <div style="font-size: 18px; font-weight: 700; color: #15803d;">kr 14 200 000</div>
                            <div style="font-size: 11px; color: #166534; margin-top: 2px;">78 idretts- og kulturforeninger</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid var(--navy-dark); padding: 10px 14px; background: #f8fafc;">
                            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">🍁 Gjenstående Høsttildeling</div>
                            <div style="font-size: 18px; font-weight: 700; color: var(--navy-dark);">kr 3 800 000</div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">Klar for politisk tildeling</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid #0284c7; padding: 10px 14px; background: #f0f9ff;">
                            <div style="font-size: 11px; color: #0369a1; text-transform: uppercase;">🎟️ Egeninntekter (Art 16200)</div>
                            <div style="font-size: 18px; font-weight: 700; color: #0284c7;">+kr 2 100 000</div>
                            <div style="font-size: 11px; color: #0369a1; margin-top: 2px;">Kulturskole &amp; Kilden over budsjett</div>
                        </div>
                    </div>

                    <!-- Interaktiv Tilskuddskalkulator -->
                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: 4px; padding: 14px;">
                        <div style="font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px;">
                            💡 Kultursjefens Tilskuddssimulator (Høstfordeling til lag og foreninger)
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary);">Antall søkerlag:</span>
                            <button type="button" class="btn btn-sm kultur-soker-pill" data-sokere="10" onclick="setKulturSimSokere(10)" style="background:#f1f5f9;">10 lag</button>
                            <button type="button" class="btn btn-sm kultur-soker-pill" data-sokere="25" onclick="setKulturSimSokere(25)" style="background:var(--navy-dark); color:#fff; font-weight:700;">25 lag</button>
                            <button type="button" class="btn btn-sm kultur-soker-pill" data-sokere="40" onclick="setKulturSimSokere(40)" style="background:#f1f5f9;">40 lag</button>
                            <button type="button" class="btn btn-sm kultur-soker-pill" data-sokere="60" onclick="setKulturSimSokere(60)" style="background:#f1f5f9;">60 lag</button>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; background: #ffffff; padding: 12px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Snittstøtte per lag</div>
                                <div style="font-size: 16px; font-weight: 700; color: var(--navy-dark);" id="kultur-res-snitt">152 000 kr</div>
                            </div>
                            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 8px 10px;">
                                <div style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase;">Beregnet støtte per aktivt barn:</div>
                                <div style="font-size: 17px; font-weight: 800; color: #15803d;" id="kultur-res-barn">ca. 3 378 kr/år</div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                recalcKulturKalkulator();

            } else if (isOrgTek) {
                // ==============================================================
                // 5. ORGANISASJON OG TEKNOLOGI (Digitalisering & IKT)
                // ==============================================================
                container.innerHTML = `
                <div class="bank-card" style="border: 2px solid #6366f1; background: #ffffff; padding: 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1.5px solid #e0e7ff; padding-bottom: 14px; margin-bottom: 16px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 20px;">💻</span>
                                <span style="font-size: 16px; font-weight: 700; color: var(--navy-dark);">Organisasjon, IKT &amp; Digitalisering</span>
                                <span class="badge" style="background: #e0e7ff; color: #3730a3; font-weight: 700;">FinOps Lisenser &bull; M365 &bull; Konsulentreduksjon</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                <strong>Styringsfokus:</strong> M365 Copilot lisensoptimalisering, skykostnader og reduksjon av konsulentinnleie
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <a href="templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx" download class="btn btn-sm" style="background:#eef2ff; color:#3730a3; border-color:#c7d2fe; font-weight:600;" title="Last ned FRIA og DPIA risikovurdering i Word">
                                🛡️ DPIA Mal (.docx)
                            </a>
                            <button class="btn btn-sm" onclick="sendOrgTekReportToSjef()" style="background: #4f46e5; color: #fff; border-color: #4f46e5;" title="Send månedsrapport til kommunalsjef Geir Askvik">
                                📤 Send Rapport til Kommunalsjefen
                            </button>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 16px;">
                        <div class="kpi-card" style="border-left: 3px solid #4f46e5; padding: 10px 14px; background: #eef2ff;">
                            <div style="font-size: 11px; color: #3730a3; text-transform: uppercase;">☁️ Sky- &amp; Lisenskostnader</div>
                            <div style="font-size: 18px; font-weight: 700; color: #4f46e5;">kr 18 400 000 YTD</div>
                            <div style="font-size: 11px; color: #3730a3; margin-top: 2px;">M365, Visma &amp; Framsikt</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid var(--navy-dark); padding: 10px 14px; background: #f8fafc;">
                            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">💼 Konsulentandel (Art 12000)</div>
                            <div style="font-size: 18px; font-weight: 700; color: var(--navy-dark);">14.2 % av driftsrammen</div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">🟢 Ned 3.5 % etter insourcing</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid #15803d; padding: 10px 14px; background: #f0fdf4;">
                            <div style="font-size: 11px; color: #166534; text-transform: uppercase;">🚀 Digitaliseringsprosjekter</div>
                            <div style="font-size: 18px; font-weight: 700; color: #15803d;">8 aktive løp</div>
                            <div style="font-size: 11px; color: #166534; margin-top: 2px;">Felles innbyggerportal &amp; AI-pilot</div>
                        </div>
                    </div>

                    <!-- Interaktiv FinOps Lisenskalkulator -->
                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: 4px; padding: 14px;">
                        <div style="font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px;">
                            💡 IKT-direktørens FinOps Lisenskalkulator (Gevinst ved lisenssanering)
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary);">Inaktive M365/Copilot lisenser:</span>
                            <button type="button" class="btn btn-sm ikt-lisens-pill" data-lisenser="50" onclick="setIktSimLisenser(50)" style="background:#f1f5f9;">50 lisenser</button>
                            <button type="button" class="btn btn-sm ikt-lisens-pill" data-lisenser="100" onclick="setIktSimLisenser(100)" style="background:var(--navy-dark); color:#fff; font-weight:700;">100 lisenser</button>
                            <button type="button" class="btn btn-sm ikt-lisens-pill" data-lisenser="150" onclick="setIktSimLisenser(150)" style="background:#f1f5f9;">150 lisenser</button>
                            <button type="button" class="btn btn-sm ikt-lisens-pill" data-lisenser="250" onclick="setIktSimLisenser(250)" style="background:#f1f5f9;">250 lisenser</button>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; background: #ffffff; padding: 12px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Månedlig innsparing</div>
                                <div style="font-size: 16px; font-weight: 700; color: #0284c7;" id="ikt-res-mnd">36 000 kr / mnd</div>
                            </div>
                            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 8px 10px;">
                                <div style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase;">Frigjort årlig IT-driftsbudsjett:</div>
                                <div style="font-size: 17px; font-weight: 800; color: #15803d;" id="ikt-res-aar">432 000 kr / år</div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                recalcIktKalkulator();

            } else {
                // ==============================================================
                // 6. KONSERN OG TOPPLEDELSE (Kommunedirektør & Økonomidirektør)
                // ==============================================================
                container.innerHTML = `
                <div class="bank-card" style="border: 2px solid var(--navy-dark); background: #ffffff; padding: 20px; border-radius: 4px; box-shadow: 0 4px 12px rgba(27, 54, 93, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 14px; margin-bottom: 16px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 20px;">🏛️</span>
                                <span style="font-size: 16px; font-weight: 700; color: var(--navy-dark);">Konsernledelse &bull; Kristiansand Bystyre &amp; Formannskap</span>
                                <span class="badge" style="background: #f1f5f9; color: var(--navy-dark); font-weight: 700;">7.24 mrd NOK Totalbudsjett &bull; Kommuneloven § 14-5</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                <strong>Toppledelse:</strong> Kommunedirektør Camilla Dunsæd &bull; Økonomidirektør Terje Fjellvang &bull; Senior Controller Frank Ellingsen
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <a href="templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx" download class="btn btn-sm" style="background:#f1f5f9; color:var(--navy-dark); border-color:#cbd5e1; font-weight:600;" title="Last ned politisk saksfremlegg-mal i Word">
                                🏛️ Politisk Sak (.docx)
                            </a>
                            <button class="btn btn-sm btn-primary" onclick="sendKonsernReportToBystyret()" style="background: var(--navy-dark); border-color: var(--navy-dark);" title="Generer politisk saksfremlegg til Formannskapet">
                                📤 Utarbeid Sak til Formannskapet
                            </button>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 16px;">
                        <div class="kpi-card" style="border-left: 3px solid #15803d; padding: 10px 14px; background: #f0fdf4;">
                            <div style="font-size: 11px; color: #166534; text-transform: uppercase;">🛡️ Disposisjonsfond (Mål &gt; 5.0 %)</div>
                            <div style="font-size: 18px; font-weight: 700; color: #15803d;">kr 418 000 000 (5.8 %)</div>
                            <div style="font-size: 11px; color: #166534; margin-top: 2px;">🟢 Robust buffer over målkrav</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid #d97706; padding: 10px 14px; background: #fffbeb;">
                            <div style="font-size: 11px; color: #92400e; text-transform: uppercase;">⚖️ Netto driftsresultat (§ 14-5)</div>
                            <div style="font-size: 18px; font-weight: 700; color: #d97706;">1.42 % (kr 102 MNOK)</div>
                            <div style="font-size: 11px; color: #92400e; margin-top: 2px;">Mål: 1.75 % (kr 126 MNOK) 🟡</div>
                        </div>
                        <div class="kpi-card" style="border-left: 3px solid #0284c7; padding: 10px 14px; background: #f0f9ff;">
                            <div style="font-size: 11px; color: #0369a1; text-transform: uppercase;">🏛️ Skatt &amp; Rammetilskudd</div>
                            <div style="font-size: 18px; font-weight: 700; color: #0284c7;">kr 4 120 000 000</div>
                            <div style="font-size: 11px; color: #0369a1; margin-top: 2px;">YTD -14.2 MNOK mot statsbudsjett</div>
                        </div>
                    </div>

                    <!-- Interaktiv Rente- og Skattesimulator -->
                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: 4px; padding: 14px;">
                        <div style="font-size: 13px; font-weight: 700; color: var(--navy-dark); margin-bottom: 4px;">
                            💡 Finansdirektørens Rente- og Soliditetssimulator (Lånegjeld: 4.2 milliarder NOK)
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary);">3M NIBOR renteøkning:</span>
                            <button type="button" class="btn btn-sm konsern-rente-pill" data-rente="0.5" onclick="setKonsernSimRente(0.5)" style="background:#f1f5f9;">+0.5 %</button>
                            <button type="button" class="btn btn-sm konsern-rente-pill" data-rente="1.0" onclick="setKonsernSimRente(1.0)" style="background:var(--navy-dark); color:#fff; font-weight:700;">+1.0 %</button>
                            <button type="button" class="btn btn-sm konsern-rente-pill" data-rente="1.5" onclick="setKonsernSimRente(1.5)" style="background:#f1f5f9;">+1.5 %</button>
                            <button type="button" class="btn btn-sm konsern-rente-pill" data-rente="2.0" onclick="setKonsernSimRente(2.0)" style="background:#f1f5f9;">+2.0 %</button>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; background: #ffffff; padding: 12px; border-radius: 4px; border: 1px solid var(--border-light);">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Årlig økt rentekostnad</div>
                                <div style="font-size: 16px; font-weight: 700; color: #c0392b;" id="konsern-res-kostnad">+42.0 MNOK</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Ny Disposisjonsfondsaldo</div>
                                <div style="font-size: 16px; font-weight: 700; color: #0284c7;" id="konsern-res-fond">376.0 MNOK (5.2 %)</div>
                            </div>
                            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 8px 10px;">
                                <div style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase;">Soliditetsstatus:</div>
                                <div style="font-size: 17px; font-weight: 800; color: #15803d;" id="konsern-res-buffer">🟢 Over 5% målkrav</div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                recalcKonsernKalkulator();
            }
        }
'''
        html = html[:idx_mod_start] + new_module_code + html[idx_mod_end:]
        print("✓ Satt inn komplett modul for alle 6 sektorer og personas")
    else:
        print("⚠️ Fant ikke modulmarkører")

    # Valider HTML før skriving
    validator = StrictHTMLValidator()
    validator.feed(html)
    if validator.errors:
        print("❌ HTML-VALIDERING FEILET:")
        for err in validator.errors[:10]:
            print(f"   {err}")
        sys.exit(1)
    else:
        print("✓ HTML-syntaks er 100 % strengt velformet!")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🎉 Vellykket oppgradering av {INDEX_FILE}!")

if __name__ == "__main__":
    build_upgrade()
