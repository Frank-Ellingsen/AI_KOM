# Best Practice Datavisualisering & Storytelling med Data (10-Sekunders Regelen)
## Kristiansand Kommune EPM & Virksomhetsstyring

---

## 1. Visuelt Designsystem & Fargekoding (Color & Typography System)

For å sikre at alle interessenter umiddelbart kjenner igjen dataelementer på tvers av Power BI, Excel, PDF-rapporter og presentasjoner, er det etablert en strikt, universell farge- og typografistandard:

### A. Fargekoding for Finansielle Størrelser (Konsekvent i Bilde og Tekst)
* **Faktisk Regnskap (Visma Bokført):** **Mørk Blå / Koksgrå (`#1B365D`)**
  * *Signal:* Håndfaste, historiske faktiske tall.
  * *Bruk i tekst:* Boldsats eller mørkeblå tekstfarge.
* **Budsjett & Korrigert Ramme (Framsikt):** **Stålblå / Muted Teal (`#4A77A0` / `#2B6CB0`)**
  * *Signal:* Vedtatt og konsekvensjustert ramme.
  * *Bruk i diagrammer:* Stiplet linje, tynnere stolpe eller konturfyll mot Faktisk.
* **Teknisk Visma-Støy / NAV-Etterslep:** **Nøytral Lys Grå (`#CBD5E0` / `#95A5A6`)**
  * *Signal:* Periodiseringsstøy som skal nøytraliseres (f.eks. forsinket art 1690).
* **Reelt Driftsavvik (RAG System):**
  * 🔴 **Rød (`#E53E3E` / `#C0392B`):** Merforbruk / Reelt avvik over $+2,0\%$ (eller $> +200$ tkr). Krever umiddelbar handlingsplan.
  * 🟡 **Amber / Gul (`#DD6B20` / `#D69E2E`):** Avvik mellom $0,0\%$ og $+2,0\%$ (eller $+50$ tkr til $+200$ tkr). Krever observasjon.
  * 🟢 **Grønn (`#38A169` / `#27AE60`):** Mindreforbruk / Avvik $\le 0,0\%$. Innenfor rammen.

---

## 2. 10-Sekunders Regelen & Aksjonstitler (Narrative Headlines)

Hvert eneste visuelle element (Power BI visuals, Excel-diagrammer, PDF-figurer) **MÅ** bestå "10-sekunders testen": En interessent skal forstå hovedbudskapet og konsekvensen innen 10 sekunder uten å måtte studere akser eller tabeller.

### Regler for Aksjonstitler:
1. **Inneholder et aktivt verb** (*nøytraliseres*, *drives av*, *reduserer*, *overskrider*).
2. **Knytter sammen tall og årsak** (f.eks. Faktisk vs. Budsjett + Visma-støy).
3. **Svarer på «Hva så?» / Beslutningsbehovet**.

* ❌ **Dårlig tittel (Emneknagg):** "Avvik K1 Per Sektor"
* ✅ **Best Practice Aksjonstittel:** "Reelt merforbruk i Grunnskole er kun 150 tkr etter at Visma-etterslep på 300 tkr er nøytralisert"

---

## 3. Interessenttilpassede Nivåer (Stakeholder Matrix)

| Nivå | Målgruppe / Stakeholder | Fokus & Visuelt Behov | 10-Sekunders Visualisering | Primært Verktøy |
| :--- | :--- | :--- | :--- | :--- |
| **Nivå 1** | **Bystyret & Formannskapet** | Overordnet måloppnåelse, Bystyrets handlingsregel ($\ge 1,0\%$ Netto Driftsresultat). | KPI-kort med RAG-status, Trendlinje med konfidensintervall, Banan-diagram. | Power BI Executive / PDF Briefing |
| **Nivå 2** | **Kommunedirektør & Lederteam** | Sektorfordeling, Framsikt-deflator, Visma-støy vs. Reelt avvik, tiltakseffekt. | Waterfall-diagram (Visma-støy bro), Bullet Charts (Faktisk vs Budsjett). | Power BI CFO App / Excel Hub |
| **Nivå 3** | **Kommunalsjefer & Enhetsledere** | Operativ rammestyring (Skole, Boenhet), vikarbruk (1020) vs NAV-refusjon (1690). | Dekomponeringstre (Drill-down til art), Heatmap tabeller, Betinget formatering. | Power BI Matrix / Excel What-If |
| **Nivå 4** | **Økonomirådgiver & Controller** | Dybdeanalyse, RAG Glass-Box kildehenvisninger, RLS, bilagsgransking. | Transaksjonstabeller med Rich Tooltips, RAG Reasoning Chain, Audit Log. | Controller AI Portal / Excel CLI |

---

## 4. Konkrete Visuelle Teknikker i Power BI & Excel

### A. RAG Betinget Formatering (Traffic Lights)
* **Regel i Power BI / Excel:**
  * `=IF(Reelt_Avvik_Prosent <= 0, "Grønn", IF(Reelt_Avvik_Prosent <= 0.02, "Amber", "Rød"))`
  * Bruk ikonsett (🔴 🟡 🟢) kombinert med myke bakgrunnsfarger slik at fargeblindhet tas hensyn til (fargetone + symbol).

### B. Interaktive Tooltips (Rich Custom Tooltips)
Når brukeren hovrer over en stolpe eller enhetszelle, viser tooltippet:
1. **Bokført Visma-tall:** Bruttoposisjon i regnskapet.
2. **Framsikt Deflator-tillegg:** Hvor mye ekstra ramme enheten fikk tilført i RNB.
3. **Beregnet NAV-etterslep:** Hvor mye refusjon som venter fra NAV på art 1690.
4. **Reelt Driftsavvik:** Netto underliggende avvik etter nøytralisering.
5. **Historisk 3-års Snitt:** Trend sammenlignet med K1 2023–2025.

---

## 5. Fargekodet Tekst- og Grafikkstandard

Slik skal Faktisk vs. Budsjett fremstilles i alle rapporter:

```text
[ FAKTISK REGNSKAP ]   ████████████████████  (Mørk Blå: #1B365D)
[ FRAMSIKT BUDSJETT ]  ░░░░░░░░░░░░░░░░░░░░  (Muted Blå: #4A77A0 / Kontur)
[ VISMA-STØY (NAV) ]   ▒▒▒▒▒▒▒▒▒▒▒▒          (Lys Grå: #CBD5E0)
[ REELT MERFORBRUK ]   ████                  (RAG Rød: #E53E3E)
```
