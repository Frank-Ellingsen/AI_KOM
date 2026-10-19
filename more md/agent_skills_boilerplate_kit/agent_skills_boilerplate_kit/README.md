# Agent Skills Starter & Boilerplate Kit

Dette er en produksjonsklar mal-mappe for utvikling av nye **Agent Skills** optimalisert for **Agentic AI, MCP (Model Context Protocol) og token-effektivitet**.

---

## 📁 Mappestruktur

```text
agent_skills_boilerplate_kit/
├── README.md                      # Denne veiledningen
├── validate.sh                    # Hurtigskript for kjøring av validering
├── validator/
│   └── skills_ref_validate.py     # CLI-validator for linje- og token-sjekk
└── my_custom_skill/              # Eksempel på en ny Agent Skill
    ├── SKILL.md                   # L1 + L2: Frontmatter & kjerneinstruksjoner (< 500 linjer)
    ├── scripts/                   # L3: Eksekverbar Python/Bash-kode (0 kontekst-tokens)
    │   └── example_script.py
    ├── references/                # L3: Detaljerte fagmanualer og oppslagsdokumenter
    │   └── domain_knowledge.md
    └── assets/                    # L3: Statiske maler og eksempelfiler
        └── config_template.json
```

---

## 🚀 Slik bruker du malen

1. **Kopier `my_custom_skill`** og gi mappen navnet på din nye ferdighet (f.eks. `faktura_kontroll_skill`).
2. Rediger `SKILL.md`:
   - Oppdater YAML-frontmatter (`name` og `description`).
   - Beskriv fremgangsmåten trinnvis.
   - Hold `SKILL.md` under **500 linjer / ~5 000 tokens**.
3. Legg tunge oppslagsdata i `references/` og eksekverbar logikk i `scripts/`.
4. Kjør validering før publisering:
   ```bash
   bash validate.sh my_custom_skill
   ```
