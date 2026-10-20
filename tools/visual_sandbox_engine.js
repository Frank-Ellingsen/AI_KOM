// ==============================================================================
// 🎨 VISUAL SANDBOX — FINANCIAL TIMES VISUAL VOCABULARY ENGINE (DYNAMIC 2026)
// jf. FT-Visual Guide (Alan Smith) & Edward Tufte Data-Ink Ratio
// Full Dynamisk Støtte for Alle 6 Virksomhetsområder + Konsern
// ==============================================================================

let currentVsCategory = 'ALL';
let currentVsStakeholder = 'ALL';
let currentVsSector = 'ALL';

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

function setVisualSandboxSector(sectorKey, btn, syncGlobal) {
    if (!sectorKey || !VS_SECTOR_META[sectorKey]) sectorKey = "ALL";
    currentVsSector = sectorKey;

    try {
        localStorage.setItem("aikom_selected_sector", sectorKey);
    } catch(e) {}

    // 1. Synkroniser knapper i sandbox-headeren
    const pills = document.querySelectorAll("#vs-scope-pills .vs-pill-btn");
    pills.forEach(p => {
        if (p.getAttribute("data-vs-sec") === sectorKey) {
            p.classList.add("active");
        } else {
            p.classList.remove("active");
        }
    });

    // 2. Oppdater live status-badge i filterbaren
    const meta = VS_SECTOR_META[sectorKey] || VS_SECTOR_META["ALL"];
    const sumEl = document.getElementById("vs-active-sector-summary");
    if (sumEl) {
        const isNeg = meta.avvik < 0;
        const avvikFmt = `${meta.avvik > 0 ? '+' : ''}${meta.avvik.toFixed(2)} Mkr`;
        const avvikCol = isNeg ? '#dc2626' : '#166534';
        sumEl.innerHTML = `📍 <strong>${meta.shortName}</strong> | Ramme: ${meta.rammeStr} | Avvik YTD: <span style="color:${avvikCol}">${avvikFmt}</span> | CPI: ${meta.cpi.toFixed(3)}`;
    }

    // 3. Valgfritt: Synkroniser resten av huben hvis brukeren klikket internt i Visual Sandbox
    if (syncGlobal && typeof window.selectSector === 'function') {
        window.selectSector(sectorKey, false);
    }

    // 4. Oppdater titler og forklaringer på alle 8 diagramkort
    updateSandboxCardTitles(sectorKey);

    // 5. Gjengi alle 8 diagrammer dynamisk for valgt budsjettområde
    renderVsDeviation();
    renderVsTime();
    renderVsRanking();
    renderVsDistribution();
    renderVsPartToWhole();
    renderVsCorrelation();
    renderVsMagnitude();
    renderVsFlow();

    if (typeof showToast === 'function' && syncGlobal) {
        showToast(`🎨 Visual Sandbox oppdatert for ${meta.title}`);
    }
}

function updateSandboxCardTitles(sectorKey) {
    const meta = VS_SECTOR_META[sectorKey] || VS_SECTOR_META["ALL"];
    const isAll = sectorKey === 'ALL';

    const tDeviation = document.getElementById("vs-title-deviation");
    const dDeviation = document.getElementById("vs-desc-deviation");
    if (tDeviation) {
        tDeviation.innerText = isAll ? "Avvik YTD per Virksomhetsområde (CV)" : `Avvik YTD per Enhet — ${meta.shortName} (CV)`;
    }
    if (dDeviation) {
        dDeviation.innerHTML = isAll 
            ? "<strong>Diverging Bar:</strong> Viser variasjon (+/-) mot null-punktet for alle 6 områder. Tydeliggjør merforbruk under § 14-5 uten unødvendige 3D-effekter."
            : `<strong>Diverging Bar:</strong> Viser enhetsavvik (+/-) innen ${meta.shortName} mot null-punktet. Identifiserer resultatenheter med budsjettoverskridelse jf. § 14-5.`;
    }

    const tTime = document.getElementById("vs-title-time");
    const dTime = document.getElementById("vs-desc-time");
    if (tTime) {
        tTime.innerText = isAll ? "Helårsprognose EAC (Monte Carlo Fan Chart)" : `Helårsprognose EAC — ${meta.shortName} (Fan Chart)`;
    }
    if (dTime) {
        dTime.innerHTML = `<strong>Fan Chart:</strong> Viser faktisk forbruk (M1–M9: ${meta.m9} Mkr) og 80 % konvolutt mot årsslutt (P10: ${meta.p10}M / P50: ${meta.p50}M / P90: ${meta.p90}M) målt mot BAC (${meta.rammeStr}).`;
    }

    const tRanking = document.getElementById("vs-title-ranking");
    const dRanking = document.getElementById("vs-desc-ranking");
    if (tRanking) {
        tRanking.innerText = isAll ? "Cost Performance Index (CPI) Rangering" : `Cost Performance Index (CPI) — ${meta.shortName}`;
    }
    if (dRanking) {
        dRanking.innerHTML = isAll
            ? "<strong>Lollipop Chart:</strong> Reduserer «heavy ink» fra brede stolper. Viser hvilke sektorer og nøkkelområder som presterer under budsjettbalansen (CPI &lt; 1.000)."
            : `<strong>Lollipop Chart:</strong> Rangering av resultatenheter i ${meta.shortName} etter kostnadseffektivitet mot balansekravet (CPI = 1.000).`;
    }

    const tDist = document.getElementById("vs-title-distribution");
    const dDist = document.getElementById("vs-desc-distribution");
    if (tDist) {
        tDist.innerText = isAll ? "Sykefraværsvarians i Virksomhetsområder (Box Plot)" : `Sykefraværsvarians per Fagdisiplin — ${meta.shortName} (Box Plot)`;
    }
    if (dDist) {
        dDist.innerHTML = `<strong>Box &amp; Whisker:</strong> Avdekker skjevhet, median og ekstreme uteliggere mot den kritiske faresonen på 8.0 % jf. HTA § 4 drøftingsplikt.`;
    }

    const tPart = document.getElementById("vs-title-part-to-whole");
    const dPart = document.getElementById("vs-desc-part-to-whole");
    if (tPart) {
        tPart.innerText = isAll ? "Budsjettbro fra BAC til EAC (Waterfall)" : `Budsjettbro fra BAC til EAC — ${meta.shortName} (Waterfall)`;
    }
    if (dPart) {
        dPart.innerHTML = isAll
            ? "<strong>Waterfall:</strong> Forklarer broen fra opprinnelig årsbudsjett 7 240 Mkr til sluttprognose 7 268 Mkr dekomponert på lønn, vikar, rente og innsparingstiltak."
            : `<strong>Waterfall:</strong> Dekomponerer endringen fra vedtatt ramme (${meta.bac} Mkr) til sluttprognose EAC (${meta.p50} Mkr) fordelt på tariff, vikarer og tiltak.`;
    }

    const tCorr = document.getElementById("vs-title-correlation");
    const dCorr = document.getElementById("vs-desc-correlation");
    if (tCorr) {
        tCorr.innerText = isAll ? "Sykefravær vs. Ekstraordinære Vikarkostnader" : `Sykefravær vs. Vikarutgifter — ${meta.shortName}`;
    }
    if (dCorr) {
        dCorr.innerHTML = `<strong>Scatterplot med regresjonslinje:</strong> Dokumenterer sammenheng mellom høyt sykefravær og overskridelse på vikarbudsjett for enhetene i ${meta.shortName}.`;
    }

    const tMag = document.getElementById("vs-title-magnitude");
    const dMag = document.getElementById("vs-desc-magnitude");
    if (tMag) {
        tMag.innerText = isAll ? "Top 3 Kommunale Nøkkeltall (Bullet Graphs)" : `Styringsnøkkeltall for ${meta.shortName} (Bullet Graphs)`;
    }
    if (dMag) {
        dMag.innerHTML = isAll
            ? "<strong>Stephen Few / Tufte Bullet Graph:</strong> Erstatter sirkulære speedometre med lineær presisjon. Viser faktisk oppnåelse mot TBU-krav og lovtak."
            : `<strong>Bullet Graph:</strong> Lineær visning av måloppnåelse for ${meta.shortName} (Budsjettoverholdelse, vikartakt og sykefravær) mot politiske krav.`;
    }

    const tFlow = document.getElementById("vs-title-flow");
    const dFlow = document.getElementById("vs-desc-flow");
    if (tFlow) {
        tFlow.innerText = isAll ? "Pengestrøm 7.24 Mrd (Sankey-Diagram)" : `Pengestrøm & Ressursflyt — ${meta.shortName} (Sankey)`;
    }
    if (dFlow) {
        dFlow.innerHTML = isAll
            ? "<strong>Sankey Diagram:</strong> Visualiserer inntektskilder (Skatt, Rammetilskudd, Gebyrer, MVA) gjennom kommunekassen til de 6 tjenesteområdene."
            : `<strong>Sankey Diagram:</strong> Visualiserer tildelte inntekter og finansieringskilder gjennom ${meta.treasuryName.split('(')[0].trim()} til fagdisipliner og enheter jf. bruttoprinsippet § 14-6.`;
    }
}

function applyVisualSandboxFilters() {
    const cards = document.querySelectorAll("#vs-cards-grid .vs-chart-card");
    cards.forEach(card => {
        const cat = card.getAttribute("data-ft-cat");
        const stakeholders = card.getAttribute("data-stakeholder") || "";
        
        const catMatch = (currentVsCategory === 'ALL' || cat === currentVsCategory);
        const stakeholderMatch = (currentVsStakeholder === 'ALL' || stakeholders.includes(currentVsStakeholder));
        
        if (catMatch && stakeholderMatch) {
            card.style.display = "flex";
        } else {
            card.style.display = "none";
        }
    });
}

function copyCardSvg(containerId, chartName) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const svg = el.querySelector("svg");
    if (!svg) return;
    
    const svgCode = svg.outerHTML;
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(svgCode).then(() => {
            if (typeof showToast === 'function') {
                showToast(`📋 Kopierte ren SVG for ${chartName}! Klar for Word/PPTX saksfremlegg.`);
            }
        });
    } else {
        if (typeof showToast === 'function') showToast(`📋 SVG generert for ${chartName}`);
    }
}

function copyAllSandboxReport() {
    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const isAll = currentVsSector === 'ALL';

    const report = `# KRISTIANSAND KOMMUNE — BEST-PRACTICE VISUAL BRIEFING
Kilde: Financial Times Visual Vocabulary (Alan Smith) & Edward Tufte Data-Ink Ratio
Analyseområde: ${meta.title} (Ramme: ${meta.rammeStr})
Målgruppe: Bystyret, Formannskapet og Kommunedirektøren jf. Kommuneloven §§ 13-1 og 14-5

1. DEVIATION (Avvik): Diverging Bar er valgt for å tydeliggjøre handleplikt etter § 14-5.
   - Aktivt område: ${meta.shortName}
   - Akkumulert Avvik YTD: ${meta.avvik > 0 ? '+' : ''}${meta.avvik.toFixed(2)} MNOK (${meta.avvik < 0 ? '🔴 Merforbruk' : '🟢 Positiv buffer'})
   - Cost Performance Index: ${meta.cpi.toFixed(3)} (Mål: 1.000)

2. CHANGE OVER TIME (Tidsutvikling): Fan Chart viser P10/P50/P90 Monte Carlo usikkerhetsvifte for EAC.
   - Vedtatt budsjettramme (BAC): ${meta.bac} Mkr
   - Faktisk forbruk per M9: ${meta.m9} Mkr
   - P10 (Optimistisk anslag): ${meta.p10} Mkr
   - P50 (Forventet base-case): ${meta.p50} Mkr
   - P90 (Konservativt risikoscenario): ${meta.p90} Mkr

3. PART-TO-WHOLE (Helhet): Waterfall-bro dekomponerer bevegelsen fra ${meta.bac} Mkr til ${meta.p50} Mkr.
   - Identifiserer lønnsvekst, vikartakt og iverksatte styringstiltak.

4. DISTRIBUTION & KORRELASJON:
   - Sykefraværsfordeling dokumenterer spredning og identifiserer enheter over 8.0 % kritisk grense for HTA § 4.
   - Scatterplot påviser sammenheng mellom høyt sykefravær og ekstraordinære vikarutgifter.

5. MAGNITUDE (Nøkkeltall): Bullet graphs erstatter speedometre og sikrer lineær presisjon mot styringskrav.
   - Rammeoverholdelse: ${(meta.m9 / (meta.bac * 0.75) * 100).toFixed(1)} % mot periodisert plan.`;

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(report).then(() => {
            if (typeof showToast === 'function') {
                showToast(`📋 Saksnotat for ${meta.shortName} kopiert til utklippstavlen!`);
            }
        });
    }
}

// ==============================================================================
// 2. SVG RENDERING FUNKSJONER (8 DYNAMISKE FT DIAGRAMMER)
// ==============================================================================

// 1. DEVIATION — Diverging Bar Chart
function renderVsDeviation() {
    const el = document.getElementById("vs-svg-deviation");
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
        const secUnits = (typeof ALL_81_UNITS_DATA !== 'undefined')
            ? ALL_81_UNITS_DATA.filter(u => u.sectorKey === currentVsSector)
            : [];
        
        if (secUnits.length > 0) {
            // Sorter etter avvik (størst merforbruk først)
            const sorted = [...secUnits].sort((a, b) => (a.cv || 0) - (b.cv || 0));
            // Velg topp 6 enheter med størst avvik
            const topUnits = sorted.slice(0, 6);
            items = topUnits.map(u => ({
                name: u.name.length > 24 ? u.name.substring(0, 22) + '…' : u.name,
                val: Number(((u.cv || 0) / 1000000).toFixed(2))
            }));
            items.push({
                name: `${meta.shortName} Samlet`,
                val: meta.avvik,
                isTotal: true
            });
        } else {
            items = [
                { name: `${meta.shortName} Samlet`, val: meta.avvik, isTotal: true }
            ];
        }
    }

    const w = 460, h = 180, padL = 135, padR = 60, top = 18, rowH = Math.min(22, (h - top - 10) / items.length);

    // Finn ekstremverdier for dynamisk skala
    let minVal = 0, maxVal = 0;
    items.forEach(it => {
        if (it.val < minVal) minVal = it.val;
        if (it.val > maxVal) maxVal = it.val;
    });
    if (minVal === 0 && maxVal === 0) { minVal = -1; maxVal = 1; }
    
    // Gi litt margin
    const absMax = Math.max(Math.abs(minVal), Math.abs(maxVal), 0.5);
    const spanNeg = Math.abs(minVal);
    const spanPos = Math.max(maxVal, 0.2);
    const totalSpan = spanNeg + spanPos;
    
    // Plasser 0-linjen proporsjonalt
    const availPlotW = w - padL - padR;
    const midX = padL + (spanNeg / totalSpan) * availPlotW;
    const scaleNeg = (midX - padL) / (spanNeg || 1);
    const scalePos = (w - padR - midX) / (spanPos || 1);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Null-linje (Referanse jf. FT Deviation) -->
        <line x1="${midX}" y1="${top - 5}" x2="${midX}" y2="${top + items.length * rowH + 2}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${midX}" y="${top - 7}" font-size="8" font-weight="700" fill="#64748b" text-anchor="middle">0 kr (Balanse)</text>
    `;

    items.forEach((item, i) => {
        const y = top + i * rowH;
        const isNeg = item.val < 0;
        const barW = isNeg ? Math.abs(item.val) * scaleNeg : item.val * scalePos;
        const color = item.isTotal 
            ? (isNeg ? "#991b1b" : "#166534") 
            : (isNeg ? "#c0392b" : "#27ae60");
        const barX = isNeg ? (midX - barW) : midX;

        svg += `
            <text x="${padL - 8}" y="${y + rowH * 0.55 + 3}" font-size="8.5" font-weight="${item.isTotal ? '800' : '600'}" fill="${item.isTotal ? 'var(--navy-dark, #1b365d)' : 'var(--text-primary, #1e293b)'}" text-anchor="end">${item.name}</text>
            <rect x="${barX}" y="${y + 2}" width="${Math.max(barW, 1.5)}" height="${item.isTotal ? rowH - 4 : rowH - 7}" fill="${color}" rx="2" opacity="${item.isTotal ? '1' : '0.85'}"/>
        `;

        const labelX = isNeg ? (barX - 4) : (barX + barW + 4);
        const labelAnchor = isNeg ? "end" : "start";
        const sign = item.val > 0 ? "+" : "";
        svg += `
            <text x="${labelX}" y="${y + rowH * 0.55 + 3}" font-size="8" font-family="var(--font-mono, monospace)" font-weight="700" fill="${color}" text-anchor="${labelAnchor}">
                ${sign}${item.val.toFixed(2)}M
            </text>
        `;
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}

// 2. CHANGE OVER TIME — Fan Chart (Monte Carlo EAC)
function renderVsTime() {
    const el = document.getElementById("vs-svg-time");
    if (!el) return;

    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const w = 460, h = 180, padL = 36, padR = 86, padTop = 16, padBottom = 22;
    const plotW = w - padL - padR;
    const plotH = h - padTop - padBottom;

    const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
    
    // Normalisert Y-skala tilpasset sektorens budsjett
    const maxY = Math.ceil(Math.max(meta.bac, meta.p90) * 1.05 / 50) * 50;
    const minY = 0;
    const getX = (m) => padL + (m / 11) * plotW;
    const getY = (val) => padTop + plotH - (val / maxY) * plotH;

    // Generer 9 måneders historisk forbruk opp til M9
    const stepM = meta.m9 / 8.8;
    const mPoints = [
        {m: 0, val: stepM * 0.95},
        {m: 1, val: stepM * 1.95},
        {m: 2, val: stepM * 2.96},
        {m: 3, val: stepM * 3.96},
        {m: 4, val: stepM * 4.96},
        {m: 5, val: stepM * 5.95},
        {m: 6, val: stepM * 6.90},
        {m: 7, val: stepM * 7.90},
        {m: 8, val: meta.m9}
    ];

    let pathActual = `M ${getX(0)},${getY(mPoints[0].val)}`;
    for (let i = 1; i < mPoints.length; i++) {
        pathActual += ` L ${getX(mPoints[i].m)},${getY(mPoints[i].val)}`;
    }

    // Viftepunkter for M9 -> M12
    const p90 = [
        {m: 8, val: meta.m9},
        {m: 9, val: meta.m9 + (meta.p90 - meta.m9) * 0.35},
        {m: 10, val: meta.m9 + (meta.p90 - meta.m9) * 0.68},
        {m: 11, val: meta.p90}
    ];
    const p50 = [
        {m: 8, val: meta.m9},
        {m: 9, val: meta.m9 + (meta.p50 - meta.m9) * 0.34},
        {m: 10, val: meta.m9 + (meta.p50 - meta.m9) * 0.67},
        {m: 11, val: meta.p50}
    ];
    const p10 = [
        {m: 8, val: meta.m9},
        {m: 9, val: meta.m9 + (meta.p10 - meta.m9) * 0.33},
        {m: 10, val: meta.m9 + (meta.p10 - meta.m9) * 0.66},
        {m: 11, val: meta.p10}
    ];

    // Fan polygon P10 til P90
    let fanArea = `M ${getX(8)},${getY(meta.m9)}`;
    for (let i = 1; i < p90.length; i++) fanArea += ` L ${getX(p90[i].m)},${getY(p90[i].val)}`;
    for (let i = p10.length - 1; i >= 0; i--) fanArea += ` L ${getX(p10[i].m)},${getY(p10[i].val)}`;
    fanArea += ` Z`;

    let pathP50 = `M ${getX(8)},${getY(meta.m9)}`;
    for (let i = 1; i < p50.length; i++) pathP50 += ` L ${getX(p50[i].m)},${getY(p50[i].val)}`;

    let pathP90 = `M ${getX(8)},${getY(meta.m9)}`;
    for (let i = 1; i < p90.length; i++) pathP90 += ` L ${getX(p90[i].m)},${getY(p90[i].val)}`;

    let pathP10 = `M ${getX(8)},${getY(meta.m9)}`;
    for (let i = 1; i < p10.length; i++) pathP10 += ` L ${getX(p10[i].m)},${getY(p10[i].val)}`;

    const yBac = getY(meta.bac);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Vedtatt Budsjettramme (BAC) -->
        <line x1="${padL}" y1="${yBac}" x2="${w - padR + 4}" y2="${yBac}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="${w - padR + 6}" y="${yBac + 3}" font-size="8" font-family="var(--font-mono, monospace)" fill="#64748b">BAC: ${meta.bac}M</text>

        <!-- Viftefelt (Usikkerhetskonvolutt) -->
        <path d="${fanArea}" fill="rgba(27, 54, 93, 0.08)"/>

        <!-- P10 stiplet grønn linje -->
        <path d="${pathP10}" fill="none" stroke="#27ae60" stroke-width="1.2" stroke-dasharray="3,2"/>
        <text x="${w - padR + 6}" y="${getY(meta.p10) + 3}" font-size="8" font-family="var(--font-mono, monospace)" fill="#27ae60" font-weight="700">P10: ${meta.p10}M</text>

        <!-- P90 stiplet rød linje -->
        <path d="${pathP90}" fill="none" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="3,2"/>
        <text x="${w - padR + 6}" y="${getY(meta.p90) + 3}" font-size="8" font-family="var(--font-mono, monospace)" fill="#c0392b" font-weight="700">P90: ${meta.p90}M</text>

        <!-- P50 hel marine linje -->
        <path d="${pathP50}" fill="none" stroke="#1b365d" stroke-width="1.8"/>
        <text x="${w - padR + 6}" y="${getY(meta.p50) + 3}" font-size="8.5" font-family="var(--font-mono, monospace)" fill="#1b365d" font-weight="800">P50: ${meta.p50}M</text>

        <!-- Faktisk kurve M1-M9 -->
        <path d="${pathActual}" fill="none" stroke="#1b365d" stroke-width="2.2" stroke-linecap="round"/>
        <circle cx="${getX(8)}" cy="${getY(meta.m9)}" r="3.5" fill="#1b365d"/>
        <text x="${getX(8) - 4}" y="${getY(meta.m9) - 6}" font-size="8" font-weight="700" fill="#1b365d" text-anchor="end">M9: ${meta.m9}M</text>

        <!-- X-akse måneder -->
        ${months.map((m, idx) => `
            <text x="${getX(idx)}" y="${h - 4}" font-size="8" fill="${idx <= 8 ? '#1e293b' : '#94a3b8'}" font-weight="${idx <= 8 ? '700' : '400'}" text-anchor="middle">${m}</text>
        `).join('')}
    </svg>`;

    el.innerHTML = svg;
}

// 3. RANKING — Lollipop Chart (CPI)
function renderVsRanking() {
    const el = document.getElementById("vs-svg-ranking");
    if (!el) return;

    let units = [];
    if (currentVsSector === 'ALL') {
        units = [
            { name: "5200 Sykehjem & Døgnpleie", cpi: 0.988 },
            { name: "2020 Grunnskoler (KRS)", cpi: 0.991 },
            { name: "2010 Kommunale Barnehager", cpi: 0.993 },
            { name: "3800 Kultur & Idrett", cpi: 1.000 },
            { name: "1800 IKT & Fellestjenester", cpi: 1.000 },
            { name: "3300 Samferdsel & VAR", cpi: 1.001 },
            { name: "8000 Finans & Gjeldsforv.", cpi: 1.003 }
        ];
    } else {
        const secUnits = (typeof ALL_81_UNITS_DATA !== 'undefined')
            ? ALL_81_UNITS_DATA.filter(u => u.sectorKey === currentVsSector)
            : [];
        
        if (secUnits.length > 0) {
            const sorted = [...secUnits].sort((a, b) => (a.cpi || 1) - (b.cpi || 1));
            units = sorted.slice(0, 7).map(u => ({
                name: u.name.length > 25 ? u.name.substring(0, 23) + '…' : u.name,
                cpi: Number(u.cpi || 1.000)
            }));
        } else {
            const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
            units = [{ name: meta.title, cpi: meta.cpi }];
        }
    }

    const w = 460, h = 180, padL = 145, padR = 50, top = 16, rowH = Math.min(22, (h - top - 8) / units.length);

    // Beregn CPI grenser dynamisk
    let minCpi = 0.985, maxCpi = 1.010;
    units.forEach(u => {
        if (u.cpi < minCpi) minCpi = Math.floor(u.cpi * 1000) / 1000 - 0.003;
        if (u.cpi > maxCpi) maxCpi = Math.ceil(u.cpi * 1000) / 1000 + 0.003;
    });

    const getX = (val) => padL + ((val - minCpi) / (maxCpi - minCpi)) * (w - padL - padR);
    const xBase = getX(1.000);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Referanselinje ved CPI = 1.000 -->
        <line x1="${xBase}" y1="${top - 4}" x2="${xBase}" y2="${top + units.length * rowH + 2}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${xBase}" y="${top - 6}" font-size="8" font-weight="700" fill="#64748b" text-anchor="middle">1.000 (Balanse)</text>
    `;

    units.forEach((u, i) => {
        const y = top + i * rowH;
        const xVal = getX(u.cpi);
        const isAlert = u.cpi < 0.995;
        const color = isAlert ? "#c0392b" : (u.cpi >= 1.000 ? "#27ae60" : "#d35400");

        svg += `
            <text x="${padL - 8}" y="${y + rowH * 0.55 + 2}" font-size="8.5" font-weight="600" fill="var(--text-primary, #1e293b)" text-anchor="end">${u.name}</text>
            <!-- Lollipop stem -->
            <line x1="${Math.min(xBase, xVal)}" y1="${y + rowH * 0.5}" x2="${Math.max(xBase, xVal)}" y2="${y + rowH * 0.5}" stroke="${color}" stroke-width="1.8"/>
            <!-- Lollipop dot -->
            <circle cx="${xVal}" cy="${y + rowH * 0.5}" r="4.2" fill="${color}"/>
            <!-- Verdi label -->
            <text x="${xVal + (u.cpi >= 1.0 ? 7 : -7)}" y="${y + rowH * 0.55 + 2}" font-size="8" font-family="var(--font-mono, monospace)" font-weight="700" fill="${color}" text-anchor="${u.cpi >= 1.0 ? 'start' : 'end'}">
                ${u.cpi.toFixed(3)}
            </text>
        `;
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}

// 4. DISTRIBUTION — Box Plot (Sykefravær)
function renderVsDistribution() {
    const el = document.getElementById("vs-svg-distribution");
    if (!el) return;

    let data = [];
    if (currentVsSector === 'ALL') {
        data = [
            { name: "1. Helse & mestring", min: 5.2, q1: 7.8, med: 9.6, q3: 11.4, max: 13.5, outliers: [14.8] },
            { name: "2. Oppvekst", min: 4.8, q1: 6.9, med: 8.4, q3: 9.6, max: 11.2, outliers: [12.4] },
            { name: "3. By- & stedsutvikling", min: 2.8, q1: 3.8, med: 4.8, q3: 5.9, max: 7.2, outliers: [] },
            { name: "4. Kultur & dialog", min: 3.1, q1: 4.1, med: 5.2, q3: 6.4, max: 7.8, outliers: [] },
            { name: "5. Org & teknologi", min: 2.9, q1: 3.9, med: 4.9, q3: 5.8, max: 7.0, outliers: [] },
            { name: "6. Økonomi & styring", min: 2.2, q1: 3.1, med: 3.9, q3: 4.6, max: 5.5, outliers: [] }
        ];
    } else if (currentVsSector === 'HELSE') {
        data = [
            { name: "Sykehjem & Døgnpleie", min: 6.2, q1: 8.5, med: 10.4, q3: 12.6, max: 14.8, outliers: [16.2] },
            { name: "Hjemmetjenester & Omsorg", min: 5.8, q1: 8.0, med: 9.8, q3: 11.8, max: 13.9, outliers: [15.0] },
            { name: "Døgnrehabilitering", min: 4.5, q1: 6.8, med: 8.4, q3: 10.2, max: 12.0, outliers: [] },
            { name: "Rus & Psykisk Helse", min: 4.2, q1: 6.2, med: 7.6, q3: 9.1, max: 10.8, outliers: [] },
            { name: "Legevakt & Fellestjeneste", min: 3.5, q1: 4.8, med: 5.9, q3: 7.2, max: 8.5, outliers: [] }
        ];
    } else if (currentVsSector === 'OPPVEKST') {
        data = [
            { name: "Grunnskoler 1–7. trinn", min: 5.2, q1: 7.2, med: 8.6, q3: 10.1, max: 12.0, outliers: [13.2] },
            { name: "Ungdomsskoler 8–10.", min: 4.8, q1: 6.5, med: 7.9, q3: 9.4, max: 11.0, outliers: [12.1] },
            { name: "Kommunale Barnehager", min: 5.6, q1: 7.8, med: 9.4, q3: 11.2, max: 13.0, outliers: [14.1] },
            { name: "PPT & Familiens hus", min: 3.2, q1: 4.4, med: 5.5, q3: 6.8, max: 8.0, outliers: [] },
            { name: "SFO & Fellesoppvekst", min: 4.9, q1: 6.8, med: 8.2, q3: 9.8, max: 11.5, outliers: [] }
        ];
    } else if (currentVsSector === 'BYUTVIKLING') {
        data = [
            { name: "Samferdsel & Veidrift", min: 3.5, q1: 4.6, med: 5.8, q3: 7.1, max: 8.8, outliers: [] },
            { name: "Parkvesen & Idrettsanlegg", min: 3.8, q1: 5.0, med: 6.2, q3: 7.5, max: 9.2, outliers: [] },
            { name: "VAR Drift (Vann/Avløp)", min: 2.8, q1: 3.5, med: 4.4, q3: 5.6, max: 6.8, outliers: [] },
            { name: "Plan & Byggesak", min: 2.4, q1: 3.0, med: 3.8, q3: 4.8, max: 6.0, outliers: [] },
            { name: "Eiendomsforvaltning", min: 3.2, q1: 4.0, med: 5.1, q3: 6.2, max: 7.4, outliers: [] }
        ];
    } else if (currentVsSector === 'KULTUR') {
        data = [
            { name: "Idrettshaller & Bad", min: 4.2, q1: 5.4, med: 6.8, q3: 8.2, max: 10.1, outliers: [11.2] },
            { name: "Folkebiblioteket", min: 3.1, q1: 3.9, med: 4.8, q3: 5.9, max: 7.2, outliers: [] },
            { name: "Kulturskolen", min: 2.5, q1: 3.2, med: 4.1, q3: 5.1, max: 6.4, outliers: [] },
            { name: "Fritid & Ungdomsklubber", min: 3.5, q1: 4.3, med: 5.4, q3: 6.6, max: 8.0, outliers: [] }
        ];
    } else if (currentVsSector === 'ORG_TEK') {
        data = [
            { name: "Dokumentsenter & Service", min: 4.0, q1: 5.1, med: 6.2, q3: 7.5, max: 9.0, outliers: [] },
            { name: "HR & Arbeidsmiljø", min: 2.8, q1: 3.6, med: 4.5, q3: 5.6, max: 6.9, outliers: [] },
            { name: "IKT Drift & Systemer", min: 2.5, q1: 3.1, med: 3.9, q3: 4.8, max: 6.0, outliers: [] },
            { name: "Lønn & Regnskapssenter", min: 3.0, q1: 3.9, med: 4.8, q3: 5.8, max: 7.1, outliers: [] }
        ];
    } else {
        // OKONOMI
        data = [
            { name: "Kemner & Skatteoppkreving", min: 2.8, q1: 3.7, med: 4.6, q3: 5.5, max: 6.8, outliers: [] },
            { name: "Innkjøp & Anskaffelser", min: 2.5, q1: 3.2, med: 4.1, q3: 5.0, max: 6.2, outliers: [] },
            { name: "Konserncontroller & Stab", min: 2.1, q1: 2.7, med: 3.4, q3: 4.2, max: 5.1, outliers: [] },
            { name: "Politisk stab & Bystyre", min: 1.8, q1: 2.2, med: 2.8, q3: 3.6, max: 4.5, outliers: [] }
        ];
    }

    const w = 460, h = 180, padL = 135, padR = 40, top = 16, rowH = Math.min(24, (h - top - 8) / data.length);
    const minVal = 0, maxVal = 18;
    const getX = (val) => padL + (val / maxVal) * (w - padL - padR);

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Kritisk grense for vikartrøkk (8.0 %) jf. HTA § 4 -->
        <line x1="${getX(8.0)}" y1="${top - 4}" x2="${getX(8.0)}" y2="${top + data.length * rowH + 2}" stroke="#fca5a5" stroke-width="1.2" stroke-dasharray="2,2"/>
        <text x="${getX(8.0)}" y="${top - 6}" font-size="8" font-weight="700" fill="#dc2626" text-anchor="middle">8.0 % Faresone (HTA § 4)</text>
    `;

    data.forEach((d, i) => {
        const y = top + i * rowH;
        const xMin = getX(d.min), xMax = getX(d.max);
        const xQ1 = getX(d.q1), xQ3 = getX(d.q3);
        const xMed = getX(d.med);
        const isHigh = d.med >= 8.0;
        const boxColor = isHigh ? "rgba(239, 68, 68, 0.15)" : "rgba(30, 41, 59, 0.08)";
        const strokeColor = isHigh ? "#c0392b" : "#334155";

        svg += `
            <text x="${padL - 8}" y="${y + rowH * 0.55 + 2}" font-size="8.5" font-weight="600" fill="var(--text-primary, #1e293b)" text-anchor="end">${d.name}</text>
            <!-- Whisker line -->
            <line x1="${xMin}" y1="${y + rowH * 0.45}" x2="${xMax}" y2="${y + rowH * 0.45}" stroke="#94a3b8" stroke-width="1.2"/>
            <line x1="${xMin}" y1="${y + rowH * 0.25}" x2="${xMin}" y2="${y + rowH * 0.65}" stroke="#94a3b8" stroke-width="1.2"/>
            <line x1="${xMax}" y1="${y + rowH * 0.25}" x2="${xMax}" y2="${y + rowH * 0.65}" stroke="#94a3b8" stroke-width="1.2"/>
            
            <!-- IQR Box -->
            <rect x="${xQ1}" y="${y + 2}" width="${Math.max(xQ3 - xQ1, 2)}" height="${rowH - 6}" fill="${boxColor}" stroke="${strokeColor}" stroke-width="1.2" rx="1"/>
            
            <!-- Median mark -->
            <line x1="${xMed}" y1="${y + 1}" x2="${xMed}" y2="${y + rowH - 3}" stroke="${strokeColor}" stroke-width="2.2"/>
            
            <!-- Median tekst -->
            <text x="${xMed}" y="${y - 1}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="${strokeColor}" text-anchor="middle">${d.med.toFixed(1)}%</text>
        `;

        // Outliers
        if (d.outliers) {
            d.outliers.forEach(outVal => {
                svg += `<circle cx="${getX(outVal)}" cy="${y + rowH * 0.45}" r="3" fill="#ef4444" stroke="#991b1b" stroke-width="0.8"/>`;
            });
        }
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}

// 5. PART-TO-WHOLE — Financial Waterfall Chart (BAC til EAC)
function renderVsPartToWhole() {
    const el = document.getElementById("vs-svg-part-to-whole");
    if (!el) return;

    let steps = [];
    let minVal = 7000, maxVal = 7600;

    if (currentVsSector === 'ALL') {
        steps = [
            { label: "Vedtatt BAC", val: 7240, type: "base", runVal: 7240 },
            { label: "+ Lønnsoppgjør", val: 185, type: "pos", runVal: 7425 },
            { label: "+ Vikar/overtid", val: 42, type: "pos", runVal: 7467 },
            { label: "+ Renter/pris", val: 28, type: "pos", runVal: 7495 },
            { label: "- Triage tiltak", val: -227, type: "neg", runVal: 7268 },
            { label: "Estimat EAC", val: 7268, type: "total", runVal: 7268 }
        ];
        minVal = 7000; maxVal = 7600;
    } else if (currentVsSector === 'HELSE') {
        steps = [
            { label: "Vedtatt BAC", val: 1850, type: "base", runVal: 1850 },
            { label: "+ Tariff/lønn", val: 48, type: "pos", runVal: 1898 },
            { label: "+ Døgnvikarer", val: 32, type: "pos", runVal: 1930 },
            { label: "+ Med. utstyr", val: 9, type: "pos", runVal: 1939 },
            { label: "- Turnustiltak", val: -74, type: "neg", runVal: 1865 },
            { label: "Estimat EAC", val: 1865, type: "total", runVal: 1865 }
        ];
        minVal = 1750; maxVal = 1980;
    } else if (currentVsSector === 'OPPVEKST') {
        steps = [
            { label: "Vedtatt BAC", val: 2120, type: "base", runVal: 2120 },
            { label: "+ Tariffvekst", val: 54, type: "pos", runVal: 2174 },
            { label: "+ Lærervikarer", val: 26, type: "pos", runVal: 2200 },
            { label: "+ Skoleskyss", val: 8, type: "pos", runVal: 2208 },
            { label: "- Stillingsgrep", val: -70, type: "neg", runVal: 2138 },
            { label: "Estimat EAC", val: 2138, type: "total", runVal: 2138 }
        ];
        minVal = 2050; maxVal = 2250;
    } else if (currentVsSector === 'BYUTVIKLING') {
        steps = [
            { label: "Vedtatt BAC", val: 940, type: "base", runVal: 940 },
            { label: "+ Entreprenør", val: 18, type: "pos", runVal: 958 },
            { label: "+ Vinterdrift", val: 7, type: "pos", runVal: 965 },
            { label: "- Selvkostfond", val: -25.5, type: "neg", runVal: 939.5 },
            { label: "Estimat EAC", val: 939.5, type: "total", runVal: 939.5 }
        ];
        minVal = 910; maxVal = 980;
    } else if (currentVsSector === 'KULTUR') {
        steps = [
            { label: "Vedtatt BAC", val: 380, type: "base", runVal: 380 },
            { label: "+ Lønnsvekst", val: 5.8, type: "pos", runVal: 385.8 },
            { label: "+ Strøm haller", val: 4.2, type: "pos", runVal: 390.0 },
            { label: "- Frivilliggrep", val: -9.9, type: "neg", runVal: 380.1 },
            { label: "Estimat EAC", val: 380.1, type: "total", runVal: 380.1 }
        ];
        minVal = 365; maxVal = 398;
    } else if (currentVsSector === 'ORG_TEK') {
        steps = [
            { label: "Vedtatt BAC", val: 460, type: "base", runVal: 460 },
            { label: "+ SaaS/skyliser", val: 8.5, type: "pos", runVal: 468.5 },
            { label: "+ Lønnsvekst", val: 7.2, type: "pos", runVal: 475.7 },
            { label: "- Konsulentkutt", val: -15.5, type: "neg", runVal: 460.2 },
            { label: "Estimat EAC", val: 460.2, type: "total", runVal: 460.2 }
        ];
        minVal = 445; maxVal = 485;
    } else {
        // OKONOMI
        steps = [
            { label: "Vedtatt BAC", val: 1490, type: "base", runVal: 1490 },
            { label: "+ Lånerenter", val: 22, type: "pos", runVal: 1512 },
            { label: "+ Pensjonstab", val: 14, type: "pos", runVal: 1526 },
            { label: "- Rentegevinst", val: -38.5, type: "neg", runVal: 1487.5 },
            { label: "Estimat EAC", val: 1487.5, type: "total", runVal: 1487.5 }
        ];
        minVal = 1450; maxVal = 1550;
    }

    const w = 460, h = 180, padL = 36, padR = 24, padTop = 22, padBottom = 26;
    const colW = (w - padL - padR) / steps.length;
    const getY = (val) => padTop + (h - padTop - padBottom) - ((val - minVal) / (maxVal - minVal)) * (h - padTop - padBottom);

    const baseBac = steps[0].val;
    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Nullreferanse ved BAC -->
        <line x1="${padL}" y1="${getY(baseBac)}" x2="${w - padR}" y2="${getY(baseBac)}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="${w - padR + 2}" y="${getY(baseBac) + 3}" font-size="7.5" font-family="var(--font-mono, monospace)" fill="#64748b">BAC</text>
    `;

    steps.forEach((s, i) => {
        const x = padL + i * colW + 4;
        const bw = colW - 8;
        let yTop, yHeight, color;

        if (s.type === "base" || s.type === "total") {
            yTop = getY(s.val);
            yHeight = (h - padBottom) - yTop;
            color = "#1b365d";
        } else if (s.type === "pos") {
            const prevVal = s.runVal - s.val;
            yTop = getY(s.runVal);
            yHeight = getY(prevVal) - yTop;
            color = "#c0392b";
        } else {
            const prevVal = s.runVal - s.val;
            yTop = getY(prevVal);
            yHeight = getY(s.runVal) - yTop;
            color = "#27ae60";
        }

        svg += `
            <rect x="${x}" y="${yTop}" width="${bw}" height="${Math.max(yHeight, 2)}" fill="${color}" rx="2"/>
            <text x="${x + bw / 2}" y="${yTop - 4}" font-size="7.5" font-family="var(--font-mono, monospace)" font-weight="700" fill="${color}" text-anchor="middle">
                ${s.val > 0 && s.type !== 'base' && s.type !== 'total' ? '+' : ''}${s.val}M
            </text>
            <text x="${x + bw / 2}" y="${h - 8}" font-size="7.2" font-weight="600" fill="#334155" text-anchor="middle">
                ${s.label}
            </text>
        `;

        if (i < steps.length - 1) {
            const nextX = padL + (i + 1) * colW + 4;
            const lineY = getY(s.runVal);
            svg += `<line x1="${x + bw}" y1="${lineY}" x2="${nextX}" y2="${lineY}" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="2,2"/>`;
        }
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}

// 6. CORRELATION — Driver Scatterplot (Sykefravær vs Vikar)
function renderVsCorrelation() {
    const el = document.getElementById("vs-svg-correlation");
    if (!el) return;

    let points = [];
    if (currentVsSector === 'ALL') {
        points = [
            { name: "Valhall Sykehjem", frav: 11.8, vik: 98, size: 6 },
            { name: "Strai Omsorg", frav: 10.4, vik: 84, size: 5 },
            { name: "Lunderød Bo", frav: 9.6, vik: 76, size: 4 },
            { name: "Torridal Skole", frav: 8.9, vik: 68, size: 6 },
            { name: "Vågsbygd Skole", frav: 8.2, vik: 58, size: 7 },
            { name: "Hellemyr Barnehage", frav: 8.6, vik: 62, size: 4 },
            { name: "Grim Skole", frav: 7.4, vik: 48, size: 5 },
            { name: "Søm Barnehage", frav: 7.1, vik: 44, size: 4 },
            { name: "Krossen Skole", frav: 6.8, vik: 38, size: 5 },
            { name: "Oddernes Barnehage", frav: 6.2, vik: 32, size: 4 },
            { name: "VAR-drift", frav: 4.4, vik: 18, size: 5 },
            { name: "Parkvesen", frav: 4.8, vik: 22, size: 4 },
            { name: "Kilden Teater", frav: 5.1, vik: 24, size: 5 },
            { name: "IKT Drift", frav: 4.2, vik: 16, size: 4 },
            { name: "Lønn/Regnskap", frav: 3.8, vik: 12, size: 4 },
            { name: "Kommuneadvokaten", frav: 3.2, vik: 8, size: 3 }
        ];
    } else if (currentVsSector === 'HELSE') {
        points = [
            { name: "Valhall Sykehjem", frav: 11.8, vik: 98, size: 6 },
            { name: "Strai Omsorgssenter", frav: 10.4, vik: 84, size: 5 },
            { name: "Lunderød Bo & Dag", frav: 9.6, vik: 76, size: 5 },
            { name: "Bispegra Omsorg", frav: 9.2, vik: 72, size: 5 },
            { name: "Hjemmetjenesten Vågsbygd", frav: 8.8, vik: 66, size: 6 },
            { name: "Hjemmetjenesten Lund", frav: 8.3, vik: 56, size: 5 },
            { name: "Rehabilitering Helsehus", frav: 7.6, vik: 45, size: 4 },
            { name: "Psykisk helse & Rus", frav: 7.1, vik: 40, size: 5 },
            { name: "Legevakten Akutt", frav: 5.9, vik: 28, size: 4 },
            { name: "Helsestasjonstjenesten", frav: 4.8, vik: 16, size: 4 }
        ];
    } else if (currentVsSector === 'OPPVEKST') {
        points = [
            { name: "Torridal Skole", frav: 8.9, vik: 68, size: 6 },
            { name: "Vågsbygd Skole", frav: 8.2, vik: 58, size: 6 },
            { name: "Hellemyr Barnehage", frav: 9.4, vik: 72, size: 5 },
            { name: "Grim Skole", frav: 7.4, vik: 48, size: 5 },
            { name: "Søm Barnehage", frav: 7.8, vik: 52, size: 4 },
            { name: "Krossen Skole", frav: 6.8, vik: 38, size: 5 },
            { name: "Oddernes Barnehage", frav: 6.2, vik: 32, size: 4 },
            { name: "Roligheden Skole", frav: 7.9, vik: 50, size: 5 },
            { name: "Wilds Minne Skole", frav: 6.5, vik: 34, size: 5 },
            { name: "PPT Kristiansand", frav: 5.2, vik: 18, size: 4 }
        ];
    } else if (currentVsSector === 'BYUTVIKLING') {
        points = [
            { name: "Samferdsel & Veidrift", frav: 5.8, vik: 34, size: 5 },
            { name: "Parkvesenet", frav: 6.2, vik: 38, size: 5 },
            { name: "VAR Drift", frav: 4.4, vik: 20, size: 6 },
            { name: "Eiendomsforvaltning", frav: 5.1, vik: 26, size: 5 },
            { name: "Byggesak & Kart", frav: 3.8, vik: 14, size: 4 },
            { name: "Klima & Landbruk", frav: 3.2, vik: 8, size: 3 }
        ];
    } else if (currentVsSector === 'KULTUR') {
        points = [
            { name: "Idrettsanlegg Aquarama", frav: 6.8, vik: 42, size: 5 },
            { name: "Kilden Drift", frav: 5.1, vik: 26, size: 5 },
            { name: "Hovedbiblioteket", frav: 4.8, vik: 22, size: 5 },
            { name: "Kulturskolen", frav: 4.1, vik: 16, size: 4 },
            { name: "Fritidsetaten", frav: 5.4, vik: 28, size: 4 }
        ];
    } else if (currentVsSector === 'ORG_TEK') {
        points = [
            { name: "Dokumentsenter & Arkiv", frav: 6.2, vik: 36, size: 5 },
            { name: "Lønnssenter", frav: 4.8, vik: 22, size: 4 },
            { name: "HR-avdelingen", frav: 4.5, vik: 18, size: 4 },
            { name: "IKT Brukerstøtte", frav: 4.2, vik: 16, size: 5 },
            { name: "Infrastruktur Sky", frav: 3.5, vik: 10, size: 4 }
        ];
    } else {
        // OKONOMI
        points = [
            { name: "Kemnerkontoret", frav: 4.6, vik: 20, size: 4 },
            { name: "Innkjøpsseksjonen", frav: 4.1, vik: 16, size: 4 },
            { name: "Konserncontroller", frav: 3.4, vik: 12, size: 4 },
            { name: "Regnskapsavdelingen", frav: 3.8, vik: 15, size: 4 },
            { name: "Politisk sekretariat", frav: 2.8, vik: 8, size: 3 }
        ];
    }

    const w = 460, h = 180, padL = 42, padR = 24, padTop = 18, padBottom = 26;
    const plotW = w - padL - padR;
    const plotH = h - padTop - padBottom;

    const minX = 2, maxX = 14;
    const minY = 0, maxY = 110;
    const getX = (val) => padL + ((val - minX) / (maxX - minX)) * plotW;
    const getY = (val) => padTop + plotH - ((val - minY) / (maxY - minY)) * plotH;

    // Beregn lineær regresjon dynamisk: y = mx + c
    let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0, sumYY = 0, n = points.length;
    points.forEach(p => {
        sumX += p.frav;
        sumY += p.vik;
        sumXY += p.frav * p.vik;
        sumXX += p.frav * p.frav;
        sumYY += p.vik * p.vik;
    });
    const meanX = sumX / n;
    const meanY = sumY / n;
    const slope = (sumXY - n * meanX * meanY) / (sumXX - n * meanX * meanX || 1);
    const intercept = meanY - slope * meanX;
    
    // Beregn R²
    const numR2 = Math.pow(sumXY - n * meanX * meanY, 2);
    const denR2 = (sumXX - n * meanX * meanX) * (sumYY - n * meanY * meanY) || 1;
    const r2 = Math.min(0.99, Math.max(0.40, numR2 / denR2));

    const regX1 = 3, regY1 = Math.max(minY, Math.min(maxY, slope * 3 + intercept));
    const regX2 = 12, regY2 = Math.max(minY, Math.min(maxY, slope * 12 + intercept));

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">
        <!-- Høyrisiko-kvadrant: Fravær > 8% & Vikar > 50k -->
        <rect x="${getX(8.0)}" y="${getY(110)}" width="${getX(14) - getX(8.0)}" height="${getY(50) - getY(110)}" fill="rgba(239, 68, 68, 0.06)" rx="2"/>
        <text x="${w - padR - 6}" y="${padTop + 14}" font-size="8" font-weight="700" fill="#dc2626" text-anchor="end">⚠️ Faresone: Fravær &gt; 8 % &amp; Vikar &gt; 50k</text>

        <!-- Akser -->
        <line x1="${padL}" y1="${getY(0)}" x2="${w - padR}" y2="${getY(0)}" stroke="#cbd5e1" stroke-width="1"/>
        <line x1="${padL}" y1="${padTop}" x2="${padL}" y2="${getY(0)}" stroke="#cbd5e1" stroke-width="1"/>

        <!-- Trendlinje -->
        <line x1="${getX(regX1)}" y1="${getY(regY1)}" x2="${getX(regX2)}" y2="${getY(regY2)}" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="3,2"/>
        <text x="${getX(regX2) - 8}" y="${getY(regY2) + 12}" font-size="8" font-family="var(--font-mono, monospace)" fill="#c0392b" font-weight="700">R² = ${r2.toFixed(2)}</text>

        <!-- Punkter -->
        ${points.map(p => {
            const isHigh = p.frav >= 8.0 && p.vik >= 50;
            const col = isHigh ? "#c0392b" : "#1b365d";
            return `
                <circle cx="${getX(p.frav)}" cy="${getY(p.vik)}" r="${p.size}" fill="${col}" opacity="0.85" stroke="#ffffff" stroke-width="1">
                    <title>${p.name}: ${p.frav}% fravær, ${p.vik}k kr vikar/årsverk</title>
                </circle>
            `;
        }).join('')}

        <!-- Akse-titler -->
        <text x="${w - padR}" y="${h - 6}" font-size="8" fill="#64748b" font-weight="600" text-anchor="end">Sykefravær (%) →</text>
        <text x="${padL - 4}" y="${padTop - 4}" font-size="8" fill="#64748b" font-weight="600" text-anchor="start">↑ Vikar/overtid (k kr per årsverk)</text>
    </svg>`;

    el.innerHTML = svg;
}

// 7. MAGNITUDE — Bullet Graphs
function renderVsMagnitude() {
    const el = document.getElementById("vs-svg-magnitude");
    if (!el) return;

    const w = 460, h = 180, padL = 145, padR = 40, top = 16, rowH = 46;
    const barH = 14;

    let bullets = [];
    if (currentVsSector === 'ALL') {
        bullets = [
            {
                title: "Netto driftsresultat",
                unit: "%",
                val: 1.42,
                target: 1.75,
                min: 0,
                max: 3.0,
                ranges: [
                    { val: 1.0, color: "#fee2e2" },
                    { val: 1.75, color: "#fef3c7" },
                    { val: 3.0, color: "#dcfce7" }
                ]
            },
            {
                title: "Disposisjonsfond",
                unit: "% (485M)",
                val: 6.70,
                target: 6.00,
                min: 0,
                max: 10.0,
                ranges: [
                    { val: 4.0, color: "#fee2e2" },
                    { val: 6.0, color: "#fef3c7" },
                    { val: 10.0, color: "#dcfce7" }
                ]
            },
            {
                title: "Netto lånegjeld",
                unit: "% (5.68 Mrd)",
                val: 78.4,
                target: 80.0,
                min: 50,
                max: 100,
                ranges: [
                    { val: 75.0, color: "#dcfce7" },
                    { val: 80.0, color: "#fef3c7" },
                    { val: 100.0, color: "#fee2e2" }
                ]
            }
        ];
    } else {
        const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
        const burnRate = Number(((meta.m9 / (meta.bac * 0.75)) * 100).toFixed(1));
        const cpiVal = meta.cpi;
        const sickRate = currentVsSector === 'HELSE' ? 9.6 : (currentVsSector === 'OPPVEKST' ? 8.4 : (currentVsSector === 'BYUTVIKLING' ? 4.8 : 4.5));
        const vikarRate = currentVsSector === 'HELSE' ? 8.2 : (currentVsSector === 'OPPVEKST' ? 6.8 : 3.0);

        bullets = [
            {
                title: "Budsjettoverholdelse YTD",
                unit: `% (${meta.m9}M)`,
                val: burnRate,
                target: 100.0,
                min: 90,
                max: 110,
                ranges: [
                    { val: 100.0, color: "#dcfce7" },
                    { val: 102.5, color: "#fef3c7" },
                    { val: 110.0, color: "#fee2e2" }
                ]
            },
            {
                title: "Vikar- & overtidsandel",
                unit: "% av lønn",
                val: vikarRate,
                target: 4.5,
                min: 0,
                max: 12.0,
                ranges: [
                    { val: 4.5, color: "#dcfce7" },
                    { val: 7.0, color: "#fef3c7" },
                    { val: 12.0, color: "#fee2e2" }
                ]
            },
            {
                title: "Sykefraværsnivå",
                unit: "% (HTA § 4)",
                val: sickRate,
                target: 6.5,
                min: 0,
                max: 14.0,
                ranges: [
                    { val: 6.5, color: "#dcfce7" },
                    { val: 8.0, color: "#fef3c7" },
                    { val: 14.0, color: "#fee2e2" }
                ]
            }
        ];
    }

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;

    bullets.forEach((b, i) => {
        const y = top + i * rowH;
        const plotW = w - padL - padR;
        const getX = (val) => padL + Math.max(0, Math.min(1, (val - b.min) / (b.max - b.min))) * plotW;

        svg += `
            <text x="${padL - 8}" y="${y + 10}" font-size="8.8" font-weight="700" fill="var(--navy-dark, #1b365d)" text-anchor="end">${b.title}</text>
            <text x="${padL - 8}" y="${y + 20}" font-size="7.8" fill="#64748b" text-anchor="end">${b.unit}</text>
        `;

        let prevX = padL;
        b.ranges.forEach(r => {
            const rx = getX(r.val);
            svg += `<rect x="${prevX}" y="${y + 2}" width="${rx - prevX}" height="${barH + 8}" fill="${r.color}"/>`;
            prevX = rx;
        });

        const valX = getX(b.val);
        svg += `<rect x="${padL}" y="${y + 6}" width="${valX - padL}" height="${barH}" fill="#1b365d" rx="1"/>`;

        const targetX = getX(b.target);
        svg += `
            <line x1="${targetX}" y1="${y}" x2="${targetX}" y2="${y + barH + 12}" stroke="#0f172a" stroke-width="2.5"/>
            <text x="${valX + 4}" y="${y + 16}" font-size="8.5" font-family="var(--font-mono, monospace)" font-weight="800" fill="#1b365d">${b.val.toFixed(1)}${b.unit.includes('%') ? '%' : ''}</text>
        `;
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}

// 8. FLOW — Sankey Diagram (Pengestrøm)
function renderVsFlow() {
    const el = document.getElementById("vs-svg-flow");
    if (!el) return;

    const meta = VS_SECTOR_META[currentVsSector] || VS_SECTOR_META["ALL"];
    const w = 460, h = 180, padL = 10, padR = 10, top = 10, bot = 10;
    const availH = h - top - bot;

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
    } else if (currentVsSector === 'HELSE') {
        totalVal = 1850;
        inNodes = [
            { name: "Kommunal Ramme", val: 1420, color: "#0369a1" },
            { name: "Toppfinansiering", val: 185, color: "#0284c7" },
            { name: "Egenbetaling", val: 165, color: "#0ea5e9" },
            { name: "NAV Refusjon", val: 80, color: "#38bdf8" }
        ];
        outNodes = [
            { name: "Sykehjem/Helsehus", val: 840, color: "#b91c1c" },
            { name: "Hjemmetjenester", val: 580, color: "#c2410c" },
            { name: "Rus/Psykisk helse", val: 210, color: "#d97706" },
            { name: "Legevakt/Felles", val: 140, color: "#475569" },
            { name: "Stab/Tildeling", val: 80, color: "#1e293b" }
        ];
    } else if (currentVsSector === 'OPPVEKST') {
        totalVal = 2120;
        inNodes = [
            { name: "Kommunal Ramme", val: 1720, color: "#0369a1" },
            { name: "Foreldrebetaling", val: 280, color: "#0284c7" },
            { name: "Statstilskudd", val: 95, color: "#0ea5e9" },
            { name: "NAV/Refusjoner", val: 25, color: "#38bdf8" }
        ];
        outNodes = [
            { name: "Grunnskoler (1-10)", val: 1040, color: "#b91c1c" },
            { name: "Komm. Barnehager", val: 560, color: "#c2410c" },
            { name: "Priv. Barnehager", val: 360, color: "#d97706" },
            { name: "PPT/Fam. Hus", val: 110, color: "#475569" },
            { name: "Fagstab/SFO", val: 50, color: "#1e293b" }
        ];
    } else if (currentVsSector === 'BYUTVIKLING') {
        totalVal = 940;
        inNodes = [
            { name: "Kommunal Ramme", val: 410, color: "#0369a1" },
            { name: "VAR Selvkost", val: 360, color: "#0284c7" },
            { name: "Parkering/Bom", val: 100, color: "#0ea5e9" },
            { name: "Byggesak/Kart", val: 70, color: "#38bdf8" }
        ];
        outNodes = [
            { name: "Vann & Avløp", val: 360, color: "#15803d" },
            { name: "Samferdsel & Vei", val: 310, color: "#b91c1c" },
            { name: "Eiendom & Drift", val: 140, color: "#475569" },
            { name: "Plan/Byggesak", val: 90, color: "#c2410c" },
            { name: "Miljø/Grønt", val: 40, color: "#1e293b" }
        ];
    } else if (currentVsSector === 'KULTUR') {
        totalVal = 380;
        inNodes = [
            { name: "Kommunal Ramme", val: 315, color: "#0369a1" },
            { name: "Billetter/Leie", val: 38, color: "#0284c7" },
            { name: "Kulturskoleegenbet.", val: 18, color: "#0ea5e9" },
            { name: "Stat/Fylkesstøtte", val: 9, color: "#38bdf8" }
        ];
        outNodes = [
            { name: "Idrett & Bad", val: 155, color: "#7e22ce" },
            { name: "Folkebibliotek", val: 95, color: "#0284c7" },
            { name: "Kulturskolen", val: 58, color: "#d97706" },
            { name: "Kulturvern/Støtte", val: 52, color: "#475569" },
            { name: "Fritidstilbud", val: 20, color: "#1e293b" }
        ];
    } else if (currentVsSector === 'ORG_TEK') {
        totalVal = 460;
        inNodes = [
            { name: "Rammetildeling", val: 420, color: "#0369a1" },
            { name: "Interne IKT-gebyr", val: 28, color: "#0284c7" },
            { name: "Refusjoner Lærling", val: 12, color: "#0ea5e9" }
        ];
        outNodes = [
            { name: "IKT Drift & Sky", val: 240, color: "#475569" },
            { name: "HR & Arbeidsmiljø", val: 115, color: "#0369a1" },
            { name: "Dokumentsenter", val: 65, color: "#1e293b" },
            { name: "Digitalisering", val: 40, color: "#0284c7" }
        ];
    } else {
        // OKONOMI
        totalVal = 1490;
        inNodes = [
            { name: "Felles Ramme/Skatt", val: 1350, color: "#0369a1" },
            { name: "Renter & Utbytte", val: 95, color: "#0284c7" },
            { name: "Finansfond", val: 45, color: "#0ea5e9" }
        ];
        outNodes = [
            { name: "Lånerenter/Avdrag", val: 820, color: "#1e293b" },
            { name: "Pensjon/Premieavvik", val: 380, color: "#475569" },
            { name: "Politisk styring/Stab", val: 180, color: "#0284c7" },
            { name: "Beredskap/Næring", val: 110, color: "#15803d" }
        ];
    }

    const scaleY = (availH - (inNodes.length - 1) * 4) / totalVal;

    let svg = `<svg viewBox="0 0 ${w} ${h}" style="width:100%; height:100%; font-family:var(--font-sans, system-ui);">`;

    // Venstre noder (Inntekter)
    let curY = top;
    inNodes.forEach(n => {
        n.h = n.val * scaleY;
        n.y = curY;
        curY += n.h + 4;
        svg += `
            <rect x="14" y="${n.y}" width="10" height="${n.h}" fill="${n.color}" rx="1"/>
            <text x="28" y="${n.y + Math.max(n.h / 2 + 3, 7)}" font-size="7.5" font-weight="700" fill="#334155">${n.name} (${n.val}M)</text>
        `;
    });

    // Senter kasse
    const midX = 220, midW = 14;
    const midH = totalVal * scaleY + (inNodes.length - 1) * 2;
    const midY = top + (availH - midH) / 2;
    svg += `
        <rect x="${midX}" y="${midY}" width="${midW}" height="${midH}" fill="#1b365d" rx="2"/>
        <text x="${midX + midW / 2}" y="${midY - 4}" font-size="8" font-weight="800" fill="#1b365d" text-anchor="middle">${treasuryLabel}</text>
    `;

    // Høyre noder (Utgifter)
    const outScaleY = (availH - (outNodes.length - 1) * 3) / totalVal;
    let outCurY = top;
    outNodes.forEach(n => {
        n.h = n.val * outScaleY;
        n.y = outCurY;
        outCurY += n.h + 3;
        svg += `
            <rect x="436" y="${n.y}" width="10" height="${n.h}" fill="${n.color}" rx="1"/>
            <text x="430" y="${n.y + Math.max(n.h / 2 + 3, 7)}" font-size="7.5" font-weight="700" fill="#334155" text-anchor="end">${n.name} (${n.val}M)</text>
        `;
    });

    // Bånd fra venstre til senter
    inNodes.forEach(n => {
        const x1 = 24, y1 = n.y;
        const x2 = midX, y2 = midY + (n.y - top) * 0.95;
        const cpX1 = x1 + (x2 - x1) * 0.5;
        const cpX2 = x2 - (x2 - x1) * 0.5;
        svg += `
            <path d="M ${x1},${y1} C ${cpX1},${y1} ${cpX2},${y2} ${x2},${y2} L ${x2},${y2 + n.h} C ${cpX2},${y2 + n.h} ${cpX1},${y1 + n.h} ${x1},${y1 + n.h} Z"
                  fill="${n.color}" fill-opacity="0.28"/>
        `;
    });

    // Bånd fra senter til høyre
    outNodes.forEach(n => {
        const x1 = midX + midW, y1 = midY + (n.y - top) * 0.95;
        const x2 = 436, y2 = n.y;
        const cpX1 = x1 + (x2 - x1) * 0.5;
        const cpX2 = x2 - (x2 - x1) * 0.5;
        svg += `
            <path d="M ${x1},${y1} C ${cpX1},${y1} ${cpX2},${y2} ${x2},${y2} L ${x2},${y2 + n.h} C ${cpX2},${y2 + n.h} ${cpX1},${y1 + n.h} ${x1},${y1 + n.h} Z"
                  fill="${n.color}" fill-opacity="0.25"/>
        `;
    });

    svg += `</svg>`;
    el.innerHTML = svg;
}
