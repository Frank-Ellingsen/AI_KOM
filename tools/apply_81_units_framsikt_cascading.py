# -*- coding: utf-8 -*-
"""
tools/apply_81_units_framsikt_cascading.py
Complete 81 units catalog and Framsikt cascading logic.
"""
import sys
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# -----------------------------------------------------------------------------
# 1. CSS INJECTION FOR GLOBAL UNIT BAR
# -----------------------------------------------------------------------------
css_needle = ".global-sector-bar {"
new_css = """
        .global-unit-bar {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            padding: 8px 12px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            margin-top: 4px;
        }
        .global-unit-label-group {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 11.5px;
            color: var(--navy-dark);
            font-weight: 700;
            white-space: nowrap;
        }
        .global-unit-dropdown {
            padding: 5px 10px;
            font-size: 11.5px;
            font-family: var(--font-sans);
            font-weight: 600;
            color: var(--navy-dark);
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 3px;
            cursor: pointer;
            min-width: 320px;
            max-width: 480px;
            outline: none;
            transition: border-color 0.15s ease;
        }
        .global-unit-dropdown:focus {
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.15);
        }
        .global-unit-meta-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            flex-wrap: wrap;
        }
        .cascade-tag {
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 3px;
            background: #eff6ff;
            color: #0369a1;
            border: 1px solid #bae6fd;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .cascade-tag.active-unit {
            background: #fef2f2;
            color: #b91c1c;
            border-color: #fecaca;
        }
"""

if ".global-unit-bar {" not in content:
    idx_css = content.find(css_needle)
    if idx_css != -1:
        content = content[:idx_css] + new_css + "\n        " + content[idx_css:]
        print("✓ Injected .global-unit-bar CSS.")
else:
    print("Notice: .global-unit-bar CSS already present.")

# -----------------------------------------------------------------------------
# 2. HTML INJECTION FOR GLOBAL UNIT BAR IN #global-sector-selector-bar
# -----------------------------------------------------------------------------
unit_bar_html = """
        <!-- Enhetsvelger (81 resultatenheter med kaskadert Framsikt-innsyn) -->
        <div class="global-unit-bar" id="global-unit-bar">
            <div class="global-unit-label-group">
                <span>🏢</span>
                <span>Velg Enhet (81 resultatenheter):</span>
            </div>
            <div style="flex:1; min-width:280px; max-width:500px;">
                <select id="global-unit-dropdown" class="global-unit-dropdown" onchange="selectUnit(this.value)" title="Velg enhet for å se kun ditt budsjettnivå og kaskadert nedover">
                    <!-- Fylles dynamisk av populateGlobalUnitDropdown() -->
                </select>
            </div>
            <div class="global-unit-meta-pill" id="global-unit-meta-pill">
                <span class="framsikt-level-badge lvl-1" id="global-unit-lvl-badge">Nivå 1: Konsern</span>
                <span id="global-unit-leader-text" style="font-weight:600; color:var(--navy-dark);">Camilla Dunsæd (Kommunedirektør)</span>
                <span id="global-unit-cascade-notice" class="cascade-tag">🔓 Konserninnsyn (Alle 81 enheter)</span>
                <button type="button" id="global-unit-reset-btn" class="btn btn-sm" onclick="resetUnitToSector()" style="display:none; font-size:10px; padding:2px 8px; margin-left:4px; background:#ffffff; border:1px solid #cbd5e1; font-weight:700;">
                    ↺ Vis hele området
                </button>
            </div>
        </div>
"""

notice_needle = '<div class="global-sector-notice" id="global-sector-active-notice">'
if 'id="global-unit-bar"' not in content:
    idx_notice = content.find(notice_needle)
    if idx_notice != -1:
        content = content[:idx_notice] + unit_bar_html + "\n        " + content[idx_notice:]
        print("✓ Injected #global-unit-bar HTML.")
    else:
        print("Error: Could not find notice needle in index.html.")
else:
    print("Notice: #global-unit-bar HTML already present.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML and CSS updated.")
