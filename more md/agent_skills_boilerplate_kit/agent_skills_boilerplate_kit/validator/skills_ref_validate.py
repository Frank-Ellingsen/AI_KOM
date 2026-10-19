#!/usr/bin/env python3
import sys
import os
import re

def validate_skill(skill_dir: str):
    print("=" * 65)
    print(f"📊 SKILL VALIDATION REPORT: {os.path.basename(skill_dir)}")
    print("=" * 65)
    
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        print("❌ CRITICAL ERROR: Missing SKILL.md file!")
        return False

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)
    est_tokens = len(content) // 4

    passed = True
    warnings = []

    if line_count > 500:
        passed = False
        print(f"❌ SIZE EXCEEDED: SKILL.md is {line_count} lines (limit: 500 lines / ~5000 tokens).")
    else:
        print(f"✅ SIZE OK: SKILL.md is {line_count} lines (~{est_tokens} tokens).")

    if not content.startswith("---"):
        warnings.append("Missing YAML frontmatter header ('---').")
    else:
        if "name:" not in content or "description:" not in content:
            warnings.append("YAML frontmatter should contain 'name:' and 'description:'.")

    scripts_dir = os.path.join(skill_dir, "scripts")
    has_scripts = os.path.exists(scripts_dir) and len(os.listdir(scripts_dir)) > 0
    if has_scripts:
        print(f"ℹ️ FOUND SCRIPTS: Executable scripts present in scripts/ (0 context tokens).")

    if warnings:
        print("\n⚠️ WARNINGS:")
        for w in warnings:
            print(f"  • {w}")

    print("\nSTATUS: " + ("✅ PASSED" if passed else "❌ FAILED"))
    print("=" * 65)
    return passed

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    validate_skill(target)
