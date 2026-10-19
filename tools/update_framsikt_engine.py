# -*- coding: utf-8 -*-
"""
tools/update_framsikt_engine.py
Polishes Framsikt engine, ensures 4 levels across all 6 sectors, isolates comparison table,
and connects meeting pack sync.
"""
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update filterSectorComparisonTable to strictly show ONLY the target sector row when not ALL
old_comp = """        } else {
            const targetId = `row-sec-${sectorKey.toLowerCase()}`;
            if (r.id === targetId || r.id === "row-sec-all") {
                r.style.display = "";
                if (r.id === targetId) {
                    r.style.background = "#e0f2fe";
                } else {
                    r.style.background = "#f8fafc";
                }
            } else {
                r.style.display = "none";
            }
        }"""

new_comp = """        } else {
            const targetId = `row-sec-${sectorKey.toLowerCase()}`;
            if (r.id === targetId) {
                r.style.display = "";
                r.style.background = "#e0f2fe";
            } else {
                r.style.display = "none";
            }
        }"""

if old_comp in content:
    content = content.replace(old_comp, new_comp, 1)
    print("✓ Updated filterSectorComparisonTable for strict single-sector isolation.")
else:
    print("Notice: filterSectorComparisonTable already updated or pattern differed.")

# 2. Update renderMeetingPack fallback so MEETING_PACKS["ALL"] never crashes
old_mp = 'const secPacks = MEETING_PACKS[secKey] || MEETING_PACKS["ALL"];'
new_mp = 'const secPacks = MEETING_PACKS[secKey] || MEETING_PACKS["ALL"] || MEETING_PACKS["OPPVEKST"];'
if old_mp in content:
    content = content.replace(old_mp, new_mp, 1)
    print("✓ Updated renderMeetingPack fallback.")

# 3. Cut out current FRAMSIKT_ENGINE_JS and replace with full version
start_marker = "// ==============================================================================\n// 🏛️ FRAMSIKT BUDSJETTNIVÅ-HIERARKI & DYNAMISK ISOLERINGSMOTOR"
end_marker = "function initTop3KpiDashboard()"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + content[idx_end:]
    print("✓ Removed previous engine block for replacement.")

with open('tools/full_framsikt_engine.js', 'r', encoding='utf-8') as f_js:
    engine_js = f_js.read()

insert_pos = content.find("function initTop3KpiDashboard()")
if insert_pos != -1:
    content = content[:insert_pos] + engine_js + "\n\n" + content[insert_pos:]
    print("✓ Inserted updated full Framsikt engine before initTop3KpiDashboard.")
else:
    print("Error: Could not find insert position.")
    sys.exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Saved updated index.html successfully.")
