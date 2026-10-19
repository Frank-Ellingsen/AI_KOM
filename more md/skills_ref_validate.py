#!/usr/bin/env python3
"""
CLI Tool: skills-ref validate
Validates Agent Skill packages against token budget rules, structural specifications,
and frontmatter metadata standards.
"""

import sys
import os
import re
import argparse

def estimate_tokens(text: str) -> int:
    """Rough estimation of token count (~4 chars per token for standard English/code)."""
    return len(text) // 4

def validate_skill_dir(skill_path: str) -> dict:
    results = {
        "path": skill_path,
        "valid": True,
        "errors": [],
        "warnings": [],
        "info": []
    }
    
    if not os.path.isdir(skill_path):
        results["valid"] = False
        results["errors"].append(f"Directory not found: {skill_path}")
        return results
    
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        results["valid"] = False
        results["errors"].append("Missing required 'SKILL.md' file.")
        return results
    
    # Read SKILL.md
    with open(skill_md_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        lines = content.splitlines()
    
    # 1. Frontmatter check
    if not content.startswith("---"):
        results["warnings"].append("SKILL.md does not start with YAML frontmatter ('---').")
    else:
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            results["errors"].append("Malformed YAML frontmatter in SKILL.md.")
            results["valid"] = False
        else:
            fm_text = frontmatter_match.group(1)
            if "name:" not in fm_text:
                results["errors"].append("Missing 'name:' key in YAML frontmatter.")
                results["valid"] = False
            if "description:" not in fm_text:
                results["warnings"].append("Missing 'description:' key in YAML frontmatter.")

    # 2. Token & Line Budget Check
    line_count = len(lines)
    token_est = estimate_tokens(content)
    
    results["info"].append(f"SKILL.md Size: {line_count} lines (~{token_est} tokens)")
    
    if line_count > 500:
        results["warnings"].append(
            f"SKILL.md exceeds recommended 500 lines limit ({line_count} lines). "
            "Consider moving detailed reference tables to 'references/' to optimize L1 context window."
        )
    if token_est > 5000:
        results["warnings"].append(
            f"SKILL.md token footprint is high (~{token_est} tokens). "
            "Level 2 instructions should ideally remain under 5000 tokens."
        )

    # 3. Mappestruktur (Standard layout)
    allowed_subdirs = {"scripts", "references", "assets", "__pycache__"}
    actual_items = os.listdir(skill_path)
    
    for item in actual_items:
        full_item = os.path.join(skill_path, item)
        if os.path.isdir(full_item):
            if item not in allowed_subdirs:
                results["warnings"].append(f"Non-standard subfolder '{item}'. Standard subfolders: scripts/, references/, assets/.")
        else:
            if item != "SKILL.md" and not item.startswith("."):
                results["warnings"].append(f"Unexpected file '{item}' in skill root. Consider placing scripts in scripts/ or docs in references/.")

    # 4. Check scripts folder if exists
    scripts_dir = os.path.join(skill_path, "scripts")
    if os.path.exists(scripts_dir) and os.path.isdir(scripts_dir):
        script_files = os.listdir(scripts_dir)
        results["info"].append(f"Found {len(script_files)} executable script(s) in scripts/")
        for s in script_files:
            s_path = os.path.join(scripts_dir, s)
            if os.path.isfile(s_path):
                # Check line counts of scripts
                with open(s_path, 'r', encoding='utf-8', errors='ignore') as sf:
                    s_lines = len(sf.readlines())
                    if s_lines > 1000:
                        results["warnings"].append(f"Script '{s}' is very large ({s_lines} lines). Consider modularizing.")

    return results

def print_report(res: dict):
    print("=" * 65)
    print(f"📊 SKILL VALIDATION REPORT: {os.path.basename(os.path.abspath(res['path']))}")
    print("=" * 65)
    
    status = "✅ PASSED" if res["valid"] and not res["warnings"] else ("⚠️ PASSED WITH WARNINGS" if res["valid"] else "❌ FAILED")
    print(f"Status: {status}\n")
    
    if res["info"]:
        print("ℹ️ INFORMATION:")
        for info in res["info"]:
            print(f"  • {info}")
        print()
        
    if res["warnings"]:
        print("⚠️ WARNINGS (Optimization Opportunities):")
        for w in res["warnings"]:
            print(f"  • {w}")
        print()
        
    if res["errors"]:
        print("❌ CRITICAL ERRORS:")
        for err in res["errors"]:
            print(f"  • {err}")
        print()
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Validate Agent Skill packages for structure and token optimization.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Path to the skill directory to validate.")
    args = parser.parse_args()
    
    results = validate_skill_dir(args.skill_dir)
    print_report(results)
    
    if not results["valid"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
