# tools/deduplicate_markdown.py
# -*- coding: utf-8 -*-
"""
Dedupliserings- og kontekstoptimaliseringsskript for markdown-filer i AI_KOM.
Flytter overflødige/dupliserte mapper til archive/ og sikrer én kanonisk kilde for sannhet.
"""

import os
import shutil

ARCHIVE_DIR = "archive"
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 1. Flytt kommune_ai_agent_skills til archive/legacy_skills_export
if os.path.exists("kommune_ai_agent_skills"):
    target = os.path.join(ARCHIVE_DIR, "legacy_skills_export")
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.move("kommune_ai_agent_skills", target)
    print("Archived kommune_ai_agent_skills -> archive/legacy_skills_export")

# 2. Flytt dupliserte SKILL.md-mapper ut av tools/ til archive/legacy_tools_skills
tools_skill_dirs = [
    "document-parser",
    "duckdb-analytics",
    "llm-gateway",
    "ollama-api-bridge",
    "python-sandbox",
    "sqlite-vec-executor",
    "streamlit-builder"
]

target_tools_archive = os.path.join(ARCHIVE_DIR, "legacy_tools_skills")
os.makedirs(target_tools_archive, exist_ok=True)

for sd in tools_skill_dirs:
    src = os.path.join("tools", sd)
    if os.path.exists(src):
        dst = os.path.join(target_tools_archive, sd)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)
        print(f"Archived tools/{sd} -> archive/legacy_tools_skills/{sd}")

# 3. Flytt kristiansand_epm_rammeverk_norsk/agent_ferdigheter til archive og lag en kort peker-README
src_epm_agents = os.path.join("kristiansand_epm_rammeverk_norsk", "agent_ferdigheter")
if os.path.exists(src_epm_agents):
    dst_epm_agents = os.path.join(ARCHIVE_DIR, "legacy_epm_agent_ferdigheter")
    if os.path.exists(dst_epm_agents):
        shutil.rmtree(dst_epm_agents)
    shutil.move(src_epm_agents, dst_epm_agents)
    print("Archived kristiansand_epm_rammeverk_norsk/agent_ferdigheter -> archive/legacy_epm_agent_ferdigheter")
    
    # Lag en lettvekts peker slik at ev. lenker ikke brekker
    os.makedirs(src_epm_agents, exist_ok=True)
    with open(os.path.join(src_epm_agents, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# 🏛️ De 12 Spesialiserte Agentene — Kanonisk Plassering

Dokumentasjonen for de 12 spesialiserte agentene er samlet i den kanoniske mappen:
👉 [`../../agenter/`](../../agenter/)

Se [`../../agenter/README.md`](../../agenter/README.md) for fullstendig oversikt.
""")
    print("Created lightweight pointer README in kristiansand_epm_rammeverk_norsk/agent_ferdigheter/")

# 4. Forenkle spesifikasjoner/SKILL_PREDICTIVE_FORECASTING_AI.md til en peker
spec_skill = os.path.join("spesifikasjoner", "SKILL_PREDICTIVE_FORECASTING_AI.md")
if os.path.exists(spec_skill):
    with open(spec_skill, "w", encoding="utf-8") as f:
        f.write("""# 📈 Predictive AI Forecasting Skill

Dette dokumentet er en peker til den kanoniske Antigravity-ferdigheten:
👉 [`.agents/skills/predictive-forecasting/SKILL.md`](../.agents/skills/predictive-forecasting/SKILL.md)

Se også teknisk spesifikasjon i:
👉 [`PREDICTIVE_AI_FORECASTING_SPEC.md`](./PREDICTIVE_AI_FORECASTING_SPEC.md)
""")
    print("Replaced spesifikasjoner/SKILL_PREDICTIVE_FORECASTING_AI.md with canonical pointer.")

print("Deduplication step completed.")
