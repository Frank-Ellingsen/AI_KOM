#!/usr/bin/env python3
"""
Update and Expand Kristiansand Control Office Hub (index.html)
Fyller Office Hub med:
1. Oppdaterte hurtiglenker til faktiske filer (inkl. nye .docx og .xlsx maler)
2. Operativ Saksbehandlingsflyt (Trinn 1-6) med interaktiv saksgenerator
3. Dokument- og Malbank med filtrering, direkte nedlasting og forhåndsvisning
4. Interaktiv Power BI & DAX Måltalls-Hub (KOSTRA drilldown, S-kurver, EVM)
5. Full forhåndsvisningsmodal (Modal Dialog) for samtlige maler og sjekklister
"""

from __future__ import annotations
from pathlib import Path
import re
import sys

# Sikre UTF-8 i konsoll på Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"


def build_new_html():
    raw_html = INDEX_PATH.read_text(encoding="utf-8")

    # 1. NY CSS STIL
    new_css = """
        /* ==========================================================================
           TUFTE DATA-INK TILLEGGSMODULER: MALER, SAKSFLYT, POWER BI & MODAL
           ========================================================================== */
        
        /* Stepper / Saksbehandlingsflyt */
        .workflow-section {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 18px 20px;
            margin-bottom: 24px;
        }

        .stepper-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 12px;
            margin: 14px 0 18px 0;
        }

        .step-card {
            border: 1px solid var(--border-light);
            border-top: 3px solid var(--navy-dark);
            border-radius: 3px;
            padding: 10px 12px;
            background: #fafafa;
            font-size: 11.5px;
            transition: all 0.15s ease;
            cursor: pointer;
        }

        .step-card:hover {
            background: #f1f5f9;
            border-color: var(--navy-dark);
        }

        .step-card.active-step {
            border-top-color: var(--success-green);
            background: var(--success-green-bg);
            border-color: rgba(39, 174, 96, 0.4);
        }

        .step-num {
            font-family: var(--font-mono);
            font-weight: 700;
            color: var(--navy-dark);
            font-size: 11px;
            margin-bottom: 2px;
            text-transform: uppercase;
        }

        .step-title {
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
            font-size: 12px;
        }

        .step-desc {
            color: var(--text-secondary);
            line-height: 1.4;
        }

        /* Interaktiv Saksgenerator Boks */
        .saksgenerator-box {
            background: #f8fafc;
            border: 1px solid var(--border-light);
            border-left: 3px solid var(--accent-blue);
            border-radius: 3px;
            padding: 14px 16px;
            margin-top: 12px;
        }

        .generator-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr auto;
            gap: 12px;
            align-items: flex-end;
            margin-bottom: 12px;
        }

        @media (max-width: 900px) {
            .generator-grid {
                grid-template-columns: 1fr;
            }
        }

        .form-group label {
            display: block;
            font-size: 11px;
            font-weight: 600;
            color: var(--navy-dark);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-select, .form-input {
            width: 100%;
            padding: 7px 10px;
            font-size: 12px;
            font-family: var(--font-sans);
            border: 1px solid var(--border-light);
            border-radius: 3px;
            background: #ffffff;
        }

        .generated-output {
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 3px;
            padding: 12px 14px;
            font-family: var(--font-mono);
            font-size: 11.5px;
            line-height: 1.6;
            color: var(--text-primary);
            max-height: 240px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        /* Dokument- og Malbank */
        .docbank-section {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 18px 20px;
            margin-bottom: 24px;
        }

        .filter-tabs {
            display: flex;
            gap: 8px;
            margin: 12px 0 16px 0;
            flex-wrap: wrap;
        }

        .tab-btn {
            font-family: var(--font-sans);
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid var(--border-light);
            background: #f8fafc;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .tab-btn:hover {
            background: #e2e8f0;
            color: var(--navy-dark);
        }

        .tab-btn.active-tab {
            background: var(--navy-dark);
            color: #ffffff;
            border-color: var(--navy-dark);
        }

        .doc-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 14px;
        }

        .doc-card {
            border: 1px solid var(--border-light);
            border-radius: 3px;
            padding: 14px 16px;
            background: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: border-color 0.15s ease;
        }

        .doc-card:hover {
            border-color: var(--navy-dark);
        }

        .doc-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 6px;
        }

        .format-badge {
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 2px;
            text-transform: uppercase;
        }

        .badge-docx { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
        .badge-xlsx { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
        .badge-dax  { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
        .badge-md   { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
        .badge-pdf  { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

        .doc-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--navy-dark);
            margin-bottom: 4px;
            line-height: 1.35;
        }

        .doc-law {
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 8px;
            font-weight: 500;
        }

        .doc-desc {
            font-size: 11.5px;
            color: var(--text-secondary);
            margin-bottom: 12px;
            line-height: 1.45;
            flex-grow: 1;
        }

        .doc-actions {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            padding-top: 10px;
            border-top: 1px solid var(--border-subtle);
        }

        .btn-sm {
            padding: 4px 8px;
            font-size: 11px;
            font-weight: 600;
        }

        /* Power BI & DAX Showcase */
        .powerbi-section {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 18px 20px;
            margin-bottom: 24px;
        }

        .pbi-tabs-bar {
            display: flex;
            border-bottom: 1px solid var(--border-light);
            gap: 16px;
            margin-bottom: 16px;
        }

        .pbi-tab {
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.15s ease;
        }

        .pbi-tab:hover {
            color: var(--navy-dark);
        }

        .pbi-tab.active {
            color: var(--navy-dark);
            border-bottom-color: var(--navy-dark);
        }

        .dax-code-block {
            background: #1e293b;
            color: #f8fafc;
            padding: 12px 16px;
            border-radius: 3px;
            font-family: var(--font-mono);
            font-size: 11.5px;
            line-height: 1.6;
            position: relative;
            max-height: 320px;
            overflow-y: auto;
        }

        .copy-code-btn {
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(255,255,255,0.15);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.25);
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 2px;
            cursor: pointer;
        }

        .copy-code-btn:hover {
            background: rgba(255,255,255,0.3);
        }

        /* Modal Dialog */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            padding: 20px;
        }

        .modal-box {
            background: #ffffff;
            border-radius: 4px;
            max-width: 820px;
            width: 100%;
            max-height: 90vh;
            display: flex;
            flex-direction: column;
            border: 1px solid var(--border-light);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        .modal-header {
            padding: 14px 20px;
            border-bottom: 1.5px solid var(--navy-dark);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--navy-dark);
        }

        .modal-close-btn {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: var(--text-muted);
            line-height: 1;
        }

        .modal-body {
            padding: 18px 20px;
            overflow-y: auto;
            font-size: 12.5px;
            line-height: 1.6;
            color: var(--text-primary);
        }

        .modal-footer {
            padding: 12px 20px;
            border-top: 1px solid var(--border-light);
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            background: #fafafa;
        }
    """

    # Erstatt slutt av style med ny CSS
    raw_html = raw_html.replace("    </style>", new_css + "\n    </style>")

    # 2. OPPDATER TOOLBAR
    old_toolbar = """    <!-- 2. HURTIG-HANDLINGER / TOOLBAR -->
    <div class="hub-toolbar">
        <a href="http://localhost:8501" target="_blank" class="btn btn-primary">
            🚀 Åpne Streamlit Fullskjerm (Port 8501)
        </a>
        <a href="reports/Kommune_Project_Controller_Reporting_2026.xlsx" download class="btn" style="background: #107c41; color: white; border-color: #107c41;">
            📊 Last ned Excel Mastermodell (.xlsx)
        </a>
        <a href="STYRINGSKALENDER_OG_ARSHJUL_2026.md" target="_blank" class="btn">
            📅 Årshjul 2026/2027
        </a>
        <a href="CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md" target="_blank" class="btn">
            🛡️ Sjekkliste & Periodelukking
        </a>
        <a href="TERTIALRAPPORT_NOTAT_OG_SAKSFREMLEGG.md" target="_blank" class="btn">
            📝 Politisk Notat (T2)
        </a>
        <button class="btn btn-accent" id="btn-update-vectordb" onclick="triggerVectorDbUpdate()">
            ⚡ Oppdater Vektor-DB
        </button>
        <button class="btn" onclick="exportAuditTrail()">
            📥 Eksporter SHA-256 Audit Log (JSON)
        </button>
        <button class="btn" onclick="filterEntity('ALL')">
            🏛️ Alle Enheter
        </button>
        <button class="btn" onclick="filterEntity('SKOLE')">
            🏫 Kommunal Skole
        </button>
        <button class="btn" onclick="filterEntity('BO')">
            🏥 Kommunal Boenhet
        </button>
        <button class="btn" onclick="toggleEngine()" id="engine-btn">
            🔄 Bytt Motor (Gemini / Ollama)
        </button>
    </div>"""

    new_toolbar = """    <!-- 2. HURTIG-HANDLINGER / TOOLBAR -->
    <div class="hub-toolbar">
        <a href="http://localhost:8501" target="_blank" class="btn btn-primary">
            🚀 Åpne Streamlit (Port 8501)
        </a>
        <a href="reports/Kommune_Project_Controller_Reporting_2026.xlsx" download class="btn" style="background: #107c41; color: white; border-color: #107c41;">
            📊 Excel Mastermodell (.xlsx)
        </a>
        <a href="reports/Mal_Saksbehandling_Tiltak_Avstemming_2026.xlsx" download class="btn" style="background: #107c41; color: white; border-color: #107c41;">
            📑 Saksbehandlingsmodell (.xlsx)
        </a>
        <a href="#dokumentbank" class="btn btn-accent">
            📂 Dokument- & Malbank
        </a>
        <a href="#saksflyt" class="btn">
            🔄 Saksbehandlingsflyt
        </a>
        <a href="#powerbi-showcase" class="btn">
            📊 Power BI & DAX Hub
        </a>
        <a href="bruker-guides/STYRINGSKALENDER_OG_ARSHJUL_2026.md" target="_blank" class="btn">
            📅 Årshjul 2026/2027
        </a>
        <a href="revisjon-og-kontroll/CONTROLLER_CHECKLIST_OG_PERIODELUKKING.md" target="_blank" class="btn">
            🛡️ Sjekkliste & Lukking
        </a>
        <a href="revisjon-og-kontroll/TERTIALRAPPORT_NOTAT_OG_SAKSFREMLEGG.md" target="_blank" class="btn">
            📝 Politisk Notat (T2)
        </a>
        <button class="btn" id="btn-update-vectordb" onclick="triggerVectorDbUpdate()">
            ⚡ Oppdater Vektor-DB
        </button>
        <button class="btn" onclick="exportAuditTrail()">
            📥 Audit Log (JSON)
        </button>
        <button class="btn" onclick="filterEntity('ALL')">
            🏛️ Alle
        </button>
        <button class="btn" onclick="filterEntity('SKOLE')">
            🏫 Skole
        </button>
        <button class="btn" onclick="filterEntity('BO')">
            🏥 Boenhet
        </button>
        <button class="btn" onclick="toggleEngine()" id="engine-btn">
            🔄 Bytt Motor
        </button>
    </div>"""

    raw_html = raw_html.replace(old_toolbar, new_toolbar)

    # 3. NYE SEKSJONER FØR FOOTER
    # Finn: <!-- 6. BUNNLINJE / FOOTER -->
    new_sections = """
    <!-- =======================================================================
         6. OPERATIV SAKSBEHANDLINGSFLYT & STAGE-GATE SLØYFE
         ======================================================================= -->
    <section class="workflow-section" id="saksflyt">
        <div class="section-header">
            <span>🔄 Operativ Saksbehandlingsflyt & Stage-Gate Sløyfe (Trinn 1–6)</span>
            <span class="status-badge">Kommuneloven § 14-5 & EU AI Act Art. 14</span>
        </div>
        <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 12px;">
            Standardisert arbeidsflyt for saksbehandling, partssamarbeid og sign-off fra oppdaget avvik til politisk vedtak i Formannskapet/Bystyret.
        </p>

        <div class="stepper-grid">
            <div class="step-card active-step" onclick="selectFlowStep(1)">
                <div class="step-num">Trinn 1</div>
                <div class="step-title">🚨 Avviksdeteksjon</div>
                <div class="step-desc">Automatisk Z-score screening av Visma ERP mot Framsikt rammer (60-90 dager før T2).</div>
            </div>
            <div class="step-card" onclick="selectFlowStep(2)">
                <div class="step-num">Trinn 2</div>
                <div class="step-title">🤖 Glass-Box RAG</div>
                <div class="step-desc">Årsaksforklaring med eksplisitt paragrafsitering (§ 14-5, § 14-6, KOSTRA-veileder).</div>
            </div>
            <div class="step-card" onclick="selectFlowStep(3)">
                <div class="step-num">Trinn 3</div>
                <div class="step-title">🤝 HTA § 4 Drøfting</div>
                <div class="step-desc">Obligatorisk partssamarbeid med tillitsvalgte ved turnus- eller vikartiltak.</div>
            </div>
            <div class="step-card" onclick="selectFlowStep(4)">
                <div class="step-num">Trinn 4</div>
                <div class="step-title">👤 HITL Overprøving</div>
                <div class="step-desc">Controller godkjenner (APPROVED), modifiserer eller avviser AI-anbefaling.</div>
            </div>
            <div class="step-card" onclick="selectFlowStep(5)">
                <div class="step-num">Trinn 5</div>
                <div class="step-title">🔒 SHA-256 Stempel</div>
                <div class="step-desc">Uforanderlig kryptografisk forsegling i Audit_AI_Actions for Kommunerevisjonen.</div>
            </div>
            <div class="step-card" onclick="selectFlowStep(6)">
                <div class="step-num">Trinn 6</div>
                <div class="step-title">🏛️ Politisk Vedtak</div>
                <div class="step-desc">Ferdigstillelse av saksfremlegg til Formannskapet og overføring til Public360.</div>
            </div>
        </div>

        <!-- INTERAKTIV SAKSGENERATOR -->
        <div class="saksgenerator-box">
            <div style="font-weight: 700; font-size: 12px; color: var(--navy-dark); margin-bottom: 8px;">
                ⚡ Interaktiv Saksgenerator & Notatbygger (Klikk og produser forvaltningsnotat)
            </div>
            <div class="generator-grid">
                <div class="form-group">
                    <label>Velg Enhet / Sektor</label>
                    <select id="gen-enhet" class="form-select" onchange="updateGeneratedNote()">
                        <option value="SKOLE">Kommunal Skole (KOSTRA 202 Oppvekst)</option>
                        <option value="BO">Kommunal Boenhet (KOSTRA 254 Helse & Mestring)</option>
                        <option value="BEGGE">Samlet Virksomhetsområde (Skole + Bo)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Behandlingsnivå & Hjemmel</label>
                    <select id="gen-niva" class="form-select" onchange="updateGeneratedNote()">
                        <option value="NIVA1">Nivå 1: Enhetsleder Mikrotiltak (< 50 000 kr jf. Delegasjon § 3)</option>
                        <option value="NIVA2">Nivå 2: Sektoromdisponering (Kommunalsjef etter PSU)</option>
                        <option value="NIVA3" selected>Nivå 3: Formell Budsjettendring (Bystyret jf. § 14-5)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Hovedtiltak for inndekning</label>
                    <select id="gen-tiltak" class="form-select" onchange="updateGeneratedNote()">
                        <option value="VIKAR">T2 Vikarstopp & Intern Vikarpool (Effekt: 28 872 kr)</option>
                        <option value="OVERTID">T3 Overtidsplanlegging iht. HTA § 4 (Effekt: 55 077 kr)</option>
                        <option value="FOND" selected>Inndekning via Disposisjonsfond jf. § 14-5 (Effekt: Saldering)</option>
                    </select>
                </div>
                <div>
                    <button class="btn btn-primary" onclick="copyGeneratedNote()">
                        📋 Kopier Saksnotat
                    </button>
                </div>
            </div>

            <div class="generated-output" id="generated-note-text">Laster forvaltningsnotat...</div>
        </div>
    </section>

    <!-- =======================================================================
         7. DOKUMENT- OG MALBANK (TEMPLATES, EXCEL, POWER BI & JUS)
         ======================================================================= -->
    <section class="docbank-section" id="dokumentbank">
        <div class="section-header">
            <span>📂 Offisiell Dokument- og Malbank (Templates, Skjemaer & Modeller)</span>
            <span class="status-badge">Klar for nedlasting & forhåndsvisning</span>
        </div>
        <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 12px;">
            Kvalitetssikrede maler utarbeidet for controllere, rådgivere og enhetsledere i Kristiansand kommune. Alle dokumenter overholder Edward Tuftes standarder og kommunelovens krav.
        </p>

        <!-- Filter-faner -->
        <div class="filter-tabs">
            <button class="tab-btn active-tab" onclick="filterDocs('ALL')">📁 Alle Ressurser (16)</button>
            <button class="tab-btn" onclick="filterDocs('MALER')">📝 Maler & Skjemaer (6)</button>
            <button class="tab-btn" onclick="filterDocs('EXCEL')">📊 Excel-modeller (3)</button>
            <button class="tab-btn" onclick="filterDocs('POWERBI')">📈 Power BI & DAX (3)</button>
            <button class="tab-btn" onclick="filterDocs('JUS')">🛡️ Revisjon & Jus (4)</button>
        </div>

        <!-- Dokumentkort Grid -->
        <div class="doc-cards-grid" id="doc-cards-container">
            
            <!-- KORT 1 -->
            <div class="doc-card" data-category="MALER">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-docx">.DOCX & .MD</span>
                        <span style="font-size: 11px; color: var(--text-muted);">Sak 26/08940</span>
                    </div>
                    <div class="doc-title">Politisk Saksfremlegg: Budsjettendring</div>
                    <div class="doc-law">Hjemmel: Kommuneloven § 14-5 & § 14-6</div>
                    <div class="doc-desc">Komplett politisk saksutredning med innstilling, dekningsforslag fra disposisjonsfond og KOSTRA-analyse for Formannskapet og Bystyret.</div>
                </div>
                <div class="doc-actions">
                    <a href="templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx" download class="btn btn-sm btn-primary">📥 Word (.docx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('SAKSFREMLEGG')">👁️ Forhåndsvis</button>
                    <a href="templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.md" target="_blank" class="btn btn-sm">📄 Markdown</a>
                </div>
            </div>

            <!-- KORT 2 -->
            <div class="doc-card" data-category="EXCEL">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-xlsx">.XLSX</span>
                        <span style="font-size: 11px; color: var(--success-green); font-weight: 600;">Ny Modell 2026</span>
                    </div>
                    <div class="doc-title">Saksbehandling & Tiltaksavstemming</div>
                    <div class="doc-law">Standard: Edward Tufte Data-Ink / FAST</div>
                    <div class="doc-desc">Interaktiv arbeidsbok med avviksdekomponering, prioritert tiltaksmeny (T1–T6) og Stage-Gate Port 9 sign-off formler.</div>
                </div>
                <div class="doc-actions">
                    <a href="reports/Mal_Saksbehandling_Tiltak_Avstemming_2026.xlsx" download class="btn btn-sm btn-primary" style="background: #107c41; border-color: #107c41;">📥 Last ned (.xlsx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('EXCEL_INFO')">ℹ️ Om arket</button>
                </div>
            </div>

            <!-- KORT 3 -->
            <div class="doc-card" data-category="EXCEL">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-xlsx">.XLSX</span>
                        <span style="font-size: 11px; color: var(--navy-dark); font-weight: 600;">Mastermodell</span>
                    </div>
                    <div class="doc-title">Master Project Controller Rapport 2026</div>
                    <div class="doc-law">Standard: ISO 21508 EVM / Tufte</div>
                    <div class="doc-desc">6 faner: Executive Dashboard, T2-avvik per art, EVM Capex (Vågsbygd & Randesund), styringskalender, kontrollsjekkliste og KOSTRA-mapping.</div>
                </div>
                <div class="doc-actions">
                    <a href="reports/Kommune_Project_Controller_Reporting_2026.xlsx" download class="btn btn-sm btn-primary" style="background: #107c41; border-color: #107c41;">📥 Last ned (.xlsx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('MASTER_INFO')">ℹ️ Faneoversikt</button>
                </div>
            </div>

            <!-- KORT 4 -->
            <div class="doc-card" data-category="MALER">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-docx">.DOCX & .MD</span>
                        <span style="font-size: 11px; color: var(--text-muted);">Enhetsnotat</span>
                    </div>
                    <div class="doc-title">Avviksnotat & Tiltaksplan (T1–T6)</div>
                    <div class="doc-law">Nivå: Enhetsleder til Kommunalsjef</div>
                    <div class="doc-desc">Månedsnotat for rektor og enhetsleder. Dekomponerer lønn, vikarer og overtid, og angir forventet EOY-effekt for hvert tiltak.</div>
                </div>
                <div class="doc-actions">
                    <a href="templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx" download class="btn btn-sm btn-primary">📥 Word (.docx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('AVVIKSNOTAT')">👁️ Forhåndsvis</button>
                    <a href="templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.md" target="_blank" class="btn btn-sm">📄 Markdown</a>
                </div>
            </div>

            <!-- KORT 5 -->
            <div class="doc-card" data-category="MALER">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-docx">.DOCX & .MD</span>
                        <span style="font-size: 11px; color: var(--alert-amber); font-weight: 600;">Partssamarbeid</span>
                    </div>
                    <div class="doc-title">HTA § 4 Drøftingsprotokoll</div>
                    <div class="doc-law">Hjemmel: HTA § 4 & Arbeidsmiljøloven</div>
                    <div class="doc-desc">Lovpålagt protokoll for drøfting av turnusendringer, overtidsstopp og vikarbruk med tillitsvalgte (Fagforbundet, Delta, NSF, Utdanningsforb).</div>
                </div>
                <div class="doc-actions">
                    <a href="templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx" download class="btn btn-sm btn-primary">📥 Word (.docx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('HTA_PROTOKOLL')">👁️ Forhåndsvis</button>
                    <a href="templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.md" target="_blank" class="btn btn-sm">📄 Markdown</a>
                </div>
            </div>

            <!-- KORT 6 -->
            <div class="doc-card" data-category="JUS">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-docx">.DOCX & .MD</span>
                        <span style="font-size: 11px; color: var(--navy-dark); font-weight: 600;">Kvalitetsport 9</span>
                    </div>
                    <div class="doc-title">Stage-Gate Port 9 HITL Sign-off</div>
                    <div class="doc-law">EU AI Act Art. 14 / GDPR Art. 22</div>
                    <div class="doc-desc">Skjema for controller-signoff med saksbehandlers skriftlige begrunnelse og kryptografisk SHA-256 revisjonsstempel.</div>
                </div>
                <div class="doc-actions">
                    <a href="templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.docx" download class="btn btn-sm btn-primary">📥 Word (.docx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('PORT9_SIGNOFF')">👁️ Forhåndsvis</button>
                    <a href="templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.md" target="_blank" class="btn btn-sm">📄 Markdown</a>
                </div>
            </div>

            <!-- KORT 7 -->
            <div class="doc-card" data-category="JUS">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-docx">.DOCX & .MD</span>
                        <span style="font-size: 11px; color: var(--alert-red); font-weight: 600;">Kvalitetsport 7</span>
                    </div>
                    <div class="doc-title">FRIA & DPIA Risikovurdering</div>
                    <div class="doc-law">EU AI Act Art. 27 / GDPR Art. 35</div>
                    <div class="doc-desc">Obligatorisk konsekvensvurdering for personvern, likebehandling og grunnleggende rettigheter, med tvingende DPO-vetorett.</div>
                </div>
                <div class="doc-actions">
                    <a href="templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx" download class="btn btn-sm btn-primary">📥 Word (.docx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('FRIA_DPIA')">👁️ Forhåndsvis</button>
                    <a href="templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.md" target="_blank" class="btn btn-sm">📄 Markdown</a>
                </div>
            </div>

            <!-- KORT 8 -->
            <div class="doc-card" data-category="JUS">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-md">.MD</span>
                        <span style="font-size: 11px; color: var(--navy-dark); font-weight: 600;">Revisjonssjekk</span>
                    </div>
                    <div class="doc-title">Kommunerevisjonens Sjekkliste</div>
                    <div class="doc-law">Kommuneloven kap. 24 & ISO 42001</div>
                    <div class="doc-desc">6 kontrollområder for årlig revisjon av AI-systemer: SHA-256 loggintegritet, HITL-frekvens, PII-vask og kildeforankring.</div>
                </div>
                <div class="doc-actions">
                    <a href="revisjon-og-kontroll/KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md" target="_blank" class="btn btn-sm btn-primary">📄 Åpne Sjekkliste</a>
                    <button class="btn btn-sm" onclick="previewDocument('REVISJON_SJEKK')">👁️ Forhåndsvis</button>
                </div>
            </div>

            <!-- KORT 9 -->
            <div class="doc-card" data-category="POWERBI">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-dax">.DAX</span>
                        <span style="font-size: 11px; color: #b45309; font-weight: 600;">DAX Library</span>
                    </div>
                    <div class="doc-title">DAX Measures Library for Power BI</div>
                    <div class="doc-law">Dokument: 02_DAX_Measures_Library.dax</div>
                    <div class="doc-desc">Ferdige DAX-beregninger for YTD regnskap, budsjett gjenstående, trendjustert merforbruk, rullende EOY og ISINSCOPE hierarkier.</div>
                </div>
                <div class="doc-actions">
                    <a href="powerbi/02_DAX_Measures_Library.dax" download class="btn btn-sm btn-primary">📥 Last ned (.dax)</a>
                    <button class="btn btn-sm" onclick="showDaxSnippet('EOY')">📋 Se DAX</button>
                </div>
            </div>

            <!-- KORT 10 -->
            <div class="doc-card" data-category="POWERBI">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-dax">.DAX</span>
                        <span style="font-size: 11px; color: #b45309; font-weight: 600;">KOSTRA Nøkkeltall</span>
                    </div>
                    <div class="doc-title">KOSTRA DAX KPI Pakke</div>
                    <div class="doc-law">Dokument: 04_KOSTRA_DAX_KPI_Package.dax</div>
                    <div class="doc-desc">Lovpålagte KOSTRA-indikatorer: Brutto driftsresultat i kr og %, korrigert netto driftsresultat (mål >= 1,7 %) og lønnsandel.</div>
                </div>
                <div class="doc-actions">
                    <a href="powerbi/04_KOSTRA_DAX_KPI_Package.dax" download class="btn btn-sm btn-primary">📥 Last ned (.dax)</a>
                    <button class="btn btn-sm" onclick="showDaxSnippet('KOSTRA')">📋 Se DAX</button>
                </div>
            </div>

            <!-- KORT 11 -->
            <div class="doc-card" data-category="POWERBI">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-md">.PQ / .M</span>
                        <span style="font-size: 11px; color: var(--navy-dark); font-weight: 600;">Power Query</span>
                    </div>
                    <div class="doc-title">Power Query M & RAG Integrasjon</div>
                    <div class="doc-law">Dokument: 01_PowerQuery_M_Code.pq</div>
                    <div class="doc-desc">ETL-transformasjoner med Query Folding mot SQLite/Fabric og tilpasset M-funksjon (fxOpenAI_RAG.m) for manuell oppdatering.</div>
                </div>
                <div class="doc-actions">
                    <a href="powerbi/01_PowerQuery_M_Code.pq" download class="btn btn-sm btn-primary">📥 Last ned (.pq)</a>
                    <a href="powerbi/fxOpenAI_RAG.m" download class="btn btn-sm">📥 RAG Funksjon (.m)</a>
                </div>
            </div>

            <!-- KORT 12 -->
            <div class="doc-card" data-category="JUS">
                <div>
                    <div class="doc-header-row">
                        <span class="format-badge badge-docx">.DOCX & .MD</span>
                        <span style="font-size: 11px; color: var(--navy-dark); font-weight: 600;">Internkontroll</span>
                    </div>
                    <div class="doc-title">Instruks for Periodelukking</div>
                    <div class="doc-law">GKRS & Kommuneloven kap. 14</div>
                    <div class="doc-desc">Månedlig og tertialvis rutine for bankavstemming, A-melding, Framsikt/Visma diff-sjekk og tidsfrister for controller.</div>
                </div>
                <div class="doc-actions">
                    <a href="templates/MAL_PERIODELUKKING_OG_AVSTEMMING.docx" download class="btn btn-sm btn-primary">📥 Word (.docx)</a>
                    <button class="btn btn-sm" onclick="previewDocument('LUKKING_INSTRUK')">👁️ Forhåndsvis</button>
                    <a href="templates/MAL_PERIODELUKKING_OG_AVSTEMMING.md" target="_blank" class="btn btn-sm">📄 Markdown</a>
                </div>
            </div>

        </div>
    </section>

    <!-- =======================================================================
         8. POWER BI & DAX ENTERPRISE SHOWCASE
         ======================================================================= -->
    <section class="powerbi-section" id="powerbi-showcase">
        <div class="section-header">
            <span>📊 Power BI & DAX Enterprise Showcase (Interaktiv Drifts- og Investeringskontroll)</span>
            <span class="status-badge">Tufte Data-Ink / ISINSCOPE</span>
        </div>
        <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 12px;">
            Simulering av Power BI Desktop / Fabric rapportmodell. Viser dynamisk KOSTRA-hierarki, Earned Value Management (EVM) for Capex, og offisielle DAX-mål.
        </p>

        <div class="pbi-tabs-bar">
            <div class="pbi-tab active" onclick="switchPbiTab('TAB1')">1. KOSTRA Driftsmatrise (Hierarki)</div>
            <div class="pbi-tab" onclick="switchPbiTab('TAB2')">2. Prosjektkontroll EVM (S-kurver)</div>
            <div class="pbi-tab" onclick="switchPbiTab('TAB3')">3. DAX Kjerneformler (Ett-klikks kopi)</div>
        </div>

        <!-- TAB 1: KOSTRA MATRISE -->
        <div id="pbi-tab-1">
            <table class="tufte-table">
                <thead>
                    <tr>
                        <th>Nivå / KOSTRA Hierarki</th>
                        <th>Enhet / Kostnadssted</th>
                        <th class="num">Årsbudsjett (BAC)</th>
                        <th class="num">Regnskap YTD (AC)</th>
                        <th class="num">EOY Rullende Prognose</th>
                        <th class="num">Est. Årsavvik</th>
                        <th>Varslingsstatus</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background: #f8fafc; font-weight: 700;">
                        <td>▼ 01 OPPVEKST OG UTDANNING</td>
                        <td>Sektor Oppvekst</td>
                        <td class="num">33 591 000</td>
                        <td class="num">36 080 000</td>
                        <td class="num">49 164 212</td>
                        <td class="num" style="color: var(--alert-red);">-15 573 212</td>
                        <td><span class="status-badge" style="color: var(--alert-red); border-color: var(--alert-red); background: var(--alert-red-bg);">KRITISK MERFORBRUK</span></td>
                    </tr>
                    <tr>
                        <td style="padding-left: 24px;">• Funksjon 202 Grunnskoleopplæring</td>
                        <td>4100 Kommunal Skole</td>
                        <td class="num">33 591 000</td>
                        <td class="num">36 080 000</td>
                        <td class="num">49 164 212</td>
                        <td class="num" style="color: var(--alert-red);">-15 573 212</td>
                        <td>§ 14-5 Sak påkrevd</td>
                    </tr>
                    <tr style="background: #f8fafc; font-weight: 700;">
                        <td>▼ 02 HELSE OG MESTRING</td>
                        <td>Sektor Helse</td>
                        <td class="num">50 339 572</td>
                        <td class="num">47 426 244</td>
                        <td class="num">67 072 639</td>
                        <td class="num" style="color: var(--alert-red);">-16 733 067</td>
                        <td><span class="status-badge" style="color: var(--alert-red); border-color: var(--alert-red); background: var(--alert-red-bg);">KRITISK MERFORBRUK</span></td>
                    </tr>
                    <tr>
                        <td style="padding-left: 24px;">• Funksjon 254 Kommunal Boenhet</td>
                        <td>5200 Bo og Miljø</td>
                        <td class="num">50 339 572</td>
                        <td class="num">47 426 244</td>
                        <td class="num">67 072 639</td>
                        <td class="num" style="color: var(--alert-red);">-16 733 067</td>
                        <td>§ 14-5 Sak påkrevd</td>
                    </tr>
                    <tr class="summary-row">
                        <td>TOTALT KONSOLIDERT KONTROLLUTVALG</td>
                        <td>2 Enheter</td>
                        <td class="num">83 930 572</td>
                        <td class="num">83 506 244</td>
                        <td class="num">116 236 851</td>
                        <td class="num" style="color: var(--alert-red);">-32 306 279</td>
                        <td>Bystyrets bord 28. sep</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- TAB 2: PROSJEKTKONTROLL EVM -->
        <div id="pbi-tab-2" style="display: none;">
            <table class="tufte-table">
                <thead>
                    <tr>
                        <th>Prosjektnavn (Kontoklasse 2)</th>
                        <th>Prosjekt-ID</th>
                        <th class="num">P50 Styringsramme (BAC)</th>
                        <th class="num">Påløpt Kostnad (AC)</th>
                        <th class="num">Earned Value (EV)</th>
                        <th class="num">CPI</th>
                        <th class="num">SPI</th>
                        <th class="num">EAC (Sluttkostnad)</th>
                        <th>Risikostatus</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Vågsbygd Barneskole (Nybygg)</td>
                        <td>PROJ-101</td>
                        <td class="num">185 000 000</td>
                        <td class="num">115 000 000</td>
                        <td class="num">104 500 000</td>
                        <td class="num">0.909</td>
                        <td class="num">0.950</td>
                        <td class="num">208 251 070</td>
                        <td><span class="status-badge" style="color: var(--alert-amber); border-color: var(--alert-amber); background: #fef3c7;">MIDDELS RISIKO</span></td>
                    </tr>
                    <tr>
                        <td>Randesund Døgnbemannet Boenhet</td>
                        <td>PROJ-201</td>
                        <td class="num">240 000 000</td>
                        <td class="num">165 000 000</td>
                        <td class="num">139 100 000</td>
                        <td class="num">0.843</td>
                        <td class="num">0.887</td>
                        <td class="num">299 529 558</td>
                        <td><span class="status-badge" style="color: var(--alert-red); border-color: var(--alert-red); background: var(--alert-red-bg);">HØY RISIKO</span></td>
                    </tr>
                    <tr>
                        <td>VA-Hovedledning Selvkost</td>
                        <td>PROJ-301</td>
                        <td class="num">92 000 000</td>
                        <td class="num">48 000 000</td>
                        <td class="num">49 300 000</td>
                        <td class="num">1.027</td>
                        <td class="num">0.997</td>
                        <td class="num">89 668 168</td>
                        <td><span class="status-badge">I RUTE (LAV RISIKO)</span></td>
                    </tr>
                    <tr class="summary-row">
                        <td>TOTAL INVESTERINGSPORTFOLJE</td>
                        <td>3 Prosjekter</td>
                        <td class="num">517 000 000</td>
                        <td class="num">328 000 000</td>
                        <td class="num">292 900 000</td>
                        <td class="num">0.893</td>
                        <td class="num">0.927</td>
                        <td class="num">597 448 796</td>
                        <td>Trekk på P85-reserve</td>
                    </tr>
                </tbody>
            </table>
            <div style="margin-top: 10px; font-size: 11px; color: var(--text-muted);">
                EVM-metodikk: CPI < 1.00 indikerer overskridelse per produsert enhet. P85-rammer og usikkerhetsavsetninger styres av prosjektcontroller.
            </div>
        </div>

        <!-- TAB 3: DAX FORMLER -->
        <div id="pbi-tab-3" style="display: none;">
            <div class="dax-code-block">
                <button class="copy-code-btn" onclick="copyDaxCode()">📋 Kopier Alle Mål</button>
<pre id="dax-display-code">// ==============================================================================
// KRISTIANSAND KOMMUNE — DAX PROGNOSE- OG KOSTRA MÅLTALL
// ==============================================================================

// 1. Akkumulert Regnskap YTD (Drift)
[Regnskap YTD] = 
CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]),
    Dim_Kontoklasse[kontoklasse_kode] = "1"
)

// 2. Gjenstående Budsjettert Ramme (T3)
[Budsjett Gjenstående] = 
CALCULATE(
    SUM(Fact_Regnskap[budsjett_belop]),
    Dim_Dato[maned] > 8
)

// 3. Trendjustert Merforbruk (Konservativ 50 % videreføring)
[Trendjustert Merforbruk] = 
VAR Avvik = [Avvik YTD]
RETURN
    IF(Avvik > 0, Avvik * 0.50, 0)

// 4. Rullerende End of Year (EOY) Prognose
[EOY Rullende Prognose] = 
[Regnskap YTD] + [Budsjett Gjenstående] + [Trendjustert Merforbruk]

// 5. Forventet Årsavvik (Varsling jf. Kommuneloven § 14-5)
[EOY Forventet Årsavvik] = 
[EOY Rullende Prognose] - [Vedtatt Årsbudsjett]

// 6. Dynamisk Hierarkimatrise (ISINSCOPE)
[Dynamisk Visning] = 
SWITCH(
    TRUE(),
    ISINSCOPE(Dim_Art[art_kode]), [Avvik YTD],
    ISINSCOPE(Dim_Funksjon[funksjon_kode]), [Avvik YTD],
    ISINSCOPE(Dim_Ansvar[kommunalsjefomrade]), [Avvik YTD],
    [Avvik YTD]
)</pre>
            </div>
        </div>
    </section>

    <!-- =======================================================================
         FORHÅNDSVISNINGSMODAL (MODAL DIALOG)
         ======================================================================= -->
    <div class="modal-overlay" id="doc-modal" onclick="closeModalOnBackdrop(event)">
        <div class="modal-box">
            <div class="modal-header">
                <div class="modal-title" id="modal-doc-title">Dokumenttittel</div>
                <button class="modal-close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modal-doc-body">
                Laster dokumentinnhold...
            </div>
            <div class="modal-footer">
                <button class="btn" onclick="copyModalContent()">📋 Kopier Tekst</button>
                <a id="modal-download-link" href="#" download class="btn btn-primary">📥 Last ned fil</a>
                <button class="btn" onclick="closeModal()">Lukk</button>
            </div>
        </div>
    </div>
"""

    raw_html = raw_html.replace("    <!-- 6. BUNNLINJE / FOOTER -->", new_sections + "\n    <!-- 6. BUNNLINJE / FOOTER -->")

    # 4. LEGG TIL JAVASCRIPT FOR DOKUMENTER, MODAL OG SAKSGENERATOR
    new_js = """
        /* ==========================================================================
           INTERAKTIV SAKSGENERATOR, DOKUMENTBANK & POWER BI VISER
           ========================================================================== */

        const SAKS_TEKSTER = {
            "SKOLE_NIVA3": `SAKSFREMLEGG: BUDSJETTREGULERING 2. TERTIAL 2026 — KOMMUNAL SKOLE (KOSTRA 202)
Arkivsak: 26/08940-1 | Utvalg: Formannskapet / Bystyret | Møtedato: 28. september 2026
Saksbehandler: Frank Ellingsen (Senior Controller) | Hjemmel: Kommuneloven § 14-5 & § 14-6

KOMMUNEDIREKTØRENS FORSLAG TIL VEDTAK:
1. Bystyret godkjenner en rammejustering på kr 3 200 000 til grunnskoleopplæring (KOSTRA 202) for å dekke lovpålagte lærertimer, spesialpedagogiske enkeltvedtak og sykefraværsdekning.
2. Netto merforbruk dekkes inn ved overføring fra kommunens disposisjonsfond jf. Kommuneloven § 14-5 andre ledd.

SAKSUTREDNING:
Hittil i år (T2 / august) har Kommunal Skole påløpt et merforbruk på kr 2 468 000 på fast lønn lærere (art 1010) og kr 645 000 på sykevikarer (art 1020). Avviket skyldes høyt korttidsfravær og forsinket refusjonsutbetaling fra NAV (art 1690). Jf. Kommuneloven § 14-6 fjerde ledd er utgifter og refusjoner ført brutto.

KRYPTOGRAFISK REVISJONSSTEMPEL:
SHA-256: d504a35181b99181c07bad48ac6964d188319f077abef265f2420caea919a32c`,

            "BO_NIVA3": `SAKSFREMLEGG: BUDSJETTREGULERING 2. TERTIAL 2026 — KOMMUNAL BOENHET (KOSTRA 254)
Arkivsak: 26/08940-2 | Utvalg: Formannskapet / Bystyret | Møtedato: 28. september 2026
Saksbehandler: Frank Ellingsen (Senior Controller) | Hjemmel: Kommuneloven § 14-5 & § 14-6

KOMMUNEDIREKTØRENS FORSLAG TIL VEDTAK:
1. Bystyret godkjenner omdisponering av kr 1 850 000 innenfor Helse og mestring til Kommunal Boenhet (KOSTRA 254) for å dekke uforutsette overtidstillegg og ekstern vikarbyråbruk ved døgnturnus.
2. Kommunedirektøren pålegges å iverksette administrativ vikarpool i tråd med drøftinger jf. Hovedtariffavtalen (HTA) § 4.
3. Resterende merforbruk dekkes inn ved overføring fra kommunens disposisjonsfond jf. Kommuneloven § 14-5.

SAKSUTREDNING:
Døgnbemannet drift (24/7) krever uavbrutt forsvarlig bemanning. Helgetillegg og overtid (art 1040/1090) har et merforbruk på kr 1 530 000, forsterket av ubudsjetterte vikarbyråkjøp (art 1270) på kr 382 656. Tiltak T2 og T3 iverksettes for å bremse videre kostnadsvekst i T3.

KRYPTOGRAFISK REVISJONSSTEMPEL:
SHA-256: 4c603149052df6ff0cf597d8f59529c01824ab15d2e09ff7b63f82aa8e6bcf12`,

            "DEFAULT": `ADMINISTRATIVT NOTAT: VIRKSOMHETSSTYRING OG DRIFTSAVVIK PER 2. TERTIAL 2026
Mottaker: Kommunalsjef / Sektorledelse | Fra: Senior Controller Frank Ellingsen
Hjemmel: Delegeringsreglementet § 3 / HTA § 4

SAMMENDRAG AV TILTAK:
- Tiltak T1: Purring av NAV-refusjonskrav iverksatt (estimert kontanteffekt kr 41 324).
- Tiltak T2 & T3: Vikar- og overtidsplanlegging drøftet med tillitsvalgte iht. HTA § 4.
- Tiltak T4: Frys i ikke-kritiske rammeavtaleinnkjøp på art 1200 fram til årsslutt.

Status: Godkjent administrativt innenfor rammen. Forseglet i Audit_AI_Actions.`
        };

        function updateGeneratedNote() {
            const enh = document.getElementById("gen-enhet").value;
            const niv = document.getElementById("gen-niva").value;
            const out = document.getElementById("generated-note-text");

            if (enh === "SKOLE" && niv === "NIVA3") {
                out.innerText = SAKS_TEKSTER["SKOLE_NIVA3"];
            } else if (enh === "BO" && niv === "NIVA3") {
                out.innerText = SAKS_TEKSTER["BO_NIVA3"];
            } else {
                out.innerText = SAKS_TEKSTER["DEFAULT"];
            }
        }

        function copyGeneratedNote() {
            const text = document.getElementById("generated-note-text").innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert("✓ Saksnotat kopiert til utklippstavlen!");
            });
        }

        function filterDocs(cat) {
            const tabs = document.querySelectorAll(".filter-tabs .tab-btn");
            tabs.forEach(t => t.classList.remove("active-tab"));
            event.target.classList.add("active-tab");

            const cards = document.querySelectorAll(".doc-card");
            cards.forEach(c => {
                if (cat === "ALL" || c.getAttribute("data-category") === cat) {
                    c.style.display = "flex";
                } else {
                    c.style.display = "none";
                }
            });
        }

        function switchPbiTab(tabId) {
            const tabs = document.querySelectorAll(".pbi-tabs-bar .pbi-tab");
            tabs.forEach(t => t.classList.remove("active"));
            event.target.classList.add("active");

            document.getElementById("pbi-tab-1").style.display = tabId === "TAB1" ? "block" : "none";
            document.getElementById("pbi-tab-2").style.display = tabId === "TAB2" ? "block" : "none";
            document.getElementById("pbi-tab-3").style.display = tabId === "TAB3" ? "block" : "none";
        }

        function showDaxSnippet(kind) {
            switchPbiTab('TAB3');
            const tabs = document.querySelectorAll(".pbi-tabs-bar .pbi-tab");
            tabs.forEach(t => t.classList.remove("active"));
            tabs[2].classList.add("active");
            document.getElementById("powerbi-showcase").scrollIntoView({ behavior: 'smooth' });
        }

        function copyDaxCode() {
            const code = document.getElementById("dax-display-code").innerText;
            navigator.clipboard.writeText(code).then(() => {
                alert("✓ DAX-kode kopiert til utklippstavlen!");
            });
        }

        function selectFlowStep(stepNum) {
            const cards = document.querySelectorAll(".stepper-grid .step-card");
            cards.forEach((c, idx) => {
                if (idx + 1 === stepNum) {
                    c.classList.add("active-step");
                } else {
                    c.classList.remove("active-step");
                }
            });
        }

        /* Modal Forhåndsvisning */
        const DOC_CONTENT = {
            "SAKSFREMLEGG": {
                title: "MAL: Politisk Saksfremlegg (Kommuneloven § 14-5 & § 14-6)",
                file: "templates/MAL_POLITISK_SAKSFREMLEGG_BUDSJETTENDRING.docx",
                body: `<h3>SAKSFREMLEGG: BUDSJETTENDRING OG OMDISPONERING PER 2. TERTIAL 2026</h3>
<p><strong>Arkivsak:</strong> 26/08940-1 | <strong>Møtedato:</strong> 28. september 2026 | <strong>Utvalg:</strong> Formannskapet / Bystyret<br>
<strong>Saksbehandler:</strong> Frank Ellingsen (Senior Controller) | <strong>Hjemmel:</strong> Kommuneloven § 14-5 og § 14-6</p>
<hr>
<h4>KOMMUNEDIREKTØRENS FORSLAG TIL VEDTAK:</h4>
<ol>
    <li>Bystyret tar orienteringen om forventet årsavvik per 2. tertial 2026 til etterretning.</li>
    <li>Bystyret bevilger en rammejustering på kr 3 200 000 til tjenesteområde Oppvekst / Grunnskole (KOSTRA 202).</li>
    <li>Bystyret godkjenner omdisponering av kr 1 850 000 innenfor Helse og mestring / Bo og Miljø (KOSTRA 254).</li>
    <li>Netto merforbruk dekkes inn ved overføring fra kommunens disposisjonsfond jf. Kommuneloven § 14-5 andre ledd.</li>
</ol>
<h4>1. SAKSUTREDNING</h4>
<p>I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak om endring av årsbudsjettet dersom det under budsjettåret oppstår vesentlige avvik som utfordrer budsjettbalansen. Ved 2. tertial er samlet merforbruk innenfor skole og boenhet beregnet til kr 32 306 000 uten korrigerende tiltak.</p>
<h4>2. BRUTTOPRINSIPPET (§ 14-6)</h4>
<p>I tråd med bruttoprinsippet holdes lønnsutgifter og refusjoner fra NAV fullt ut separate på egne artslinjer. Det foretas ingen ulovlig nettoføring.</p>
<h4>3. REVISJONSBEVIS</h4>
<p><code>SHA-256 SAKSHASH: 7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a</code></p>`
            },
            "AVVIKSNOTAT": {
                title: "MAL: Avviksnotat & Preskriptiv Tiltaksplan (T1–T6)",
                file: "templates/MAL_AVVIKSNOTAT_OG_TILTAKSPLAN_ENHETSLEDER.docx",
                body: `<h3>AVVIKSNOTAT OG PRESKRIPTIV TILTAKSPLAN (ENHETSLEDER)</h3>
<p><strong>Fra:</strong> Enhetsleder / Controller | <strong>Til:</strong> Kommunalsjef | <strong>Periode:</strong> 2. Tertial 2026</p>
<hr>
<h4>1. AVVIKSBILDE</h4>
<p>Avviket hittil i år er dekomponert på faste lønninger (art 1010), vikarer ved sykdom (art 1020/1050), overtid ved turnusdekning (art 1040/1090) og forsinkede refusjoner fra NAV (art 1690).</p>
<h4>2. PRIORITERT TILTAKSMENY</h4>
<ul>
    <li><strong>T1: Purring NAV-refusjoner:</strong> Effekt kr 41 324 (85 % sannsynlighet) — Fagkontroll</li>
    <li><strong>T2: Redusere vikarbyrå via vikarpool:</strong> Effekt kr 28 872 (70 % sannsynlighet) — HTA § 4</li>
    <li><strong>T3: Overtidsplanlegging:</strong> Effekt kr 55 077 (75 % sannsynlighet) — HTA § 4</li>
    <li><strong>T4: Stopp i ikke-kritiske kjøp:</strong> Effekt kr 9 520 (90 % sannsynlighet) — Fagkontroll</li>
</ul>
<p>Signert enhetsleder og controller. Forseglet i Stage-Gate Port 9.</p>`
            },
            "HTA_PROTOKOLL": {
                title: "MAL: HTA § 4 Drøftingsprotokoll (Partssamarbeid)",
                file: "templates/MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL.docx",
                body: `<h3>DRØFTINGSPROTOKOLL — HOVEDTARIFFVTALEN (HTA) § 4</h3>
<p><strong>Møtested:</strong> Kristiansand rådhus / Digitalt | <strong>Hjemmel:</strong> HTA § 4, Hovedavtalen del B § 3 & AML kap. 10</p>
<hr>
<h4>1. DELTAKERE</h4>
<p>Arbeidsgiver: Enhetsleder, HR-rådgiver, Økonomirådgiver.<br>
Tillitsvalgte: Fagforbundet, Delta, Norsk Sykepleierforbund, Utdanningsforbundet.</p>
<h4>2. ARBEIDSGIVERS REDEGJØRELSE</h4>
<p>Orientering om økonomisk situasjon og forslag til tiltak for å dempe overtids- og vikarkostnader uten å svekke pasientsikkerhet eller elevrettigheter.</p>
<h4>3. TILLITSVALGTES MERKNADER</h4>
<p>Partene er enige om at arbeidsmiljølovens hviletidsbestemmelser skal overholdes ubetinget. Bruk av intern vikarpool støttes under forutsetning av tilstrekkelig opplæring.</p>`
            },
            "PORT9_SIGNOFF": {
                title: "MAL: Stage-Gate Port 9 HITL Sign-off Protokoll",
                file: "templates/MAL_STAGE_GATE_PORT_9_HITL_SIGNOFF.docx",
                body: `<h3>STAGE-GATE PORT 9: HUMAN-IN-THE-LOOP SIGNOFF</h3>
<p><strong>Hjemmel:</strong> EU AI Act Art. 14 (Human Oversight) & GDPR Art. 22 (Forbud mot helautomatisering)</p>
<hr>
<p>Saksreferanse: <code>ANOM-2026-T2-0894</code><br>
Saksbehandler: Frank Ellingsen (Senior Controller)<br>
Beslutning: <strong>APPROVED (Godkjent)</strong><br>
Kontroll dokumentert: <strong>JA</strong><br>
Faglig begrunnelse: Reelt merforbruk bekreftet i Visma ERP. Foreslåtte tiltak T1–T4 iverksettes innenfor delegert ramme.<br>
Kryptografisk Hash: <code>SHA-256: 7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a</code></p>`
            },
            "FRIA_DPIA": {
                title: "MAL: Stage-Gate Port 7 FRIA & DPIA Risikovurdering",
                file: "templates/MAL_FRIA_OG_DPIA_RISIKOVURDERING.docx",
                body: `<h3>STAGE-GATE PORT 7: FRIA & DPIA KONSEKVENSVURDERING</h3>
<p><strong>Hjemmel:</strong> EU AI Act Art. 27 (FRIA) & GDPR Art. 35 (DPIA)</p>
<hr>
<p>1. Dataminimering: All regnskaps- og lønnsdata er aggregert på KOSTRA-art; 0 personopplysninger behandles.<br>
2. PII-filter i Port 4: Automatisk regex/NER-vask fjerner personidentifikatorer i bilagstekst.<br>
3. Anti-bias & rettferdighet: Objektiv Z-score screening hindrer usaklig forskjellsbehandling mellom enheter.<br>
4. DPO-godkjenning: Restrisiko vurdert som LAV. Status: <strong>GODKJENT</strong>.</p>`
            },
            "LUKKING_INSTRUK": {
                title: "MAL: Kontrollinstruks for Periodelukking",
                file: "templates/MAL_PERIODELUKKING_OG_AVSTEMMING.docx",
                body: `<h3>KONTROLLINSTRUKS FOR PERIODELUKKING OG AVSTEMMING</h3>
<p><strong>Målgruppe:</strong> Controllere og regnskapsavdeling | <strong>Hjemmel:</strong> Kommuneloven kap. 14 & GKRS</p>
<hr>
<h4>MÅNEDSLUKKING:</h4>
<ul>
    <li>Dag 1–3: Bankavstemminger fullført på alle driftskontoer.</li>
    <li>Dag 3–4: A-melding avstemt mot lønnsarter og kvittering fra Skatteetaten.</li>
    <li>Dag 5: Leverandørreskontro avstemt og godkjent.</li>
</ul>
<h4>TERTIALAVSLUTNING:</h4>
<ul>
    <li>Avstemming mellom Visma ERP og Framsikt rammer.</li>
    <li>Verifisering av NAV sykepengerefusjoner (art 1690).</li>
    <li>Beregning av rullende EOY-prognose i Power BI.</li>
</ul>`
            },
            "EXCEL_INFO": {
                title: "Om Excel-modellen: Saksbehandling & Tiltak 2026",
                file: "reports/Mal_Saksbehandling_Tiltak_Avstemming_2026.xlsx",
                body: `<h3>EXCEL MODELL: SAKSBEHANDLING & TILTAKSAVSTEMMING 2026</h3>
<p>Arbeidsboken er designet etter Edward Tuftes Data-Ink Ratio prinsipper og inneholder:</p>
<ul>
    <li><strong>Fane 1: Avviksanalyse_KOSTRA:</strong> Budsjett vs. regnskap per KOSTRA-art med automatiske formler for avvik i kr og %.</li>
    <li><strong>Fane 2: Preskriptiv_Tiltaksplan:</strong> Tiltak T1–T6 med tvingende HITL-formel: <code>=IF(AND(I6="Godkjent", J6="Ja"), G6, 0)</code>.</li>
    <li><strong>Fane 3: HITL_Signoff_Protokoll:</strong> Forvaltningsskjema med saksreferanse, begrunnelse og SHA-256 hash.</li>
</ul>`
            },
            "MASTER_INFO": {
                title: "Om Excel Mastermodellen: Project Controller Reporting 2026",
                file: "reports/Kommune_Project_Controller_Reporting_2026.xlsx",
                body: `<h3>EXCEL MASTERMODELL: PROJECT CONTROLLER REPORTING 2026</h3>
<p>Konsolidert masterarbeidsbok for Kristiansand kommune med 6 faner:</p>
<ul>
    <li><strong>1. Executive_Dashboard:</strong> Nøkkeltall, KPI-kort, sektorfordeling og avviksmålere.</li>
    <li><strong>2. Tertialrapport_T2:</strong> Detaljert avvikstabell for topp 25 kritiske KOSTRA-arter.</li>
    <li><strong>3. Prosjektkontroll_EVM:</strong> Earned Value Management for skole, boenhet og VA-anlegg (BAC, PV, AC, EV, CPI, SPI, EAC).</li>
    <li><strong>4. Styringskalender_Arshjul:</strong> Kritiske frister og milepæler for 2026 synkronisert med Plandisc.</li>
    <li><strong>5. Revisjon_Og_Checklist:</strong> Månedsavslutning, tertiallukking og AI-revisjon (CHK-01 til CHK-14).</li>
    <li><strong>6. KOSTRA_Kontoplan_Mapping:</strong> SSBs nasjonale kontoplan for kommuner.</li>
</ul>`
            },
            "REVISJON_SJEKK": {
                title: "Kommunerevisjonens Sjekkliste for AI-systemer",
                file: "revisjon-og-kontroll/KOMMUNEREVISJONEN_AUDIT_CHECKLIST.md",
                body: `<h3>SJEKKLISTE FOR KOMMUNEREVISJONEN OG KONTROLLUTVALGET</h3>
<p><strong>Dokument-ID:</strong> REV-AI-2026-v1 | <strong>Hjemmel:</strong> Kommuneloven kap. 24 & EU AI Act</p>
<hr>
<h4>KONTROLLOMRÅDER:</h4>
<ol>
    <li><strong>Kryptografisk Audit Trail:</strong> Verifisering av SHA-256 integritet i <code>Audit_AI_Actions</code>.</li>
    <li><strong>Human-in-the-Loop (HITL):</strong> Bekreftelse på 0 autonome vedtak og undersøkelse av automation bias.</li>
    <li><strong>PII-Skjerming (Port 4):</strong> 100 % vasking av fødselsnumre og personopplysninger.</li>
    <li><strong>Glass-Box RAG (Port 8):</strong> 100 % paragrafsitering mot Kommuneloven og forskrifter.</li>
    <li><strong>Offentlig Algoritmeregister (Port 10):</strong> Innsyn jf. Eurocities standard.</li>
</ol>`
            }
        };

        function previewDocument(docKey) {
            const data = DOC_CONTENT[docKey] || DOC_CONTENT["SAKSFREMLEGG"];
            document.getElementById("modal-doc-title").innerText = data.title;
            document.getElementById("modal-doc-body").innerHTML = data.body;
            document.getElementById("modal-download-link").setAttribute("href", data.file);
            document.getElementById("doc-modal").style.display = "flex";
        }

        function closeModal() {
            document.getElementById("doc-modal").style.display = "none";
        }

        function closeModalOnBackdrop(e) {
            if (e.target.id === "doc-modal") {
                closeModal();
            }
        }

        function copyModalContent() {
            const bodyText = document.getElementById("modal-doc-body").innerText;
            navigator.clipboard.writeText(bodyText).then(() => {
                alert("✓ Dokumenttekst kopiert til utklippstavlen!");
            });
        }

        // Kjør oppdatering ved innlasting
        document.addEventListener("DOMContentLoaded", () => {
            updateGeneratedNote();
        });
    """

    # Erstatt slutt av script
    raw_html = raw_html.replace("    </script>", new_js + "\n    </script>")

    INDEX_PATH.write_text(raw_html, encoding="utf-8")
    print(f"✓ index.html er vellykket oppdatert og utvidet! ({len(raw_html)} tegn)")


if __name__ == "__main__":
    build_new_html()
