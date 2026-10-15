---
name: visual-data-communication
description: >-
  Datavisualisering, grafisk persepsjon (Cleveland & McGill), Edward Tufte Data-Ink Ratio og Kristiansand kommunes designprofil.
---

# Agent Skill: Visual Data Communication & Perception Expert (`skill-visual-data-communication`)

> **Spesifikasjon for datavisualisering, grafisk persepsjon og visuell formidling i kommunal rapportering og AI-genererte dashbord.**

---

## 1. Oversikt og Formål

Denne skill-en fungerer som ekspertregler for datavisualisering, fargebruk, målgruppetilpasset rapportering og visuell pedagogikk. Skill-en sikrer at tabeller, grafer, Power BI-dashbord, PDF-rapporter og presentasjoner bygger på etablerte persepsjonsteorier og internasjonale designstandarder.

---

## 2. Teoretisk Fundament & Grafisk Persepsjon

### A. Cleveland & McGill Rangering av Persepsjonsoppgaver (1984)
Ved valg av visuelle elementer skal AI-modellen prioritere dekodingsformer i henhold til menneskehjernens presisjon ved avlesning:
1. **Posisjon langs en felles akse** *(Høyest presisjon – stolpediagram, linjediagram)*
2. **Posisjon langs identiske, ujusterte akser** *(Eksempel: Trellis/Small Multiples)*
3. **Lengde / Vinkel** *(Stolpelengde > Vinkel i kakediagram)*
4. **Areal / Volum** *(Sirkler, boblediagram – krever forsiktighet, skalér etter areal, ikke radius)*
5. **Fargemetning og Fargenyanse (Hue)** *(Lavest presisjon ved avlesning av eksakte verdier – kun egnet for kategorisering og oppmerksomhetsstyring)*

### B. Unngå "Rainbow Color Map" (Regnbuefarger / Jet)
* **Kritisk feil:** Regnbuefargekart misviser leseren fordi fargeovergangene ikke har jevn endring i lysstyrke (luminans).
* **Krav:** Benytt **perseptuelt uniforme fargekart** (som *Viridis*, *Plasma*, *Cividis*) for kontinuerlige data, eller kontrollerte kommunale paletter for kategoriale data.
* **Fargeblindhet:** Alle fargepaletter skal oppfylle WCAG 2.1 AA-krav for fargekontrast og fungere for personer med fargeblindhet (deuteranopi/protanopi).

---

## 3. Diagramvalg etter Financial Times Visual Vocabulary

| Formål | Primært Diagramvalg | Sekundært / Alternativt | Unngå |
| :--- | :--- | :--- | :--- |
| **Sammenligning (Ranking)** | Liggende stolpediagram (Bar Chart) | Lollipop chart | 3D-stolper, kakediagram |
| **Avvik (Actual vs. Budget)** | **Bullet Chart**, Waterfall chart | Divergerende stolpediagram | Dobbel Areal-graf uten felles nullpunkt |
| **Endring over tid (Trend)** | Linjediagram, Sparklines | Områdediagram (Stacked Area) | Linjediagram med > 5 linjer uten utheving |
| **Fordeling (Part-to-Whole)** | Donut chart (max 3–4 kategorier) | Treemap, Waterfall | Kakediagram med > 5 kaker, 3D-kaker |
| **Hierarki & Struktur** | Decomposition Tree, Treemap | Sunburst | Flate tabeller uten summeringsnivåer |

---

## 4. Kommunal Designstandard (Kristiansand Kommune)

### A. Fargepalett for Økonomistyring
* **Hovedfarge (Nøytral/Kontekst):** Mørk grå (`#2C3E50`) eller Mørk blå (`#1B365D`).
* **Måloppnåelse / Positivt avvik:** Dempete grønn (`#27AE60`) eller Blå tone (`#2980B9`).
* **Merforbruk / Advarsel:** Rød/Sienna (`#C0392B`) — benyttes KUN på tall som krever handling.
* **Prognose / Stipulering:** Stiplet linje eller lysere fargetone.

### B. Tallformatering og Akseregler
* **Negativer:** Skal vises i rød farge og parentes: `#,##0;[Red](#,##0);"-"`.
* **Måleenhet:** Angi tydelig i tittel eller akse (f.eks. *"Tall i 1 000 kr"* eller *"Mill. kr"*).
* **Nullpunkt på Y-akse:** Stolpediagrammer **skal alltid** starte på null (0) for å forhindre at stolper fremstår uforholdsmessig store.

---

## 5. Datagrafisk Fortellerteknikk (Data Storytelling)

1. **Handlingstitler (Action Titles):**
   * *Dårlig:* "Utvikling i overtidskostnader 2026"
   * *Bra:* "Overtidskostnadene økte med 2,4 mill. kr i Q2 spesielt innen Helse og mestring"
2. **Fokus-Highlighting (Dekuttering):**
   * Tone ned bakgrunnsdata (grå fargetoner) og løft frem nøkkelfunnet med en accent-farge.
3. **Fjerne "Chartjunk":**
   * Slett uhensiktsmessige rutenett (*gridlines*), tunge rammer, 3D-effekter og overflødige forklaringstekster (*legends*) når direkte merking på grafen er mulig.

---

## 6. Integrasjonsmønstre i Python, Power BI og Excel

```python
# Eksempel: Matplotlib / Seaborn i Python med perseptuelt uniform design
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 5))

# Nøytral base + accent for avvik
colors = ['#2C3E50' if v < 0 else '#C0392B' for v in variance_values]
ax.barh(categories, variance_values, color=colors)

ax.set_title("Merforbruk i Q2 konsentrert om Vikarbruk i Oppvekst", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Avvik mot periodisert budsjett (1 000 kr)")
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
sns.despine(top=True, right=True)
plt.tight_layout()
```
