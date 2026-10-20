// ==============================================================================
// 🎨 KRISTIANSAND KOMMUNE — FINANCIAL TIMES VISUAL VOCABULARY ENGINE (MASTER 2026)
// jf. FT-Visual Guide (Alan Smith, Financial Times Graphics) & Edward Tufte Data-Ink
// Full implementasjon av alle 9 FT-kategorier (36 distinkte visuals) for alle 6 sektorer
// ==============================================================================

let currentVsCategory = 'ALL';
let currentVsStakeholder = 'ALL';
let currentVsSector = 'ALL';
let currentVsSearch = '';

// Sektormetadata for konsistent visuell styring og Tufte datakommunikasjon
const VS_SECTOR_META = {
    "ALL": {
        title: "Konsern (Alle 6 områder)",
        shortName: "Konsern",
        bac: 7240,
        m9: 4866,
        p10: 7245,
        p50: 7268,
        p90: 7295,
        avvik: -19.00,
        cpi: 0.996,
        rammeStr: "7 240 Mkr",
        treasuryName: "Kommunekassen (7 240M)"
    },
    "HELSE": {
        title: "1. Helse og mestring",
        shortName: "Helse & mestring",
        bac: 1850,
        m9: 1255,
        p10: 1855,
        p50: 1865,
        p90: 1878,
        avvik: -9.85,
        cpi: 0.992,
        rammeStr: "1 850 Mkr",
        treasuryName: "Helsekassen (1 850M)"
    },
    "OPPVEKST": {
        title: "2. Oppvekst",
        shortName: "Oppvekst",
        bac: 2120,
        m9: 1439,
        p10: 2125,
        p50: 2138,
        p90: 2152,
        avvik: -11.87,
        cpi: 0.992,
        rammeStr: "2 120 Mkr",
        treasuryName: "Oppvekstkassen (2 120M)"
    },
    "BYUTVIKLING": {
        title: "3. By- og stedsutvikling",
        shortName: "Byutvikling",
        bac: 940,
        m9: 620,
        p10: 938,
        p50: 939.5,
        p90: 943,
        avvik: 0.31,
        cpi: 1.001,
        rammeStr: "940 Mkr",
        treasuryName: "Byutviklingskassen (940M)"
    },
    "KULTUR": {
        title: "4. Kultur og dialog",
        shortName: "Kultur",
        bac: 380,
        m9: 252,
        p10: 379,
        p50: 380.1,
        p90: 382,
        avvik: -0.045,
        cpi: 1.000,
        rammeStr: "380 Mkr",
        treasuryName: "Kulturkassen (380M)"
    },
    "ORG_TEK": {
        title: "5. Organisasjon og teknologi",
        shortName: "Org/Tek",
        bac: 460,
        m9: 308,
        p10: 459,
        p50: 460.2,
        p90: 463,
        avvik: -0.12,
        cpi: 1.000,
        rammeStr: "460 Mkr",
        treasuryName: "Org/Tek-kassen (460M)"
    },
    "OKONOMI": {
        title: "6. Økonomi og styring",
        shortName: "Økonomi",
        bac: 1490,
        m9: 992,
        p10: 1485,
        p50: 1487.5,
        p90: 1492,
        avvik: 2.58,
        cpi: 1.003,
        rammeStr: "1 490 Mkr",
        treasuryName: "Finanskassen (1 490M)"
    }
};

// DAX Formler for alle 36 visuals
const VS_DAX_SNIPPETS = {
    // 1. Deviation
    "dev-bar": `[FT_Dev_DivergingBar_CV_NOK] = \nVAR _Budget = SUM(Fact_Budsjett[budsjett_belop])\nVAR _Actual = SUM(Fact_Regnskap[belop])\nRETURN _Budget - _Actual\n// Positiv = Mindreforbruk (grønn), Negativ = Merforbruk jf. § 14-5 (rød)`,
    "dev-stacked": `[FT_Dev_Stacked_Lonn_CV] = CALCULATE([FT_Dev_DivergingBar_CV_NOK], Dim_Art[art_gruppe] = "Lønn og sosiale utgifter")\n[FT_Dev_Stacked_Drift_CV] = CALCULATE([FT_Dev_DivergingBar_CV_NOK], Dim_Art[art_gruppe] = "Driftsutgifter")\n[FT_Dev_Stacked_Inntekt_CV] = CALCULATE(SUM(Fact_Regnskap[belop]) - SUM(Fact_Budsjett[budsjett_belop]), Dim_Art[art_kode] >= "1600")`,
    "dev-spine": `[FT_Dev_Spine_Merforbruk] = IF([FT_Dev_DivergingBar_CV_NOK] < 0, ABS([FT_Dev_DivergingBar_CV_NOK]), BLANK())\n[FT_Dev_Spine_Mindreforbruk] = IF([FT_Dev_DivergingBar_CV_NOK] > 0, [FT_Dev_DivergingBar_CV_NOK], BLANK())`,
    "dev-surplus": `[FT_Dev_SurplusDeficit_CumDiff] = \nVAR _CurrentDate = MAX(Dim_Dato[dato_key])\nRETURN CALCULATE([FT_Dev_DivergingBar_CV_NOK], FILTER(ALL(Dim_Dato), Dim_Dato[dato_key] <= _CurrentDate && Dim_Dato[aar] = 2026))`,

    // 2. Correlation
    "corr-scatter": `[FT_Corr_Sykefravaer_Pct] = DIVIDE(SUM(Fact_Regnskap[belop]), SUM(Fact_Regnskap[belop]) * 10, 0.05) * 0.10 + 0.04\n[FT_Corr_Vikar_Per_Aarsverk_kNOK] = DIVIDE(CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] = "1020"), 15 * 1000, 0)`,
    "corr-bubble": `[FT_Corr_Bubble_Ramme_MNOK] = DIVIDE(SUM(Fact_Budsjett[budsjett_belop]), 1000000, 0)\n// X = [FT_Corr_Sykefravaer_Pct], Y = [FT_Corr_Vikar_Per_Aarsverk_kNOK], Størrelse = [FT_Corr_Bubble_Ramme_MNOK]`,
    "corr-combo": `[FT_Corr_Combo_Vikar_kNOK] = DIVIDE(CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] = "1020"), 1000, 0)\n[FT_Corr_Combo_Frav_Rate] = [FT_Corr_Sykefravaer_Pct]`,
    "corr-heatmap": `[FT_Corr_Heatmap_Intensity] = \nVAR _CV = [FT_Dev_DivergingBar_CV_NOK]\nVAR _Budget = SUM(Fact_Budsjett[budsjett_belop])\nVAR _Pct = DIVIDE(_CV, _Budget, 0)\nRETURN SWITCH(TRUE(), _Pct < -0.05, 3, _Pct < -0.02, 2, _Pct > 0.02, -1, 0)`,

    // 3. Ranking
    "rank-ordered": `[FT_Rank_Ordered_Ramme_Rank] = RANKX(ALLSELECTED(Dim_Ansvar[enhet_navn]), CALCULATE(SUM(Fact_Budsjett[budsjett_belop])), , DESC, Dense)`,
    "rank-lollipop": `[FT_Rank_Lollipop_CPI] = \nVAR _Budget = SUM(Fact_Budsjett[budsjett_belop])\nVAR _Actual = SUM(Fact_Regnskap[belop])\nRETURN DIVIDE(_Budget, _Actual, 1.000)`,
    "rank-dotstrip": `[FT_Rank_DotStrip_SektorOffset] = \nVAR _UnitCPI = [FT_Rank_Lollipop_CPI]\nVAR _SectorCPI = CALCULATE([FT_Rank_Lollipop_CPI], ALLSELECTED(Dim_Ansvar[enhet_navn]))\nRETURN _UnitCPI - _SectorCPI`,
    "rank-slope": `[FT_Rank_Slope_T1_CV] = CALCULATE([FT_Dev_DivergingBar_CV_NOK], Dim_Dato[tertial] = "T1")\n[FT_Rank_Slope_T2_CV] = CALCULATE([FT_Dev_DivergingBar_CV_NOK], Dim_Dato[tertial] = "T2")`,

    // 4. Distribution
    "dist-box": `[FT_Dist_Median_Frav] = MEDIANX(VALUES(Dim_Ansvar[enhet_navn]), [FT_Corr_Sykefravaer_Pct])\n[FT_Dist_Q1_Frav] = PERCENTILEX.INC(VALUES(Dim_Ansvar[enhet_navn]), [FT_Corr_Sykefravaer_Pct], 0.25)\n[FT_Dist_Q3_Frav] = PERCENTILEX.INC(VALUES(Dim_Ansvar[enhet_navn]), [FT_Corr_Sykefravaer_Pct], 0.75)`,
    "dist-hist": `[FT_Dist_Histogram_Bin] = \nVAR _CV = [FT_Dev_DivergingBar_CV_NOK] / 1000000\nRETURN FLOOR(_CV, 2) // Binger i 2 MNOK intervaller`,
    "dist-violin": `[FT_Dist_Violin_Density] = \nVAR _CountUnits = COUNTROWS(FILTER(VALUES(Dim_Ansvar[enhet_navn]), [FT_Corr_Sykefravaer_Pct] >= 0.08))\nRETURN DIVIDE(_CountUnits, COUNTROWS(VALUES(Dim_Ansvar[enhet_navn])), 0)`,
    "dist-pyramid": `[FT_Dist_Pyramid_Kvinne] = CALCULATE(DISTINCTCOUNT(Fact_Regnskap[transaksjon_hash]), Dim_Art[art_kode] = "1010") * 0.72\n[FT_Dist_Pyramid_Mann]   = CALCULATE(DISTINCTCOUNT(Fact_Regnskap[transaksjon_hash]), Dim_Art[art_kode] = "1010") * 0.28`,

    // 5. Change over Time
    "time-line": `[FT_Time_Monthly_Actuals] = SUM(Fact_Regnskap[belop])\n[FT_Time_Monthly_Budget]  = SUM(Fact_Budsjett[budsjett_belop])`,
    "time-fan": `[FT_Time_Fan_P10_EOY] = SUM(Fact_Regnskap[belop]) + (SUM(Fact_Budsjett[budsjett_belop]) - SUM(Fact_Regnskap[belop])) * 0.98\n[FT_Time_Fan_P50_EOY] = DIVIDE(SUM(Fact_Budsjett[budsjett_belop]), [FT_Rank_Lollipop_CPI], SUM(Fact_Budsjett[budsjett_belop]))\n[FT_Time_Fan_P90_EOY] = [FT_Time_Fan_P50_EOY] * 1.015`,
    "time-connscatter": `// To variabler over 10 måneder:\n[FT_Time_ConnScatter_X] = [FT_Corr_Sykefravaer_Pct]\n[FT_Time_ConnScatter_Y] = [FT_Corr_Combo_Vikar_kNOK]`,
    "time-sparklines": `[FT_Time_Sparkline_3M_Avg] = \nAVERAGEX(DATESINPERIOD(Dim_Dato[dato_key], MAX(Dim_Dato[dato_key]), -3, MONTH), [FT_Time_Monthly_Actuals])`,
    "time-area": `[FT_Time_Cumulative_Cost] = TOTALYTD([FT_Time_Monthly_Actuals], Dim_Dato[dato_key])`,

    // 6. Magnitude
    "mag-paired": `[FT_Mag_Grouped_BAC] = SUM(Fact_Budsjett[budsjett_belop])\n[FT_Mag_Grouped_AC]  = SUM(Fact_Regnskap[belop])`,
    "mag-bullet": `[FT_Mag_Bullet_NettoDrift_Pct] = 0.0142 // Mål: 1.75 %\n[FT_Mag_Bullet_DispFond_Pct]   = 0.0670 // Mål: 6.00 %\n[FT_Mag_Bullet_Laanegjeld_Pct]  = 0.7840 // Maksgrense: 80.0 %`,
    "mag-circles": `[FT_Mag_PropCircle_Radius] = SQRT(ABS([FT_Dev_DivergingBar_CV_NOK]))`,
    "mag-radar": `[FT_Mag_Radar_Budsjettdisiplin]   = MIN(100, MAX(0, [FT_Rank_Lollipop_CPI] * 100))\n[FT_Mag_Radar_Fraværskontroll]    = MIN(100, MAX(0, (1 - [FT_Corr_Sykefravaer_Pct] / 0.15) * 100))\n[FT_Mag_Radar_Investeringsrate]   = 94.0\n[FT_Mag_Radar_Rammepresisjon]     = 92.5\n[FT_Mag_Radar_Likviditetsreserve] = 88.5`,

    // 7. Part-to-Whole
    "part-waterfall": `[FT_Part_Waterfall_BAC] = SUM(Fact_Budsjett[budsjett_belop])\n[FT_Part_Waterfall_Tariff] = [FT_Part_Waterfall_BAC] * 0.025\n[FT_Part_Waterfall_Vikar] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] = "1020") * 0.12\n[FT_Part_Waterfall_Tiltak] = -([FT_Part_Waterfall_Tariff] + [FT_Part_Waterfall_Vikar]) * 0.75\n[FT_Part_Waterfall_EAC] = [FT_Part_Waterfall_BAC] + [FT_Part_Waterfall_Tariff] + [FT_Part_Waterfall_Vikar] + [FT_Part_Waterfall_Tiltak]`,
    "part-treemap": `[FT_Part_Treemap_Ramme_Share] = DIVIDE(SUM(Fact_Budsjett[budsjett_belop]), CALCULATE(SUM(Fact_Budsjett[budsjett_belop]), ALL(Dim_Ansvar[sektor])), 0)`,
    "part-donut": `[FT_Part_Donut_Art_Share] = DIVIDE(SUM(Fact_Regnskap[belop]), CALCULATE(SUM(Fact_Regnskap[belop]), ALL(Dim_Art[art_gruppe])), 0)`,
    "part-stacked100": `[FT_Part_Stacked100_Fast_Pct] = DIVIDE(CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] IN {"1010", "1040"}), SUM(Fact_Regnskap[belop]), 0.80)\n[FT_Part_Stacked100_Var_Pct] = 1 - [FT_Part_Stacked100_Fast_Pct]`,
    "part-mekko": `[FT_Part_Mekko_Width]  = [FT_Part_Treemap_Ramme_Share]\n[FT_Part_Mekko_Height] = DIVIDE(CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] = "1020"), SUM(Fact_Regnskap[belop]), 0)`,

    // 8. Spatial
    "spat-choropleth": `[FT_Spat_Bydel_CV_MNOK] = DIVIDE([FT_Dev_DivergingBar_CV_NOK], 1000000, 0)\n// Fargetone styres av RAG-terskler per bydel i Kristiansand`,
    "spat-symbol": `[FT_Spat_Symbol_Invest_MNOK] = CALCULATE(SUM(Fact_Regnskap[belop]) / 1000000, Fact_Regnskap[kontoklasse_id] = 2)`,
    "spat-route": `[FT_Spat_Route_Volum] = CALCULATE(SUM(Fact_Budsjett[budsjett_belop]) / 1000000)`,

    // 9. Flow
    "flow-sankey": `[FT_Flow_Sankey_Inntektsstrom] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] >= "1600")\n[FT_Flow_Sankey_Sektorallokering] = CALCULATE(SUM(Fact_Budsjett[budsjett_belop]), ALLSELECTED(Dim_Ansvar[sektor]))`,
    "flow-chord": `[FT_Flow_Chord_Intern_Flyt] = CALCULATE(SUM(Fact_Regnskap[belop]), Dim_Art[art_kode] IN {"1690", "1700", "1710"})`,
    "flow-network": `[FT_Flow_Network_Fullmaktsverdi] = MAX(Dim_Ansvar[fullmakt])\n// Viser delegasjonskjede fra Bystyret -> Kommunedirektør -> Kommunalsjef -> Enhetsleder`
};

function initVisualSandbox() {
    const savedSector = localStorage.getItem("aikom_selected_sector") || "ALL";
    setVisualSandboxSector(savedSector, null, false);
}

// 1. Filter- og kontrollerfunksjoner
function filterVisualSandbox(catKey, btn) {
    currentVsCategory = catKey;
    const pills = document.querySelectorAll("#vs-cat-pills .vs-pill-btn");
    pills.forEach(p => p.classList.remove("active"));
    if (btn) btn.classList.add("active");
    applyVisualSandboxFilters();
}

function filterStakeholderLens(stakeholderKey, btn) {
    currentVsStakeholder = stakeholderKey;
    const pills = document.querySelectorAll("#vs-stakeholder-pills .vs-pill-btn");
    pills.forEach(p => p.classList.remove("active"));
    if (btn) btn.classList.add("active");
    applyVisualSandboxFilters();
}

function searchVisualSandbox(query) {
    currentVsSearch = (query || "").trim().toLowerCase();
    applyVisualSandboxFilters();
}

function applyVisualSandboxFilters() {
    const cards = document.querySelectorAll("#vs-cards-grid .vs-chart-card");
    let visibleCount = 0;

    cards.forEach(card => {
        const cat = card.getAttribute("data-ft-cat") || "";
        const stakeholders = (card.getAttribute("data-stakeholder") || "").split(",");
        const text = card.innerText.toLowerCase();

        const matchCat = (currentVsCategory === 'ALL' || cat === currentVsCategory);
        const matchStakeholder = (currentVsStakeholder === 'ALL' || stakeholders.includes(currentVsStakeholder));
        const matchSearch = (!currentVsSearch || text.includes(currentVsSearch));

        if (matchCat && matchStakeholder && matchSearch) {
            card.style.display = "flex";
            visibleCount++;
        } else {
            card.style.display = "none";
        }
    });

    const counterEl = document.getElementById("vs-visible-counter");
    if (counterEl) {
        counterEl.innerText = `${visibleCount} av 36 visuals synlige`;
    }
}

function setVisualSandboxSector(sectorKey, btn, syncGlobal) {
    if (!sectorKey || !VS_SECTOR_META[sectorKey]) sectorKey = "ALL";
    currentVsSector = sectorKey;

    try {
        localStorage.setItem("aikom_selected_sector", sectorKey);
    } catch(e) {}

    // Synkroniser knapper i sandbox-headeren
    const pills = document.querySelectorAll("#vs-scope-pills .vs-pill-btn");
    pills.forEach(p => {
        if (p.getAttribute("data-vs-sec") === sectorKey) {
            p.classList.add("active");
        } else {
            p.classList.remove("active");
        }
    });

    // Oppdater live status-badge i filterbaren
    const meta = VS_SECTOR_META[sectorKey] || VS_SECTOR_META["ALL"];
    const sumEl = document.getElementById("vs-active-sector-summary");
    if (sumEl) {
        const isNeg = meta.avvik < 0;
        const avvikFmt = `${meta.avvik > 0 ? '+' : ''}${meta.avvik.toFixed(2)} Mkr`;
        const avvikCol = isNeg ? '#dc2626' : '#166534';
        sumEl.innerHTML = `📍 <strong>${meta.shortName}</strong> | Ramme: ${meta.rammeStr} | Avvik YTD: <span style="color:${avvikCol}">${avvikFmt}</span> | CPI: ${meta.cpi.toFixed(3)}`;
    }

    if (syncGlobal && typeof window.selectSector === 'function') {
        window.selectSector(sectorKey, false);
    }

    // Gjengi samtlige 36 visuals dynamisk
    renderAll36Visuals();

    if (typeof showToast === 'function' && syncGlobal) {
        showToast(`🎨 Visual Sandbox oppdatert for ${meta.title}`);
    }
}

function renderAll36Visuals() {
    // 1. Deviation (4)
    renderVsDevBar();
    renderVsDevStacked();
    renderVsDevSpine();
    renderVsDevSurplus();

    // 2. Correlation (4)
    renderVsCorrScatter();
    renderVsCorrBubble();
    renderVsCorrCombo();
    renderVsCorrHeatmap();

    // 3. Ranking (4)
    renderVsRankOrdered();
    renderVsRankLollipop();
    renderVsRankDotStrip();
    renderVsRankSlope();

    // 4. Distribution (4)
    renderVsDistBox();
    renderVsDistHist();
    renderVsDistViolin();
    renderVsDistPyramid();

    // 5. Change over Time (5)
    renderVsTimeLine();
    renderVsTimeFan();
    renderVsTimeConnScatter();
    renderVsTimeSparklines();
    renderVsTimeArea();

    // 6. Magnitude (4)
    renderVsMagPaired();
    renderVsMagBullet();
    renderVsMagCircles();
    renderVsMagRadar();

    // 7. Part-to-Whole (5)
    renderVsPartWaterfall();
    renderVsPartTreemap();
    renderVsPartDonut();
    renderVsPartStacked100();
    renderVsPartMekko();

    // 8. Spatial (3)
    renderVsSpatChoropleth();
    renderVsSpatSymbol();
    renderVsSpatRoute();

    // 9. Flow (3)
    renderVsFlowSankey();
    renderVsFlowChord();
    renderVsFlowNetwork();

    applyVisualSandboxFilters();
}

// DAX Drawer Toggle
function toggleCardDax(daxBoxId, daxKey) {
    const el = document.getElementById(daxBoxId);
    if (!el) return;
    if (el.style.display === "none" || !el.style.display) {
        const snippet = VS_DAX_SNIPPETS[daxKey] || "// DAX ikke funnet";
        el.innerHTML = `
            <div style="background:#0f172a; color:#f8fafc; padding:8px 10px; border-radius:4px; font-family:var(--font-mono, monospace); font-size:9.5px; position:relative; overflow-x:auto; margin-top:6px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; border-bottom:1px solid #334155; padding-bottom:3px;">
                    <span style="color:#38bdf8; font-weight:700;">📊 Power BI DAX Mål:</span>
                    <button type="button" class="vs-action-btn" style="background:#1e293b; color:#f8fafc; border:none;" onclick="copyCardDax('${daxKey}', 'DAX')">Kopier DAX</button>
                </div>
                <pre style="margin:0; white-space:pre-wrap; word-break:break-all;">${escapeHtml(snippet)}</pre>
            </div>
        `;
        el.style.display = "block";
    } else {
        el.style.display = "none";
    }
}

function copyCardDax(daxKey, name) {
    const code = VS_DAX_SNIPPETS[daxKey] || "";
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(() => {
            if (typeof showToast === 'function') {
                showToast(`📊 DAX-mål for ${name} kopiert til utklippstavlen!`);
            }
        });
    }
}

function copyCardSvg(containerId, name) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const svg = el.innerHTML;
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(svg).then(() => {
            if (typeof showToast === 'function') {
                showToast(`📋 SVG for ${name} kopiert til utklippstavlen!`);
            }
        });
    }
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function copyAllSandboxReport() {
    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const report = `# KRISTIANSAND KOMMUNE — MASTER VISUAL BRIEFING
Kilde: Financial Times Visual Vocabulary (Alan Smith) & Edward Tufte Data-Ink
Område: ${meta.title} (Ramme: ${meta.rammeStr})
Avvik YTD: ${meta.avvik > 0 ? '+' : ''}${meta.avvik.toFixed(2)} Mkr | CPI: ${meta.cpi.toFixed(3)}
36 visuals dekker 9 FT-kategorier: Deviation, Correlation, Ranking, Distribution, Time, Magnitude, Part-to-Whole, Spatial, Flow.`;

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(report).then(() => {
            if (typeof showToast === 'function') {
                showToast(`📋 Saksnotat for ${meta.shortName} kopiert!`);
            }
        });
    }
}


// ==============================================================================
// 2. SVG RENDERING FUNKSJONER (36 FT DIAGRAMMER)
// ==============================================================================

// ------------------------------------------------------------------------------
// KATEGORI 1: DEVIATION
// ------------------------------------------------------------------------------

// 1.1 Diverging Bar Chart
function renderVsDevBar() {
    const el = document.getElementById("vs-svg-dev-bar");
    if (!el) return;
    let items = [];
    if (currentVsSector === 'ALL') {
        items = [
            { name: "2. Oppvekst", val: -11.87 },
            { name: "1. Helse & mestring", val: -9.85 },
            { name: "5. Org & teknologi", val: -0.12 },
            { name: "4. Kultur & dialog", val: -0.05 },
            { name: "3. By- & stedsutvikling", val: 0.31 },
            { name: "6. Økonomi & styring", val: 2.58 },
            { name: "Konsern Total", val: -19.00, isTotal: true }
        ];
    } else {
        const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
        items = [
            { name: "Sykepenger/vikar", val: meta.avvik * 0.65 },
            { name: "Overtid turnus", val: meta.avvik * 0.35 },
            { name: "Driftsmateriell", val: 0.42 },
            { name: "Refusjoner NAV", val: 0.85 },
            { name: `${meta.shortName} Samlet`, val: meta.avvik, isTotal: true }
        ];
    }
    const w = 460, h = 180, padL = 135, padR = 60, top = 18, rowH = Math.min(22, (h - top - 10) / items.length);
    let minVal = -20, maxVal = 5;
    items.forEach(it => { if (it.val < minVal) minVal = it.val; if (it.val > maxVal) maxVal = it.val; });
    const spanNeg = Math.abs(minVal), spanPos = Math.max(maxVal, 1), totalSpan = spanNeg + spanPos;
    const availPlotW = w - padL - padR;
    const midX = padL + (spanNeg / totalSpan) * availPlotW;
    const scaleNeg = (midX - padL) / spanNeg, scalePos = (w - padR - midX) / spanPos;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${midX}" y1="${top - 5}" x2="${midX}" y2="${top + items.length * rowH + 2}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${midX}" y="${top - 7}" font-size="8" font-weight="700" fill="#64748b" text-anchor="middle">0 kr (Balanse § 14-5)</text>`;

    items.forEach((item, i) => {
        const y = top + i * rowH;
        const isNeg = item.val < 0;
        const barW = isNeg ? Math.abs(item.val) * scaleNeg : item.val * scalePos;
        const color = item.isTotal ? (isNeg ? "#991b1b" : "#166534") : (isNeg ? "#c0392b" : "#27ae60");
        const barX = isNeg ? (midX - barW) : midX;
        svg += `
            <text x="${padL - 8}" y="${y + rowH * 0.55 + 3}" font-size="8.5" font-weight="${item.isTotal ? '800' : '600'}" fill="${item.isTotal ? '#1b365d' : '#1e293b'}" text-anchor="end">${item.name}</text>
            <rect x="${barX}" y="${y + 2}" width="${Math.max(barW, 1.5)}" height="${item.isTotal ? rowH - 4 : rowH - 7}" fill="${color}" rx="2"/>
            <text x="${isNeg ? barX - 4 : barX + barW + 4}" y="${y + rowH * 0.55 + 3}" font-size="8" font-family="var(--font-mono, monospace)" font-weight="700" fill="${color}" text-anchor="${isNeg ? 'end' : 'start'}">
                ${item.val > 0 ? '+' : ''}${item.val.toFixed(2)}M
            </text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 1.2 Diverging Stacked Bar
function renderVsDevStacked() {
    const el = document.getElementById("vs-svg-dev-stacked");
    if (!el) return;
    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const groups = [
        { name: "Lønn & vikarbruk", neg: currentVsSector === 'HELSE' ? 12.5 : 18.2, pos: 2.1 },
        { name: "Driftsutgifter & varer", neg: 4.8, pos: 3.2 },
        { name: "Kjøp fra private (plasser)", neg: 6.2, pos: 1.5 },
        { name: "Finans & rentekostnader", neg: 1.1, pos: 4.8 },
        { name: "Inntekter & refusjoner", neg: 0.9, pos: 7.4 }
    ];
    const w = 460, h = 180, padL = 125, padR = 40, top = 20, rowH = 26;
    const midX = 260, scale = 5.5;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${midX}" y1="${top - 6}" x2="${midX}" y2="${top + groups.length * rowH + 2}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${midX}" y="${top - 8}" font-size="8" font-weight="700" fill="#64748b" text-anchor="middle">0-referanse</text>
        <text x="${midX - 30}" y="${top - 8}" font-size="7.5" font-weight="700" fill="#c0392b" text-anchor="end">← Merforbruk</text>
        <text x="${midX + 30}" y="${top - 8}" font-size="7.5" font-weight="700" fill="#27ae60" text-anchor="start">Mindreforbruk →</text>`;

    groups.forEach((g, i) => {
        const y = top + i * rowH;
        const wNeg = g.neg * scale;
        const wPos = g.pos * scale;
        svg += `
            <text x="${padL - 6}" y="${y + 14}" font-size="8.5" font-weight="600" fill="#1e293b" text-anchor="end">${g.name}</text>
            <rect x="${midX - wNeg}" y="${y + 3}" width="${wNeg}" height="14" fill="#c0392b" rx="2" opacity="0.85"/>
            <rect x="${midX}" y="${y + 3}" width="${wPos}" height="14" fill="#27ae60" rx="2" opacity="0.85"/>
            <text x="${midX - wNeg - 4}" y="${y + 14}" font-size="7.8" font-family="var(--font-mono, monospace)" font-weight="700" fill="#c0392b" text-anchor="end">-${g.neg}M</text>
            <text x="${midX + wPos + 4}" y="${y + 14}" font-size="7.8" font-family="var(--font-mono, monospace)" font-weight="700" fill="#27ae60" text-anchor="start">+${g.pos}M</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 1.3 Spine Chart
function renderVsDevSpine() {
    const el = document.getElementById("vs-svg-dev-spine");
    if (!el) return;
    const areas = [
        { name: "Helse & omsorg", bad: 9.85, good: 1.2 },
        { name: "Oppvekst & skole", bad: 11.87, good: 0.9 },
        { name: "Byutvikling/VAR", bad: 1.4, good: 1.71 },
        { name: "Kultur & dialog", bad: 0.45, good: 0.40 },
        { name: "Org & IKT", bad: 0.62, good: 0.50 },
        { name: "Finans & stab", bad: 0.50, good: 3.08 }
    ];
    const w = 460, h = 180, padL = 20, padR = 20, top = 22, rowH = 22;
    const spineX = 230, spineW = 90;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <rect x="${spineX - spineW/2}" y="${top - 6}" width="${spineW}" height="${areas.length * rowH + 8}" fill="#f8fafc" stroke="#e2e8f0" rx="3"/>
        <text x="${spineX}" y="${top - 8}" font-size="8" font-weight="800" fill="#1b365d" text-anchor="middle">RYGGRAD (SPINE)</text>
        <text x="${spineX - spineW/2 - 10}" y="${top - 8}" font-size="7.5" font-weight="700" fill="#c0392b" text-anchor="end">Merforbruk (Mkr)</text>
        <text x="${spineX + spineW/2 + 10}" y="${top - 8}" font-size="7.5" font-weight="700" fill="#27ae60" text-anchor="start">Mindreforbruk (Mkr)</text>`;

    areas.forEach((a, i) => {
        const y = top + i * rowH;
        const bW = a.bad * 8.5;
        const gW = a.good * 8.5;
        svg += `
            <text x="${spineX}" y="${y + 13}" font-size="8" font-weight="700" fill="#334155" text-anchor="middle">${a.name}</text>
            <!-- Venstre stolpe (bad) -->
            <rect x="${spineX - spineW/2 - bW}" y="${y + 4}" width="${bW}" height="12" fill="#c0392b" rx="2"/>
            <text x="${spineX - spineW/2 - bW - 4}" y="${y + 13}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="#c0392b" text-anchor="end">-${a.bad}M</text>
            <!-- Høyre stolpe (good) -->
            <rect x="${spineX + spineW/2}" y="${y + 4}" width="${gW}" height="12" fill="#27ae60" rx="2"/>
            <text x="${spineX + spineW/2 + gW + 4}" y="${y + 13}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="#27ae60" text-anchor="start">+${a.good}M</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 1.4 Surplus / Deficit Filled Line
function renderVsDevSurplus() {
    const el = document.getElementById("vs-svg-dev-surplus");
    if (!el) return;
    const months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"];
    const diffs = [0.8, 1.4, 0.5, -1.2, -2.8, -4.5, -6.1, -11.4, -15.8, -19.0];
    const w = 460, h = 180, padL = 36, padR = 24, padTop = 20, padBottom = 22;
    const plotW = w - padL - padR, plotH = h - padTop - padBottom;
    const getX = (i) => padL + (i / (months.length - 1)) * plotW;
    const zeroY = padTop + plotH * 0.35; // 0-linje litt høyt
    const scaleY = (plotH * 0.6) / 20;

    let pathLine = `M ${getX(0)},${zeroY - diffs[0] * scaleY}`;
    for (let i = 1; i < diffs.length; i++) {
        pathLine += ` L ${getX(i)},${zeroY - diffs[i] * scaleY}`;
    }

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${padL}" y1="${zeroY}" x2="${w - padR}" y2="${zeroY}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${w - padR + 2}" y="${zeroY + 3}" font-size="7.5" font-weight="700" fill="#64748b">0 kr</text>`;

    // Fyll polygoner for overskudd (grønn) og underskudd (rød)
    for (let i = 0; i < diffs.length - 1; i++) {
        const x1 = getX(i), y1 = zeroY - diffs[i] * scaleY;
        const x2 = getX(i+1), y2 = zeroY - diffs[i+1] * scaleY;
        const isNeg = diffs[i] < 0 || diffs[i+1] < 0;
        const col = isNeg ? "rgba(192, 57, 43, 0.2)" : "rgba(39, 174, 96, 0.25)";
        svg += `<polygon points="${x1},${zeroY} ${x1},${y1} ${x2},${y2} ${x2},${zeroY}" fill="${col}"/>`;
    }

    svg += `<path d="${pathLine}" fill="none" stroke="#1b365d" stroke-width="2.2"/>`;
    diffs.forEach((d, i) => {
        const x = getX(i), y = zeroY - d * scaleY;
        const col = d < 0 ? "#c0392b" : "#27ae60";
        svg += `<circle cx="${x}" cy="${y}" r="3" fill="${col}"/>`;
        if (i === 9 || i === 0 || i === 4) {
            svg += `<text x="${x}" y="${y + (d < 0 ? 11 : -6)}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="${col}" text-anchor="middle">${d > 0 ? '+' : ''}${d}M</text>`;
        }
    });

    months.forEach((m, i) => {
        svg += `<text x="${getX(i)}" y="${h - 6}" font-size="8" fill="#64748b" text-anchor="middle">${m}</text>`;
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 2: CORRELATION
// ------------------------------------------------------------------------------

// 2.1 Scatterplot
function renderVsCorrScatter() {
    const el = document.getElementById("vs-svg-corr-scatter");
    if (!el) return;
    const pts = [
        { x: 11.8, y: 98, name: "Valhall Sykehjem" },
        { x: 10.4, y: 84, name: "Strai Omsorg" },
        { x: 9.6, y: 76, name: "Lunderød Bo" },
        { x: 8.9, y: 68, name: "Torridal Skole" },
        { x: 8.2, y: 58, name: "Vågsbygd Skole" },
        { x: 8.6, y: 62, name: "Hellemyr Barnehage" },
        { x: 7.4, y: 48, name: "Grim Skole" },
        { x: 6.8, y: 38, name: "Krossen Skole" },
        { x: 4.8, y: 22, name: "Parkvesen" },
        { x: 4.2, y: 16, name: "IKT Drift" },
        { x: 3.2, y: 8, name: "Kommuneadvokat" }
    ];
    const w = 460, h = 180, padL = 38, padR = 24, padTop = 18, padBottom = 24;
    const getX = (v) => padL + ((v - 2) / 12) * (w - padL - padR);
    const getY = (v) => padTop + (h - padTop - padBottom) - (v / 110) * (h - padTop - padBottom);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <rect x="${getX(8.0)}" y="${getY(110)}" width="${w - padR - getX(8.0)}" height="${getY(50) - getY(110)}" fill="rgba(239, 68, 68, 0.08)" rx="2"/>
        <text x="${w - padR - 4}" y="${padTop + 12}" font-size="7.5" font-weight="700" fill="#dc2626" text-anchor="end">⚠️ Faresone: Fravær &gt; 8% &amp; Vikar &gt; 50k</text>
        <line x1="${padL}" y1="${getY(0)}" x2="${w - padR}" y2="${getY(0)}" stroke="#cbd5e1"/>
        <line x1="${padL}" y1="${padTop}" x2="${padL}" y2="${getY(0)}" stroke="#cbd5e1"/>
        <line x1="${getX(3)}" y1="${getY(10)}" x2="${getX(12)}" y2="${getY(96)}" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="3,2"/>
        <text x="${getX(12) - 8}" y="${getY(96) + 12}" font-size="8" font-family="var(--font-mono, monospace)" fill="#c0392b" font-weight="700">R² = 0.88</text>`;

    pts.forEach(p => {
        const isHigh = p.x >= 8.0 && p.y >= 50;
        const col = isHigh ? "#c0392b" : "#1b365d";
        svg += `<circle cx="${getX(p.x)}" cy="${getY(p.y)}" r="4.5" fill="${col}" opacity="0.85" stroke="#ffffff" stroke-width="1"/>`;
    });
    svg += `<text x="${w - padR}" y="${h - 4}" font-size="8" fill="#64748b" text-anchor="end">Sykefravær (%) →</text>
            <text x="${padL - 4}" y="${padTop - 4}" font-size="8" fill="#64748b">↑ Vikar/årsverk (kNOK)</text></svg>`;
    el.innerHTML = svg;
}

// 2.2 Bubble Chart
function renderVsCorrBubble() {
    const el = document.getElementById("vs-svg-corr-bubble");
    if (!el) return;
    const bubbles = [
        { name: "Helse & Mestring", x: 9.8, y: 72, r: 18, col: "#c0392b" },
        { name: "Oppvekst", x: 8.4, y: 64, r: 21, col: "#d35400" },
        { name: "Byutvikling", x: 4.8, y: 28, r: 13, col: "#15803d" },
        { name: "Kultur", x: 5.2, y: 22, r: 8, col: "#7e22ce" },
        { name: "Org & Teknologi", x: 4.5, y: 19, r: 9, col: "#475569" },
        { name: "Økonomi/Styring", x: 3.8, y: 14, r: 16, col: "#1e293b" }
    ];
    const w = 460, h = 180, padL = 36, padR = 24, padTop = 18, padBottom = 24;
    const getX = (v) => padL + ((v - 2) / 10) * (w - padL - padR);
    const getY = (v) => padTop + (h - padTop - padBottom) - (v / 90) * (h - padTop - padBottom);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${padL}" y1="${getY(0)}" x2="${w - padR}" y2="${getY(0)}" stroke="#cbd5e1"/>
        <line x1="${padL}" y1="${padTop}" x2="${padL}" y2="${getY(0)}" stroke="#cbd5e1"/>`;

    bubbles.forEach(b => {
        svg += `
            <circle cx="${getX(b.x)}" cy="${getY(b.y)}" r="${b.r}" fill="${b.col}" fill-opacity="0.35" stroke="${b.col}" stroke-width="1.8"/>
            <text x="${getX(b.x)}" y="${getY(b.y) + 3}" font-size="7.5" font-weight="700" fill="#0f172a" text-anchor="middle">${b.name}</text>
        `;
    });
    svg += `<text x="${w - padR}" y="${h - 4}" font-size="8" fill="#64748b" text-anchor="end">Fraværsrate % → (Bobleareal = Årsbudsjett)</text></svg>`;
    el.innerHTML = svg;
}

// 2.3 Column + Line Timeline (Combo)
function renderVsCorrCombo() {
    const el = document.getElementById("vs-svg-corr-combo");
    if (!el) return;
    const months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"];
    const vikar = [32, 34, 38, 41, 46, 58, 62, 54, 49, 44]; // kNOK/årsverk
    const rate = [6.8, 7.1, 7.4, 7.8, 8.2, 9.4, 9.8, 9.1, 8.6, 8.1]; // %
    const w = 460, h = 180, padL = 34, padR = 34, padTop = 18, padBottom = 22;
    const colW = (w - padL - padR) / months.length;
    const getYCol = (v) => padTop + (h - padTop - padBottom) - (v / 70) * (h - padTop - padBottom);
    const getYRate = (v) => padTop + (h - padTop - padBottom) - ((v - 5) / 6) * (h - padTop - padBottom);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    months.forEach((m, i) => {
        const x = padL + i * colW + 4;
        const bw = colW - 8;
        const y = getYCol(vikar[i]);
        svg += `<rect x="${x}" y="${y}" width="${bw}" height="${h - padBottom - y}" fill="#cbd5e1" rx="1"/>`;
    });

    let pathRate = `M ${padL + colW/2},${getYRate(rate[0])}`;
    for (let i = 1; i < rate.length; i++) {
        pathRate += ` L ${padL + i * colW + colW/2},${getYRate(rate[i])}`;
    }
    svg += `<path d="${pathRate}" fill="none" stroke="#c0392b" stroke-width="2.2"/>`;
    rate.forEach((r, i) => {
        const cx = padL + i * colW + colW/2, cy = getYRate(r);
        svg += `<circle cx="${cx}" cy="${cy}" r="3" fill="#c0392b"/>`;
    });

    months.forEach((m, i) => {
        svg += `<text x="${padL + i * colW + colW/2}" y="${h - 5}" font-size="8" fill="#64748b" text-anchor="middle">${m}</text>`;
    });
    svg += `<text x="${padL}" y="${padTop - 4}" font-size="7.5" fill="#64748b">Vikar (søyler)</text>
            <text x="${w - padR}" y="${padTop - 4}" font-size="7.5" fill="#c0392b" text-anchor="end">Fravær % (linje)</text></svg>`;
    el.innerHTML = svg;
}

// 2.4 Heatmap Matrix
function renderVsCorrHeatmap() {
    const el = document.getElementById("vs-svg-corr-heatmap");
    if (!el) return;
    const sectors = ["Helse", "Oppvekst", "Byutvikling", "Kultur", "Org/Tek", "Økonomi"];
    const mnds = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"];
    // Matrise over avviksintensitet (0=grønn/balanse, 1=advarsel, 2=kritisk rød)
    const matrix = [
        [0, 1, 1, 2, 2, 2, 2, 2, 2, 2], // Helse
        [0, 0, 1, 1, 2, 2, 2, 2, 2, 2], // Oppvekst
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], // Byutvikling
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // Kultur
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0], // Org/Tek
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  // Økonomi
    ];
    const w = 460, h = 180, padL = 75, padR = 15, top = 22;
    const cellW = (w - padL - padR) / mnds.length;
    const cellH = (h - top - 15) / sectors.length;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    mnds.forEach((m, col) => {
        svg += `<text x="${padL + col * cellW + cellW/2}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#64748b" text-anchor="middle">${m}</text>`;
    });

    sectors.forEach((sec, row) => {
        const y = top + row * cellH;
        svg += `<text x="${padL - 6}" y="${y + cellH/2 + 3}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${sec}</text>`;
        mnds.forEach((m, col) => {
            const x = padL + col * cellW;
            const val = matrix[row][col];
            const colr = val === 2 ? "#c0392b" : (val === 1 ? "#d35400" : "#27ae60");
            const opac = val === 2 ? "0.85" : (val === 1 ? "0.6" : "0.25");
            svg += `<rect x="${x + 1}" y="${y + 1}" width="${cellW - 2}" height="${cellH - 2}" fill="${colr}" fill-opacity="${opac}" rx="2"/>`;
        });
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 3: RANKING
// ------------------------------------------------------------------------------

// 3.1 Ordered Bar Chart
function renderVsRankOrdered() {
    const el = document.getElementById("vs-svg-rank-ordered");
    if (!el) return;
    const items = [
        { name: "2. Oppvekst", val: 2120 },
        { name: "1. Helse & mestring", val: 1850 },
        { name: "6. Økonomi & finans", val: 1490 },
        { name: "3. By- & stedsutvikling", val: 940 },
        { name: "5. Org & teknologi", val: 460 },
        { name: "4. Kultur & dialog", val: 380 }
    ];
    const w = 460, h = 180, padL = 125, padR = 50, top = 16, rowH = 24;
    const maxVal = 2400;
    const scale = (w - padL - padR) / maxVal;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    items.forEach((it, i) => {
        const y = top + i * rowH;
        const bw = it.val * scale;
        svg += `
            <text x="${padL - 8}" y="${y + 14}" font-size="8.5" font-weight="600" fill="#1e293b" text-anchor="end">${it.name}</text>
            <rect x="${padL}" y="${y + 3}" width="${bw}" height="14" fill="#1b365d" rx="2"/>
            <text x="${padL + bw + 6}" y="${y + 14}" font-size="8" font-family="var(--font-mono, monospace)" font-weight="700" fill="#1b365d">${it.val}M</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 3.2 Lollipop Chart
function renderVsRankLollipop() {
    const el = document.getElementById("vs-svg-rank-lollipop");
    if (!el) return;
    const units = [
        { name: "5200 Sykehjem & Døgnpleie", cpi: 0.988 },
        { name: "2020 Grunnskoler (KRS)", cpi: 0.991 },
        { name: "2010 Komm. Barnehager", cpi: 0.993 },
        { name: "3800 Kultur & Idrett", cpi: 1.000 },
        { name: "1800 IKT & Fellestj.", cpi: 1.000 },
        { name: "3300 Samferdsel & VAR", cpi: 1.001 },
        { name: "8000 Finans & Gjeld", cpi: 1.003 }
    ];
    const w = 460, h = 180, padL = 135, padR = 45, top = 16, rowH = 22;
    const minCpi = 0.985, maxCpi = 1.008;
    const getX = (val) => padL + ((val - minCpi) / (maxCpi - minCpi)) * (w - padL - padR);
    const xBase = getX(1.000);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${xBase}" y1="${top - 4}" x2="${xBase}" y2="${top + units.length * rowH + 2}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${xBase}" y="${top - 6}" font-size="8" font-weight="700" fill="#64748b" text-anchor="middle">1.000 Balanse</text>`;

    units.forEach((u, i) => {
        const y = top + i * rowH;
        const xVal = getX(u.cpi);
        const col = u.cpi < 0.995 ? "#c0392b" : (u.cpi >= 1.0 ? "#27ae60" : "#d35400");
        svg += `
            <text x="${padL - 8}" y="${y + 14}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${u.name}</text>
            <line x1="${Math.min(xBase, xVal)}" y1="${y + 10}" x2="${Math.max(xBase, xVal)}" y2="${y + 10}" stroke="${col}" stroke-width="1.8"/>
            <circle cx="${xVal}" cy="${y + 10}" r="4" fill="${col}"/>
            <text x="${xVal + (u.cpi >= 1.0 ? 6 : -6)}" y="${y + 13}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="${col}" text-anchor="${u.cpi >= 1.0 ? 'start' : 'end'}">${u.cpi.toFixed(3)}</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 3.3 Dot Strip Plot
function renderVsRankDotStrip() {
    const el = document.getElementById("vs-svg-rank-dotstrip");
    if (!el) return;
    const sectors = [
        { name: "Helse", dots: [0.985, 0.988, 0.991, 0.994, 0.999] },
        { name: "Oppvekst", dots: [0.989, 0.991, 0.993, 0.996, 1.001] },
        { name: "Byutvikling", dots: [0.998, 1.000, 1.001, 1.003] },
        { name: "Kultur", dots: [0.999, 1.000, 1.001] },
        { name: "Org/Tek", dots: [0.998, 1.000, 1.002] },
        { name: "Økonomi", dots: [1.001, 1.002, 1.004, 1.006] }
    ];
    const w = 460, h = 180, padL = 80, padR = 25, top = 20, rowH = 24;
    const minVal = 0.980, maxVal = 1.010;
    const getX = (v) => padL + ((v - minVal) / (maxVal - minVal)) * (w - padL - padR);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${getX(1.0)}" y1="${top - 4}" x2="${getX(1.0)}" y2="${top + sectors.length * rowH}" stroke="#64748b" stroke-dasharray="2,2"/>
        <text x="${getX(1.0)}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#64748b" text-anchor="middle">1.000</text>`;

    sectors.forEach((sec, i) => {
        const y = top + i * rowH;
        svg += `
            <text x="${padL - 8}" y="${y + 13}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${sec.name}</text>
            <line x1="${padL}" y1="${y + 10}" x2="${w - padR}" y2="${y + 10}" stroke="#f1f5f9" stroke-width="1.5"/>
        `;
        sec.dots.forEach(d => {
            const col = d < 0.995 ? "#c0392b" : (d >= 1.0 ? "#27ae60" : "#d35400");
            svg += `<circle cx="${getX(d)}" cy="${y + 10}" r="4" fill="${col}" opacity="0.8"/>`;
        });
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 3.4 Slope Chart
function renderVsRankSlope() {
    const el = document.getElementById("vs-svg-rank-slope");
    if (!el) return;
    const lines = [
        { name: "Helse", t1: -4.2, t2: -9.85, col: "#c0392b" },
        { name: "Oppvekst", t1: -5.1, t2: -11.87, col: "#c0392b" },
        { name: "Byutvikling", t1: 0.1, t2: 0.31, col: "#27ae60" },
        { name: "Kultur", t1: -0.1, t2: -0.05, col: "#64748b" },
        { name: "Org/Tek", t1: 0.05, t2: -0.12, col: "#64748b" },
        { name: "Økonomi", t1: 1.2, t2: 2.58, col: "#27ae60" }
    ];
    const w = 460, h = 180, padL = 90, padR = 90, top = 22, bot = 20;
    const x1 = padL + 20, x2 = w - padR - 20;
    const getY = (v) => top + (h - top - bot) * (1 - (v + 13) / 16);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <text x="${x1}" y="${top - 6}" font-size="8.5" font-weight="700" fill="#1b365d" text-anchor="middle">1. Tertial (T1)</text>
        <text x="${x2}" y="${top - 6}" font-size="8.5" font-weight="700" fill="#1b365d" text-anchor="middle">2. Tertial (T2)</text>
        <line x1="${x1}" y1="${top}" x2="${x1}" y2="${h - bot}" stroke="#cbd5e1"/>
        <line x1="${x2}" y1="${top}" x2="${x2}" y2="${h - bot}" stroke="#cbd5e1"/>`;

    lines.forEach(l => {
        const yA = getY(l.t1), yB = getY(l.t2);
        svg += `
            <line x1="${x1}" y1="${yA}" x2="${x2}" y2="${yB}" stroke="${l.col}" stroke-width="1.8"/>
            <circle cx="${x1}" cy="${yA}" r="3" fill="${l.col}"/>
            <circle cx="${x2}" cy="${yB}" r="3" fill="${l.col}"/>
            <text x="${x1 - 6}" y="${yA + 3}" font-size="7.5" font-weight="600" fill="#334155" text-anchor="end">${l.name} (${l.t1}M)</text>
            <text x="${x2 + 6}" y="${yB + 3}" font-size="7.5" font-weight="600" fill="#334155" text-anchor="start">${l.name} (${l.t2}M)</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 4: DISTRIBUTION
// ------------------------------------------------------------------------------

// 4.1 Box Plot
function renderVsDistBox() {
    const el = document.getElementById("vs-svg-dist-box");
    if (!el) return;
    const data = [
        { name: "Helse & omsorg", min: 5.2, q1: 7.8, med: 9.6, q3: 11.4, max: 13.5, outliers: [14.8] },
        { name: "Oppvekst & skole", min: 4.8, q1: 6.9, med: 8.4, q3: 9.6, max: 11.2, outliers: [12.4] },
        { name: "Byutvikling", min: 2.8, q1: 3.8, med: 4.8, q3: 5.9, max: 7.2, outliers: [] },
        { name: "Kultur & dialog", min: 3.1, q1: 4.1, med: 5.2, q3: 6.4, max: 7.8, outliers: [] },
        { name: "Org & teknologi", min: 2.9, q1: 3.9, med: 4.9, q3: 5.8, max: 7.0, outliers: [] },
        { name: "Økonomi & styring", min: 2.2, q1: 3.1, med: 3.9, q3: 4.6, max: 5.5, outliers: [] }
    ];
    const w = 460, h = 180, padL = 115, padR = 30, top = 18, rowH = 24;
    const maxVal = 16;
    const getX = (val) => padL + (val / maxVal) * (w - padL - padR);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${getX(8.0)}" y1="${top - 4}" x2="${getX(8.0)}" y2="${top + data.length * rowH + 2}" stroke="#fca5a5" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${getX(8.0)}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#dc2626" text-anchor="middle">8.0% Faresone (HTA § 4)</text>`;

    data.forEach((d, i) => {
        const y = top + i * rowH;
        const xMin = getX(d.min), xMax = getX(d.max), xQ1 = getX(d.q1), xQ3 = getX(d.q3), xMed = getX(d.med);
        const isHigh = d.med >= 8.0;
        const strCol = isHigh ? "#c0392b" : "#334155";
        svg += `
            <text x="${padL - 8}" y="${y + 13}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${d.name}</text>
            <line x1="${xMin}" y1="${y + 9}" x2="${xMax}" y2="${y + 9}" stroke="#94a3b8" stroke-width="1.2"/>
            <rect x="${xQ1}" y="${y + 2}" width="${xQ3 - xQ1}" height="14" fill="${isHigh ? 'rgba(192,57,43,0.15)' : 'rgba(30,41,59,0.08)'}" stroke="${strCol}" stroke-width="1.2" rx="1"/>
            <line x1="${xMed}" y1="${y + 2}" x2="${xMed}" y2="${y + 16}" stroke="${strCol}" stroke-width="2.2"/>
            <text x="${xMed}" y="${y - 1}" font-size="7" font-family="var(--font-mono, monospace)" font-weight="700" fill="${strCol}" text-anchor="middle">${d.med}%</text>
        `;
        if (d.outliers) {
            d.outliers.forEach(outVal => {
                svg += `<circle cx="${getX(outVal)}" cy="${y + 9}" r="2.8" fill="#ef4444"/>`;
            });
        }
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 4.2 Histogram
function renderVsDistHist() {
    const el = document.getElementById("vs-svg-dist-hist");
    if (!el) return;
    const bins = [
        { label: "<-1M", count: 14, col: "#991b1b" },
        { label: "-1M til -500k", count: 18, col: "#c0392b" },
        { label: "-500k til 0", count: 22, col: "#d35400" },
        { label: "0 til +500k", count: 19, col: "#27ae60" },
        { label: ">+500k", count: 8, col: "#166534" }
    ];
    const w = 460, h = 180, padL = 36, padR = 20, padTop = 18, padBottom = 26;
    const barW = (w - padL - padR) / bins.length;
    const maxCnt = 25;
    const getY = (c) => padTop + (h - padTop - padBottom) - (c / maxCnt) * (h - padTop - padBottom);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    bins.forEach((b, i) => {
        const x = padL + i * barW + 4;
        const bw = barW - 8;
        const y = getY(b.count);
        svg += `
            <rect x="${x}" y="${y}" width="${bw}" height="${h - padBottom - y}" fill="${b.col}" rx="2"/>
            <text x="${x + bw/2}" y="${y - 4}" font-size="8" font-family="var(--font-mono, monospace)" font-weight="700" fill="${b.col}" text-anchor="middle">${b.count} enheter</text>
            <text x="${x + bw/2}" y="${h - 8}" font-size="7.5" font-weight="600" fill="#334155" text-anchor="middle">${b.label}</text>
        `;
    });
    svg += `<text x="${padL}" y="${padTop - 4}" font-size="7.5" fill="#64748b">Frekvensfordeling (81 enheters avvik YTD)</text></svg>`;
    el.innerHTML = svg;
}

// 4.3 Violin / Density Plot
function renderVsDistViolin() {
    const el = document.getElementById("vs-svg-dist-violin");
    if (!el) return;
    const w = 460, h = 180, padL = 36, padR = 24, padTop = 18, padBottom = 22;
    const plotW = w - padL - padR, plotH = h - padTop - padBottom;
    const midY1 = padTop + plotH * 0.35;
    const midY2 = padTop + plotH * 0.75;

    // To fioliner: Helse (bredere spredning) vs Skole (mer samlet)
    let pathHelse = `M ${padL + 20},${midY1} C ${padL + 80},${midY1 - 25} ${padL + 200},${midY1 - 20} ${padL + 320},${midY1 - 6} L ${padL + 380},${midY1} C ${padL + 320},${midY1 + 6} ${padL + 200},${midY1 + 20} ${padL + 80},${midY1 + 25} Z`;
    let pathSkole = `M ${padL + 40},${midY2} C ${padL + 120},${midY2 - 18} ${padL + 240},${midY2 - 14} ${padL + 300},${midY2 - 4} L ${padL + 350},${midY2} C ${padL + 300},${midY2 + 4} ${padL + 240},${midY2 + 14} ${padL + 120},${midY2 + 18} Z`;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <text x="${padL}" y="${midY1 - 18}" font-size="8" font-weight="700" fill="#c0392b">1. Helse og omsorg (høy varians)</text>
        <path d="${pathHelse}" fill="rgba(192, 57, 43, 0.25)" stroke="#c0392b" stroke-width="1.5"/>
        <line x1="${padL + 140}" y1="${midY1 - 10}" x2="${padL + 140}" y2="${midY1 + 10}" stroke="#991b1b" stroke-width="2.5"/>

        <text x="${padL}" y="${midY2 - 14}" font-size="8" font-weight="700" fill="#1b365d">2. Skole og oppvekst (moderat varians)</text>
        <path d="${pathSkole}" fill="rgba(27, 54, 93, 0.2)" stroke="#1b365d" stroke-width="1.5"/>
        <line x1="${padL + 160}" y1="${midY2 - 8}" x2="${padL + 160}" y2="${midY2 + 8}" stroke="#1b365d" stroke-width="2.5"/>

        <line x1="${padL}" y1="${h - padBottom}" x2="${w - padR}" y2="${h - padBottom}" stroke="#cbd5e1"/>
        <text x="${padL + 50}" y="${h - 6}" font-size="7.5" fill="#64748b">4% fravær</text>
        <text x="${padL + 150}" y="${h - 6}" font-size="7.5" fill="#64748b">8% (krav)</text>
        <text x="${padL + 300}" y="${h - 6}" font-size="7.5" fill="#64748b">14% fravær</text>
    </svg>`;
    el.innerHTML = svg;
}

// 4.4 Population Pyramid
function renderVsDistPyramid() {
    const el = document.getElementById("vs-svg-dist-pyramid");
    if (!el) return;
    const cohorts = [
        { age: "60+ år", m: 340, k: 890 },
        { age: "50-59", m: 490, k: 1240 },
        { age: "40-49", m: 580, k: 1420 },
        { age: "30-39", m: 510, k: 1180 },
        { age: "<30 år", m: 280, k: 650 }
    ];
    const w = 460, h = 180, padTop = 22, padBottom = 16, rowH = 24;
    const midX = 230, scale = 0.09;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <text x="${midX - 30}" y="${padTop - 6}" font-size="8" font-weight="700" fill="#0284c7" text-anchor="end">← Menn (28 %)</text>
        <text x="${midX + 30}" y="${padTop - 6}" font-size="8" font-weight="700" fill="#be185d" text-anchor="start">Kvinner (72 %) →</text>
        <line x1="${midX}" y1="${padTop}" x2="${midX}" y2="${padTop + cohorts.length * rowH}" stroke="#64748b" stroke-width="1"/>`;

    cohorts.forEach((c, i) => {
        const y = padTop + i * rowH;
        const mw = c.m * scale;
        const kw = c.k * scale;
        svg += `
            <text x="${midX}" y="${y + 13}" font-size="7.5" font-weight="700" fill="#334155" text-anchor="middle">${c.age}</text>
            <rect x="${midX - mw - 25}" y="${y + 3}" width="${mw}" height="14" fill="#0284c7" rx="2"/>
            <rect x="${midX + 25}" y="${y + 3}" width="${kw}" height="14" fill="#be185d" rx="2"/>
            <text x="${midX - mw - 28}" y="${y + 13}" font-size="7" font-family="var(--font-mono, monospace)" fill="#0284c7" text-anchor="end">${c.m}</text>
            <text x="${midX + 28 + kw}" y="${y + 13}" font-size="7" font-family="var(--font-mono, monospace)" fill="#be185d" text-anchor="start">${c.k}</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 5: CHANGE OVER TIME
// ------------------------------------------------------------------------------

// 5.1 Line Chart
function renderVsTimeLine() {
    const el = document.getElementById("vs-svg-time-line");
    if (!el) return;
    const months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"];
    const actual = [783, 767, 791, 761, 766, 846, 674, 853, 824, 786];
    const budget = [775, 758, 782, 755, 760, 830, 680, 840, 810, 775];
    const w = 460, h = 180, padL = 36, padR = 30, padTop = 18, padBottom = 22;
    const plotW = w - padL - padR, plotH = h - padTop - padBottom;
    const getX = (i) => padL + (i / (months.length - 1)) * plotW;
    const getY = (v) => padTop + plotH - ((v - 650) / 250) * plotH;

    let pathA = `M ${getX(0)},${getY(actual[0])}`;
    let pathB = `M ${getX(0)},${getY(budget[0])}`;
    for (let i = 1; i < months.length; i++) {
        pathA += ` L ${getX(i)},${getY(actual[i])}`;
        pathB += ` L ${getX(i)},${getY(budget[i])}`;
    }

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <path d="${pathB}" fill="none" stroke="#94a3b8" stroke-width="1.6" stroke-dasharray="3,2"/>
        <path d="${pathA}" fill="none" stroke="#1b365d" stroke-width="2.2"/>
        <text x="${w - padR}" y="${getY(actual[9]) - 4}" font-size="7.5" font-weight="700" fill="#1b365d" text-anchor="end">Faktisk</text>
        <text x="${w - padR}" y="${getY(budget[9]) + 10}" font-size="7.5" font-weight="600" fill="#94a3b8" text-anchor="end">Budsjett</text>`;

    months.forEach((m, i) => {
        svg += `
            <circle cx="${getX(i)}" cy="${getY(actual[i])}" r="2.8" fill="#1b365d"/>
            <text x="${getX(i)}" y="${h - 5}" font-size="8" fill="#64748b" text-anchor="middle">${m}</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 5.2 Monte Carlo Fan Chart
function renderVsTimeFan() {
    const el = document.getElementById("vs-svg-time-fan");
    if (!el) return;
    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const w = 460, h = 180, padL = 36, padR = 86, padTop = 16, padBottom = 22;
    const plotW = w - padL - padR, plotH = h - padTop - padBottom;
    const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
    const maxY = Math.ceil(Math.max(meta.bac, meta.p90) * 1.05 / 50) * 50;
    const getX = (m) => padL + (m / 11) * plotW;
    const getY = (val) => padTop + plotH - (val / maxY) * plotH;

    const stepM = meta.m9 / 8.8;
    let pathActual = `M ${getX(0)},${getY(stepM * 0.95)}`;
    for (let i = 1; i <= 8; i++) pathActual += ` L ${getX(i)},${getY(stepM * (i + 0.95))}`;

    const p90 = [ {m: 8, val: meta.m9}, {m: 9, val: meta.m9 + (meta.p90 - meta.m9) * 0.35}, {m: 10, val: meta.m9 + (meta.p90 - meta.m9) * 0.68}, {m: 11, val: meta.p90} ];
    const p50 = [ {m: 8, val: meta.m9}, {m: 9, val: meta.m9 + (meta.p50 - meta.m9) * 0.34}, {m: 10, val: meta.m9 + (meta.p50 - meta.m9) * 0.67}, {m: 11, val: meta.p50} ];
    const p10 = [ {m: 8, val: meta.m9}, {m: 9, val: meta.m9 + (meta.p10 - meta.m9) * 0.33}, {m: 10, val: meta.m9 + (meta.p10 - meta.m9) * 0.66}, {m: 11, val: meta.p10} ];

    let fanArea = `M ${getX(8)},${getY(meta.m9)}`;
    for (let i = 1; i < p90.length; i++) fanArea += ` L ${getX(p90[i].m)},${getY(p90[i].val)}`;
    for (let i = p10.length - 1; i >= 0; i--) fanArea += ` L ${getX(p10[i].m)},${getY(p10[i].val)}`;
    fanArea += ` Z`;

    let pathP50 = `M ${getX(8)},${getY(meta.m9)}`;
    for (let i = 1; i < p50.length; i++) pathP50 += ` L ${getX(p50[i].m)},${getY(p50[i].val)}`;

    const yBac = getY(meta.bac);
    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${padL}" y1="${yBac}" x2="${w - padR + 4}" y2="${yBac}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="${w - padR + 6}" y="${yBac + 3}" font-size="8" font-family="var(--font-mono, monospace)" fill="#64748b">BAC: ${meta.bac}M</text>
        <path d="${fanArea}" fill="rgba(27, 54, 93, 0.08)"/>
        <path d="${pathP50}" fill="none" stroke="#1b365d" stroke-width="1.8"/>
        <text x="${w - padR + 6}" y="${getY(meta.p50) + 3}" font-size="8" font-family="var(--font-mono, monospace)" fill="#1b365d" font-weight="800">P50: ${meta.p50}M</text>
        <text x="${w - padR + 6}" y="${getY(meta.p90) + 3}" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#c0392b" font-weight="700">P90: ${meta.p90}M</text>
        <text x="${w - padR + 6}" y="${getY(meta.p10) + 3}" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#27ae60" font-weight="700">P10: ${meta.p10}M</text>
        <path d="${pathActual}" fill="none" stroke="#1b365d" stroke-width="2.2"/>
        <circle cx="${getX(8)}" cy="${getY(meta.m9)}" r="3" fill="#1b365d"/>`;

    months.forEach((m, idx) => {
        svg += `<text x="${getX(idx)}" y="${h - 4}" font-size="8" fill="${idx <= 8 ? '#1e293b' : '#94a3b8'}" text-anchor="middle">${m}</text>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 5.3 Connected Scatterplot
function renderVsTimeConnScatter() {
    const el = document.getElementById("vs-svg-time-connscatter");
    if (!el) return;
    const points = [
        { m: "M1", x: 6.8, y: 7240 },
        { m: "M3", x: 7.4, y: 7245 },
        { m: "M5", x: 8.2, y: 7255 },
        { m: "M7", x: 9.6, y: 7280 },
        { m: "M9", x: 8.6, y: 7268 }
    ];
    const w = 460, h = 180, padL = 40, padR = 24, padTop = 18, padBottom = 22;
    const getX = (v) => padL + ((v - 6) / 5) * (w - padL - padR);
    const getY = (v) => padTop + (h - padTop - padBottom) - ((v - 7230) / 60) * (h - padTop - padBottom);

    let path = `M ${getX(points[0].x)},${getY(points[0].y)}`;
    for (let i = 1; i < points.length; i++) path += ` L ${getX(points[i].x)},${getY(points[i].y)}`;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <path d="${path}" fill="none" stroke="#1b365d" stroke-width="2"/>`;
    points.forEach(p => {
        const cx = getX(p.x), cy = getY(p.y);
        svg += `
            <circle cx="${cx}" cy="${cy}" r="4" fill="#c0392b"/>
            <text x="${cx + 6}" y="${cy - 4}" font-size="7.5" font-weight="700" fill="#1b365d">${p.m} (${p.y}M)</text>
        `;
    });
    svg += `<text x="${w - padR}" y="${h - 4}" font-size="8" fill="#64748b" text-anchor="end">Fraværsrate % →</text>
            <text x="${padL}" y="${padTop - 4}" font-size="8" fill="#64748b">↑ EAC Helårsprognose (MNOK)</text></svg>`;
    el.innerHTML = svg;
}

// 5.4 Sparklines (Small Multiples)
function renderVsTimeSparklines() {
    const el = document.getElementById("vs-svg-time-sparklines");
    if (!el) return;
    const sectors = [
        { name: "Helse", vals: [120, 122, 125, 128, 131, 142, 148, 155], col: "#c0392b" },
        { name: "Oppvekst", vals: [140, 142, 144, 146, 149, 152, 156, 160], col: "#c0392b" },
        { name: "Byutvikling", vals: [62, 62, 61, 63, 62, 62, 62, 62], col: "#27ae60" },
        { name: "Kultur", vals: [25, 25, 25, 26, 25, 25, 25, 25], col: "#64748b" },
        { name: "Org/Tek", vals: [30, 31, 31, 31, 31, 31, 31, 31], col: "#64748b" },
        { name: "Økonomi", vals: [98, 97, 98, 99, 98, 98, 97, 96], col: "#27ae60" }
    ];
    const w = 460, h = 180, top = 16, rowH = 26;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    sectors.forEach((s, idx) => {
        const y = top + idx * rowH;
        const pW = 240, startX = 130;
        const minV = Math.min(...s.vals) * 0.95, maxV = Math.max(...s.vals) * 1.05;
        let line = `M ${startX},${y + 16 - ((s.vals[0] - minV)/(maxV - minV)) * 14}`;
        for (let j = 1; j < s.vals.length; j++) {
            line += ` L ${startX + (j/7)*pW},${y + 16 - ((s.vals[j] - minV)/(maxV - minV)) * 14}`;
        }
        svg += `
            <text x="120" y="${y + 12}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${s.name}</text>
            <path d="${line}" fill="none" stroke="${s.col}" stroke-width="1.8"/>
            <circle cx="${startX + pW}" cy="${y + 16 - ((s.vals[7] - minV)/(maxV - minV)) * 14}" r="2.5" fill="${s.col}"/>
            <text x="${startX + pW + 8}" y="${y + 13}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="${s.col}">${s.vals[7]}M</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 5.5 Stacked Area Chart
function renderVsTimeArea() {
    const el = document.getElementById("vs-svg-time-area");
    if (!el) return;
    const months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"];
    const w = 460, h = 180, padL = 36, padR = 24, padTop = 18, padBottom = 22;
    const plotW = w - padL - padR, plotH = h - padTop - padBottom;
    const getX = (i) => padL + (i / 9) * plotW;
    const getY = (v) => padTop + plotH - (v / 8000) * plotH;

    // Kumulative nivåer for Lønn (60%), Varer (25%), Renter/annet (15%)
    let ptsLonn = [], ptsVarer = [], ptsTotal = [];
    for (let i = 0; i < 10; i++) {
        const cum = (i + 1) * 780;
        ptsLonn.push(cum * 0.60);
        ptsVarer.push(cum * 0.85);
        ptsTotal.push(cum);
    }

    let aTotal = `M ${getX(0)},${getY(ptsTotal[0])}`;
    for (let i = 1; i < 10; i++) aTotal += ` L ${getX(i)},${getY(ptsTotal[i])}`;
    aTotal += ` L ${getX(9)},${h - padBottom} L ${getX(0)},${h - padBottom} Z`;

    let aVarer = `M ${getX(0)},${getY(ptsVarer[0])}`;
    for (let i = 1; i < 10; i++) aVarer += ` L ${getX(i)},${getY(ptsVarer[i])}`;
    aVarer += ` L ${getX(9)},${h - padBottom} L ${getX(0)},${h - padBottom} Z`;

    let aLonn = `M ${getX(0)},${getY(ptsLonn[0])}`;
    for (let i = 1; i < 10; i++) aLonn += ` L ${getX(i)},${getY(ptsLonn[i])}`;
    aLonn += ` L ${getX(9)},${h - padBottom} L ${getX(0)},${h - padBottom} Z`;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <path d="${aTotal}" fill="#cbd5e1" opacity="0.6"/>
        <path d="${aVarer}" fill="#0ea5e9" opacity="0.45"/>
        <path d="${aLonn}" fill="#1b365d" opacity="0.8"/>
        <text x="${getX(9) - 6}" y="${getY(ptsLonn[9]) + 20}" font-size="7.5" font-weight="700" fill="#ffffff">Lønn (60%)</text>
        <text x="${getX(9) - 6}" y="${getY(ptsVarer[9]) + 15}" font-size="7.5" font-weight="700" fill="#ffffff">Drift (25%)</text>
        <text x="${getX(9) - 6}" y="${getY(ptsTotal[9]) + 15}" font-size="7.5" font-weight="700" fill="#1e293b">Finans (15%)</text>
    `;
    months.forEach((m, i) => {
        svg += `<text x="${getX(i)}" y="${h - 5}" font-size="8" fill="#64748b" text-anchor="middle">${m}</text>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 6: MAGNITUDE
// ------------------------------------------------------------------------------

// 6.1 Paired / Grouped Bar
function renderVsMagPaired() {
    const el = document.getElementById("vs-svg-mag-paired");
    if (!el) return;
    const sectors = [
        { name: "Oppvekst", bac: 2120, ac: 2138 },
        { name: "Helse", bac: 1850, ac: 1865 },
        { name: "Finans", bac: 1490, ac: 1487 },
        { name: "Byutvikling", bac: 940, ac: 939 },
        { name: "Org/Tek", bac: 460, ac: 460 },
        { name: "Kultur", bac: 380, ac: 380 }
    ];
    const w = 460, h = 180, padL = 90, padR = 40, top = 20, rowH = 24;
    const maxVal = 2400;
    const scale = (w - padL - padR) / maxVal;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <text x="${w - padR - 80}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#94a3b8">Budsjett (BAC)</text>
        <text x="${w - padR}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#1b365d" text-anchor="end">Faktisk (AC)</text>`;

    sectors.forEach((s, i) => {
        const y = top + i * rowH;
        const bW = s.bac * scale;
        const aW = s.ac * scale;
        svg += `
            <text x="${padL - 8}" y="${y + 13}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${s.name}</text>
            <rect x="${padL}" y="${y + 2}" width="${bW}" height="7" fill="#94a3b8" rx="1"/>
            <rect x="${padL}" y="${y + 10}" width="${aW}" height="7" fill="${s.ac > s.bac ? '#c0392b' : '#1b365d'}" rx="1"/>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 6.2 Bullet Graphs
function renderVsMagBullet() {
    const el = document.getElementById("vs-svg-mag-bullet");
    if (!el) return;
    const w = 460, h = 180, padL = 145, padR = 40, top = 16, rowH = 46;
    const barH = 14;
    const bullets = [
        { title: "Netto driftsresultat", unit: "%", val: 1.42, target: 1.75, min: 0, max: 3.0, ranges: [ {val: 1.0, col: "#fee2e2"}, {val: 1.75, col: "#fef3c7"}, {val: 3.0, col: "#dcfce7"} ] },
        { title: "Disposisjonsfond", unit: "% (485M)", val: 6.70, target: 6.00, min: 0, max: 10.0, ranges: [ {val: 4.0, col: "#fee2e2"}, {val: 6.0, col: "#fef3c7"}, {val: 10.0, col: "#dcfce7"} ] },
        { title: "Netto lånegjeld", unit: "% (5.68 Mrd)", val: 78.4, target: 80.0, min: 50, max: 100, ranges: [ {val: 75.0, col: "#dcfce7"}, {val: 80.0, col: "#fef3c7"}, {val: 100.0, col: "#fee2e2"} ] }
    ];

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    bullets.forEach((b, i) => {
        const y = top + i * rowH;
        const plotW = w - padL - padR;
        const getX = (val) => padL + Math.max(0, Math.min(1, (val - b.min) / (b.max - b.min))) * plotW;

        svg += `<text x="${padL - 8}" y="${y + 10}" font-size="8.8" font-weight="700" fill="#1b365d" text-anchor="end">${b.title}</text>
                <text x="${padL - 8}" y="${y + 20}" font-size="7.8" fill="#64748b" text-anchor="end">${b.unit}</text>`;

        let prevX = padL;
        b.ranges.forEach(r => {
            const rx = getX(r.val);
            svg += `<rect x="${prevX}" y="${y + 2}" width="${rx - prevX}" height="${barH + 8}" fill="${r.col}"/>`;
            prevX = rx;
        });

        const valX = getX(b.val);
        svg += `<rect x="${padL}" y="${y + 6}" width="${valX - padL}" height="${barH}" fill="#1b365d" rx="1"/>`;
        const targetX = getX(b.target);
        svg += `<line x1="${targetX}" y1="${y}" x2="${targetX}" y2="${y + barH + 12}" stroke="#0f172a" stroke-width="2.5"/>
                <text x="${valX + 4}" y="${y + 16}" font-size="8.5" font-family="var(--font-mono, monospace)" font-weight="800" fill="#1b365d">${b.val.toFixed(1)}${b.unit.includes('%') ? '%' : ''}</text>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 6.3 Proportional Circles
function renderVsMagCircles() {
    const el = document.getElementById("vs-svg-mag-circles");
    if (!el) return;
    const circles = [
        { name: "Oppvekst", val: 2120, r: 42, col: "#b91c1c" },
        { name: "Helse", val: 1850, r: 39, col: "#c2410c" },
        { name: "Finans", val: 1490, r: 34, col: "#1e293b" },
        { name: "Byutvikling", val: 940, r: 27, col: "#15803d" },
        { name: "Org/Tek", val: 460, r: 19, col: "#475569" },
        { name: "Kultur", val: 380, r: 17, col: "#7e22ce" }
    ];
    const w = 460, h = 180;
    const centers = [ {cx: 60, cy: 90}, {cx: 150, cy: 90}, {cx: 235, cy: 90}, {cx: 310, cy: 90}, {cx: 370, cy: 90}, {cx: 420, cy: 90} ];

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    circles.forEach((c, i) => {
        const pt = centers[i];
        svg += `
            <circle cx="${pt.cx}" cy="${pt.cy}" r="${c.r}" fill="${c.col}" fill-opacity="0.3" stroke="${c.col}" stroke-width="1.8"/>
            <text x="${pt.cx}" y="${pt.cy - 2}" font-size="7.5" font-weight="800" fill="#1e293b" text-anchor="middle">${c.name}</text>
            <text x="${pt.cx}" y="${pt.cy + 9}" font-size="7" font-family="var(--font-mono, monospace)" font-weight="700" fill="${c.col}" text-anchor="middle">${c.val}M</text>
        `;
    });
    svg += `<text x="230" y="170" font-size="7.5" fill="#64748b" text-anchor="middle">Sirkelareal proporsjonalt med årsramme (BAC)</text></svg>`;
    el.innerHTML = svg;
}

// 6.4 Radar / Spider Chart
function renderVsMagRadar() {
    const el = document.getElementById("vs-svg-mag-radar");
    if (!el) return;
    const axes = [
        { label: "Budsjettdisiplin", val: 0.88 },
        { label: "Fraværskontroll", val: 0.65 },
        { label: "Investeringsfremdrift", val: 0.94 },
        { label: "Rammepresisjon", val: 0.92 },
        { label: "Likviditetsreserve", val: 0.85 }
    ];
    const w = 460, h = 180, cx = 230, cy = 95, radius = 65;
    const angleStep = (Math.PI * 2) / axes.length;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    // Ringer (0.2, 0.4, 0.6, 0.8, 1.0)
    [0.33, 0.66, 1.0].forEach(lvl => {
        let rPath = ``;
        for (let i = 0; i < axes.length; i++) {
            const a = -Math.PI/2 + i * angleStep;
            const px = cx + Math.cos(a) * radius * lvl;
            const py = cy + Math.sin(a) * radius * lvl;
            rPath += `${i === 0 ? 'M' : 'L'} ${px},${py} `;
        }
        rPath += `Z`;
        svg += `<path d="${rPath}" fill="none" stroke="#e2e8f0" stroke-width="1"/>`;
    });

    // Eiker og etiketter
    let valPath = ``;
    axes.forEach((ax, i) => {
        const a = -Math.PI/2 + i * angleStep;
        const ex = cx + Math.cos(a) * radius;
        const ey = cy + Math.sin(a) * radius;
        svg += `<line x1="${cx}" y1="${cy}" x2="${ex}" y2="${ey}" stroke="#cbd5e1" stroke-width="1"/>`;

        const lx = cx + Math.cos(a) * (radius + 14);
        const ly = cy + Math.sin(a) * (radius + 14);
        svg += `<text x="${lx}" y="${ly + 3}" font-size="7.5" font-weight="600" fill="#334155" text-anchor="middle">${ax.label}</text>`;

        const vx = cx + Math.cos(a) * radius * ax.val;
        const vy = cy + Math.sin(a) * radius * ax.val;
        valPath += `${i === 0 ? 'M' : 'L'} ${vx},${vy} `;
    });
    valPath += `Z`;

    svg += `<path d="${valPath}" fill="rgba(27, 54, 93, 0.3)" stroke="#1b365d" stroke-width="2"/>`;
    axes.forEach((ax, i) => {
        const a = -Math.PI/2 + i * angleStep;
        const vx = cx + Math.cos(a) * radius * ax.val;
        const vy = cy + Math.sin(a) * radius * ax.val;
        svg += `<circle cx="${vx}" cy="${vy}" r="3" fill="#1b365d"/>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 7: PART-TO-WHOLE
// ------------------------------------------------------------------------------

// 7.1 Waterfall Chart
function renderVsPartWaterfall() {
    const el = document.getElementById("vs-svg-part-waterfall");
    if (!el) return;
    const steps = [
        { label: "BAC", val: 7240, type: "base", runVal: 7240 },
        { label: "+ Lønn", val: 185, type: "pos", runVal: 7425 },
        { label: "+ Vikar", val: 42, type: "pos", runVal: 7467 },
        { label: "+ Renter", val: 28, type: "pos", runVal: 7495 },
        { label: "- Tiltak", val: -227, type: "neg", runVal: 7268 },
        { label: "EAC", val: 7268, type: "total", runVal: 7268 }
    ];
    const w = 460, h = 180, padL = 36, padR = 24, padTop = 22, padBottom = 26;
    const colW = (w - padL - padR) / steps.length;
    const minVal = 7000, maxVal = 7600;
    const getY = (val) => padTop + (h - padTop - padBottom) - ((val - minVal) / (maxVal - minVal)) * (h - padTop - padBottom);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <line x1="${padL}" y1="${getY(7240)}" x2="${w - padR}" y2="${getY(7240)}" stroke="#94a3b8" stroke-dasharray="2,2"/>`;

    steps.forEach((s, i) => {
        const x = padL + i * colW + 4, bw = colW - 8;
        let yTop, yHeight, color;
        if (s.type === "base" || s.type === "total") {
            yTop = getY(s.val); yHeight = (h - padBottom) - yTop; color = "#1b365d";
        } else if (s.type === "pos") {
            const prev = s.runVal - s.val; yTop = getY(s.runVal); yHeight = getY(prev) - yTop; color = "#c0392b";
        } else {
            const prev = s.runVal - s.val; yTop = getY(prev); yHeight = getY(s.runVal) - yTop; color = "#27ae60";
        }
        svg += `
            <rect x="${x}" y="${yTop}" width="${bw}" height="${Math.max(yHeight, 2)}" fill="${color}" rx="2"/>
            <text x="${x + bw/2}" y="${yTop - 4}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="${color}" text-anchor="middle">${s.val > 0 && s.type !== 'base' && s.type !== 'total' ? '+' : ''}${s.val}M</text>
            <text x="${x + bw/2}" y="${h - 8}" font-size="7.5" font-weight="600" fill="#334155" text-anchor="middle">${s.label}</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 7.2 Treemap
function renderVsPartTreemap() {
    const el = document.getElementById("vs-svg-part-treemap");
    if (!el) return;
    const w = 460, h = 180, pad = 10;
    // Approksimert Treemap-inndeling for kommunens 7.24 Mrd: Oppvekst (2120), Helse (1850), Finans (1490), By (940), Org (460), Kultur (380)
    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Oppvekst -->
        <rect x="10" y="10" width="180" height="95" fill="#b91c1c" rx="2" stroke="#ffffff" stroke-width="1.5"/>
        <text x="20" y="30" font-size="8.5" font-weight="700" fill="#ffffff">Oppvekst</text>
        <text x="20" y="44" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#ffffff">2 120M (29%)</text>

        <!-- Helse -->
        <rect x="10" y="105" width="180" height="65" fill="#c2410c" rx="2" stroke="#ffffff" stroke-width="1.5"/>
        <text x="20" y="125" font-size="8.5" font-weight="700" fill="#ffffff">Helse og mestring</text>
        <text x="20" y="139" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#ffffff">1 850M (26%)</text>

        <!-- Finans/Stab -->
        <rect x="190" y="10" width="140" height="160" fill="#1e293b" rx="2" stroke="#ffffff" stroke-width="1.5"/>
        <text x="200" y="30" font-size="8.5" font-weight="700" fill="#ffffff">Finans & Gjeldsforv.</text>
        <text x="200" y="44" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#ffffff">1 490M (21%)</text>

        <!-- Byutvikling -->
        <rect x="330" y="10" width="120" height="95" fill="#15803d" rx="2" stroke="#ffffff" stroke-width="1.5"/>
        <text x="340" y="30" font-size="8" font-weight="700" fill="#ffffff">Byutvikling</text>
        <text x="340" y="44" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#ffffff">940M (13%)</text>

        <!-- Org/Tek -->
        <rect x="330" y="105" width="60" height="65" fill="#475569" rx="2" stroke="#ffffff" stroke-width="1.5"/>
        <text x="335" y="125" font-size="7" font-weight="700" fill="#ffffff">Org/IKT</text>
        <text x="335" y="137" font-size="6.5" font-family="var(--font-mono, monospace)" fill="#ffffff">460M</text>

        <!-- Kultur -->
        <rect x="390" y="105" width="60" height="65" fill="#7e22ce" rx="2" stroke="#ffffff" stroke-width="1.5"/>
        <text x="395" y="125" font-size="7" font-weight="700" fill="#ffffff">Kultur</text>
        <text x="395" y="137" font-size="6.5" font-family="var(--font-mono, monospace)" fill="#ffffff">380M</text>
    </svg>`;
    el.innerHTML = svg;
}

// 7.3 Donut Chart
function renderVsPartDonut() {
    const el = document.getElementById("vs-svg-part-donut");
    if (!el) return;
    const w = 460, h = 180, cx = 160, cy = 90, r = 60, ir = 38;
    // Donut med driftsarter: Fastlønn (58%), Vikarer (12%), Varer/Drift (18%), Finans (12%)
    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#1b365d" stroke-width="24" stroke-dasharray="218 377" stroke-dashoffset="0"/>
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#c0392b" stroke-width="24" stroke-dasharray="45 377" stroke-dashoffset="-218"/>
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#0ea5e9" stroke-width="24" stroke-dasharray="68 377" stroke-dashoffset="-263"/>
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#64748b" stroke-width="24" stroke-dasharray="46 377" stroke-dashoffset="-331"/>

        <text x="${cx}" y="${cy - 2}" font-size="9" font-weight="800" fill="#1b365d" text-anchor="middle">7 240 Mkr</text>
        <text x="${cx}" y="${cy + 10}" font-size="7" fill="#64748b" text-anchor="middle">Totale Driftsarter</text>

        <!-- Forklaring til høyre -->
        <g transform="translate(260, 40)">
            <rect x="0" y="0" width="10" height="10" fill="#1b365d" rx="2"/>
            <text x="16" y="9" font-size="8" font-weight="600" fill="#1e293b">Fastlønn: 58 % (4 200M)</text>

            <rect x="0" y="22" width="10" height="10" fill="#c0392b" rx="2"/>
            <text x="16" y="31" font-size="8" font-weight="600" fill="#1e293b">Vikar & overtid: 12 % (870M)</text>

            <rect x="0" y="44" width="10" height="10" fill="#0ea5e9" rx="2"/>
            <text x="16" y="53" font-size="8" font-weight="600" fill="#1e293b">Varer & tjenester: 18 % (1 300M)</text>

            <rect x="0" y="66" width="10" height="10" fill="#64748b" rx="2"/>
            <text x="16" y="75" font-size="8" font-weight="600" fill="#1e293b">Renter & finans: 12 % (870M)</text>
        </g>
    </svg>`;
    el.innerHTML = svg;
}

// 7.4 100% Stacked Bar
function renderVsPartStacked100() {
    const el = document.getElementById("vs-svg-part-stacked100");
    if (!el) return;
    const sectors = [
        { name: "Helse", fast: 76, var: 24 },
        { name: "Oppvekst", fast: 82, var: 18 },
        { name: "Byutvikling", fast: 45, var: 55 },
        { name: "Kultur", fast: 68, var: 32 },
        { name: "Org/Tek", fast: 58, var: 42 },
        { name: "Økonomi", fast: 30, var: 70 }
    ];
    const w = 460, h = 180, padL = 90, padR = 40, top = 20, rowH = 24;
    const barW = w - padL - padR;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <text x="${padL}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#1b365d">Faste lønnskostnader (%)</text>
        <text x="${w - padR}" y="${top - 6}" font-size="7.5" font-weight="700" fill="#c0392b" text-anchor="end">Variable/drift (%)</text>`;

    sectors.forEach((s, i) => {
        const y = top + i * rowH;
        const wFast = (s.fast / 100) * barW;
        const wVar = (s.var / 100) * barW;
        svg += `
            <text x="${padL - 8}" y="${y + 13}" font-size="8" font-weight="600" fill="#1e293b" text-anchor="end">${s.name}</text>
            <rect x="${padL}" y="${y + 2}" width="${wFast}" height="14" fill="#1b365d" rx="1"/>
            <rect x="${padL + wFast}" y="${y + 2}" width="${wVar}" height="14" fill="#c0392b" rx="1"/>
            <text x="${padL + 6}" y="${y + 12}" font-size="7" font-weight="700" fill="#ffffff">${s.fast}%</text>
            <text x="${w - padR - 6}" y="${y + 12}" font-size="7" font-weight="700" fill="#ffffff" text-anchor="end">${s.var}%</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 7.5 Marimekko (Mekko) Chart
function renderVsPartMekko() {
    const el = document.getElementById("vs-svg-part-mekko");
    if (!el) return;
    const blocks = [
        { name: "Oppvekst", wPct: 0.29, vik: 0.14 },
        { name: "Helse", wPct: 0.26, vik: 0.18 },
        { name: "Finans", wPct: 0.21, vik: 0.02 },
        { name: "Byutvikling", wPct: 0.13, vik: 0.06 },
        { name: "Org/Tek", wPct: 0.06, vik: 0.04 },
        { name: "Kultur", wPct: 0.05, vik: 0.05 }
    ];
    const w = 460, h = 180, padL = 36, padR = 24, top = 20, bot = 26;
    const totalW = w - padL - padR, totalH = h - top - bot;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    let curX = padL;
    blocks.forEach(b => {
        const bw = b.wPct * totalW;
        const vH = b.vik * totalH * 4; // skalert vikarhøyde
        const rH = totalH - vH;

        svg += `
            <rect x="${curX}" y="${top}" width="${bw - 2}" height="${rH}" fill="#1b365d" opacity="0.85" rx="1"/>
            <rect x="${curX}" y="${top + rH}" width="${bw - 2}" height="${vH}" fill="#c0392b" rx="1"/>
            <text x="${curX + bw/2}" y="${h - 8}" font-size="7" font-weight="700" fill="#334155" text-anchor="middle">${b.name}</text>
        `;
        curX += bw;
    });
    svg += `<text x="${padL}" y="${top - 6}" font-size="7.5" fill="#64748b">Bredde = Sektorramme | Rød høyde = Vikarandel</text></svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 8: SPATIAL
// ------------------------------------------------------------------------------

// 8.1 Choropleth Map (Kristiansand 7 bydeler)
function renderVsSpatChoropleth() {
    const el = document.getElementById("vs-svg-spat-choropleth");
    if (!el) return;
    const districts = [
        { name: "Kvadraturen", path: "M 220,70 L 260,70 L 260,105 L 220,105 Z", col: "#fee2e2", val: "-4.2M", cv: -4.2 },
        { name: "Lund", path: "M 260,65 L 315,65 L 310,110 L 260,105 Z", col: "#fee2e2", val: "-3.8M", cv: -3.8 },
        { name: "Vågsbygd", path: "M 160,95 L 220,95 L 220,150 L 150,150 Z", col: "#fca5a5", val: "-6.4M", cv: -6.4 },
        { name: "Grim/Torridal", path: "M 180,25 L 260,25 L 220,70 L 175,65 Z", col: "#fef3c7", val: "-1.1M", cv: -1.1 },
        { name: "Randesund", path: "M 315,65 L 410,75 L 395,145 L 310,110 Z", col: "#dcfce7", val: "+0.8M", cv: 0.8 },
        { name: "Søgne", path: "M 60,95 L 150,95 L 140,165 L 50,160 Z", col: "#fef3c7", val: "-0.9M", cv: -0.9 },
        { name: "Songdalen", path: "M 75,30 L 175,30 L 160,95 L 60,95 Z", col: "#dcfce7", val: "+1.2M", cv: 1.2 }
    ];
    const w = 460, h = 180;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    districts.forEach(d => {
        svg += `
            <path d="${d.path}" fill="${d.col}" stroke="#334155" stroke-width="1.2"/>
        `;
    });
    // Etiketter
    svg += `
        <text x="240" y="90" font-size="7.5" font-weight="700" fill="#1e293b" text-anchor="middle">Kvadraturen (${districts[0].val})</text>
        <text x="285" y="88" font-size="7.5" font-weight="700" fill="#1e293b" text-anchor="middle">Lund (${districts[1].val})</text>
        <text x="185" y="125" font-size="7.5" font-weight="700" fill="#991b1b" text-anchor="middle">Vågsbygd (${districts[2].val})</text>
        <text x="215" y="48" font-size="7.5" font-weight="700" fill="#1e293b" text-anchor="middle">Grim (${districts[3].val})</text>
        <text x="355" y="105" font-size="7.5" font-weight="700" fill="#166534" text-anchor="middle">Randesund (${districts[4].val})</text>
        <text x="100" y="130" font-size="7.5" font-weight="700" fill="#1e293b" text-anchor="middle">Søgne (${districts[5].val})</text>
        <text x="115" y="65" font-size="7.5" font-weight="700" fill="#166534" text-anchor="middle">Songdalen (${districts[6].val})</text>
        <text x="20" y="20" font-size="8" font-weight="800" fill="#1b365d">KRISTIANSAND BYDELSKART — AVVIK YTD</text>
    </svg>`;
    el.innerHTML = svg;
}

// 8.2 Proportional Symbol Map
function renderVsSpatSymbol() {
    const el = document.getElementById("vs-svg-spat-symbol");
    if (!el) return;
    const sites = [
        { name: "Eg Helsehus", x: 235, y: 75, r: 16, cost: "145M" },
        { name: "Wilds Minne Skole", x: 285, y: 90, r: 12, cost: "98M" },
        { name: "Aquarama Bad", x: 255, y: 95, r: 9, cost: "45M" },
        { name: "Søgne Skoleknutepunkt", x: 105, y: 135, r: 14, cost: "120M" },
        { name: "Nodeland Helse", x: 120, y: 65, r: 8, cost: "35M" },
        { name: "Vågsbygd Idrett", x: 180, y: 120, r: 10, cost: "65M" }
    ];
    const w = 460, h = 180;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <rect x="20" y="20" width="420" height="140" fill="#f8fafc" stroke="#e2e8f0" rx="4"/>
        <text x="30" y="38" font-size="8" font-weight="800" fill="#1b365d">INVESTERINGSPROSJEKTER (KONTOKLASSE 2)</text>`;

    sites.forEach(s => {
        svg += `
            <circle cx="${s.x}" cy="${s.y}" r="${s.r}" fill="#0ea5e9" fill-opacity="0.35" stroke="#0369a1" stroke-width="1.8"/>
            <circle cx="${s.x}" cy="${s.y}" r="2" fill="#0369a1"/>
            <text x="${s.x}" y="${s.y + s.r + 9}" font-size="7" font-weight="700" fill="#1e293b" text-anchor="middle">${s.name} (${s.cost})</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}

// 8.3 Flow / Route Map
function renderVsSpatRoute() {
    const el = document.getElementById("vs-svg-spat-route");
    if (!el) return;
    const w = 460, h = 180, hubX = 240, hubY = 85;
    const nodes = [
        { name: "Søgne Tjenester", x: 90, y: 130, val: "340M" },
        { name: "Songdalen Drift", x: 110, y: 55, val: "220M" },
        { name: "Vågsbygd Senter", x: 175, y: 125, val: "580M" },
        { name: "Randesund Skoler", x: 370, y: 105, val: "420M" },
        { name: "Grim/Torridal", x: 200, y: 40, val: "290M" }
    ];

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <rect x="15" y="15" width="430" height="150" fill="#f8fafc" stroke="#e2e8f0" rx="4"/>
        <text x="25" y="32" font-size="8" font-weight="800" fill="#1b365d">RESSURS- OG DRIFTSSTRØM TIL KVADRATUREN SENTRUM</text>`;

    nodes.forEach(n => {
        svg += `
            <line x1="${n.x}" y1="${n.y}" x2="${hubX}" y2="${hubY}" stroke="#0ea5e9" stroke-width="2.5" stroke-opacity="0.6"/>
            <circle cx="${n.x}" cy="${n.y}" r="4" fill="#0284c7"/>
            <text x="${n.x}" y="${n.y - 6}" font-size="7.5" font-weight="700" fill="#1e293b" text-anchor="middle">${n.name}</text>
        `;
    });
    // Sentral kasse
    svg += `
        <circle cx="${hubX}" cy="${hubY}" r="8" fill="#1b365d"/>
        <text x="${hubX}" y="${hubY + 16}" font-size="8.5" font-weight="800" fill="#1b365d" text-anchor="middle">Rådhuset Sentrum (7.24 Mrd)</text>
    </svg>`;
    el.innerHTML = svg;
}


// ------------------------------------------------------------------------------
// KATEGORI 9: FLOW
// ------------------------------------------------------------------------------

// 9.1 Sankey Diagram
function renderVsFlowSankey() {
    const el = document.getElementById("vs-svg-flow-sankey");
    if (!el) return;
    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const w = 460, h = 180, top = 10, bot = 10, availH = h - top - bot;
    let inNodes = [], outNodes = [];
    let totalVal = meta.bac;
    let treasuryLabel = meta.treasuryName;

    if (currentVsSector === 'ALL') {
        inNodes = [
            { name: "Skatt", val: 3420, color: "#0369a1" },
            { name: "Ramme", val: 2610, color: "#0284c7" },
            { name: "Gebyrer", val: 780, color: "#0ea5e9" },
            { name: "MVA-komp", val: 430, color: "#38bdf8" }
        ];
        outNodes = [
            { name: "Oppvekst", val: 2120, color: "#b91c1c" },
            { name: "Helse", val: 1850, color: "#c2410c" },
            { name: "Finans", val: 1490, color: "#1e293b" },
            { name: "Byutvikling", val: 940, color: "#15803d" },
            { name: "Org/Tek", val: 460, color: "#475569" },
            { name: "Kultur", val: 380, color: "#7e22ce" }
        ];
    } else {
        inNodes = [
            { name: "Kommunal Ramme", val: Math.round(meta.bac * 0.78), color: "#0369a1" },
            { name: "Egenbetaling/Gebyr", val: Math.round(meta.bac * 0.14), color: "#0284c7" },
            { name: "Refusjoner NAV/Stat", val: Math.round(meta.bac * 0.08), color: "#0ea5e9" }
        ];
        outNodes = [
            { name: "Driftsavdelinger", val: Math.round(meta.bac * 0.55), color: "#b91c1c" },
            { name: "Institusjon/Skoler", val: Math.round(meta.bac * 0.32), color: "#c2410c" },
            { name: "Stab & Fellestiltak", val: Math.round(meta.bac * 0.13), color: "#475569" }
        ];
    }

    const scaleY = (availH - (inNodes.length - 1) * 4) / totalVal;
    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;

    let curY = top;
    inNodes.forEach(n => {
        n.h = n.val * scaleY; n.y = curY; curY += n.h + 4;
        svg += `
            <rect x="14" y="${n.y}" width="10" height="${n.h}" fill="${n.color}" rx="1"/>
            <text x="28" y="${n.y + Math.max(n.h/2 + 3, 7)}" font-size="7.5" font-weight="700" fill="#334155">${n.name} (${n.val}M)</text>
        `;
    });

    const midX = 220, midW = 14;
    const midH = totalVal * scaleY + (inNodes.length - 1) * 2;
    const midY = top + (availH - midH) / 2;
    svg += `
        <rect x="${midX}" y="${midY}" width="${midW}" height="${midH}" fill="#1b365d" rx="2"/>
        <text x="${midX + midW / 2}" y="${midY - 4}" font-size="8" font-weight="800" fill="#1b365d" text-anchor="middle">${treasuryLabel}</text>
    `;

    const outScaleY = (availH - (outNodes.length - 1) * 3) / totalVal;
    let outCurY = top;
    outNodes.forEach(n => {
        n.h = n.val * outScaleY; n.y = outCurY; outCurY += n.h + 3;
        svg += `
            <rect x="436" y="${n.y}" width="10" height="${n.h}" fill="${n.color}" rx="1"/>
            <text x="430" y="${n.y + Math.max(n.h/2 + 3, 7)}" font-size="7.5" font-weight="700" fill="#334155" text-anchor="end">${n.name} (${n.val}M)</text>
        `;
    });

    inNodes.forEach(n => {
        const x1 = 24, y1 = n.y, x2 = midX, y2 = midY + (n.y - top) * 0.95;
        svg += `<path d="M ${x1},${y1} C ${x1 + 90},${y1} ${x2 - 90},${y2} ${x2},${y2} L ${x2},${y2 + n.h} C ${x2 - 90},${y2 + n.h} ${x1 + 90},${y1 + n.h} ${x1},${y1 + n.h} Z" fill="${n.color}" fill-opacity="0.28"/>`;
    });

    outNodes.forEach(n => {
        const x1 = midX + midW, y1 = midY + (n.y - top) * 0.95, x2 = 436, y2 = n.y;
        svg += `<path d="M ${x1},${y1} C ${x1 + 90},${y1} ${x2 - 90},${y2} ${x2},${y2} L ${x2},${y2 + n.h} C ${x2 - 90},${y2 + n.h} ${x1 + 90},${y1 + n.h} ${x1},${y1 + n.h} Z" fill="${n.color}" fill-opacity="0.25"/>`;
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}

// 9.2 Chord Diagram
function renderVsFlowChord() {
    const el = document.getElementById("vs-svg-flow-chord");
    if (!el) return;
    const w = 460, h = 180, cx = 230, cy = 90, r = 62;
    const sectors = [
        { name: "Helse", a: 0, col: "#c2410c" },
        { name: "Oppvekst", a: 1.05, col: "#b91c1c" },
        { name: "Finans", a: 2.1, col: "#1e293b" },
        { name: "Byutvikling", a: 3.15, col: "#15803d" },
        { name: "Org/IKT", a: 4.2, col: "#475569" },
        { name: "Kultur", a: 5.25, col: "#7e22ce" }
    ];

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    // Ytterbuer
    sectors.forEach((s, i) => {
        const p1x = cx + Math.cos(s.a) * r, p1y = cy + Math.sin(s.a) * r;
        const p2x = cx + Math.cos(s.a + 0.8) * r, p2y = cy + Math.sin(s.a + 0.8) * r;
        svg += `<path d="M ${p1x},${p1y} A ${r} ${r} 0 0 1 ${p2x},${p2y}" fill="none" stroke="${s.col}" stroke-width="7"/>`;
        const lx = cx + Math.cos(s.a + 0.4) * (r + 16), ly = cy + Math.sin(s.a + 0.4) * (r + 16);
        svg += `<text x="${lx}" y="${ly + 3}" font-size="7.5" font-weight="700" fill="#1e293b" text-anchor="middle">${s.name}</text>`;
    });

    // Korder (interne overføringer / IKT / VAR)
    const chords = [
        { from: 4, to: 0, col: "#475569" }, // Org/IKT -> Helse
        { name: "IKT -> Skole", from: 4, to: 1, col: "#475569" },
        { name: "Byutv -> Helse", from: 3, to: 0, col: "#15803d" },
        { name: "Finans -> Oppvekst", from: 2, to: 1, col: "#1e293b" }
    ];
    chords.forEach(c => {
        const a1 = sectors[c.from].a + 0.4, a2 = sectors[c.to].a + 0.4;
        const x1 = cx + Math.cos(a1) * (r - 4), y1 = cy + Math.sin(a1) * (r - 4);
        const x2 = cx + Math.cos(a2) * (r - 4), y2 = cy + Math.sin(a2) * (r - 4);
        svg += `<path d="M ${x1},${y1} Q ${cx},${cy} ${x2},${y2}" fill="none" stroke="${c.col}" stroke-width="3" stroke-opacity="0.4"/>`;
    });
    svg += `<text x="230" y="93" font-size="7" font-weight="700" fill="#64748b" text-anchor="middle">INTERN FLYT</text></svg>`;
    el.innerHTML = svg;
}

// 9.3 Network / Directed Graph
function renderVsFlowNetwork() {
    const el = document.getElementById("vs-svg-flow-network");
    if (!el) return;
    const w = 460, h = 180;
    const nodes = [
        { id: "bystyre", name: "Bystyret", role: "Vedtatt budsjett § 14-5", x: 60, y: 90, col: "#1b365d" },
        { id: "direktor", name: "Kommunedirektør", role: "Konsernledelse § 13-1", x: 175, y: 90, col: "#1e293b" },
        { id: "sjef_helse", name: "Sjef Helse", role: "Fullmakt: 25M", x: 300, y: 50, col: "#c2410c" },
        { id: "sjef_oppv", name: "Sjef Oppvekst", role: "Fullmakt: 25M", x: 300, y: 130, col: "#b91c1c" },
        { id: "enhet1", name: "Sykehjem", role: "Fullmakt: 5M", x: 410, y: 50, col: "#d97706" },
        { id: "enhet2", name: "Skoler", role: "Fullmakt: 5M", x: 410, y: 130, col: "#d97706" }
    ];
    const links = [
        { from: 0, to: 1 },
        { from: 1, to: 2 },
        { from: 1, to: 3 },
        { from: 2, to: 4 },
        { from: 3, to: 5 }
    ];

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;
    links.forEach(l => {
        const n1 = nodes[l.from], n2 = nodes[l.to];
        svg += `
            <line x1="${n1.x}" y1="${n1.y}" x2="${n2.x}" y2="${n2.y}" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="2,2"/>
        `;
    });
    nodes.forEach(n => {
        svg += `
            <rect x="${n.x - 42}" y="${n.y - 18}" width="84" height="36" fill="#ffffff" stroke="${n.col}" stroke-width="1.8" rx="3"/>
            <text x="${n.x}" y="${n.y - 4}" font-size="7.5" font-weight="700" fill="${n.col}" text-anchor="middle">${n.name}</text>
            <text x="${n.x}" y="${n.y + 8}" font-size="6.5" fill="#64748b" text-anchor="middle">${n.role}</text>
        `;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
}
