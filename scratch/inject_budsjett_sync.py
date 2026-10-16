# tools/inject_budsjett_sync.py
# -*- coding: utf-8 -*-
import sys

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    content = f.read()

OLD_SYNC = """// 8. Register over Budsjettansvarlige
    if (typeof updateBudgetHoldersForSector === 'function') {
        updateBudgetHoldersForSector(sectorKey);
    }
    }"""

NEW_SYNC = """// 8. Register over Budsjettansvarlige
    if (typeof updateBudgetHoldersForSector === 'function') {
        updateBudgetHoldersForSector(sectorKey);
    }

    // 9. Budsjettmodul (Framsikt)
    if (typeof updateBudsjettModulForSector === 'function') {
        updateBudsjettModulForSector(sectorKey);
    }
}

function updateBudsjettModulForSector(sectorKey) {
    if (sectorKey === "ALL") return;
    const secSelect = document.getElementById("bm-calc-sector");
    if (!secSelect) return;

    if (sectorKey === "OPPVEKST" || sectorKey === "HELSE" || sectorKey === "BYUTVIKLING" || 
        sectorKey === "KULTUR" || sectorKey === "ORG_TEK" || sectorKey === "OKONOMI") {
        secSelect.value = sectorKey;
        onBmSectorChange();

        if (sectorKey === "BYUTVIKLING") {
            switchSelvkostService("VANN");
        }
    }
}"""

if "updateBudsjettModulForSector(sectorKey)" not in content:
    if OLD_SYNC in content:
        content = content.replace(OLD_SYNC, NEW_SYNC, 1)
        print("Inserted updateBudsjettModulForSector into syncAllSectionsForSector")
    else:
        print("Warning: OLD_SYNC not found")
else:
    print("Already hooked.")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("Sync update done.")
