#!/usr/bin/env python3
"""
Skill Validator Script (validate_skill.py)
------------------------------------------
Validates an Agent Skill directory against the open agentskills.io specification:
1. Verifies SKILL.md existence and YAML frontmatter structure.
2. Checks description field length and progressive discovery metadata.
3. Enforces SKILL.md line limit (< 500 lines) to prevent context window bloat.
4. Validates optional subdirectories (scripts/, references/, assets/).
"""

import os
import sys
import re
import yaml
from pathlib import Path

# Force UTF-8 encoding on Windows to prevent UnicodeEncodeError on standard console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def validate_skill(target_path: str) -> bool:
    path = Path(target_path)

    if path.is_file():
        skill_file = path
        skill_dir = path.parent
    else:
        skill_dir = path
        skill_file = skill_dir / "SKILL.md"

    print(f"=== Validating Agent Skill at: {skill_file.resolve()} ===\n")

    if not skill_file.exists():
        print(f"❌ ERROR: Missing target 'SKILL.md' file at {skill_file}")
        return False

    if skill_file.name != "SKILL.md":
        print(f"⚠️ WARNING: Skill file is named '{skill_file.name}'. The canonical standard requires 'SKILL.md'.")

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    print(f"✓ Found skill file ({len(lines)} lines)")

    # 1. Enforce line count limit (< 500 lines)
    if len(lines) > 500:
        print(f"⚠️ WARNING: Skill file exceeds 500 lines ({len(lines)} lines). Offload detailed docs to references/")
    else:
        print("✓ Line count constraint passed (< 500 lines)")

    # 2. Extract and parse YAML frontmatter
    frontmatter_match = re.match(r"^---\s*[\r\n]+(.*?)\n---\s*[\r\n]+", content, re.DOTALL)
    if not frontmatter_match:
        print("❌ ERROR: Missing or malformed YAML frontmatter enclosed in '---'")
        return False

    try:
        metadata = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Failed to parse YAML frontmatter: {e}")
        return False

    if not isinstance(metadata, dict):
        print("❌ ERROR: YAML frontmatter must parse into a key-value dictionary.")
        return False

    # 3. Validate mandatory frontmatter fields
    required_fields = ["name", "description"]
    missing = [field for field in required_fields if field not in metadata or not metadata[field]]
    if missing:
        print(f"❌ ERROR: Missing required YAML frontmatter fields: {missing}")
        return False

    skill_name = str(metadata["name"])
    description = str(metadata["description"])

    # Slugified name check
    if not re.match(r"^[a-z0-9\-_]+$", skill_name):
        print(f"⚠️ WARNING: Skill name '{skill_name}' should be lowercase slugified (e.g. 'code-reviewer-secops')")
    else:
        print(f"✓ Valid skill name format: '{skill_name}'")

    # Folder-name matching check
    if skill_file.name == "SKILL.md" and skill_dir.name != skill_name:
        print(f"ℹ️ Note: Parent directory '{skill_dir.name}' differs from skill name '{skill_name}'. Recommended to match.")

    # Description quality check for Progressive Discovery
    if len(description) < 30:
        print(f"⚠️ WARNING: Description too short ({len(description)} chars). Ensure it describes WHAT it does and WHEN to trigger.")
    else:
        print(f"✓ Progressive Discovery Description validated ({len(description)} chars)")

    # 4. Allowed tools validation
    allowed_tools = metadata.get("allowed-tools", [])
    if allowed_tools:
        if isinstance(allowed_tools, list):
            print(f"✓ Scoped tool permissions defined: {allowed_tools}")
        else:
            print(f"⚠️ WARNING: 'allowed-tools' should be a YAML list, got {type(allowed_tools).__name__}")
    else:
        print("ℹ️ Note: No 'allowed-tools' defined. Skill operates with default harness tool permissions.")

    # 5. Validate optional subdirectories (scripts/, references/, assets/)
    subdirs = ["scripts", "references", "assets"]
    found_subdirs = []
    for sub in subdirs:
        sub_path = skill_dir / sub
        if sub_path.is_dir():
            file_count = len(list(sub_path.glob("*")))
            found_subdirs.append(f"{sub}/ ({file_count} items)")
    if found_subdirs:
        print(f"✓ Detected auxiliary subdirectories: {', '.join(found_subdirs)}")
    else:
        print("ℹ️ Note: No auxiliary subdirectories found (scripts/, references/, assets/).")

    print("\n✅ Skill Validation Passed Successfully!")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Default to local code-reviewer-skill.md or SKILL.md in current dir
        if Path("code-reviewer-skill.md").exists():
            target = "code-reviewer-skill.md"
        elif Path(".agents/skills/code-reviewer-secops/SKILL.md").exists():
            target = ".agents/skills/code-reviewer-secops/SKILL.md"
        else:
            target = "SKILL.md"

    success = validate_skill(target)
    sys.exit(0 if success else 1)
