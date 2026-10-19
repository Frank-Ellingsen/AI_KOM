# -*- coding: utf-8 -*-
"""
apply_framsikt_expansion.py
Adds:
1. Universal Virksomhetsområde Selector Bar & Active Filter Banner at the top of index.html.
2. Complete Framsikt Budsjettnivå-Hierarki (Levels 1 to 4) mirroring Framsikt with interactive drilldown:
   - Nøkkeltall (BAC, PV, AC, CV, CPI, Forbruk %)
   - Diagnose (KOSTRA-driftsarter, sykefravær, vikarforbruk, § 14-5 & HTA § 4)
   - Prognose (EAC per 31.12, VAC, P10/P50/P90 Monte Carlo)
   - Action to take (1-2-3-4 konkrete tiltak for budsjettansvarlig, saksnotat, triage, e-post, SHA-256 forsegling)
3. Strict Sector Isolation across ALL components:
   - When HELSE is selected: ONLY Helse og mestring data is shown.
   - When OPPVEKST is selected: ONLY Oppvekst data is shown.
   - When Konsern is selected: Full consolidated overview.
"""
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# -----------------------------------------------------------------------------
# 1. CSS STYLES
# -----------------------------------------------------------------------------
FRAMSIKT_CSS = """
        /* ==========================================================================
           UNIVERSAL VIRKSOMHETSOMRÅDE-FILTER & FRAMSIKT BUDSJETTHIERARKI
           Edward Tufte Data-Ink Ratio, Navy/Slate disiplin, Ingen unødvendig støy.
           ========================================================================== */
        .global-sector-bar {
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-left: 4px solid var(--navy-dark);
            border-radius: 4px;
            padding: 12px 18px;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .global-sector-bar-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .global-sector-label {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--navy-dark);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .global-sector-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .gsec-pill {
            font-family: var(--font-sans);
            font-size: 11.5px;
            font-weight: 600;
            padding: 6px 12px;
            border-radius: 3px;
            border: 1px solid #cbd5e1;
            background: #f8fafc;
            color: #1e293b;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s ease;
        }
        .gsec-pill:hover {
            background: #e2e8f0;
            border-color: #94a3b8;
        }
        .gsec-pill.active {
            background: var(--navy-dark);
            color: #ffffff;
            border-color: var(--navy-dark);
            box-shadow: 0 1px 3px rgba(27, 54, 93, 0.25);
        }
        .gsec-pill .pill-badge {
            font-size: 10px;
            padding: 1px 5px;
            border-radius: 2px;
            background: rgba(0, 0, 0, 0.08);
            font-weight: 700;
        }
        .gsec-pill.active .pill-badge {
            background: rgba(255, 255, 255, 0.2);
            color: #ffffff;
        }
        .global-sector-notice {
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 3px;
            padding: 6px 12px;
            font-size: 11.5px;
            color: #0369a1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }
        .global-sector-notice strong {
            color: var(--navy-dark);
        }

        /* Framsikt Budsjettnivå-Hierarki Container */
        .framsikt-section {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-top: 3px solid var(--navy-dark);
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 24px;
        }
        .framsikt-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border-light);
            padding-bottom: 12px;
        }
        .framsikt-title h2 {
            font-size: 16px;
            font-weight: 800;
            color: var(--navy-dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .framsikt-title p {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 3px;
        }
        .framsikt-layout {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 20px;
            align-items: start;
        }
        @media (max-width: 1080px) {
            .framsikt-layout {
                grid-template-columns: 1fr;
            }
        }
        .framsikt-tree-col {
            background: #f8fafc;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 14px;
            max-height: 820px;
            overflow-y: auto;
        }
        .framsikt-search-box {
            margin-bottom: 12px;
        }
        .framsikt-search-box input {
            width: 100%;
            padding: 7px 10px;
            font-size: 12px;
            border: 1px solid var(--border-light);
            border-radius: 3px;
            background: #ffffff;
            font-family: var(--font-sans);
        }
        .framsikt-tree-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text-secondary);
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #e2e8f0;
        }
        .framsikt-tree-list {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        .framsikt-tree-node {
            margin: 2px 0;
        }
        .framsikt-node-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 8px;
            border-radius: 3px;
            cursor: pointer;
            transition: background 0.12s ease;
            font-size: 12px;
            border: 1px solid transparent;
        }
        .framsikt-node-row:hover {
            background: #f1f5f9;
        }
        .framsikt-node-row.active {
            background: #eff6ff;
            border-color: #bfdbfe;
            border-left: 3px solid #0284c7;
            font-weight: 700;
        }
        .framsikt-node-left {
            display: flex;
            align-items: center;
            gap: 6px;
            min-width: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .framsikt-toggle-btn {
            background: none;
            border: none;
            cursor: pointer;
            color: #64748b;
            font-size: 10px;
            width: 16px;
            height: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0;
        }
        .framsikt-level-badge {
            font-size: 9.5px;
            font-weight: 700;
            padding: 1px 4px;
            border-radius: 2px;
            text-transform: uppercase;
            font-family: var(--font-mono);
        }
        .lvl-1 { background: #0f172a; color: #ffffff; }
        .lvl-2 { background: #1e3a8a; color: #ffffff; }
        .lvl-3 { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
        .lvl-4 { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
        .framsikt-node-title {
            color: var(--navy-dark);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .framsikt-node-right {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-variant-numeric: tabular-nums;
        }
        .framsikt-node-cv {
            font-weight: 700;
        }
        .framsikt-sub-tree {
            list-style: none;
            padding-left: 18px;
            margin: 2px 0 4px 0;
            border-left: 1px dashed #cbd5e1;
        }

        /* Framsikt Detail Panel (Right Column) */
        .framsikt-detail-col {
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 18px;
            min-width: 0;
        }
        .framsikt-breadcrumb-bar {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 3px;
            padding: 6px 12px;
            font-size: 11.5px;
            color: var(--text-secondary);
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
        }
        .framsikt-breadcrumb-step {
            cursor: pointer;
            color: #0284c7;
            text-decoration: none;
            font-weight: 600;
        }
        .framsikt-breadcrumb-step:hover {
            text-decoration: underline;
        }
        .framsikt-breadcrumb-current {
            color: var(--navy-dark);
            font-weight: 700;
        }
        .framsikt-leader-card {
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-left: 4px solid var(--navy-dark);
            border-radius: 3px;
            padding: 14px 16px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 12px;
        }
        .framsikt-leader-info h3 {
            font-size: 16px;
            font-weight: 800;
            color: var(--navy-dark);
            margin-bottom: 2px;
        }
        .framsikt-leader-info .subtitle {
            font-size: 12px;
            color: var(--text-secondary);
        }
        .framsikt-leader-meta {
            margin-top: 6px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 11.5px;
            color: #475569;
        }
        .framsikt-leader-meta strong {
            color: var(--text-primary);
        }
        .framsikt-four-dimensions {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .framsikt-dimension-box {
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 14px 16px;
        }
        .framsikt-dim-title {
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--navy-dark);
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 6px;
        }
        .framsikt-kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
        }
        .f-kpi-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 3px;
            padding: 10px 12px;
        }
        .f-kpi-label {
            font-size: 10.5px;
            text-transform: uppercase;
            font-weight: 700;
            color: #64748b;
            margin-bottom: 2px;
        }
        .f-kpi-val {
            font-size: 16px;
            font-weight: 800;
            font-variant-numeric: tabular-nums;
            color: var(--text-primary);
        }
        .f-kpi-sub {
            font-size: 10.5px;
            color: var(--text-secondary);
            margin-top: 2px;
        }
        .f-val-red { color: #b91c1c; }
        .f-val-green { color: #15803d; }
        .f-val-amber { color: #b45309; }

        /* Diagnose and Action Styling */
        .f-diagnose-card {
            background: #fffdf5;
            border-left: 3px solid #d97706;
        }
        .f-action-card {
            background: #f0fdf4;
            border-left: 3px solid #16a34a;
        }
        .f-prognose-card {
            background: #f8fafc;
            border-left: 3px solid var(--navy-dark);
        }
        .framsikt-action-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .framsikt-action-item {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            font-size: 12px;
            background: #ffffff;
            border: 1px solid #dcfce7;
            padding: 8px 10px;
            border-radius: 3px;
        }
        .framsikt-action-item .action-num {
            background: #16a34a;
            color: #ffffff;
            font-size: 10px;
            font-weight: 800;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
        }
        .framsikt-action-btns {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
        }
"""

# Insert CSS before </style>
if "</style>" in content and ".global-sector-bar" not in content:
    content = content.replace("</style>", FRAMSIKT_CSS + "\n</style>", 1)
    print("Inserted FRAMSIKT_CSS into <style>.")
else:
    print("CSS already present or </style> missing.")

# -----------------------------------------------------------------------------
# 2. GLOBAL SECTOR SELECTOR BAR (HTML)
# -----------------------------------------------------------------------------
GLOBAL_BAR_HTML = """
    <!-- =======================================================================
         UNIVERSAL VIRKSOMHETSOMRÅDE-VELGER & FILTERBAR (GLOBAL)
         Garanterer at valgt virksomhetsområde filtrerer data på tvers av hele huben.
         ======================================================================= -->
    <div class="global-sector-bar" id="global-sector-selector-bar">
        <div class="global-sector-bar-top">
            <div class="global-sector-label">
                <span>🏛️ Aktivt Virksomhetsområde:</span>
            </div>
            <div class="global-sector-pills" id="global-sector-pills">
                <button type="button" class="gsec-pill active" data-sec="ALL" onclick="selectSector('ALL')">
                    <span>🌐 Konsern (Alle områder)</span>
                    <span class="pill-badge">7.24 mrd</span>
                </button>
                <button type="button" class="gsec-pill" data-sec="HELSE" onclick="selectSector('HELSE')">
                    <span>🏥 1. Helse og mestring</span>
                    <span class="pill-badge" style="background:#fee2e2; color:#b91c1c;">-9.85M</span>
                </button>
                <button type="button" class="gsec-pill" data-sec="OPPVEKST" onclick="selectSector('OPPVEKST')">
                    <span>🏫 2. Oppvekst og utdanning</span>
                    <span class="pill-badge" style="background:#fee2e2; color:#b91c1c;">-11.87M</span>
                </button>
                <button type="button" class="gsec-pill" data-sec="BYUTVIKLING" onclick="selectSector('BYUTVIKLING')">
                    <span>🏗️ 3. By- og stedsutvikling</span>
                    <span class="pill-badge" style="background:#dcfce7; color:#15803d;">+310k</span>
                </button>
                <button type="button" class="gsec-pill" data-sec="KULTUR" onclick="selectSector('KULTUR')">
                    <span>🎭 4. Kultur og innbyggerdialog</span>
                    <span class="pill-badge" style="background:#f1f5f9; color:#475569;">380M</span>
                </button>
                <button type="button" class="gsec-pill" data-sec="ORG_TEK" onclick="selectSector('ORG_TEK')">
                    <span>💻 5. Organisasjon og teknologi</span>
                    <span class="pill-badge" style="background:#f1f5f9; color:#475569;">460M</span>
                </button>
                <button type="button" class="gsec-pill" data-sec="OKONOMI" onclick="selectSector('OKONOMI')">
                    <span>⚖️ 6. Økonomi og virksomhetsstyring</span>
                    <span class="pill-badge" style="background:#dcfce7; color:#15803d;">+2.58M</span>
                </button>
            </div>
        </div>
        <div class="global-sector-notice" id="global-sector-active-notice">
            <div style="display:flex; align-items:center; gap:8px;">
                <span>📍 <strong>Gjeldende visning:</strong></span>
                <span id="global-sector-notice-text">🌐 Konsern (Alle virksomhetsområder inkludert). Klikk et område over for å isolere data.</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <button type="button" id="global-sector-reset-btn" class="btn btn-sm" onclick="selectSector('ALL')" style="font-size:11px; padding:3px 8px; display:none; background:#ffffff;">
                    ↺ Vis hele konsernet
                </button>
                <button type="button" class="btn btn-sm" onclick="jumpToFramsiktHierarchy()" style="font-size:11px; padding:3px 8px; background:var(--navy-dark); color:#ffffff; font-weight:700;">
                    🏛️ Framsikt Budsjettre (Drilldown)
                </button>
            </div>
        </div>
    </div>
"""

# Insert Global Sector Bar right above `<div class="hub-tab-pane active" id="tab-min-enhet"`
target_tab_min = '    <!-- FANE 1: MIN ENHET & MIN MÅNED -->'
if target_tab_min in content and "global-sector-selector-bar" not in content:
    content = content.replace(target_tab_min, GLOBAL_BAR_HTML + "\n" + target_tab_min, 1)
    print("Inserted GLOBAL_BAR_HTML above tab-min-enhet.")
else:
    print("GLOBAL_BAR_HTML already present or target missing.")

# -----------------------------------------------------------------------------
# 3. FRAMSIKT BUDSJETTNIVÅ-HIERARKI SECTION (HTML)
# -----------------------------------------------------------------------------
FRAMSIKT_SECTION_HTML = """
<!-- ============================================================================== -->
<!-- 🏛️ FRAMSIKT BUDSJETTNIVÅ-HIERARKI & DRILLDOWN (NIVÅ 1–4)                      -->
<!-- Speiler Framsikt EPM: Virksomhetsområde ➔ Sektor ➔ Enhet ➔ Avdeling            -->
<!-- jf. Kommuneloven §§ 13-1, 14-5 og Bystyrets Økonomireglement                  -->
<!-- ============================================================================== -->
<section class="workflow-section framsikt-section" id="framsikt-budsjetthierarki-seksjon">
    <div class="framsikt-header">
        <div class="framsikt-title">
            <h2>🏛️ Framsikt Budsjettstruktur &amp; Hierarkisk Drilldown (Nivå 1–4)</h2>
            <p>
                Speiler <strong>Framsikt EPM</strong> og Kristiansand kommunes formelle styringshierarki: 
                <strong>Virksomhetsområde (Nivå 1)</strong> ➔ <strong>Tjenesteområde (Nivå 2)</strong> ➔ 
                <strong>Resultatenhet/Skole/Sykehjem (Nivå 3)</strong> ➔ <strong>Avdeling/Kostnadssted (Nivå 4)</strong>.
                Klikk på enhver leder eller enhet for å se <strong>Nøkkeltall</strong>, <strong>Diagnose</strong>, 
                <strong>Prognose (EAC)</strong> og <strong>Action to take</strong> jf. <strong>Kommuneloven § 14-5</strong>.
            </p>
        </div>
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <button type="button" class="btn btn-sm" onclick="expandAllFramsiktTree()" style="font-size:11px; padding:4px 10px;">
                ➕ Fold ut alle
            </button>
            <button type="button" class="btn btn-sm" onclick="collapseAllFramsiktTree()" style="font-size:11px; padding:4px 10px;">
                ➖ Lukk alle
            </button>
            <button type="button" class="btn btn-sm btn-primary" onclick="exportFramsiktHierarchyXlsx()" style="font-size:11px; padding:4px 10px;">
                📥 Eksport til Excel
            </button>
        </div>
    </div>

    <div class="framsikt-layout">
        <!-- Venstre kolonne: Framsikt Hierarkitre -->
        <div class="framsikt-tree-col">
            <div class="framsikt-search-box">
                <input type="text" id="framsikt-search-input" placeholder="🔍 Søk i Framsikt (leder, enhet, avd, ansvar 202, 401)..." oninput="searchFramsiktTree(this.value)">
            </div>
            <div class="framsikt-tree-toolbar">
                <span id="framsikt-tree-count-label">Viser struktur for: <strong>Alle områder</strong></span>
                <span style="font-size:10px; color:#64748b;">Klikk rad for detaljer</span>
            </div>

            <!-- Trerot / Noder -->
            <ul class="framsikt-tree-list" id="framsikt-tree-root">
                <!-- Genereres dynamisk via renderFramsiktTree() -->
            </ul>
        </div>

        <!-- Høyre kolonne: Budsjettansvarlig Detalj- og Handlingskort -->
        <div class="framsikt-detail-col" id="framsikt-detail-panel">
            <!-- Fylles dynamisk via renderFramsiktDetail() -->
        </div>
    </div>
</section>
"""

# Insert Framsikt section right above `<div class="triage-grid" id="triage-seksjon">`
target_triage = '<div class="triage-grid" id="triage-seksjon">'
if target_triage in content and "framsikt-budsjetthierarki-seksjon" not in content:
    content = content.replace(target_triage, FRAMSIKT_SECTION_HTML + "\n\n" + target_triage, 1)
    print("Inserted FRAMSIKT_SECTION_HTML above triage-seksjon.")
else:
    print("FRAMSIKT_SECTION_HTML already present or target missing.")

# Write back preliminary modifications
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved HTML and CSS changes to index.html.")
