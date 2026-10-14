# 📊 Visuell Datakommunikasjon og Storytelling med Data
## Basert på Financial Times Visual Vocabulary for Økonomi og Virksomhetsstyring i Kristiansand Kommune

---

### 1. 🏛️ Formål og Kognitivt Rammeverk

I en hektisk kommunal hverdag med stor arbeidsbelastning må visuelle fremstillinger i rapporter til Bystyret, Kommunedirektøren, Kommunalsjef, Seksjonsleder og Enhetsleder fortelle en **umiddelbar, tydelig og udiskutabel historie**.

Dette rammeverket kombinerer **Financial Times (FT) Visual Vocabulary** med **Cleveland & McGills teori for grafisk persepsjon** og **data storytelling-prinsipper**. Formålet er å eliminere visuell støy (*chartjunk*) og velge **eksakt riktig diagramtype** for den økonomiske problemstillingen som skal kommuniseres.

---

### 2. 🎨 Kognitiv Prioritering (Cleveland & McGill)

Når menneskehjernen avleser visuelle data, skjer det etter en streng hierarkisk nøyaktighetsskala. Vi velger alltid visualiseringer øverst på skalaen:

1. **Posisjon langs en felles akse** (Høyest nøyaktighet: Stolpe-/Stasjonsdiagram, Linjediagram)
2. **Posisjon langs usentrerte akser** (Gjentatte linjer, Sparklines)
3. **Lengde og vinkel** (Middels nøyaktighet: Trappediagram, Waterfall)
4. **Areal og Fargemetning** (Lavest nøyaktighet: Heatmaps, Treemaps)
5. **Vinkel og Romfang** (Forbudt i økonomirapportering: Kakediagrammer / 3D-diagrammer)

---

### 3. 📐 FT Visual Vocabulary – Tilpasset Kommunal Økonomistyring

Financial Times deler datavisualisering inn i **9 primære relasjonskategorier**. Nedenfor er oppskriften på hvordan hver kategori anvendes i månedlige avviks- og prognoserapporter i Kristiansand kommune:

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│              FINANCIAL TIMES VISUAL VOCABULARY FOR KOMMUNAL ØKONOMI                       │
├──────────────────────┬──────────────────────────────────────────┬─────────────────────────┤
│ FT KATEGORI          │ ANBEFALT DIAGRAMTYPE                     │ KOMMUNALT BRUKSOMRÅDE   │
├──────────────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ 1. AVVIK             │ • Bullet Chart (Mål- og stolpediagram)   │ YTD Avvik mot ramme     │
│    (Deviation)       │ • Diverging Bar (Tofarget avviksstolpe)  │ Mer-/mindreforbruk      │
├──────────────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ 2. ENDRING OVER TID  │ • Fan Chart (Viftediagram / Band Plot)   │ EOY Balanseprognose     │
│    (Change over Time)│ • Sparklines (Mini-trender i tabell)    │ Månedlig vikarforbruk   │
├──────────────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ 3. FLYT & BRO        │ • Waterfall Chart (Vannfallsdiagram)     │ Budsjettbro (Opprinnelig│
│    (Flow & Process)  │ • Decomposition Tree (Sammentre)         │ -> Endring -> EOY)      │
├──────────────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ 4. RANGERUNG         │ • Ordered Horizontal Bar Chart           │ Rangering av enheter    │
│    (Ranking)         │ • Slope Chart (Helningsdiagram)          │ Endring fra T1 til T2   │
├──────────────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ 5. HELHET / STRUKTUR │ • Treemap (Rektangulær fordeling)        │ Sektorfordeling av ramme│
│    (Part-to-Whole)   │ • Stacked Bar (100% trappet stolpe)     │ Lønn vs. Drift vs. Kjøp │
└──────────────────────┴──────────────────────────────────────────┴─────────────────────────┘
```

---

### 4. 📈 Praktiske Diagrammønstre for de 4 Rapportkravene

For å underbygge den obligatoriske **4-punkts rapportstandarden** (1. Avvik YTD, 2. Årsak, 3. Action, 4. Effekt/EOY Balanse), anvendes følgende visuelle mønstre:

#### A. Avvik YTD & Budsjettforbruk -> **Bullet Chart & Diverging Bar**
* **Hvorfor:** Et Bullet chart viser faktisk tidsbruk/forbruk mot vedtatt ramme (stiplet linje) og kildekontroll uten å ta opp stor plass.
* **Fargebruk:** Mørk blå for faktisk forbruk, stiplet rød linje for rammegrense. Rød stolpe kun ved kritisk merforbruk (> 3 %).

#### B. Årsaksforklaring & Sammenheng -> **Waterfall Chart (Vannfallsdiagram / Budsjettbro)**
* **Hvorfor:** Viser nøyaktig *hva* som har bygget opp avviket fra opprinnelig budsjett til dagens situasjon.
* **Mønster:**
  * Start: Opprinnelig ramme (100 MNOK)
  * + Stolpe 1: Sykepengerefusjonsforsinkelse (+ 1,2 MNOK)
  * + Stolpe 2: Vikarbruk overtid (+ 0,8 MNOK)
  * - Stolpe 3: Innkjøpsstopp tiltak (- 0,4 MNOK)
  * Slutt: Forventet årsresultat (101,6 MNOK)

#### C. Helårsprognose og Effekt av Tiltak -> **Fan Chart (Viftediagram for EOY)**
* **Hvorfor:** Viser utviklingen hittil i år (M1–M9) som en fast linje, og fremtidige måneder (M10–M12) som tre konfidensbaner:
  * **P10 (Best Case / Tiltak full effekt):** Balanse per 31.12.
  * **P50 (Forventet / Base Case):** Mild overskridelse.
  * **P90 (Worst Case / Null tiltak):** Kritisk merforbruk.

#### D. Rask Overtids- og Vikarmonitor -> **Sparklines i Tabeller**
* **Hvorfor:** I stedet for store, tunge diagrammer for alle 50 enheter, integreres 12-måneders mikrolinjer (*sparklines*) direkte inn i tabellkolonnene i Streamlit Hub og Power BI.

---

### 5. 🎨 Fargeregler og Tilgjengelighet (WCAG 2.1 AA)

1. **Forbud mot Regnbuekart (Rainbow / Jet Colormaps):**
   * Regnbuefargekart villeder leseren fordi fargeovergangene ikke er perceptuelt uniforme.
2. **Kommune-palett:**
   * **Nøytral / Struktur:** Mørk blå (`#1E3A8A`) og mørk grå (`#374151`) for akser, ordinære tall og nøytrale stolper.
   * **Avvik / Alarm:** Dempet rød/sienna (`#DC2626`) reserveres **kun** for kritiske avvik der tiltak kreves.
   * **Gunstig / Måloppnåelse:** Dempet grønn (`#16A34A`) for innsparinger og positive avvik.
   * **Tiltakseffekt (Prognose):** Stiplet lilla/blå linje (`#2563EB`) for å vise prognosebane *etter* iverksatt tiltak.
3. **Handlingstitler (Action Titles):**
   * Alle diagrammer skal ha en konkluderende handlingstittel i stedet for en nøytral beskrivelse:
     * ❌ *Feil:* "Utvikling i vikarforbruk 2026"
     * ✅ *Riktig:* "Vikarforbruk i Oppvekst økte med 8,4 % i Q2 – Tiltak iverksatt fra september stabiliserer EOY-balansen"

---

### 6. 📝 Integration i Office Hub V2 & Streamlit UI

I **Streamlit Office Hub** og rapporteringsmodulene implementeres disse visualiseringene ved hjelp av `plotly.graph_objects` og `matplotlib`:

```python
import plotly.graph_objects as go

def create_eoy_fan_chart(months, actual_data, p10_proj, p50_proj, p90_proj):
    fig = go.Figure()
    
    # Historisk linje
    fig.add_trace(go.Scatter(x=months[:len(actual_data)], y=actual_data, name="Faktisk (YTD)", line=dict(color="#1E3A8A", width=3)))
    
    # P50 Forventet
    fig.add_trace(go.Scatter(x=months[len(actual_data)-1:], y=p50_proj, name="P50 Forventet", line=dict(color="#DC2626", dash="dash")))
    
    # P10 Effekt med tiltak
    fig.add_trace(go.Scatter(x=months[len(actual_data)-1:], y=p10_proj, name="P10 Med Tiltak", line=dict(color="#16A34A", dash="dot")))
    
    fig.update_layout(
        title="<b>EOY Balanseprognose:</b> Effekt av tiltak bringer helårsresultatet tilbake til rammen",
        xaxis_title="Måned", yaxis_title="MNOK",
        template="plotly_white"
    )
    return fig
```

---

### 7. 🔒 Audit & Kildeforankring

Alle grafiske visninger i Office Hub og rapporteringsmodulene lenkes direkte til de underliggende transaksjonene i Visma ERP og rammevedtakene i Framsikt, samt det kryptografiske **SHA-256 stempel** for uforanderlig revisjonssporing.
