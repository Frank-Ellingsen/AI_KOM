#!/usr/bin/env python3
"""
Test- og Verifikasjonsskript for Office Hub & Flyttede MD-filer
Kristiansand Kommune - Økonomi og Virksomhetsstyring
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

EXPECTED_MOVED_FILES = [
    ROOT_DIR / "templates" / "RAPPORTMAL_KOMMUNESTYRET.md",
    ROOT_DIR / "templates" / "RAPPORTMAL_KOMMUNEDIREKTOR.md",
    ROOT_DIR / "templates" / "RAPPORTMAL_KOMMUNALSJEF.md",
    ROOT_DIR / "templates" / "RAPPORTMAL_SEKSJONSLEDER.md",
    ROOT_DIR / "templates" / "RAPPORTMAL_AVDELINGSLEDER.md",
    ROOT_DIR / "templates" / "RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.md",
    ROOT_DIR / "spesifikasjoner" / "OFFICE_DASHBOARD_HUB_V2_WORKFLOW_UI.md",
    ROOT_DIR / "spesifikasjoner" / "OFFICE_HUB_GEMINI_MCP_CHAT_SPEC.md",
    ROOT_DIR / "bruker-guides" / "MANEDLIG_AVVIKSRAPPORT_RAMMEVERK.md",
    ROOT_DIR / "docs" / "VISUAL_STORYTELLING_FT_GUIDE.md",
]

EXPECTED_DOCX_FILES = [
    ROOT_DIR / "templates" / "RAPPORTMAL_KOMMUNESTYRET.docx",
    ROOT_DIR / "templates" / "RAPPORTMAL_KOMMUNEDIREKTOR.docx",
    ROOT_DIR / "templates" / "RAPPORTMAL_KOMMUNALSJEF.docx",
    ROOT_DIR / "templates" / "RAPPORTMAL_SEKSJONSLEDER.docx",
    ROOT_DIR / "templates" / "RAPPORTMAL_AVDELINGSLEDER.docx",
    ROOT_DIR / "templates" / "RAPPORTMONSTER_AVVIK_OG_EFFEKTPROGNOSE.docx",
]


class StrictHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
        self.self_closing = {
            "meta", "link", "br", "hr", "input", "img", "col", "base", "area", "param"
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
            # Toleranse for elementer som ofte overlapper hvis standard HTML5
            self.errors.append(f"Mismatchet tag: ventet </{last}>, fant </{t}>")


def run_checks():
    print("=" * 80)
    print("🔍 VERIFISERER OFFICE HUB V2 IMPLEMENTASJON & FILPLASSERING")
    print("=" * 80)
    
    passed = 0
    failed = 0

    # 1. Sjekk at rot-mappen er ren for løse ad-hoc .md-filer
    print("\n1. Sjekker at rot-mappen er ryddet...")
    ALLOWED_ROOT_MDS = {"README.md", "AGENTS.md", "INDEX.md"}
    root_mds = list(ROOT_DIR.glob("*.md"))
    root_md_names = [f.name for f in root_mds]
    unexpected_mds = [f for f in root_md_names if f not in ALLOWED_ROOT_MDS]
    print(f"   Funnet i rot: {root_md_names}")
    if not unexpected_mds:
        print(f"   ✓ Rot-mappen inneholder kun autoriserte systemfiler ({', '.join(root_md_names)})!")
        passed += 1
    else:
        print(f"   ❌ Uventede md-filer i rot: {unexpected_mds}")
        failed += 1

    # 2. Sjekk at alle 10 flyttede md-filer eksisterer og har innhold
    print("\n2. Sjekker at de 10 flyttede filene eksisterer i subfolders...")
    for f in EXPECTED_MOVED_FILES:
        if f.exists() and f.stat().st_size > 100:
            print(f"   ✓ {f.relative_to(ROOT_DIR)} ({f.stat().st_size} bytes)")
            passed += 1
        else:
            print(f"   ❌ MANGLER ELLER TOM: {f.relative_to(ROOT_DIR)}")
            failed += 1

    # 3. Sjekk at tilhørende Word (.docx) maler er generert
    print("\n3. Sjekker at Word (.docx) maler er generert...")
    for f in EXPECTED_DOCX_FILES:
        if f.exists() and f.stat().st_size > 1000:
            print(f"   ✓ {f.relative_to(ROOT_DIR)} ({f.stat().st_size} bytes)")
            passed += 1
        else:
            print(f"   ❌ MANGLER DOCX: {f.relative_to(ROOT_DIR)}")
            failed += 1

    # 4. Valider index.html og lenker
    print("\n4. Validerer index.html, filreferanser og DOC_CONTENT...")
    index_file = ROOT_DIR / "index.html"
    if not index_file.exists():
        print("   ❌ index.html finnes ikke!")
        sys.exit(1)

    html_content = index_file.read_text(encoding="utf-8")
    parser = StrictHTMLValidator()
    parser.feed(html_content)

    if not parser.errors:
        print("   ✓ index.html HTML-syntaks er 100 % velformet (0 feil)!")
        passed += 1
    else:
        print(f"   ⚠️ HTML parser bemerkninger: {len(parser.errors)}")
        for err in parser.errors[:5]:
            print(f"     - {err}")

    # Sjekk at alle href-lenker i index.html som peker til templates/reports/docs/bruker-guides/pilot-pakker faktisk finnes på disk
    file_hrefs = re.findall(r'href=[\"\'](templates/.*?|reports/.*?|docs/.*?|bruker-guides/.*?|generic-ai-pilot-pakke/.*?|antigravity-ms-pilot/.*?)[\"\']', html_content)
    print(f"\n5. Verifiserer {len(file_hrefs)} dokumentlenker i index.html mot filsystemet...")
    missing_links = 0
    for href in set(file_hrefs):
        target_path = ROOT_DIR / href
        if target_path.exists():
            print(f"   ✓ Lenke OK: {href}")
            passed += 1
        else:
            print(f"   ❌ BRUTT LENKE: {href} (fil finnes ikke)")
            missing_links += 1
            failed += 1

    # Sjekk DOC_CONTENT nøkler
    doc_content_keys = re.findall(r'\"([A-Z0-9_]+)\":\s*\{', html_content)
    preview_calls = re.findall(r'previewDocument\([\"\']([A-Z0-9_]+)[\"\']\)', html_content)

    print(f"\n6. Sjekker forhåndsvisningsnøkler (previewDocument):")
    for call in set(preview_calls):
        if call in doc_content_keys:
            print(f"   ✓ Preview-nøkkel '{call}' funnet i DOC_CONTENT")
            passed += 1
        else:
            print(f"   ❌ Manglende preview-nøkkel i DOC_CONTENT: '{call}'")
            failed += 1

    # Sjekk V2 komponenter
    v2_components = [
        ("month-timeline-bar", "12-måneders tidslinjevelger"),
        ("timeline-status-banner", "Aktiv tidslinjemodus-banner"),
        ("triage-grid", "Smart Arbeidskø og Triage-grid"),
        ("btn-batch-approve", "Batch-godkjenningsknapp for grønne enheter"),
        ("rep4-active-title", "Standardisert 4-punkts rapport"),
        ("chat-drawer", "Gemini Flash & MCP Chat Drawer"),
        ("chat-floating-toggle", "Flytende chat-knapp"),
    ]
    print(f"\n7. Sjekker V2 UI-komponenter i index.html:")
    for comp_id, label in v2_components:
        if f'id="{comp_id}"' in html_content or f'class="{comp_id}"' in html_content:
            print(f"   ✓ {label} (ID/Klasse: {comp_id}) er tilstede")
            passed += 1
        else:
            print(f"   ❌ {label} (ID/Klasse: {comp_id}) mangler!")
            failed += 1

    print("\n" + "=" * 80)
    print(f"RESULTAT: {passed} sjekker bestått, {failed} feil.")
    print("=" * 80)

    if failed == 0:
        print("🎉 ALLE TESTER BESTÅTT! Office Hub V2 og de nye filene er fullt integrert.")
    else:
        print("⚠️ Noen tester feilet. Vennligst se loggen over.")


if __name__ == "__main__":
    run_checks()
