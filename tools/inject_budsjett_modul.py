# tools/inject_budsjett_modul.py
# -*- coding: utf-8 -*-
"""
Injektor for Budsjettmodul i Kristiansand Kommune Control Office Hub (index.html).
Basert på dokumentasjonspakken i budsjett-framsikt/:
- budsjettering-kristiansand-kommune-v2.md
- lonnsbudsjettering-kristiansand-framsikt-v2.md
- driftsarter-og-selvkost-alle-omrader-framsikt.md
- kostra-artskontoer-konteringsregler-framsikt.md
"""

import sys
import os

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read {HTML_FILE}: {len(content)} characters, {content.count(chr(10))} lines")

# 1. CSS FOR BUDSJETTMODUL
CSS_BLOCK = """
        /* ==========================================================================
           BUDSJETTMODUL: FRAMSIKT EPM, STILLINGS- & LØNNSMOTOR, SELVKOST (TUFTE STANDARD)
           ========================================================================== */
        .budsjett-modul-section {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 20px 24px;
            margin-bottom: 24px;
            border-top: 3px solid var(--navy-dark);
        }

        .bm-header-container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 14px;
        }

        .bm-header-title {
            font-size: 16px;
            font-weight: 800;
            color: var(--navy-dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .bm-header-sub {
            font-size: 12.5px;
            color: var(--text-secondary);
            margin-top: 4px;
            line-height: 1.5;
        }

        .bm-header-badges {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }

        .bm-badge {
            font-size: 10.5px;
            font-family: var(--font-mono);
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 3px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .bm-badge-primary {
            background: #e0f2fe;
            color: #0369a1;
            border: 1px solid #bae6fd;
        }

        .bm-badge-success {
            background: var(--success-green-bg);
            color: var(--success-green);
            border: 1px solid rgba(39, 174, 96, 0.3);
        }

        .bm-badge-navy {
            background: var(--navy-dark);
            color: #ffffff;
        }

        .bm-kpi-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin-bottom: 18px;
        }

        .bm-kpi-card {
            background: #fafbfc;
            border: 1px solid var(--border-light);
            border-radius: 3px;
            padding: 10px 14px;
        }

        .bm-kpi-card .bm-kpi-label {
            font-size: 10.5px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--text-muted);
            letter-spacing: 0.5px;
            margin-bottom: 3px;
        }

        .bm-kpi-card .bm-kpi-val {
            font-size: 18px;
            font-weight: 800;
            font-family: var(--font-mono);
            color: var(--navy-dark);
        }

        .bm-kpi-card .bm-kpi-note {
            font-size: 10.5px;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .bm-nav-tabs {
            display: flex;
            gap: 6px;
            background: #f1f5f9;
            padding: 6px;
            border-radius: 4px;
            border: 1px solid var(--border-light);
            margin-bottom: 20px;
            overflow-x: auto;
            flex-wrap: wrap;
        }

        .bm-tab-btn {
            font-family: var(--font-sans);
            font-size: 12px;
            font-weight: 600;
            padding: 7px 14px;
            border-radius: 3px;
            border: 1px solid transparent;
            background: transparent;
            color: var(--navy-dark);
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        .bm-tab-btn:hover {
            background: #e2e8f0;
            color: var(--navy-dark);
        }

        .bm-tab-btn.active {
            background: var(--navy-dark);
            color: #ffffff;
            border-color: var(--navy-dark);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .bm-tab-pane {
            display: none;
            animation: fadeIn 0.15s ease-in;
        }

        .bm-tab-pane.active {
            display: block;
        }

        .bm-grid-2col {
            display: grid;
            grid-template-columns: 1.15fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        @media (max-width: 1024px) {
            .bm-grid-2col {
                grid-template-columns: 1fr;
            }
        }

        .bm-box {
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 16px 18px;
        }

        .bm-box-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--navy-dark);
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.5px solid var(--border-subtle);
            padding-bottom: 6px;
        }

        .bm-form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 10px;
        }

        .bm-form-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .bm-form-group label {
            font-size: 11px;
            font-weight: 600;
            color: var(--navy-dark);
        }

        .bm-form-group select,
        .bm-form-group input {
            padding: 6px 10px;
            font-size: 12px;
            border: 1px solid var(--border-light);
            border-radius: 3px;
            font-family: var(--font-sans);
            background: #ffffff;
        }

        .bm-form-group select:focus,
        .bm-form-group input:focus {
            outline: none;
            border-color: var(--navy-dark);
        }

        .bm-result-summary {
            background: #fafbfc;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 14px;
        }

        .bm-res-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0;
            border-bottom: 1px solid var(--border-subtle);
            font-size: 12px;
        }

        .bm-res-item:last-child {
            border-bottom: none;
        }

        .bm-res-item.highlight-total {
            border-top: 1.5px solid var(--navy-dark);
            border-bottom: 2px solid var(--navy-dark);
            font-weight: 700;
            font-size: 13px;
            color: var(--navy-dark);
            padding: 8px 0;
        }

        .bm-res-item .num-val {
            font-family: var(--font-mono);
            font-weight: 600;
        }

        .bm-alert-banner {
            background: #fef3c7;
            border-left: 3px solid #d97706;
            padding: 9px 12px;
            font-size: 11.5px;
            color: #92400e;
            margin: 12px 0;
            border-radius: 2px;
            line-height: 1.45;
        }

        .bm-formula-banner {
            background: #f8fafc;
            border: 1px solid var(--border-subtle);
            border-left: 3px solid var(--navy-dark);
            padding: 10px 14px;
            font-size: 12px;
            margin-bottom: 14px;
            border-radius: 2px;
            line-height: 1.5;
        }

        .bm-year-stepper {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 12px;
            margin: 16px 0;
        }

        .bm-step-card {
            border: 1px solid var(--border-light);
            border-top: 3px solid var(--navy-light);
            border-radius: 3px;
            padding: 12px 14px;
            background: #ffffff;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .bm-step-card:hover {
            border-color: var(--navy-dark);
            background: #f8fafc;
        }

        .bm-step-card.active-phase {
            border-top-color: #0284c7;
            background: #f0f9ff;
            border-color: #bae6fd;
        }

        .bm-step-period {
            font-family: var(--font-mono);
            font-size: 10.5px;
            font-weight: 700;
            color: var(--navy-dark);
            margin-bottom: 2px;
            text-transform: uppercase;
        }

        .bm-step-title {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .bm-step-desc {
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .bm-step-role {
            font-size: 10px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            margin-top: 6px;
            display: block;
        }

        .bm-check-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 14px 0;
        }

        .bm-check-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 9px 12px;
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 3px;
            font-size: 12px;
            cursor: pointer;
            transition: background 0.1s;
        }

        .bm-check-item:hover {
            background: #f8fafc;
        }

        .bm-check-item input[type="checkbox"] {
            margin-top: 2px;
            cursor: pointer;
        }

        .bm-check-text {
            flex: 1;
        }

        .bm-check-title {
            font-weight: 600;
            color: var(--navy-dark);
            margin-bottom: 2px;
        }

        .bm-check-sub {
            font-size: 11px;
            color: var(--text-secondary);
        }
"""

# Insert CSS before </style>
if "/* BUDSJETTMODUL: FRAMSIKT EPM" not in content:
    content = content.replace("</style>", CSS_BLOCK + "\n</style>", 1)
    print("Inserted CSS_BLOCK")
else:
    print("CSS_BLOCK already present")

# 2. SIDEBAR NAV LINK
SIDEBAR_TARGET = """                <a href="#avvik-seksjon" class="sidebar-nav-item">
                    <span>🚨 KOSTRA Artsavvik</span>
                </a>"""

SIDEBAR_LINK = """                <a href="#avvik-seksjon" class="sidebar-nav-item">
                    <span>🚨 KOSTRA Artsavvik</span>
                </a>
                <a href="#budsjett-modul-seksjon" class="sidebar-nav-item" id="side-budsjett-modul" onclick="switchBudsjettModulTab('LONN')">
                    <span>🏛️ Budsjettmodul (Framsikt)</span>
                    <span class="badge-phase" style="background:#0369a1; color:#fff;">HØP 26</span>
                </a>"""

if "id=\"side-budsjett-modul\"" not in content:
    if SIDEBAR_TARGET in content:
        content = content.replace(SIDEBAR_TARGET, SIDEBAR_LINK, 1)
        print("Inserted SIDEBAR_LINK")
    else:
        print("Warning: SIDEBAR_TARGET not found")
else:
    print("Sidebar link already present")

# 3. COMMAND PALETTE ITEMS
CMD_TARGET = """                <div class="cmd-palette-item" onclick="executeCommand('SEC_OKO')">
                    <div class="cmd-item-left">
                        <span class="cmd-item-icon">⚖️</span>
                        <div>
                            <div class="cmd-item-label">6. Økonomi og virksomhetsstyring</div>
                            <div style="font-size:11px; color:var(--text-secondary);">Overordnet økonomiplan, budsjett, regnskap, innkjøp, staber</div>
                        </div>
                    </div>
                    <span class="cmd-item-badge">Ansvarsområde</span>
                </div>"""

CMD_ITEMS = """                <div class="cmd-palette-item" onclick="executeCommand('SEC_OKO')">
                    <div class="cmd-item-left">
                        <span class="cmd-item-icon">⚖️</span>
                        <div>
                            <div class="cmd-item-label">6. Økonomi og virksomhetsstyring</div>
                            <div style="font-size:11px; color:var(--text-secondary);">Overordnet økonomiplan, budsjett, regnskap, innkjøp, staber</div>
                        </div>
                    </div>
                    <span class="cmd-item-badge">Ansvarsområde</span>
                </div>
                <div class="cmd-palette-item" onclick="executeCommand('BUDSJETT_MODUL')">
                    <div class="cmd-item-left">
                        <span class="cmd-item-icon">🏛️</span>
                        <div>
                            <div class="cmd-item-label">Budsjettmodul & Framsikt EPM</div>
                            <div style="font-size:11px; color:var(--text-secondary);">Stillingsbudsjett, lønnsmotor, selvkost VAR og HØP årshjul</div>
                        </div>
                    </div>
                    <span class="cmd-item-badge">Framsikt</span>
                </div>
                <div class="cmd-palette-item" onclick="executeCommand('BUDSJETT_LONN')">
                    <div class="cmd-item-left">
                        <span class="cmd-item-icon">👥</span>
                        <div>
                            <div class="cmd-item-label">Stillings- og Lønnsberegning (Framsikt)</div>
                            <div style="font-size:11px; color:var(--text-secondary);">KLP vs SPK, feriepenger (12%/14,3%), 14,1% AGA og bruttoføring</div>
                        </div>
                    </div>
                    <span class="cmd-item-badge">Lønnsmotor</span>
                </div>
                <div class="cmd-palette-item" onclick="executeCommand('BUDSJETT_SELVKOST')">
                    <div class="cmd-item-left">
                        <span class="cmd-item-icon">💧</span>
                        <div>
                            <div class="cmd-item-label">Selvkostkalkulator (VAR & Byggesak)</div>
                            <div style="font-size:11px; color:var(--text-secondary);">Funksjon 3400/3450/3500/3600, kapitalkostnader og 5-årsfond</div>
                        </div>
                    </div>
                    <span class="cmd-item-badge">Selvkost</span>
                </div>
                <div class="cmd-palette-item" onclick="executeCommand('BUDSJETT_ARSHJUL')">
                    <div class="cmd-item-left">
                        <span class="cmd-item-icon">📅</span>
                        <div>
                            <div class="cmd-item-label">Budsjett-Årshjul & Framsikt Tidslinje</div>
                            <div style="font-size:11px; color:var(--text-secondary);">Interne frister fra mai til desember jf. Bystyrets økonomireglement</div>
                        </div>
                    </div>
                    <span class="cmd-item-badge">Årshjul</span>
                </div>"""

if "executeCommand('BUDSJETT_MODUL')" not in content:
    if CMD_TARGET in content:
        content = content.replace(CMD_TARGET, CMD_ITEMS, 1)
        print("Inserted CMD_ITEMS")
    else:
        print("Warning: CMD_TARGET not found")

# 4. EXECUTE COMMAND HANDLERS
EXEC_TARGET = """            } else if (cmd === 'MOTE_NIVA1') {"""

EXEC_NEW = """            } else if (cmd === 'BUDSJETT_MODUL') {
                switchBudsjettModulTab('LONN');
                const el = document.getElementById("budsjett-modul-seksjon");
                if (el) el.scrollIntoView({ behavior: "smooth" });
            } else if (cmd === 'BUDSJETT_LONN') {
                switchBudsjettModulTab('LONN');
                const el = document.getElementById("budsjett-modul-seksjon");
                if (el) el.scrollIntoView({ behavior: "smooth" });
            } else if (cmd === 'BUDSJETT_SELVKOST') {
                switchBudsjettModulTab('SELVKOST');
                const el = document.getElementById("budsjett-modul-seksjon");
                if (el) el.scrollIntoView({ behavior: "smooth" });
            } else if (cmd === 'BUDSJETT_ARSHJUL') {
                switchBudsjettModulTab('ARSHJUL');
                const el = document.getElementById("budsjett-modul-seksjon");
                if (el) el.scrollIntoView({ behavior: "smooth" });
            } else if (cmd === 'BUDSJETT_KOSTRA') {
                switchBudsjettModulTab('KOSTRA');
                const el = document.getElementById("budsjett-modul-seksjon");
                if (el) el.scrollIntoView({ behavior: "smooth" });
            } else if (cmd === 'BUDSJETT_QA') {
                switchBudsjettModulTab('QA');
                const el = document.getElementById("budsjett-modul-seksjon");
                if (el) el.scrollIntoView({ behavior: "smooth" });
            } else if (cmd === 'MOTE_NIVA1') {"""

if "cmd === 'BUDSJETT_MODUL'" not in content:
    if EXEC_TARGET in content:
        content = content.replace(EXEC_TARGET, EXEC_NEW, 1)
        print("Inserted EXEC_NEW")
    else:
        print("Warning: EXEC_TARGET not found")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("Stage 1 complete: CSS and Navigation hooked.")
