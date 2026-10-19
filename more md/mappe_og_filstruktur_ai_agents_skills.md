# Standardisert Mappe- og Filstruktur for AI-Agenter og Agent Skills
> **Optimaliseringsveileder for Token-Budsjett, Konteksteffektivitet og Modularitet i Agentiske AI-Systemer**

---

## 1. Formål og Kjernefilosofi

I moderne AI-engineering og agentarkitektur er **kontekstvinduet ikke et uendelig minne — det er en dyr L1-cache**. Å laste alle systemprompter, verktøyskjemaer (JSON schemas), bedriftsinterne retningslinjer og historikk inn i modellens aktive kontekstvindu ved oppstart fører til tre alvorlige problemer:
1. **$O(N^2)$ Kvadratisk Token-Eksplosjon**: Hver eneste nye samtalerunde må prosessere hele den opphopede teksten på nytt, noe som mangedobler API-kostnadene og øker latenstiden (*Time-to-First-Token*).
2. **Attention Degradation ("Lost in the Middle")**: Når kontekstvinduet fylles opp med irrelevant informasjon, svekkes modellens evne til å følge instruksjoner og hente ut korrekte fakta.
3. **Kognitiv Støy og Forvirring**: Sammenblanding av tilkoblingslag (APIs/MCP), prosedyrekunnskap (SOPs) og agenters resonneringssløyfer gjør kildekoden uoversiktlig og vanskelig å vedlikeholde.

**Løsningen er filbasert minnearkitektur og progressiv avdekking (Progressive Disclosure)**: Informasjon struktureres i modulære mapper og filer på filsystemet, og lastes dynamisk inn i modellens kontekst kun når oppgaven faktisk krever det.

---

## 2. Standard Mappestruktur (Agent Skills Specification)

I henhold til den åpne **Agent Skills-spesifikasjonen** (utviklet av Anthropic og benyttet i plattformer som Claude Code, OpenAI Codex, Cursor og AGNT.gg), skal enhver ferdighet/kompetansepakke organiseres som en selvstendig mappe med følgende oppbygning:

```text
my-skill/
├── SKILL.md          # Påkrevd: Metadata (YAML) + Kjerneinstruksjoner (< 500 linjer)
├── scripts/          # Valgfritt: Eksekverbar kode (Python, Bash, Node.js)
├── references/       # Valgfritt: Spesialiserte fagmanualer, API-referanser og skjemaer
└── assets/           # Valgfritt: Statiske maler, konfigurasjoner og visualiseringer
```

### Mappe/Fil-roller forklart:

* **`SKILL.md` (Obligatorisk)**: Det primære aktiveringsdokumentet. Inneholder YAML frontmatter øverst (metadata for søk/oppdagelse) og en konsis steg-for-steg veileder.
* **`scripts/` (Valgfritt)**: Inneholder deterministisk skriptkode (`.py`, `.sh`). 
  * *Hvorfor?* Når agenter kjører et skript via terminalen/bash, **lastes skriptkoden ALDRI inn i kontekstvinduet**. Kun skriptets utskrift (*stdout/stderr*) forbruker tokens. Dette sparer opptil 95 % token-forbruk sammenlignet med at modellen skal generere eller lese koden på nytt hver gang.
* **`references/` (Valgfritt)**: Inneholder dypere tekniske spesifikasjoner, lovverk, API-dokumentasjon (`schema.json`, `rules.md`). Modellene leser disse filene med `cat` eller søk kun ved behov.
* **`assets/` (Valgfritt)**: Statiske ressurser som maler (`template.docx`), fargepaletter (`theme.json`) eller visuelle eksempler.

---

## 3. Det Trelags Kontekst-Lasteprinsippet (Progressive Disclosure)

For å maksimere nytteverdi per token deles informasjonsinnlastingen inn i tre strenge nivåer:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 1: Oppdagelse / Metadata (ALLTID LASTET)                          │
│ ~100 tokens per Skill (navn + beskrivelse fra YAML Frontmatter)         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Oppgave matcher skill-beskrivelse)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 2: Aktivering / Instruksjoner (TRIGGERED LOAD)                    │
│ < 5 000 tokens (SKILL.md leses inn i kontekst via bash/fs)             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Modellen trenger spesifikk referanse/skript)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 3: Utførelse / Skript & Referanser (DEMAND PAGED)                  │
│ 0 tokens for skriptkode (kun utdata leses). Spesifikk referansefil      │
│ hentes punktvis via Demand Paging.                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

| Nivå | Hva lastes | Når lastes det | Tokenkostnad | Innhold |
| :--- | :--- | :--- | :--- | :--- |
| **Nivå 1** | Metadata | Ved systemoppstart | **~100 tokens** per skill | `name` og `description` i YAML frontmatter |
| **Nivå 2** | Instruksjoner | Når oppgaven aktiverer skillen | **< 5 000 tokens** | Hovedteksten i `SKILL.md` (SOPs, rutiner) |
| **Nivå 3** | Skript & Referanser | Kun ved behov under utførelse | **0 tokens for kode** (kun utdata/valgt fil leses) | Filer i `scripts/`, `references/` og `assets/` |

---

## 4. Ansvarsdeling: Agenter vs. Agent Skills vs. MCP (Unngå Forvirring)

En av de vanligste årsakene til arkitektonisk forvirring er sammenblanding av **MCP (Model Context Protocol)** og **Agent Skills**. De løser to helt forskjellige, men utfyllende oppgaver:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ AGENT (Hjerne & Resonneringssløyfe)                                      │
│ Planlegger, tar beslutninger og styrer samtalehistorikken.               │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
┌───────────────────────────────────┐   ┌───────────────────────────────────┐
│ AGENT SKILLS (Kognitiv Prosedyre) │   │ MCP / TOOLS (Transport & Infras.) │
│ "Hvordan utføre domeneoppgaven"   │   │ "USB-C grensesnitt til systemer"  │
│ - Forretningsregler & SOPs        │   │ - Database-spørringer (SQL)       │
│ - Best practice & arbeidsflyt     │   │ - API-kall (REST / GraphQL)       │
│ - Dokument- og rapportstrukturer  │   │ - Filsystem- og I/O-operasjoner   │
└───────────────────────────────────┘   └───────────────────────────────────┘
```

* **MCP (Model Context Protocol)** = **Handling og Tilkobling (Hands/Tools)**. Standardiserer hvordan agenten kobler seg til eksterne databaser, enhets-API-er eller filsystemer via JSON-RPC. (Eksempel: `mcp__postgres__query`).
* **Agent Skills** = **Metode og Prosedyre (Brain/SOP)**. Standardiserer *hvordan* agenten skal resonnere, hvilke verktøy den skal velge i hvilken rekkefølge, og hvilke kvalitetssjekker/lover som må oppfylles. (Eksempel: *Hvordan gjennomføre en økonomisk avviksanalyse jf. Kommuneloven § 14-5*).

---

## 5. Komplett Prosjektelement-Struktur (Eksempel)

Her er et eksempel på et optimalisert produksjonsprosjekt som kombinerer agent-skript, MCP-konfigurasjoner og prosedyre-skills uten token-sløsing:

```text
my-enterprise-project/
├── .claude/                             # Agentkonfigurasjon og lokalt minne
│   ├── CLAUDE.md                        # Prosjektspesifikke kjerneinstruksjoner (kort)
│   └── mcp.json                         # Registrerte MCP-servere (Tools/Resources)
├── skills/                              # Prosjektets Agent Skills (Prosedyrekunnskap)
│   ├── financial-audit/
│   │   ├── SKILL.md                     # Hovedveileder for revisjon (< 300 linjer)
│   │   ├── scripts/
│   │   │   └── calc_evm.py              # Monte Carlo & EVM beregninger (kjøres via terminal)
│   │   ├── references/
│   │   │   ├── kommuneloven_rules.md    # Juridiske paragrafer (§ 14-5, § 14-6)
│   │   │   └── kostra_functions.json    # Offisielle KOSTRA-koder
│   │   └── assets/
│   │       └── saksfremlegg_template.docx # Vedtaksnotat-mal
│   └── pii-sanitizer/
│       ├── SKILL.md                     # Veileder for PII-skjerming
│       └── scripts/
│           └── mask_fnr.py              # Regex-basert sladding av 11-sifrede fnr
├── src/                                 # Applikasjonskode / Backend (Python, Node)
├── tests/                               # Unittester for skript og verktøy
└── README.md                            # Prosjektdokumentasjon for utviklere
```

---

## 6. Sjekkliste for Utviklere og AI-Engineers

For å sikre at prosjektet opprettholder lavt tokenforbruk og høy presisjon, følg denne sjekklisten:

1. **[ ] Hold `SKILL.md` under 500 linjer (~5 000 tokens)**: Flytt tunge datatabeller, store JSON-skjemaer og API-dokumentasjon over i `references/`-mappen.
2. **[ ] Optimaliser YAML Frontmatter**: Beskrivelsen (`description`) må tydelig forklare *når* og *hvorfor* ferdigheten skal aktiveres, med relevante nøkkelord for intasjonsmatching (Nivå 1 footprint < 100 tokens).
3. **[ ] Bruk Skript for Tunge Beregninger**: Utfør databehandling, filkonvertering og matematiske simuleringer i Python-skript i `scripts/` fremfor å la LLM-en generere koden i samtalen.
4. **[ ] Bruk Relative Filstier**: I `SKILL.md`, referer til underdokumenter med relative stier (f.eks. `cat references/rules.md`), slik at agenten kan hente dem via standard terminalkommandoer.
5. **[ ] Skjerm Følsomme Data (GDPR Port 4)**: Sørg for at skript i `scripts/` sladder personopplysninger og fødselsnumre lokalt før tekst sendes videre til modellens kontekstvindu.
6. **[ ] Valider Strukturen**: Kjør CLI-validering dersom verktøy er tilgjengelig (f.eks. `skills-ref validate ./skills/my-skill`).

---

*Veileder utarbeidet for optimalisering av kontekst, agentiske samspill og token-budsjett i produksjonsmiljøer.*
