# tools/clean_budsjett_framsikt.py
# -*- coding: utf-8 -*-
import os
import shutil

DIR = "budsjett-framsikt"
ARCHIVE_DIR = os.path.join("archive", "backups", "budsjett-framsikt-legacy")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 1. Update budsjettering-kristiansand-kommune.md with v2 content + Frontmatter
v2_budsjett_path = os.path.join(DIR, "budsjettering-kristiansand-kommune-v2.md")
with open(v2_budsjett_path, "r", encoding="utf-8") as f:
    v2_budsjett_content = f.read()

# Remove old H1 if present to attach clean frontmatter
clean_budsjett_body = v2_budsjett_content
if clean_budsjett_body.startswith("# "):
    clean_budsjett_body = clean_budsjett_body[clean_budsjett_body.find("\n")+1:].lstrip()

frontmatter_budsjett = """---
title: "Budsjettering i Kristiansand kommune: Rammer, Reglement og Utvidet Internt Årshjul"
canonical_path: "budsjett-framsikt/budsjettering-kristiansand-kommune.md"
version: "2.1"
domain: "Kommunal Finans og EPM"
statutory_basis: "Kommuneloven (2018) kapittel 14, Bystyrets Økonomireglement (11.10.2023)"
key_targets:
  netto_driftsresultat: "≥ 1,0 % av brutto driftsinntekter (~115 MNOK)"
  disposisjonsfond: "≥ 4,0 % av brutto driftsinntekter (~460 MNOK)"
  lanetak: "< 8,8 milliarder NOK netto lånegjeld"
summary: "Overordnede økonomiske rammer, måltall, handlingsregler og 8-faset internt årshjul for Kristiansand kommune fra mai til 31. desember."
---

# Budsjettering i Kristiansand kommune: Rammer, Reglement og Utvidet Internt Årshjul

""" + clean_budsjett_body

with open(os.path.join(DIR, "budsjettering-kristiansand-kommune.md"), "w", encoding="utf-8") as f:
    f.write(frontmatter_budsjett)
print("Updated budsjettering-kristiansand-kommune.md with canonical v2 content & frontmatter.")

# Archive the -v2 duplicate
shutil.move(v2_budsjett_path, os.path.join(ARCHIVE_DIR, "budsjettering-kristiansand-kommune-v2.md"))
print("Archived budsjettering-kristiansand-kommune-v2.md")

# 2. Update lonnsbudsjettering-kristiansand-framsikt.md with v2 content + Frontmatter
v2_lonn_path = os.path.join(DIR, "lonnsbudsjettering-kristiansand-framsikt-v2.md")
with open(v2_lonn_path, "r", encoding="utf-8") as f:
    v2_lonn_content = f.read()

clean_lonn_body = v2_lonn_content
if clean_lonn_body.startswith("# "):
    clean_lonn_body = clean_lonn_body[clean_lonn_body.find("\n")+1:].lstrip()

frontmatter_lonn = """---
title: "Lønnsbudsjettering i Kristiansand kommune med Framsikt"
canonical_path: "budsjett-framsikt/lonnsbudsjettering-kristiansand-framsikt.md"
version: "2.1"
domain: "Stillings- og Lønnsbudsjettering"
statutory_basis: "Kommuneloven § 14-6 (Bruttoprinsippet), HTA § 4, KRS 6"
key_rules:
  aga_sone: "Sone 1 (14,1 % på Lønn + Feriepenger + Pensjon)"
  feriepenger: "12,0 % under 60 år / 14,3 % ved 60+ år"
  pensjonsordning: "SPK (13,8 %) for lærere, KLP (15,2 %) for øvrige"
  bruttoprinsipp: "Ingen nettobudsjettering av vikarmidler (1020) mot NAV-refusjon (1690)"
summary: "Stillings- og bemanningsbudsjettering i Framsikt EPM, skille mellom fast lønn (1010) og variable potter (1020/1050/1090), Excel eksport/import og pensjonskontroll."
---

# Lønnsbudsjettering i Kristiansand kommune med Framsikt

""" + clean_lonn_body

with open(os.path.join(DIR, "lonnsbudsjettering-kristiansand-framsikt.md"), "w", encoding="utf-8") as f:
    f.write(frontmatter_lonn)
print("Updated lonnsbudsjettering-kristiansand-framsikt.md with canonical v2 content & frontmatter.")

# Archive the -v2 duplicate
shutil.move(v2_lonn_path, os.path.join(ARCHIVE_DIR, "lonnsbudsjettering-kristiansand-framsikt-v2.md"))
print("Archived lonnsbudsjettering-kristiansand-framsikt-v2.md")

# 3. Add frontmatter to driftsarter-og-selvkost-alle-omrader-framsikt.md
selvkost_path = os.path.join(DIR, "driftsarter-og-selvkost-alle-omrader-framsikt.md")
with open(selvkost_path, "r", encoding="utf-8") as f:
    selvkost_content = f.read()

if not selvkost_content.startswith("---"):
    clean_selvkost_body = selvkost_content
    if clean_selvkost_body.startswith("# "):
        clean_selvkost_body = clean_selvkost_body[clean_selvkost_body.find("\n")+1:].lstrip()

    frontmatter_selvkost = """---
title: "Driftsarter, Selvkost og KOSTRA-Kontering for Alle Kommunalområder i Framsikt"
canonical_path: "budsjett-framsikt/driftsarter-og-selvkost-alle-omrader-framsikt.md"
version: "2.1"
domain: "Driftsøkonomi, KOSTRA & Selvkost"
statutory_basis: "Kommuneloven § 15-1, Selvkostforskriften, KOSTRA-forskriften"
key_functions:
  vannforsyning: "Funksjon 3400"
  avloepshandtering: "Funksjon 3450 (2 mrd capex plan)"
  renovasjon: "Funksjon 3500 (Avfall Sør)"
  byggesak_geodata: "Funksjon 3600"
key_formula: "Gebyrgrunnlag = Direkte (1000-1270) + Henføring + Kapitalkostnader (1590 + Rente 4,00%) - Direkte inntekter"
summary: "Fullstendig gjennomgang av driftsarter (1100–1270), overføringer (1300–1480), finans/fond (1500–1930) og selvkostberegninger for tekniske tjenester med 5-årsregel."
---

# Driftsarter, Selvkost og KOSTRA-Kontering for Alle Kommunalområder i Framsikt

""" + clean_selvkost_body

    with open(selvkost_path, "w", encoding="utf-8") as f:
        f.write(frontmatter_selvkost)
    print("Added frontmatter to driftsarter-og-selvkost-alle-omrader-framsikt.md")

# 4. Add frontmatter to kostra-artskontoer-konteringsregler-framsikt.md
kostra_path = os.path.join(DIR, "kostra-artskontoer-konteringsregler-framsikt.md")
with open(kostra_path, "r", encoding="utf-8") as f:
    kostra_content = f.read()

if not kostra_content.startswith("---"):
    clean_kostra_body = kostra_content
    if clean_kostra_body.startswith("# "):
        clean_kostra_body = clean_kostra_body[clean_kostra_body.find("\n")+1:].lstrip()

    frontmatter_kostra = """---
title: "KOSTRA Artskontoer og Konteringsregler for Lønnsområdet i Framsikt"
canonical_path: "budsjett-framsikt/kostra-artskontoer-konteringsregler-framsikt.md"
version: "2.1"
domain: "KOSTRA Kontoplan og Konteringsregler"
statutory_basis: "KOSTRA-forskriften, Budsjett- og regnskapsforskriften, Kommuneloven § 14-6"
key_accounts:
  fastlonn: "Art 1010 (Stillingsoversikt)"
  vikarer: "Art 1020 (Kronepott per ansvar)"
  tillegg_overtid: "Art 1050 / 1090 (Turnus og overtid)"
  refusjon_nav: "Art 1690 (Sykelønnsrefusjon brutto inntekt)"
summary: "Konteringsveiledning for lønnsarter, sosiale utgifter og NAV-refusjoner, med sjekkliste for seksjonsledere før budsjettlåsing."
---

# KOSTRA Artskontoer og Konteringsregler for Lønnsområdet i Framsikt

""" + clean_kostra_body

    with open(kostra_path, "w", encoding="utf-8") as f:
        f.write(frontmatter_kostra)
    print("Added frontmatter to kostra-artskontoer-konteringsregler-framsikt.md")

# 5. Write optimized README.md in budsjett-framsikt/
optimized_readme = """# 🏛️ Kristiansand Kommune — Framsikt EPM & Budsjett Dokumentasjonspakke

> **Kanonisk dokumentasjonspakke for kommunal økonomistyring, stillingsbudsjett, KOSTRA-kontoplan og selvkost i Framsikt.**  
> Tilpasset for **Frank Ellingsen** (Senior Financial Controller) og integrert i [`index.html`](../index.html).

---

## 🧭 Kanoniske Dokumenter (Optimalisert for LLM & Vektorsøk)

| Dokument | Hovedinnhold | Lovhjemmel & Standarder | Filsti |
| :--- | :--- | :--- | :--- |
| **Budsjettering & Årshjul** | Måltall (11,48 mrd, $\ge 1,0\%$ driftsres, $\ge 4,0\%$ fond, $<8,8$ mrd lån), 6 områder, 8-faset internt årshjul fra mai til des. | Kommuneloven kap. 14, Bystyrets reglement | [`budsjettering-kristiansand-kommune.md`](./budsjettering-kristiansand-kommune.md) |
| **Stillings- & Lønnsbudsjett** | Fastlønn (1010) vs variable potter (1020/1050/1090), feriepenger (12%/14,3%), SPK vs KLP, AGA Sone 1 (14,1%), Excel import/eksport. | Kommuneloven § 14-6, HTA § 4, KRS 6 | [`lonnsbudsjettering-kristiansand-framsikt.md`](./lonnsbudsjettering-kristiansand-framsikt.md) |
| **Driftsarter & Selvkost** | Varekjøp (1100–1270), overføringer (1300–1480), finans/fond (1500–1930), selvkostkalkyler for VAR & Byggesak med 5-årsregel. | Kommuneloven § 15-1, Selvkostforskriften | [`driftsarter-og-selvkost-alle-omrader-framsikt.md`](./driftsarter-og-selvkost-alle-omrader-framsikt.md) |
| **KOSTRA Konteringsregler** | Lønnsarter, sosiale kostnader og refusjoner (1690). Krav om bruttoføring og forbud mot netting. Sjekkliste før budsjettlåsing. | KOSTRA-forskriften, Budsjettforskrift § 14-6 | [`kostra-artskontoer-konteringsregler-framsikt.md`](./kostra-artskontoer-konteringsregler-framsikt.md) |

---

## ⚡ Interaktiv Implementering i Huben
Alle 4 dokumenter er direkte implementert som kjørbare motorer i [`index.html`](../index.html) under **Kommunal Budsjettmodul** (`#budsjett-modul-seksjon`):
1. **Lønnskalkulator**: Beregner bruttolønn, feriepenger, KLP/SPK og AGA (14,1%) med live KOSTRA-konteringssplitt.
2. **Selvkostkalkulator**: Full selvkostkalkyle for Vann, Avløp, Renovasjon og Byggesak med 5-årsfondregulering.
3. **Budsjett-Årshjul**: 8 interaktive faser med oppgavepakker, roller og frister.
4. **KOSTRA-tabell**: Søkbar og filtrerbar oversikt over alle kommunale arter.
5. **QA-Motor**: 8-punkts sjekkliste med SHA-256 kryptografisk forsegling.
"""

with open(os.path.join(DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(optimized_readme)
print("Updated budsjett-framsikt/README.md with optimized router index.")
