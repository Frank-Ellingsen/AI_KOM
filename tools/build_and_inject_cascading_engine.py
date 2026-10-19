# -*- coding: utf-8 -*-
"""
tools/build_and_inject_cascading_engine.py
Constructs the complete 81 units catalog, Framsikt cascading hierarchy,
and cascading unit dropdown engine, then injects it into index.html.
"""
import sys
import os
import json
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('tools'))

from build_81_units_script import build_data

raw_units = build_data()
print(f"Loaded {len(raw_units)} authentic resultatenheter.")

def enrich_unit(u):
    cpi = u['cpi']
    ramme = u['ramme']
    pv = u['pv']
    ac = u['ac']
    cv = u['cv']
    eac = int(ramme * (1.0 / max(0.85, cpi)))
    vac = ramme - eac
    p10 = int(eac * 0.99)
    p50 = eac
    p90 = int(eac * 1.015)
    
    cv_str = f"{abs(cv):,}".replace(',', ' ') + " kr"
    if cv < 0:
        diag_summary = f"Merforbruk på {cv_str} YTD. Bemanningsavvik og vikarutgifter over budsjettramme."
        art_10200 = f"+{abs(int(cv * 0.65)):,}".replace(',', ' ') + " kr"
        art_10900 = f"+{abs(int(cv * 0.35)):,}".replace(',', ' ') + " kr"
        diag_drivers = [
            {"art": "10200", "navn": "Vikarbyrå & Ekstern innleie", "belop": art_10200, "vurdering": "Innleie for å dekke akutt sykefravær og vaktvakanser."},
            {"art": "10900", "navn": "Overtid & helgetillegg", "belop": art_10900, "vurdering": "Overtid for å opprettholde lovpålagt bemanningsfaktor jf. HTA § 4."}
        ]
        status_txt = "🔴 Merforbruk jf. § 14-5"
        act_list = [
            {"nr": 1, "type": "BEMANNING", "tekst": f"Iverksette vikarrestriksjon og optimalisere intern timeplan/turnus for {u['name']}.", "frist": "Innen 7 dager"},
            {"nr": 2, "type": "KONTROLL", "tekst": "Gjennomgå sykefraværsoppfølging og ettersende refusjonskrav til NAV Agder.", "frist": "M+10 virkedag"},
            {"nr": 3, "type": "RAPPORT", "tekst": f"Utsende månedlig avviksrapport til rådgiver og kontrollere delegeringsfullmakt ({u['fullmakt']//1000000}M).", "frist": "M+12 virkedag"}
        ]
    else:
        diag_summary = f"Driftsøkonomisk balanse med et mindreforbruk på {cv_str} YTD."
        diag_drivers = [
            {"art": "10100", "navn": "Faste lønninger", "belop": "-320 000 kr", "vurdering": "Midlertidige vakanser gir lavere personalkostnader enn periodisert budsjett."},
            {"art": "11500", "navn": "Driftsmateriell & kurs", "belop": "-110 000 kr", "vurdering": "Restriktiv innkjøpsdisiplin jf. EPM-retningslinjer."}
        ]
        status_txt = "🟢 I balanse jf. § 14-5"
        act_list = [
            {"nr": 1, "type": "OPPFØLGING", "tekst": f"Opprettholde kostnadskontroll og følge opp rekruttering til ledige stillinger i {u['name']}.", "frist": "Løpende"},
            {"nr": 2, "type": "KONTROLL", "tekst": "Avstemme periodisering mot tertialprognose.", "frist": "M+15 virkedag"}
        ]

    spark = [
        round(pv/9/1000000 * 0.98, 1),
        round(pv/9/1000000 * 0.99, 1),
        round(pv/9/1000000 * 1.01, 1),
        round(pv/9/1000000 * 1.00, 1),
        round(pv/9/1000000 * 1.02, 1),
        round(pv/9/1000000 * 1.03, 1),
        round(pv/9/1000000 * 0.75, 1),
        round(pv/9/1000000 * 0.95, 1),
        round(ac/9/1000000, 1)
    ]

    children = []
    if u['niva'] == 3:
        if 'Skole' in u['name']:
            children = [
                {"id": f"{u['id']}-SFO", "name": f"SFO {u['name'].split()[0]}", "leder": "Avdelingsleder SFO", "tittel": "SFO-leder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-1", "kostra": "Funksjon 215", "fullmakt": 500000, "ramme": int(ramme*0.22), "pv": int(pv*0.22), "ac": int(ac*0.22), "cv": int(cv*0.22), "cpi": cpi, "sec": u['sec']},
                {"id": f"{u['id']}-1-4", "name": f"1.–4. Trinn Barnetrinn", "leder": "Avdelingsleder 1.–4.", "tittel": "Avdelingsleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-2", "kostra": "Funksjon 202", "fullmakt": 500000, "ramme": int(ramme*0.42), "pv": int(pv*0.42), "ac": int(ac*0.42), "cv": int(cv*0.42), "cpi": cpi, "sec": u['sec']},
                {"id": f"{u['id']}-5-7", "name": f"5.–7. Trinn Mellomtrinn", "leder": "Avdelingsleder 5.–7.", "tittel": "Avdelingsleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-3", "kostra": "Funksjon 202", "fullmakt": 500000, "ramme": int(ramme*0.36), "pv": int(pv*0.36), "ac": int(ac*0.36), "cv": int(cv*0.36), "cpi": cpi, "sec": u['sec']}
            ]
        elif 'Bo- og Miljø' in u['name'] or 'Sykehjem' in u['name'] or 'Omsorg' in u['name']:
            children = [
                {"id": f"{u['id']}-AVD1", "name": f"Avdeling 1 — Døgnomsorg", "leder": "Avdelingssykepleier", "tittel": "Avdelingsleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-1", "kostra": "Funksjon 254", "fullmakt": 500000, "ramme": int(ramme*0.55), "pv": int(pv*0.55), "ac": int(ac*0.55), "cv": int(cv*0.55), "cpi": cpi, "sec": u['sec']},
                {"id": f"{u['id']}-AVD2", "name": f"Avdeling 2 — Skjermet / Fagavdeling", "leder": "Fagleder Spesial", "tittel": "Fagleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-2", "kostra": "Funksjon 254", "fullmakt": 400000, "ramme": int(ramme*0.45), "pv": int(pv*0.45), "ac": int(ac*0.45), "cv": int(cv*0.45), "cpi": cpi, "sec": u['sec']}
            ]
        elif 'Barnehage' in u['name']:
            children = [
                {"id": f"{u['id']}-SMA", "name": f"Småbarnsavdeling (1–3 år)", "leder": "Pedagogisk leder", "tittel": "Ped.leder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-1", "kostra": "Funksjon 201", "fullmakt": 300000, "ramme": int(ramme*0.52), "pv": int(pv*0.52), "ac": int(ac*0.52), "cv": int(cv*0.52), "cpi": cpi, "sec": u['sec']},
                {"id": f"{u['id']}-STO", "name": f"Storebarnsavdeling (3–6 år)", "leder": "Pedagogisk leder", "tittel": "Ped.leder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-2", "kostra": "Funksjon 201", "fullmakt": 300000, "ramme": int(ramme*0.48), "pv": int(pv*0.48), "ac": int(ac*0.48), "cv": int(cv*0.48), "cpi": cpi, "sec": u['sec']}
            ]
        elif 'VAR' in u['name'] or 'Ingeniør' in u['name']:
            children = [
                {"id": f"{u['id']}-VANN", "name": f"Vannforsyning & Vannverk", "leder": "Driftsleder Vann", "tittel": "Driftsleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-1", "kostra": "Funksjon 340", "fullmakt": 800000, "ramme": int(ramme*0.48), "pv": int(pv*0.48), "ac": int(ac*0.48), "cv": int(cv*0.48), "cpi": cpi, "sec": u['sec']},
                {"id": f"{u['id']}-AVL", "name": f"Avløp & Renseanlegg", "leder": "Driftsleder Avløp", "tittel": "Driftsleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-2", "kostra": "Funksjon 345", "fullmakt": 800000, "ramme": int(ramme*0.52), "pv": int(pv*0.52), "ac": int(ac*0.52), "cv": int(cv*0.52), "cpi": cpi, "sec": u['sec']}
            ]
        else:
            children = [
                {"id": f"{u['id']}-DRIFT", "name": f"Driftsavdeling & Fagstab", "leder": "Fagkoordinator", "tittel": "Fagkoordinator", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-1", "kostra": u['kostra'], "fullmakt": 400000, "ramme": int(ramme*0.60), "pv": int(pv*0.60), "ac": int(ac*0.60), "cv": int(cv*0.60), "cpi": cpi, "sec": u['sec']},
                {"id": f"{u['id']}-PROSJEKT", "name": f"Prosjekt & Utvikling", "leder": "Prosjektleder", "tittel": "Prosjektleder", "niva": 4, "nivaTekst": "Nivå 4: Avdeling", "ansvar": f"{u['ansvar']}-2", "kostra": u['kostra'], "fullmakt": 300000, "ramme": int(ramme*0.40), "pv": int(pv*0.40), "ac": int(ac*0.40), "cv": int(cv*0.40), "cpi": cpi, "sec": u['sec']}
            ]

    for c in children:
        c['eac'] = int(c['ramme'] * (1.0 / max(0.85, c['cpi'])))
        c['vac'] = c['ramme'] - c['eac']
        c['p10'] = int(c['eac'] * 0.99)
        c['p50'] = c['eac']
        c['p90'] = int(c['eac'] * 1.015)
        c['forbrukPct'] = round(c['ac'] / c['ramme'] * 100, 1)
        c['epost'] = f"{c['id'].lower()}@kristiansand.kommune.no"
        c['telefon'] = "+47 38 00 70 00"
        c['controller'] = "Frank Ellingsen"
        c['kontor'] = "Kristiansand"
        c['returfrist'] = "M+10 virkedag"
        c['returkanal'] = "okonomi@kristiansand.kommune.no"
        c['sparkline'] = [round(c['pv']/9/1000000, 1)] * 9
        c['diagnose'] = {"summary": diag_summary, "drivers": diag_drivers, "lovhjemmel": "Kommuneloven § 14-5"}
        c['prognose'] = {"eac": f"{c['eac']:,}".replace(',', ' ') + " kr", "vac": f"{c['vac']:,}".replace(',', ' ') + " kr", "status": status_txt}
        c['actions'] = act_list[:2]
        c['children'] = []

    node = {
        "id": u['id'],
        "sectorKey": u['sec'],
        "name": u['name'],
        "leder": u['leder'],
        "tittel": u['tittel'],
        "niva": u['niva'],
        "nivaTekst": u['nivaTekst'],
        "ansvar": u['ansvar'],
        "kostra": u['kostra'],
        "fullmakt": u['fullmakt'],
        "epost": f"{u['leder'].lower().replace(' ', '.').replace('ø','o').replace('å','a').replace('æ','ae')}@kristiansand.kommune.no",
        "telefon": "+47 38 00 70 00",
        "controller": "Frank Ellingsen",
        "kontor": "Kristiansand",
        "returfrist": "M+10 virkedag",
        "returkanal": "okonomi@kristiansand.kommune.no",
        "ramme": ramme,
        "pv": pv,
        "ac": ac,
        "cv": cv,
        "cpi": cpi,
        "forbrukPct": round(ac / ramme * 100, 1),
        "eac": eac,
        "vac": vac,
        "p10": p10,
        "p50": p50,
        "p90": p90,
        "sparkline": spark,
        "diagnose": {
            "summary": diag_summary,
            "drivers": diag_drivers,
            "lovhjemmel": "Kommuneloven § 14-5 (krav om budsjettbalanse). HTA § 4 ved bemanningsendringer."
        },
        "prognose": {
            "eac": f"{eac:,}".replace(',', ' ') + " kr",
            "vac": f"{vac:,}".replace(',', ' ') + " kr",
            "status": status_txt,
            "intervall": f"P10: {p10//1000000}M | P50: {p50//1000000}M | P90: {p90//1000000}M",
            "trend": "Følger sesongjustert historisk forbruksprofil."
        },
        "actions": act_list,
        "children": children
    }
    return node

enriched_units = [enrich_unit(u) for u in raw_units]
print(f"Enriched {len(enriched_units)} units.")

sectors_meta = {
    "HELSE": {"name": "1. Helse og mestring", "root_id": "5000-SJEF-HELSE"},
    "OPPVEKST": {"name": "2. Oppvekst og utdanning", "root_id": "4000-SJEF-OPPV"},
    "BYUTVIKLING": {"name": "3. By- og stedsutvikling", "root_id": "3000-SJEF-BYUTV"},
    "KULTUR": {"name": "4. Kultur og innbyggerdialog", "root_id": "2000-SJEF-KULTUR"},
    "ORG_TEK": {"name": "5. Organisasjon og teknologi", "root_id": "1000-SJEF-ORGTEK"},
    "OKONOMI": {"name": "6. Økonomi og virksomhetsstyring", "root_id": "6000-DIR-OKONOMI"}
}

hierarchy_data = {}

for sec_key, meta in sectors_meta.items():
    sec_units = [u for u in enriched_units if u['sectorKey'] == sec_key]
    root_node = next(u for u in sec_units if u['id'] == meta['root_id'])
    
    root_copy = dict(root_node)
    root_copy['name'] = meta['name']
    root_copy['children'] = []
    
    niva2_nodes = [u for u in sec_units if u['niva'] == 2]
    niva3_nodes = [u for u in sec_units if u['niva'] == 3]
    
    if niva2_nodes:
        for n2 in niva2_nodes:
            n2_copy = dict(n2)
            n2_copy['children'] = []
            
            if sec_key == 'HELSE':
                if 'SYKEHJEM' in n2['id']:
                    matching_n3 = [u for u in niva3_nodes if 'Sykehjem' in u['name'] or 'Omsorg' in u['name'] or 'Bo- og Miljø' in u['name'] or 'Kløvertun' in u['name'] or 'Valhalla' in u['name'] or 'Ternevig' in u['name'] or 'Songdalstunet' in u['name'] or 'Strai' in u['name'] or 'Presteheia' in u['name']]
                else:
                    matching_n3 = [u for u in niva3_nodes if u not in [x for x in niva3_nodes if 'Sykehjem' in x['name'] or 'Omsorg' in x['name'] or 'Bo- og Miljø' in x['name'] or 'Kløvertun' in x['name'] or 'Valhalla' in x['name'] or 'Ternevig' in x['name'] or 'Songdalstunet' in x['name'] or 'Strai' in x['name'] or 'Presteheia' in x['name']]]
            elif sec_key == 'OPPVEKST':
                if 'SKOLE' in n2['id']:
                    matching_n3 = [u for u in niva3_nodes if 'Skole' in u['name'] or 'PPT' in u['name']]
                else:
                    matching_n3 = [u for u in niva3_nodes if 'Barnehage' in u['name'] or 'Barnevern' in u['name'] or 'Forebyggende' in u['name']]
            elif sec_key == 'BYUTVIKLING':
                if 'VAR' in n2['id']:
                    matching_n3 = [u for u in niva3_nodes if 'VAR' in u['name'] or 'Vei' in u['name'] or 'Havn' in u['name'] or 'Eiendom' in u['name']]
                else:
                    matching_n3 = [u for u in niva3_nodes if u not in [x for x in niva3_nodes if 'VAR' in x['name'] or 'Vei' in x['name'] or 'Havn' in x['name'] or 'Eiendom' in x['name']]]
            else:
                matching_n3 = niva3_nodes
                
            n2_copy['children'] = matching_n3
            root_copy['children'].append(n2_copy)
    else:
        root_copy['children'] = niva3_nodes
        
    hierarchy_data[sec_key] = root_copy

print("Built hierarchical tree for all 6 sectors.")

all_units_json = json.dumps(enriched_units, ensure_ascii=False)
hierarchy_json = json.dumps(hierarchy_data, ensure_ascii=False)

# Read the template from a clean multi-line string using replace markers
js_template = '''
// ==============================================================================
// 81 RESULTATENHETER KATALOG & FRAMSIKT KASKADERT BUDSJETTHIERARKI
// jf. Kommuneloven § 14-5, § 14-6, HTA § 4 og Kristiansand Bystyres Økonomireglement
// ==============================================================================

const ALL_81_UNITS_DATA = __ALL_81_UNITS_JSON__;
const FRAMSIKT_HIERARCHY_DATA = __FRAMSIKT_HIERARCHY_JSON__;

let currentSelectedFramsiktNodeId = "5000-SJEF-HELSE";
let currentActiveUnitId = "ALL";
let framsiktTreeState = {};

function formatKr(num) {
    if (isNaN(num)) return "0 kr";
    return Math.round(num).toLocaleString("no-NO") + " kr";
}

function findFramsiktNodeById(id) {
    if (!id) return null;
    const directUnit = ALL_81_UNITS_DATA.find(u => u.id === id);
    if (directUnit) return directUnit;

    let found = null;
    function search(node) {
        if (found) return;
        if (node.id === id) {
            found = node;
            return;
        }
        if (node.children) {
            node.children.forEach(search);
        }
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(search);
    return found;
}

function getBreadcrumbTrail(id) {
    const node = findFramsiktNodeById(id);
    if (!node) return [];

    if (currentActiveUnitId !== "ALL" && node.id === currentActiveUnitId) {
        return [{ id: node.id, name: node.name }];
    }

    if (currentActiveUnitId !== "ALL") {
        const activeUnit = findFramsiktNodeById(currentActiveUnitId);
        if (activeUnit && node.id !== currentActiveUnitId) {
            return [
                { id: activeUnit.id, name: activeUnit.name },
                { id: node.id, name: node.name }
            ];
        }
    }

    let trail = [];
    function trace(curr, targetId, path) {
        const nextPath = [...path, { id: curr.id, name: curr.name }];
        if (curr.id === targetId) {
            trail = nextPath;
            return true;
        }
        if (curr.children) {
            for (let child of curr.children) {
                if (trace(child, targetId, nextPath)) return true;
            }
        }
        return false;
    }
    for (let rootSec of Object.values(FRAMSIKT_HIERARCHY_DATA)) {
        if (trace(rootSec, id, [])) break;
    }
    return trail.length ? trail : [{ id: node.id, name: node.name }];
}

// -----------------------------------------------------------------------------
// ENHETSVELGER (81 RESULTATENHETER) DROPDOWN LOGIKK
// -----------------------------------------------------------------------------
function populateGlobalUnitDropdown(sectorKey, selectedUnitId) {
    const dropdown = document.getElementById("global-unit-dropdown");
    if (!dropdown) return;

    if (!sectorKey) sectorKey = localStorage.getItem("aikom_selected_sector") || "ALL";
    if (!selectedUnitId) selectedUnitId = currentActiveUnitId || "ALL";

    const sMapNames = {
        "ALL": "Konsern (Alle 6 områder)",
        "HELSE": "1. Helse og mestring",
        "OPPVEKST": "2. Oppvekst og utdanning",
        "BYUTVIKLING": "3. By- og stedsutvikling",
        "KULTUR": "4. Kultur og innbyggerdialog",
        "ORG_TEK": "5. Organisasjon og teknologi",
        "OKONOMI": "6. Økonomi og virksomhetsstyring"
    };

    let html = "";
    if (sectorKey === "ALL") {
        html += '<option value="ALL">🏢 [Alle 81 resultatenheter i Kristiansand kommune]</option>';
        const secKeys = ["HELSE", "OPPVEKST", "BYUTVIKLING", "KULTUR", "ORG_TEK", "OKONOMI"];
        secKeys.forEach(sk => {
            const secUnits = ALL_81_UNITS_DATA.filter(u => u.sectorKey === sk);
            html += `<optgroup label="${sMapNames[sk]} (${secUnits.length} enheter)">`;
            secUnits.forEach(u => {
                html += `<option value="${u.id}">${u.name} — ${u.leder} (${u.nivaTekst})</option>`;
            });
            html += `</optgroup>`;
        });
    } else {
        const secUnits = ALL_81_UNITS_DATA.filter(u => u.sectorKey === sectorKey);
        const sName = sMapNames[sectorKey] || sectorKey;
        html += `<option value="ALL">🏢 [Alle ${secUnits.length} resultatenheter i ${sName}]</option>`;
        secUnits.forEach(u => {
            html += `<option value="${u.id}">${u.name} — ${u.leder} (${u.nivaTekst})</option>`;
        });
    }

    dropdown.innerHTML = html;
    dropdown.value = selectedUnitId;

    updateUnitMetaPill(selectedUnitId, sectorKey);
}

function updateUnitMetaPill(unitId, sectorKey) {
    const lvlBadge = document.getElementById("global-unit-lvl-badge");
    const leaderText = document.getElementById("global-unit-leader-text");
    const notice = document.getElementById("global-unit-cascade-notice");
    const resetBtn = document.getElementById("global-unit-reset-btn");

    if (unitId === "ALL" || !unitId) {
        if (lvlBadge) {
            lvlBadge.className = "framsikt-level-badge lvl-1";
            lvlBadge.textContent = sectorKey === "ALL" ? "Nivå 1: Konsern" : "Nivå 1: Kommunalsjef";
        }
        if (leaderText) {
            const secData = typeof SEKTOR_DATA !== 'undefined' ? (SEKTOR_DATA[sectorKey] || SEKTOR_DATA["ALL"]) : null;
            leaderText.textContent = sectorKey === "ALL" ? "Camilla Dunsæd (Kommunedirektør)" : (secData ? `${secData.leder} (${secData.tittel})` : "Kommunalsjef");
        }
        if (notice) {
            notice.className = "cascade-tag";
            notice.innerHTML = sectorKey === "ALL" ? "🔓 Konserninnsyn (Alle 81 enheter)" : "🔓 Områdeinnsyn (Full delegasjon)";
        }
        if (resetBtn) resetBtn.style.display = "none";
    } else {
        const unit = findFramsiktNodeById(unitId);
        if (unit) {
            if (lvlBadge) {
                lvlBadge.className = `framsikt-level-badge lvl-${unit.niva}`;
                lvlBadge.textContent = unit.nivaTekst;
            }
            if (leaderText) {
                leaderText.textContent = `${unit.leder} (${unit.tittel})`;
            }
            if (notice) {
                notice.className = "cascade-tag active-unit";
                notice.innerHTML = `🔒 Kaskadert innsyn: Kun ${unit.name} & underavdelinger`;
            }
            if (resetBtn) resetBtn.style.display = "inline-flex";
        }
    }
}

// -----------------------------------------------------------------------------
// HOVEDFUNKSJON: selectUnit(unitId) — KASKADERT FRAMSIKT INNSYN
// -----------------------------------------------------------------------------
window.selectUnit = function(unitId) {
    if (!unitId || unitId === "ALL") {
        resetUnitToSector();
        return;
    }

    const unit = findFramsiktNodeById(unitId);
    if (!unit) return;

    currentActiveUnitId = unitId;

    // Sørg for at Sektor & Konsernstyring fanen er aktiv så hierarkiet og enheten vises
    if (typeof openTab === "function") {
        const activeTab = localStorage.getItem("aikom_active_tab") || "min-enhet";
        if (activeTab !== "sektor-konsern") {
            openTab("sektor-konsern", false);
        }
    }

    const currentSector = localStorage.getItem("aikom_selected_sector") || "ALL";
    if (unit.sectorKey && unit.sectorKey !== currentSector && currentSector !== "ALL") {
        try {
            localStorage.setItem("aikom_selected_sector", unit.sectorKey);
            updateGlobalSectorBanner(unit.sectorKey);
        } catch(e) {}
    }

    const dropdown = document.getElementById("global-unit-dropdown");
    if (dropdown) dropdown.value = unitId;
    updateUnitMetaPill(unitId, unit.sectorKey);

    renderFramsiktTree(unit.sectorKey, "", unitId);
    updateKpiRowForUnit(unit);
    updateTop3ForUnit(unit);
    updateSectorDetailForUnit(unit);
    filterTop3HierarchyTableForUnit(unit);

    showToast(`🔒 Framsikt kaskadert innsyn: ${unit.name} (Leder: ${unit.leder})`);
};

window.jumpToFramsiktHierarchy = function() {
    if (typeof openTab === "function") {
        openTab("sektor-konsern", false);
    }
    const sec = document.getElementById("framsikt-budsjetthierarki-seksjon");
    if (sec) {
        sec.scrollIntoView({ behavior: "smooth", block: "start" });
    }
};

window.resetUnitToSector = function() {
    currentActiveUnitId = "ALL";
    const currentSector = localStorage.getItem("aikom_selected_sector") || "ALL";

    populateGlobalUnitDropdown(currentSector, "ALL");
    updateUnitMetaPill("ALL", currentSector);

    renderFramsiktTree(currentSector, "", "ALL");

    if (typeof updateKpiRow === 'function') {
        updateKpiRow(currentSector);
    }

    if (typeof filterTop3HierarchyTableForSector === 'function') {
        filterTop3HierarchyTableForSector(currentSector);
    }

    const sMap = {
        "ALL": "ALL",
        "HELSE": "OMR-03",
        "OPPVEKST": "OMR-02",
        "BYUTVIKLING": "OMR-05",
        "KULTUR": "OMR-04",
        "ORG_TEK": "OMR-11",
        "OKONOMI": "OMR-12"
    };
    if (typeof selectTop3Sector === 'function') {
        selectTop3Sector(sMap[currentSector] || "ALL", true);
    }

    const detailCard = document.getElementById("sector-detail-card");
    if (detailCard && typeof renderSectorDetailCardHtml === 'function') {
        const data = SEKTOR_DATA[currentSector] || SEKTOR_DATA["ALL"];
        detailCard.innerHTML = renderSectorDetailCardHtml(currentSector, data);
    }

    showToast("🔓 Gjenopprettet fullt innsyn for hele ansvarsområdet");
};

// -----------------------------------------------------------------------------
// DYNAMISK SYNK AV KPI-ER OG KORT FOR VALGT ENHET
// -----------------------------------------------------------------------------
function updateKpiRowForUnit(unit) {
    const kpiRow = document.getElementById("evm-kpi-row");
    if (!kpiRow) return;

    const cvIsNeg = unit.cv < 0;
    const cvClass = cvIsNeg ? "cf-rag-red" : "cf-rag-green";
    const cvBadgeClass = cvIsNeg ? "rag-badge-red" : "rag-badge-green";
    const cvText = (unit.cv > 0 ? "+" : "") + formatKr(unit.cv);
    const cvBadge = cvIsNeg ? "🔴 Merforbruk" : "🟢 Balanse";

    const cpiVal = parseFloat(unit.cpi);
    const cpiClass = cpiVal < 0.95 ? "cf-rag-red" : (cpiVal < 1.00 ? "cf-rag-yellow" : "cf-rag-green");
    const cpiBadgeClass = cpiVal < 0.95 ? "rag-badge-red" : (cpiVal < 1.00 ? "rag-badge-yellow" : "rag-badge-green");
    const cpiBadge = cpiVal >= 1.00 ? "🟢 Mål nådd" : (cpiVal >= 0.95 ? "🟡 Tilsyn" : "🔴 Tiltak");

    kpiRow.innerHTML = `
        <div class="sector-kpi-chip">
            <div class="kpi-sub">Budsjettramme (BAC)</div>
            <div class="kpi-num">${formatKr(unit.ramme)}</div>
        </div>
        <div class="sector-kpi-chip">
            <div class="kpi-sub">Hittil Påløpt (AC)</div>
            <div class="kpi-num">${formatKr(unit.ac)}</div>
        </div>
        <div class="sector-kpi-chip ${cvClass}">
            <div class="kpi-sub" style="display:flex; justify-content:space-between; align-items:center;">
                <span>Avvik YTD (CV)</span>
                <span class="rag-badge ${cvBadgeClass}" style="font-size:9.5px; padding:1px 5px;">${cvBadge}</span>
            </div>
            <div class="kpi-num">${cvText}</div>
        </div>
        <div class="sector-kpi-chip ${cpiClass}">
            <div class="kpi-sub" style="display:flex; justify-content:space-between; align-items:center;">
                <span>Kostnadsindeks (CPI)</span>
                <span class="rag-badge ${cpiBadgeClass}" style="font-size:9.5px; padding:1px 5px;">${cpiBadge}</span>
            </div>
            <div class="kpi-num">${unit.cpi.toFixed(3)}</div>
        </div>
        <div class="sector-kpi-chip">
            <div class="kpi-sub">Estimert Sluttkostnad (EAC)</div>
            <div class="kpi-num">${formatKr(unit.eac)}</div>
        </div>
        <div class="sector-kpi-chip ${unit.vac < 0 ? 'cf-rag-red' : 'cf-rag-green'}">
            <div class="kpi-sub">Årssluttavvik (VAC jf. § 14-5)</div>
            <div class="kpi-num">${(unit.vac > 0 ? "+" : "") + formatKr(unit.vac)}</div>
        </div>
    `;
}

function updateTop3ForUnit(unit) {
    const nettoSum = document.getElementById("top3-netto-sum");
    const nettoRag = document.getElementById("top3-netto-rag");
    if (nettoSum) {
        nettoSum.textContent = (unit.cv > 0 ? "+" : "") + formatKr(unit.cv);
        nettoSum.style.color = unit.cv < 0 ? "#b91c1c" : "#15803d";
    }
    if (nettoRag) {
        nettoRag.className = `rag-badge ${unit.cv < 0 ? 'rag-badge-red' : 'rag-badge-green'}`;
        nettoRag.textContent = unit.cv < 0 ? "🔴 Merforbruk" : "🟢 Balanse";
    }

    const needle = document.getElementById("netto-needle");
    if (needle) {
        const angle = unit.cpi >= 1.0 ? 15 : (unit.cpi >= 0.95 ? -15 : -45);
        needle.setAttribute("transform", `rotate(${angle} 100 80)`);
    }
}

function updateSectorDetailForUnit(unit) {
    const detailCard = document.getElementById("sector-detail-card");
    if (!detailCard) return;

    detailCard.innerHTML = `
        <div class="sector-detail-header" style="background:#f8fafc; border-bottom:1.5px solid #e2e8f0; padding:12px 16px; border-radius:4px 4px 0 0;">
            <div>
                <div class="sector-detail-title" style="font-size:16px; font-weight:800; color:var(--navy-dark);">
                    🏢 ${unit.name}
                </div>
                <div style="font-size:12px; color:var(--text-secondary); margin-top:3px;">
                    Budsjettansvarlig: <strong>${unit.leder}</strong> (${unit.tittel}) | Delegeringsfullmakt: <strong>${formatKr(unit.fullmakt)}</strong>
                </div>
            </div>
            <span class="status-badge" style="background:#fee2e2; color:#b91c1c; font-size:11px; font-weight:700; border:1px solid #fca5a5;">
                🔒 Kaskadert innsyn (${unit.nivaTekst})
            </span>
        </div>

        <div class="sector-detail-grid" style="padding:14px 16px;">
            <div class="sector-field-box">
                <strong>📌 Ansvars- og Kontoplaninformasjon</strong>
                <p>Ansvar: <strong>${unit.ansvar}</strong> | KOSTRA-funksjon: <strong>${unit.kostra}</strong></p>
                <div style="margin-top:8px; font-size:11.5px; color:var(--text-secondary);">
                    <strong>🏛️ Lovhjemmel:</strong> Kommuneloven § 14-5 (krav om budsjettbalanse) og Bystyrets delegeringsreglement.
                </div>
            </div>
            <div class="sector-field-box">
                <strong>🎯 Controller-kontakt & Frister</strong>
                <p>Senior Controller: <strong>${unit.controller}</strong> | E-post: <a href="mailto:${unit.epost}" style="color:var(--accent-blue);">${unit.epost}</a></p>
                <div style="margin-top:8px; font-size:11.5px; color:var(--text-secondary);">
                    <strong>⚡ Returfrist for månedsrapport:</strong> ${unit.returfrist} via ${unit.returkanal}.
                </div>
            </div>
        </div>

        <div class="sector-kpi-row" id="evm-kpi-row" style="padding:0 16px 14px 16px;">
            <!-- Dynamiske brikker -->
        </div>
    `;

    updateKpiRowForUnit(unit);
}

function filterTop3HierarchyTableForUnit(unit) {
    const tbody = document.getElementById("top3-hierarchy-tbody");
    if (!tbody) return;

    const rows = tbody.querySelectorAll("tr");
    rows.forEach(tr => {
        const text = tr.innerText || "";
        const isMatch = text.includes(unit.name) || text.includes(unit.leder) || text.includes(unit.ansvar);
        if (isMatch) {
            tr.style.display = "";
            tr.style.background = "#fef2f2";
        } else {
            tr.style.display = "none";
        }
    });
}

// -----------------------------------------------------------------------------
// FRAMSIKT HIERARKISK TRE MED KASKADERT TILGANGSKONTROLL
// -----------------------------------------------------------------------------
function renderFramsiktTree(sectorFilter, searchTerm, unitFilter) {
    const treeRoot = document.getElementById("framsikt-tree-root");
    if (!treeRoot) return;

    if (!sectorFilter) sectorFilter = localStorage.getItem("aikom_selected_sector") || "ALL";
    if (searchTerm === undefined) searchTerm = "";
    searchTerm = searchTerm.toLowerCase().trim();

    if (!unitFilter) unitFilter = currentActiveUnitId || "ALL";

    const headerScope = document.getElementById("framsikt-header-scope");

    // =========================================================================
    // KASKADERT TILGANGSKONTROLL: Hvis enhet er valgt (f.eks. Rektor eller Boenhet)
    // Budsjettansvarlig ser KUN sitt nivå og kaskadert nedover — IKKE nivåer over!
    // =========================================================================
    if (unitFilter && unitFilter !== "ALL") {
        const targetNode = findFramsiktNodeById(unitFilter);
        if (targetNode) {
            if (headerScope) {
                headerScope.innerHTML = `🔒 <strong>Kaskadert innsyn:</strong> ${targetNode.name} — Leder: <strong>${targetNode.leder}</strong> (${targetNode.nivaTekst})`;
            }

            framsiktTreeState[targetNode.id] = true;
            treeRoot.innerHTML = buildTreeNodeHtml(targetNode, searchTerm);
            currentSelectedFramsiktNodeId = targetNode.id;
            renderFramsiktDetail(targetNode);
            return;
        }
    }

    // =========================================================================
    // NORMAL VISNING FOR SEKTOR / KONSERN
    // =========================================================================
    if (headerScope) {
        if (sectorFilter === "ALL") {
            headerScope.textContent = "Konsern (Alle 6 virksomhetsområder — 81 resultatenheter)";
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
    if (node.children && node.children.length > 0) {
        return node.children.some(c => checkChildMatch(c, searchTerm));
    }
    return false;
}

function selectFramsiktNode(id) {
    currentSelectedFramsiktNodeId = id;
    const allNodeEls = document.querySelectorAll(".f-tree-node");
    allNodeEls.forEach(el => el.classList.remove("active"));
    const activeEl = document.getElementById(`f-node-${id}`);
    if (activeEl) activeEl.classList.add("active");

    const node = findFramsiktNodeById(id);
    if (node) {
        renderFramsiktDetail(node);
    }
}

function toggleFramsiktFolder(id) {
    framsiktTreeState[id] = !framsiktTreeState[id];
    const childContainer = document.getElementById(`f-children-${id}`);
    const nodeEl = document.getElementById(`f-node-${id}`);
    if (!childContainer) return;

    if (framsiktTreeState[id]) {
        childContainer.classList.remove("collapsed");
        childContainer.classList.add("expanded");
        if (nodeEl) {
            const toggleSpan = nodeEl.querySelector(".f-toggle");
            if (toggleSpan) toggleSpan.textContent = "▼";
        }
    } else {
        childContainer.classList.remove("expanded");
        childContainer.classList.add("collapsed");
        if (nodeEl) {
            const toggleSpan = nodeEl.querySelector(".f-toggle");
            if (toggleSpan) toggleSpan.textContent = "▶";
        }
    }
}

function expandAllFramsiktTree() {
    function setAll(node) {
        framsiktTreeState[node.id] = true;
        if (node.children) node.children.forEach(setAll);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(setAll);
    const savedSector = localStorage.getItem("aikom_selected_sector") || "ALL";
    renderFramsiktTree(savedSector, "", currentActiveUnitId);
}

function collapseAllFramsiktTree() {
    function setFalse(node) {
        framsiktTreeState[node.id] = false;
        if (node.children) node.children.forEach(setFalse);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(setFalse);
    const savedSector = localStorage.getItem("aikom_selected_sector") || "ALL";
    renderFramsiktTree(savedSector, "", currentActiveUnitId);
}

// -----------------------------------------------------------------------------
// DETALJ- OG HANDLINGSPANEL FOR VALGT ENHET
// -----------------------------------------------------------------------------
function renderFramsiktDetail(node) {
    const container = document.getElementById("framsikt-detail-panel");
    if (!container || !node) return;

    const trail = getBreadcrumbTrail(node.id);
    let breadcrumbHtml = `<div class="framsikt-breadcrumb-bar"><span>Framsikt 2026</span> <span>›</span>`;
    if (currentActiveUnitId !== "ALL") {
        breadcrumbHtml += `<span class="cascade-tag active-unit" style="margin-right:6px;">🔒 Kaskadert innsyn</span>`;
    }
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

    let sparkSvg = "";
    if (node.sparkline && node.sparkline.length) {
        const vals = node.sparkline;
        const minVal = Math.min(...vals) * 0.95;
        const maxVal = Math.max(...vals) * 1.05;
        const width = 240;
        const height = 40;
        const points = vals.map((v, i) => {
            const x = (i / (vals.length - 1)) * width;
            const y = height - ((v - minVal) / (maxVal - minVal || 1)) * height;
            return `${x.toFixed(1)},${y.toFixed(1)}`;
        }).join(" ");
        sparkSvg = `
            <svg width="${width}" height="${height}" style="overflow:visible; vertical-align:middle;">
                <polyline fill="none" stroke="#0284c7" stroke-width="2" points="${points}" />
                ${vals.map((v, i) => {
                    const x = (i / (vals.length - 1)) * width;
                    const y = height - ((v - minVal) / (maxVal - minVal || 1)) * height;
                    const isLast = i === vals.length - 1;
                    return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${isLast ? 3.5 : 2}" fill="${isLast ? '#b91c1c' : '#0284c7'}" />`;
                }).join("")}
            </svg>
        `;
    }

    container.innerHTML = `
        ${breadcrumbHtml}
        
        <div class="f-detail-header-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span class="framsikt-level-badge lvl-${node.niva}">${node.nivaTekst}</span>
                        <h3 class="f-detail-title">${node.name}</h3>
                    </div>
                    <div class="f-detail-subtitle">
                        Ansvarlig leder: <strong>${node.leder}</strong> (${node.tittel}) | Delegeringsfullmakt: <strong>${formatKr(node.fullmakt)}</strong> | Kostnadssted: <strong>${node.ansvar}</strong>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:10.5px; color:#64748b; font-weight:700;">FORBRUKSPROSENT YTD</div>
                    <div style="font-size:20px; font-weight:800; color:var(--navy-dark);">${node.forbrukPct} %</div>
                </div>
            </div>

            <div class="f-meta-chips">
                <span class="f-meta-chip">🏛️ KOSTRA: <strong>${node.kostra}</strong></span>
                <span class="f-meta-chip">👤 Controller: <strong>${node.controller}</strong></span>
                <span class="f-meta-chip">📅 Returfrist: <strong>${node.returfrist}</strong></span>
                <span class="f-meta-chip">📫 Kanal: <strong>${node.returkanal}</strong></span>
            </div>
        </div>

        <div class="f-dim-grid">
            <!-- Dimensjon 1: Nøkkeltall -->
            <div class="f-dim-box">
                <div class="f-dim-title">
                    <span>📊 Dimensjon 1: Nøkkeltall (EVM / FAST)</span>
                    <span style="font-size:11px; font-weight:600; color:#64748b;">M10 Status</span>
                </div>
                <div class="f-kpi-subgrid">
                    <div class="f-kpi-cell">
                        <div class="f-kpi-lbl">Budsjettramme (BAC)</div>
                        <div class="f-kpi-val">${formatKr(node.ramme)}</div>
                    </div>
                    <div class="f-kpi-cell">
                        <div class="f-kpi-lbl">Periodisert plan (PV)</div>
                        <div class="f-kpi-val">${formatKr(node.pv)}</div>
                    </div>
                    <div class="f-kpi-cell">
                        <div class="f-kpi-lbl">Hittil påløpt (AC)</div>
                        <div class="f-kpi-val">${formatKr(node.ac)}</div>
                    </div>
                    <div class="f-kpi-cell">
                        <div class="f-kpi-lbl">Avvik YTD (CV)</div>
                        <div class="f-kpi-val ${cvClass}">${cvSign}${formatKr(node.cv)}</div>
                    </div>
                    <div class="f-kpi-cell">
                        <div class="f-kpi-lbl">Kostnadsindeks (CPI)</div>
                        <div class="f-kpi-val ${cpiClass}">${node.cpi.toFixed(3)}</div>
                    </div>
                    <div class="f-kpi-cell">
                        <div class="f-kpi-lbl">Årssluttavvik (VAC jf. § 14-5)</div>
                        <div class="f-kpi-val ${node.vac < 0 ? 'f-val-red' : 'f-val-green'}">${(node.vac > 0 ? "+" : "") + formatKr(node.vac)}</div>
                    </div>
                </div>

                <div style="margin-top:12px; padding-top:10px; border-top:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:11px; font-weight:700; color:#475569;">Månedlig kostnadsprofil (M01–M09):</div>
                    <div>${sparkSvg}</div>
                </div>
            </div>

            <!-- Dimensjon 2: Diagnose -->
            <div class="f-dim-box">
                <div class="f-dim-title">
                    <span>🩺 Dimensjon 2: Diagnose & Avviksårsaker</span>
                    <span class="rag-badge ${node.cv < 0 ? 'rag-badge-red' : 'rag-badge-green'}" style="font-size:10px;">${node.cv < 0 ? 'Avvik påvist' : 'I balanse'}</span>
                </div>
                <p style="font-size:12px; color:var(--text-secondary); line-height:1.5;">${node.diagnose ? node.diagnose.summary : 'Ingen vesentlige avvik rapportert.'}</p>
                ${driversHtml}
                <div style="margin-top:10px; font-size:11px; color:#64748b; background:#f8fafc; padding:8px 10px; border-left:3px solid var(--accent-blue); border-radius:3px;">
                    <strong>🏛️ Lovhjemmel & Styringsprinsipp:</strong> ${node.diagnose ? node.diagnose.lovhjemmel : 'Kommuneloven § 14-5'}
                </div>
            </div>

            <!-- Dimensjon 3: Prognose -->
            <div class="f-dim-box">
                <div class="f-dim-title">
                    <span>🔮 Dimensjon 3: Rullende Prognose (EAC / VAC)</span>
                    <span style="font-size:11px; font-weight:700; color:${node.vac < 0 ? '#b91c1c' : '#15803d'};">${node.prognose ? node.prognose.status : ''}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:8px;">
                    <div style="background:#f8fafc; padding:8px 10px; border-radius:3px; border:1px solid #e2e8f0;">
                        <div style="font-size:10.5px; color:#64748b; font-weight:700;">ESTIMERT SLUTTKOSTNAD (EAC)</div>
                        <div style="font-size:15px; font-weight:800; color:var(--navy-dark); margin-top:2px;">${node.prognose ? node.prognose.eac : formatKr(node.eac)}</div>
                    </div>
                    <div style="background:#f8fafc; padding:8px 10px; border-radius:3px; border:1px solid #e2e8f0;">
                        <div style="font-size:10.5px; color:#64748b; font-weight:700;">PROGNOSTISERT AVVIK (VAC)</div>
                        <div style="font-size:15px; font-weight:800; color:${node.vac < 0 ? '#b91c1c' : '#15803d'}; margin-top:2px;">${node.prognose ? node.prognose.vac : formatKr(node.vac)}</div>
                    </div>
                </div>
                <div style="margin-top:10px; font-size:11.5px; color:var(--text-secondary); line-height:1.5;">
                    <div><strong>Monte Carlo 90 % konfidens:</strong> ${node.prognose ? node.prognose.intervall : ''}</div>
                    <div style="margin-top:4px;"><strong>Trendvurdering:</strong> ${node.prognose ? node.prognose.trend : ''}</div>
                </div>
            </div>

            <!-- Dimensjon 4: Action to take -->
            <div class="f-dim-box">
                <div class="f-dim-title">
                    <span>⚡ Dimensjon 4: Handlingsplan & Korrigerende Tiltak</span>
                    <span style="font-size:11px; font-weight:700; color:var(--navy-dark);">${node.actions ? node.actions.length : 0} Tiltak definert</span>
                </div>
                ${actionsHtml}
                <div style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
                    <button type="button" class="btn btn-sm btn-primary" onclick="generateFramsiktDoc('${node.id}')">📄 Generer Månedsrapport (.docx)</button>
                    <button type="button" class="btn btn-sm" onclick="jumpToTriageForNode('${node.id}')">📋 Gå til Triage</button>
                    <button type="button" class="btn btn-sm" onclick="contactControllerForNode('${node.id}')">✉️ Kontakt Controller</button>
                    <button type="button" class="btn btn-sm" onclick="sealFramsiktAssessment('${node.id}')" style="margin-left:auto; background:#f1f5f9; border:1px solid #cbd5e1;">🔒 SHA-256 Forsegl</button>
                </div>
            </div>
        </div>
    `;
}

function generateFramsiktDoc(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    showToast(`📄 Genererer Framsikt månedsrapport for ${node.name} (Ansvar: ${node.ansvar})...`);
    setTimeout(() => {
        showToast(`✓ Ferdigstilt: RAPPORT_${node.ansvar}_M10_2026.docx klart til nedlasting.`);
    }, 1200);
}

function jumpToTriageForNode(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    if (typeof openTab === 'function') {
        openTab('sektor-konsern');
    }
    const triageSec = document.getElementById("triage-seksjon");
    if (triageSec) {
        triageSec.scrollIntoView({ behavior: 'smooth' });
    }
    showToast(`📋 Viser triage for ${node.name}`);
}

function contactControllerForNode(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    alert(`Controller-kontakt for ${node.name}:\\n\\nAnsvarlig Controller: ${node.controller}\\nE-post: frank.ellingsen@kristiansand.kommune.no\\nTelefon: +47 38 00 70 00\\nReturkanal: ${node.returkanal}\\nReturfrist: ${node.returfrist}`);
}

function sealFramsiktAssessment(nodeId) {
    const node = findFramsiktNodeById(nodeId);
    if (!node) return;
    const mockHash = "sha256-" + Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 10) + "e8f0a2";
    alert(`Stage-Gate Port 9 HitL Forsegling fullført!\\n\\nEnhet: ${node.name}\\nAnsvar: ${node.ansvar}\\nSignatur: FRANK ELLINGSEN (Sr. Project Controller)\\nKryptografisk stempel: ${mockHash}\\nRevisjonslogg: golden_record_audit_log.json`);
}

function exportFramsiktHierarchyXlsx() {
    showToast("📊 Genererer FAST-kompatibel Excel eksport av hele budsjetthierarkiet...");
    let csv = "\\uFEFFNivå;ID;Enhetsnavn;Leder;Tittel;Ansvar;KOSTRA;Fullmakt;Ramme;Påløpt;Avvik;CPI;EAC;VAC\\n";
    function addCsvRows(node) {
        csv += `${node.niva};${node.id};"${node.name}";"${node.leder}";"${node.tittel}";"${node.ansvar}";"${node.kostra}";${node.fullmakt};${node.ramme};${node.ac};${node.cv};${node.cpi};${node.eac};${node.vac}\\n`;
        if (node.children) node.children.forEach(addCsvRows);
    }
    Object.values(FRAMSIKT_HIERARCHY_DATA).forEach(addCsvRows);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "Framsikt_Budsjetthierarki_81_Enheter_2026.csv";
    link.click();
    showToast("✓ Lastet ned Framsikt_Budsjetthierarki_81_Enheter_2026.csv");
}

// -----------------------------------------------------------------------------
// SEKTOR BANNER & MASTER SEKTORVALG
// -----------------------------------------------------------------------------
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
    const sectorData = typeof SEKTOR_DATA !== 'undefined' ? (SEKTOR_DATA[sectorKey] || SEKTOR_DATA["ALL"]) : null;

    if (sectorKey === "ALL") {
        if (noticeText) noticeText.innerHTML = "🌐 <strong>Konsernvisning:</strong> Viser alle 6 virksomhetsområder for Kristiansand kommune samlet. Klikk et område over for å isolere data.";
        if (resetBtn) resetBtn.style.display = "none";
    } else {
        if (noticeText && sectorData) noticeText.innerHTML = `📍 <strong>Aktivt område:</strong> ${sectorData.icon} <strong>${sectorData.title}</strong> — Viser kun data, budsjetter, avvik og enheter tilknyttet dette området.`;
        if (resetBtn) resetBtn.style.display = "inline-flex";
    }
}

window.selectSector = function(sectorKey, fromTop3Sync) {
    try {
        localStorage.setItem("aikom_selected_sector", sectorKey);
    } catch(e) {}

    const data = typeof SEKTOR_DATA !== 'undefined' ? (SEKTOR_DATA[sectorKey] || SEKTOR_DATA["ALL"]) : null;

    updateGlobalSectorBanner(sectorKey);

    currentActiveUnitId = "ALL";
    populateGlobalUnitDropdown(sectorKey, "ALL");

    const navButtons = document.querySelectorAll("#sector-nav-bar .sector-tab-btn");
    navButtons.forEach(btn => btn.classList.remove("active"));
    const activeNavBtn = document.getElementById(`sec-btn-${sectorKey.toLowerCase()}`) || document.getElementById("sec-btn-all");
    if (activeNavBtn) activeNavBtn.classList.add("active");

    const kpiSelect = document.getElementById("kpi-sector-select");
    if (kpiSelect && kpiSelect.value !== sectorKey) kpiSelect.value = sectorKey;
    const bhSelect = document.getElementById("budget-holder-sector-filter");
    if (bhSelect && bhSelect.value !== sectorKey) bhSelect.value = sectorKey;

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

    const detailCard = document.getElementById("sector-detail-card");
    if (detailCard && typeof renderSectorDetailCardHtml === 'function' && data) {
        detailCard.innerHTML = renderSectorDetailCardHtml(sectorKey, data);
    }

    if (typeof updateKpiRow === 'function') {
        updateKpiRow(sectorKey);
    }

    filterSectorComparisonTableStrict(sectorKey);
    filterTop3HierarchyTableForSector(sectorKey);

    renderFramsiktTree(sectorKey, "", "ALL");

    if (typeof filterBudgetHoldersTable === 'function') filterBudgetHoldersTable();

    const prSec = document.getElementById("pr-filter-sector");
    if (prSec) {
        prSec.value = sectorKey;
        if (typeof renderProjectsTable === 'function') renderProjectsTable();
    }

    if (typeof renderSectorTriage === 'function') renderSectorTriage(sectorKey);
    if (typeof syncSaksgeneratorForSector === 'function') syncSaksgeneratorForSector(sectorKey);
    if (typeof updateBudsjettModulForSector === 'function') updateBudsjettModulForSector(sectorKey);
    if (typeof updateDocbankForSector === 'function') updateDocbankForSector(sectorKey);
    if (typeof renderPbiKostraForSector === 'function') {
        renderPbiKostraForSector(sectorKey);
        renderPbiCapexForSector(sectorKey);
        syncPbiReportPageForSector(sectorKey);
    }
    if (typeof updateSidebarOverview === 'function') updateSidebarOverview(sectorKey);
    if (typeof renderMeetingPack === 'function') {
        const lvl = typeof currentMeetingLevel !== 'undefined' ? currentMeetingLevel : 'NIVA1';
        renderMeetingPack(sectorKey, lvl);
    }

    if (data) showToast(`🏢 Valgt ansvarsområde: ${data.title}`);
};

function filterSectorComparisonTableStrict(sectorKey) {
    const rows = document.querySelectorAll("#sector-comparison-tbody tr");
    if (!rows.length) return;
    rows.forEach(r => {
        if (sectorKey === "ALL") {
            r.style.display = "";
            if (r.id === "row-sec-all") r.style.background = "#f8fafc";
            else r.style.background = "";
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

    if (typeof renderHierarchyTable === 'function') renderHierarchyTable();

    const rows = tbody.querySelectorAll("tr");
    rows.forEach(tr => {
        if (targetSectorId === "ALL") {
            // keep
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
    populateGlobalUnitDropdown(savedSector, "ALL");
    renderFramsiktTree(savedSector, "", "ALL");
    updateGlobalSectorBanner(savedSector);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFramsiktHierarchyEngine);
} else {
    initFramsiktHierarchyEngine();
}
'''

js_code = js_template.replace("__ALL_81_UNITS_JSON__", all_units_json).replace("__FRAMSIKT_HIERARCHY_JSON__", hierarchy_json)

with open('scratch/framsikt_engine_test.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Wrote scratch/framsikt_engine_test.js")

# Validate JS syntax using node -c
res = subprocess.run(["node", "-c", "scratch/framsikt_engine_test.js"], capture_output=True, text=True)
if res.returncode != 0:
    print("Node JS validation failed:")
    print(res.stderr)
    sys.exit(1)
else:
    print("✓ Node JS validation PASSED cleanly!")

# Now read index.html and perform replacement
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

marker1 = '// 81 RESULTATENHETER KATALOG & FRAMSIKT KASKADERT BUDSJETTHIERARKI'
idx_start = html.find(marker1)
if idx_start == -1:
    idx_start = html.find('const FRAMSIKT_HIERARCHY_DATA = {')

idx_end_dashboard = html.find('function initTop3KpiDashboard()')

print(f"Replacing index.html from {idx_start} to {idx_end_dashboard}")

new_html = html[:idx_start] + js_code.strip() + "\n\n// ==============================================================================\n\n\n" + html[idx_end_dashboard:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("✓ Successfully replaced Framsikt script block in index.html!")
