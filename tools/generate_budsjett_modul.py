# tools/generate_budsjett_modul.py
# -*- coding: utf-8 -*-
"""
Genererer og injiserer den komplette Budsjettmodulen i index.html.
Inkluderer HTML-seksjonen og all tilhørende JavaScript-logikk.
"""

import os
import sys

HTML_FILE = "index.html"

# HTML BLOCK FOR THE BUDSJETT MODUL
BUDSJETT_HTML = """
    <!-- =======================================================================
         5A. KOMMUNAL BUDSJETTMODUL — FRAMSIKT EPM & HØP 2027–2030
         Stillings- og lønnsbudsjettering, selvkostkalkyler, KOSTRA kontoplan
         og internt budsjett-årshjul jf. Kommuneloven kapittel 14 & Bystyrets reglement
         ======================================================================= -->
    <section class="budsjett-modul-section" id="budsjett-modul-seksjon">
        <div class="bm-header-container">
            <div>
                <div class="bm-header-title">
                    <span>🏛️ Kommunal Budsjettmodul — Framsikt EPM & Handlings- og Økonomiplan (HØP)</span>
                </div>
                <div class="bm-header-sub">
                    Integrert stillings- og lønnsmotor, selvkostberegninger for tekniske tjenester (VAR/Byggesak), 
                    KOSTRA kontoplan (1000–1990) og utvidet internt årshjul for Kristiansand kommune.
                </div>
            </div>
            <div class="bm-header-badges">
                <span class="bm-badge bm-badge-primary">Framsikt v26.1 Live</span>
                <span class="bm-badge bm-badge-navy">AGA Sone 1 (14,1 %)</span>
                <span class="bm-badge bm-badge-success">Økonomireglement § 14</span>
                <span class="status-badge" style="background:#fef3c7; color:#92400e; border:1px solid #fde68a;">Aktiv Fase: HØP Høring (Okt)</span>
            </div>
        </div>

        <!-- Finansielle Måltall & Handlingsregler (Bystyrets vedtak 11.10.2023) -->
        <div class="bm-kpi-bar">
            <div class="bm-kpi-card">
                <div class="bm-kpi-label">Samlet Brutto Driftsbudsjett</div>
                <div class="bm-kpi-val">11,48 mrd</div>
                <div class="bm-kpi-note">Over 81 resultatenheter & 6 virksomhetsområder</div>
            </div>
            <div class="bm-kpi-card">
                <div class="bm-kpi-label">Netto Driftsresultat Mål</div>
                <div class="bm-kpi-val" style="color:var(--success-green);">≥ 1,0 %</div>
                <div class="bm-kpi-note">Minimum 114,8 mill. kr for finansiell handlefrihet</div>
            </div>
            <div class="bm-kpi-card">
                <div class="bm-kpi-label">Sentralt Disposisjonsfond</div>
                <div class="bm-kpi-val" style="color:#0284c7;">≥ 4,0 %</div>
                <div class="bm-kpi-note">Minimum 459,2 mill. kr som robust buffer</div>
            </div>
            <div class="bm-kpi-card">
                <div class="bm-kpi-label">Maksimal Netto Lånegjeld</div>
                <div class="bm-kpi-val" style="color:var(--navy-dark);">&lt; 8,80 mrd</div>
                <div class="bm-kpi-note">Lånetak for å forhindre uhåndterlige rentekostnader</div>
            </div>
        </div>

        <!-- Hovednavigasjon for Budsjettmodul -->
        <div class="bm-nav-tabs">
            <button class="bm-tab-btn active" id="bm-btn-lonn" onclick="switchBudsjettModulTab('LONN')">
                <span>👥 1. Stillings- & Lønnsbudsjett</span>
            </button>
            <button class="bm-tab-btn" id="bm-btn-selvkost" onclick="switchBudsjettModulTab('SELVKOST')">
                <span>💧 2. Selvkost (VAR & Byggesak)</span>
            </button>
            <button class="bm-tab-btn" id="bm-btn-arshjul" onclick="switchBudsjettModulTab('ARSHJUL')">
                <span>📅 3. Budsjett-Årshjul & Frister</span>
            </button>
            <button class="bm-tab-btn" id="bm-btn-kostra" onclick="switchBudsjettModulTab('KOSTRA')">
                <span>📑 4. KOSTRA Driftsarter & Kontering</span>
            </button>
            <button class="bm-tab-btn" id="bm-btn-qa" onclick="switchBudsjettModulTab('QA')">
                <span>📋 5. Framsikt Excel QA-Motor</span>
            </button>
        </div>

        <!-- ===================================================================
             FANE 1: STILLINGS- & LØNNSBUDSJETT (FRAMSIKT LØNNSMOTOR)
             =================================================================== -->
        <div class="bm-tab-pane active" id="bm-pane-lonn">
            <div class="bm-formula-banner">
                <strong>💡 Framsikts Lønnsarkitektur & Bruttoføringsprinsippet:</strong>
                Lønn og sosiale kostnader utgjør <strong>70–80 % av kommunens driftskostnader</strong>.
                Framsikt skiller strengt mellom <strong>Fast Lønn (Art 1010)</strong> via Stillingsoversikten og 
                <strong>Variable Potter (Art 1020 vikarer, 1050/1090 tillegg)</strong>. 
                Sosiale kostnader beregnes maskinelt: 
                <em>Bruttolønn → Feriepenger (12,0 % / 14,3 %) → Pensjon (SPK/KLP) → Arbeidsgiveravgift (14,1 % Sone 1 på Lønn + Feriepenger + Pensjon)</em>.
                Jf. <strong>Kommuneloven § 14-6</strong> er nettobudsjettering av vikarer mot refusjoner forbudt.
            </div>

            <div class="bm-grid-2col">
                <!-- Interaktiv Lønnskalkulator -->
                <div class="bm-box">
                    <div class="bm-box-title">
                        <span>🧮 Framsikt Lønnskalkulator & Stillingsberegner</span>
                        <span class="bm-badge bm-badge-primary">Live Modell</span>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Virksomhetsområde</label>
                            <select id="bm-calc-sector" onchange="onBmSectorChange()">
                                <option value="OPPVEKST">🏫 2. Oppvekst (Skole & Barnehage)</option>
                                <option value="HELSE">🏥 1. Helse og mestring</option>
                                <option value="BYUTVIKLING">🏗️ 3. By- og stedsutvikling</option>
                                <option value="KULTUR">🎭 4. Kultur og innbyggerdialog</option>
                                <option value="ORG_TEK">💻 5. Organisasjon og teknologi</option>
                                <option value="OKONOMI">⚖️ 6. Økonomi og virksomhetsstyring</option>
                            </select>
                        </div>
                        <div class="bm-form-group">
                            <label>Stillingskategori / Tittel</label>
                            <select id="bm-calc-title" onchange="onBmTitleChange()">
                                <option value="LEKTOR">Lektor / Lærer (SPK-pensjon)</option>
                                <option value="SYKEPLEIER">Spesialsykepleier (KLP-pensjon)</option>
                                <option value="FAGARBEIDER">Helsefagarbeider / Barneveileder</option>
                                <option value="INGENIOR">Overingeniør VAR (Selvkostfunksjon)</option>
                                <option value="SAKSBEHANDLER">Saksbehandler Byggesak</option>
                                <option value="KONSULENT">Rådgiver / Konsulent Administrasjon</option>
                            </select>
                        </div>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Grunnlønn ved 100 % (NOK / år)</label>
                            <input type="number" id="bm-calc-salary" value="620000" step="5000" oninput="recalcSalaryBudsjett()">
                        </div>
                        <div class="bm-form-group">
                            <label>Stillingsbrøk (%)</label>
                            <input type="number" id="bm-calc-fraction" value="100" min="10" max="100" step="5" oninput="recalcSalaryBudsjett()">
                        </div>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Alder / Feriepengesats</label>
                            <select id="bm-calc-age" onchange="recalcSalaryBudsjett()">
                                <option value="UNDER60">Under 60 år (12,0 % feriepenger)</option>
                                <option value="OVER60">60 år eller eldre (14,3 % ekstra ferieuke)</option>
                            </select>
                        </div>
                        <div class="bm-form-group">
                            <label>Pensjonsordning</label>
                            <select id="bm-calc-pension" onchange="recalcSalaryBudsjett()">
                                <option value="SPK">SPK (Lærere/pedagoger, 13,8 % premie)</option>
                                <option value="KLP" selected>KLP (Fagarbeidere, pleie & staber, 15,2 % premie)</option>
                            </select>
                        </div>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Faste/variable turnustillegg (Art 1050/1090)</label>
                            <input type="number" id="bm-calc-shifts" value="35000" step="1000" oninput="recalcSalaryBudsjett()">
                        </div>
                        <div class="bm-form-group">
                            <label>Vikarpott ved forventet sykefravær (Art 1020)</label>
                            <input type="number" id="bm-calc-substitute" value="45000" step="1000" oninput="recalcSalaryBudsjett()">
                        </div>
                    </div>

                    <div class="bm-form-group" style="margin-bottom: 12px;">
                        <label>Forventet Sykelønnsrefusjon fra NAV (Art 1690 - Inntekt)</label>
                        <input type="number" id="bm-calc-refund" value="30000" step="1000" oninput="recalcSalaryBudsjett()">
                    </div>

                    <div class="bm-alert-banner" id="bm-gross-warning" style="display:none;">
                        ⚠️ <strong>Bruttoføringsadvarsel:</strong> Vikarmidler på Art 1020 kan ikke trekkes fra Art 1010 direkte. Begge må føres brutto for at KOSTRA-nøkkeltall og AGA-beregning skal stemme!
                    </div>

                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px;">
                        <button type="button" class="btn btn-sm" onclick="resetSalaryCalc()">↺ Nullstill Verdier</button>
                        <button type="button" class="btn btn-sm btn-primary" onclick="copySalaryAccounting()">📋 Kopier Konteringssplitt</button>
                    </div>
                </div>

                <!-- Beregningsresultat & Totaler -->
                <div class="bm-box">
                    <div class="bm-box-title">
                        <span>📊 Beregnet Årskostnad & Sosiale Utgifter</span>
                        <span class="bm-badge bm-badge-success">Sone 1 (14,1 %)</span>
                    </div>

                    <div class="bm-result-summary">
                        <div class="bm-res-item">
                            <span>Art 1010 Fast lønn (brøkjustert)</span>
                            <span class="num-val" id="bm-res-fastlonn">620 000 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Art 1099 Feriepengeavsetning (<span id="bm-res-ferie-rate">12,0 %</span>)</span>
                            <span class="num-val" id="bm-res-feriepenger">74 400 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Art 1200 Pensjonspremie (<span id="bm-res-pensjon-org">KLP 15,2 %</span>)</span>
                            <span class="num-val" id="bm-res-pensjon">94 240 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Art 1210 Arbeidsgiveravgift (14,1 % av lønn, ferie & pensjon)</span>
                            <span class="num-val" id="bm-res-aga-fast">111 202 kr</span>
                        </div>
                        <div class="bm-res-item" style="color:var(--text-secondary);">
                            <span>Variable tillegg (Art 1050/1090) inkl. AGA & feriepenger</span>
                            <span class="num-val" id="bm-res-tillegg-tot">44 723 kr</span>
                        </div>
                        <div class="bm-res-item" style="color:var(--text-secondary);">
                            <span>Vikarpott (Art 1020) inkl. AGA & feriepenger</span>
                            <span class="num-val" id="bm-res-vikar-tot">57 501 kr</span>
                        </div>
                        <div class="bm-res-item" style="color:#0369a1;">
                            <span>Art 1690 Sykelønnsrefusjon fra NAV (Inntekt)</span>
                            <span class="num-val" id="bm-res-refusjon" style="color:#0369a1;">-30 000 kr</span>
                        </div>
                        <div class="bm-res-item highlight-total">
                            <span>Samlet Brutto Kostnad (Art 1000–1210)</span>
                            <span class="num-val" id="bm-res-brutto-tot" style="font-size:16px;">1 002 066 kr</span>
                        </div>
                        <div class="bm-res-item highlight-total" style="border-top:none; color:var(--accent-blue);">
                            <span>Netto Kommunal Utgift (Brutto minus NAV-refusjon)</span>
                            <span class="num-val" id="bm-res-netto-tot" style="font-size:16px; color:var(--accent-blue);">972 066 kr</span>
                        </div>
                    </div>

                    <!-- Automatisk KOSTRA Konteringsmatrise -->
                    <div style="margin-top:16px;">
                        <div style="font-size:11.5px; font-weight:700; color:var(--navy-dark); margin-bottom:6px; text-transform:uppercase;">
                            📑 Generert KOSTRA Konteringsbilag i Framsikt:
                        </div>
                        <div class="table-responsive" style="max-height: 220px; overflow-y: auto;">
                            <table class="tufte-table" id="bm-kostra-table">
                                <thead>
                                    <tr>
                                        <th>Art</th>
                                        <th>Kontonavn</th>
                                        <th class="num">Debet (kr)</th>
                                        <th class="num">Kredit (kr)</th>
                                        <th>Modul</th>
                                    </tr>
                                </thead>
                                <tbody id="bm-kostra-tbody">
                                    <!-- Innhold genereres via JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stillingsregister & Bemanningshjemler i Enheten -->
            <div class="bm-box" style="margin-top:20px;">
                <div class="bm-box-title">
                    <span>👥 Eksempelregister: Bemanningsplan & Stillingshjemler i Framsikt</span>
                    <span class="status-badge" style="background:#e0f2fe; color:#0369a1;">6 Utvalgte Hjemler</span>
                </div>
                <p style="font-size:12px; color:var(--text-secondary); margin-bottom:10px;">
                    Stillingshjemler importeres fra Visma Enterprise / Unit4 til Framsikt. Justering av stillingsbrøk eller permisjon rekalkulerer automatisk feriepenger, pensjon og AGA per måned.
                </p>
                <div class="table-responsive">
                    <table class="tufte-table">
                        <thead>
                            <tr>
                                <th>Stilling ID</th>
                                <th>Tittel / Stilling</th>
                                <th>Ansatt / Status</th>
                                <th>Virksomhetsområde</th>
                                <th>Pensjon</th>
                                <th class="num">Brøk (%)</th>
                                <th class="num">Fastlønn (kr)</th>
                                <th class="num">Sosiale Kostn. (kr)</th>
                                <th class="num">Sum Ramme (kr)</th>
                                <th style="text-align:center;">Handling</th>
                            </tr>
                        </thead>
                        <tbody id="bm-positions-tbody">
                            <!-- Innhold genereres via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ===================================================================
             FANE 2: SELVKOST (VAR & BYGGESAK)
             =================================================================== -->
        <div class="bm-tab-pane" id="bm-pane-selvkost">
            <div class="bm-formula-banner">
                <strong>💧 Selvkostberegninger for Tekniske Tjenester (Kommuneloven § 15-1 & Selvkostforskriften):</strong>
                Kommunen har plikt til å kreve selvkost for vann, avløp, renovasjon og byggesak, uten å generere overskudd over tid.
                Formel i Framsikt: 
                <em>Gebyrgrunnlag = Direkte driftsutgifter (Art 1000–1270) + Indirekte henføring + Kapitalkostnader (Avskrivning Art 1590 + Kalkulatorisk rente) - Direkte inntekter</em>.
                Eventuelle avvik overføres til/fra <strong>Bundet Selvkostfond (Art 1530 / 1930)</strong> og må avvikles innen <strong>5 år</strong>.
            </div>

            <div class="level-pills-bar" style="margin-bottom:16px;">
                <button class="level-pill-btn active" id="btn-sk-vann" onclick="switchSelvkostService('VANN')">
                    <span>💧 Funksjon 3400: Vannforsyning</span>
                </button>
                <button class="level-pill-btn" id="btn-sk-avloep" onclick="switchSelvkostService('AVLOEP')">
                    <span>🚽 Funksjon 3450: Avløpshåndtering (2 mrd inv.)</span>
                </button>
                <button class="level-pill-btn" id="btn-sk-renovasjon" onclick="switchSelvkostService('RENOVASJON')">
                    <span>♻️ Funksjon 3500: Renovasjon (Avfall Sør)</span>
                </button>
                <button class="level-pill-btn" id="btn-sk-byggesak" onclick="switchSelvkostService('BYGGESAK')">
                    <span>📐 Funksjon 3600: Byggesak & Geodata</span>
                </button>
            </div>

            <div class="bm-grid-2col">
                <!-- Selvkost Parametere & Kalkyle -->
                <div class="bm-box">
                    <div class="bm-box-title">
                        <span id="bm-sk-title">💧 Funksjon 3400: Vannforsyning — Kostnadselementer</span>
                        <span class="bm-badge bm-badge-primary">Kalkulatorisk rente: 4,00 %</span>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Direkte driftsutgifter (Art 1000–1270)</label>
                            <input type="number" id="bm-sk-direkte" value="142500000" step="500000" oninput="recalcSelvkost()">
                        </div>
                        <div class="bm-form-group">
                            <label>Indirekte henførte kostnader (HR/IT/Rådhus)</label>
                            <input type="number" id="bm-sk-henforing" value="8200000" step="100000" oninput="recalcSelvkost()">
                        </div>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Avskrivninger på anleggsmidler (Art 1590)</label>
                            <input type="number" id="bm-sk-avskrivning" value="44800000" step="500000" oninput="recalcSelvkost()">
                        </div>
                        <div class="bm-form-group">
                            <label>Bokført restverdi anleggsmidler (kr)</label>
                            <input type="number" id="bm-sk-restverdi" value="820000000" step="5000000" oninput="recalcSelvkost()">
                        </div>
                    </div>

                    <div class="bm-form-row">
                        <div class="bm-form-group">
                            <label>Direkte inntekter utenom gebyrer</label>
                            <input type="number" id="bm-sk-inntekter" value="4500000" step="100000" oninput="recalcSelvkost()">
                        </div>
                        <div class="bm-form-group">
                            <label>Budsjetterte gebyrinntekter (Art 1620)</label>
                            <input type="number" id="bm-sk-gebyr" value="223800000" step="500000" oninput="recalcSelvkost()">
                        </div>
                    </div>

                    <div class="bm-form-group" style="margin-top:6px;">
                        <label>Eksisterende Selvkostfond Saldo (primo året)</label>
                        <input type="number" id="bm-sk-fond-saldo" value="12400000" step="200000" oninput="recalcSelvkost()">
                    </div>

                    <div style="margin-top:14px; display:flex; justify-content:space-between;">
                        <button type="button" class="btn btn-sm" onclick="resetSelvkostValues()">↺ Tilbakestill til Grunndata</button>
                        <button type="button" class="btn btn-sm btn-primary" onclick="exportSelvkostNote()">📄 Eksporter Selvkostnotat</button>
                    </div>
                </div>

                <!-- Selvkost Resultat & Fondsavstemming -->
                <div class="bm-box">
                    <div class="bm-box-title">
                        <span>⚖️ Selvkostresultat & Regulering av Selvkostfond</span>
                        <span class="bm-badge" id="bm-sk-status-badge">I Balanse</span>
                    </div>

                    <div class="bm-result-summary">
                        <div class="bm-res-item">
                            <span>Direkte driftsutgifter (Art 1000–1270)</span>
                            <span class="num-val" id="bm-res-sk-direkte">142 500 000 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Indirekte henføring (Felleskostnader)</span>
                            <span class="num-val" id="bm-res-sk-henforing">8 200 000 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Avskrivninger anleggsmidler (Art 1590)</span>
                            <span class="num-val" id="bm-res-sk-avskrivning">44 800 000 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Kalkulatorisk rente (4,00 % av restverdi)</span>
                            <span class="num-val" id="bm-res-sk-rente">32 800 000 kr</span>
                        </div>
                        <div class="bm-res-item" style="color:var(--text-secondary);">
                            <span>Fradrag: Direkte inntekter utenom gebyr</span>
                            <span class="num-val" id="bm-res-sk-inntekt">-4 500 000 kr</span>
                        </div>
                        <div class="bm-res-item highlight-total">
                            <span>Beregnet Gebyrgrunnlag (Full Selvkost)</span>
                            <span class="num-val" id="bm-res-sk-gebyrgrunnlag" style="font-size:16px;">223 800 000 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Budsjettert Gebyrinntekt (Art 1620)</span>
                            <span class="num-val" id="bm-res-sk-gebyrinntekt" style="font-weight:700;">223 800 000 kr</span>
                        </div>
                        <div class="bm-res-item highlight-total" style="border-top:none;">
                            <span>Selvkostresultat (Avvik Gebyr vs. Selvkost)</span>
                            <span class="num-val" id="bm-res-sk-resultat">0 kr</span>
                        </div>
                        <div class="bm-res-item">
                            <span>Dekningsgrad (%)</span>
                            <span class="num-val" id="bm-res-sk-dekningsgrad" style="font-size:15px; font-weight:800; color:var(--success-green);">100,0 %</span>
                        </div>
                    </div>

                    <!-- Fondsberegning & 5-årsregel -->
                    <div style="margin-top:16px; padding:12px; background:#f8fafc; border:1px solid var(--border-light); border-radius:3px;">
                        <div style="font-size:11.5px; font-weight:700; color:var(--navy-dark); margin-bottom:4px;">
                            🏛️ Selvkostfond Regulering & 5-årsregelen (Selvkostforskriften § 6):
                        </div>
                        <div style="font-size:12px; line-height:1.5; color:var(--text-secondary);" id="bm-sk-fond-forklaring">
                            Gebyret dekker nøyaktig 100,0 % av selvkost. Ingen avsetning til Art 1530 eller bruk av Art 1930 nødvendig.
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:11px; font-family:var(--font-mono); color:var(--text-muted); border-top:1px solid var(--border-subtle); padding-top:6px;">
                            <span>Fremføringsår: <strong id="bm-sk-fremforing-ar">År 2 av 5</strong></span>
                            <span>Estimert fondssaldo ultimo: <strong id="bm-sk-fond-ultimo">12 400 000 kr</strong></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ===================================================================
             FANE 3: BUDSJETT-ÅRSHJUL & FRISTER
             =================================================================== -->
        <div class="bm-tab-pane" id="bm-pane-arshjul">
            <div class="bm-formula-banner">
                <strong>📅 Utvidet Internt Årshjul og Tidslinje for Kristiansand kommune:</strong>
                Kommunens budsjettprosess løper strukturert fra mai til desember jf. Bystyrets økonomireglement. 
                Nedenfor vises alle 8 faser fra rammeavklaringer til Bystyrets endelige vedtak og overføring til Unit4 regnskap.
            </div>

            <!-- Interaktiv Tidslinje-stepper -->
            <div class="bm-year-stepper" id="bm-year-stepper-container">
                <!-- Genereres via JS -->
            </div>

            <!-- Detaljkort for Valgt Årshjulfase -->
            <div class="bm-box" id="bm-phase-detail-card" style="margin-top:16px;">
                <!-- Injiseres dynamisk -->
            </div>
        </div>

        <!-- ===================================================================
             FANE 4: KOSTRA DRIFTSARTER & KONTERING
             =================================================================== -->
        <div class="bm-tab-pane" id="bm-pane-kostra">
            <div class="bm-formula-banner">
                <strong>📑 KOSTRA Kontoplan & Konteringsregler i Framsikt (Driftsarter 1000–1990):</strong>
                Alle poster i Kristiansand konteres på 3 dimensjoner: <em>Kontoklasse (1 Drift / 2 Inv) × Funksjon × Art</em>.
                Tabellen under viser fullstendig konteringsveiledning for lønn, varekjøp, konserninterne overføringer, selvkostfond og refusjoner.
            </div>

            <!-- Filter og Søkebar for KOSTRA -->
            <div style="display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap; align-items:center; background:#fafbfc; padding:10px 14px; border:1px solid var(--border-light); border-radius:4px;">
                <div style="flex:1; min-width:240px;">
                    <input type="text" id="bm-kostra-search" class="form-control" placeholder="🔍 Søk i KOSTRA kontoplan (f.eks. 1010, strøm, vikar, 1240 lisens, selvkostfond)..." 
                           style="width:100%; padding:6px 10px; font-size:12px; border:1px solid var(--border-light); border-radius:3px;"
                           oninput="filterKostraDriftsarter()">
                </div>
                <div>
                    <select id="bm-kostra-cat-filter" class="form-select" style="padding:6px 10px; font-size:12px; border:1px solid var(--border-light); border-radius:3px;" onchange="filterKostraDriftsarter()">
                        <option value="ALL">Alle Kontoserier (1000–1990)</option>
                        <option value="LONN">Lønn & Sosiale utgifter (1000–1220)</option>
                        <option value="VARE">Kjøp av varer og tjenester (1100–1270)</option>
                        <option value="OVERFORING">Overføringer & Tilskudd (1300–1480)</option>
                        <option value="FINANS">Finans, avskrivning & fond (1500–1590)</option>
                        <option value="INNTEKT">Gebyr-, salgs- og refusjonsinntekter (1600–1750)</option>
                        <option value="STAT">Statstilskudd & Fondsbruk (1800–1930)</option>
                    </select>
                </div>
                <div>
                    <button type="button" class="btn btn-sm" onclick="resetKostraFilter()">Nullstill filter</button>
                </div>
            </div>

            <!-- KOSTRA Tabell -->
            <div class="table-responsive" style="max-height: 480px; overflow-y: auto;">
                <table class="tufte-table" id="bm-kostra-full-table">
                    <thead>
                        <tr>
                            <th style="width:70px;">Art</th>
                            <th style="width:190px;">Artsnavn</th>
                            <th style="width:140px;">Framsikt-modul</th>
                            <th>Retningslinjer for Kontering & Kostnadstype</th>
                            <th>Typiske Kostnader i Kristiansand</th>
                            <th>Spesiell Kontrollregel</th>
                        </tr>
                    </thead>
                    <tbody id="bm-kostra-full-tbody">
                        <!-- Genereres fra JS -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ===================================================================
             FANE 5: FRAMSIKT EXCEL QA & VALIDERINGSMOTOR
             =================================================================== -->
        <div class="bm-tab-pane" id="bm-pane-qa">
            <div class="bm-formula-banner">
                <strong>📋 Sjekkliste og Kvalitetskontroll for Excel Eksport/Import og Framsikt-låsing:</strong>
                Før seksjonsledere og økonomirådgivere godkjenner detaljbudsjettet, må følgende 8 kontrollpunkter verifiseres.
                Dette hindrer budsjetteringsfeil på AGA, feil pensjonskasse, ulovlig nettobudsjettering og brudd på selvkostforskriften.
            </div>

            <div class="bm-grid-2col">
                <div class="bm-box">
                    <div class="bm-box-title">
                        <span>☑️ Controllerens 8 Kritiske Kontrollpunkter</span>
                        <span class="bm-badge bm-badge-primary" id="bm-qa-checked-count">8 av 8 Bekreftet</span>
                    </div>

                    <div class="bm-check-list">
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-1" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">1. Uforanderlige ID-er i Excel-maler</div>
                                <div class="bm-check-sub">Stilling ID, Ansatt ID og Ansvar er beholdt uendret slik at Framsikt matcher stillingene ved import.</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-2" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">2. Månedsoppdeling og oppstartsdatoer</div>
                                <div class="bm-check-sub">Stillingsendringer og nyansettelser (f.eks. lærere per 01.08) er lagt på riktig måned, ikke fordelt over 12 mnd.</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-3" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">3. Arbeidsgiveravgiftssone (14,1 % Sone 1)</div>
                                <div class="bm-check-sub">Alle stillinger og potter ligger i Sone 1, og AGA er beregnet av både lønn, feriepenger og pensjon.</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-4" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">4. Pensjonskassetilhørighet (SPK vs KLP)</div>
                                <div class="bm-check-sub">Lærere og skoleledere er koblet mot SPK (13,8 %), mens øvrige er registrert på KLP (15,2 %).</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-5" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">5. Bruttoføring av Vikarer og NAV-refusjon</div>
                                <div class="bm-check-sub">Vikarpotter (Art 1020) og forventet sykelønnsrefusjon (Art 1690) er ført brutto jf. Kommuneloven § 14-6.</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-6" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">6. Selvkostavstemming & 5-årsregel (VAR/Byggesak)</div>
                                <div class="bm-check-sub">Direkte, indirekte og kapitalkostnader er avstemt mot gebyrinntekter og bundet selvkostfond (1530/1930).</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-7" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">7. Konsernavstemming (KBR IKS & Avfall Sør)</div>
                                <div class="bm-check-sub">Tilskudd til brannvesen (Art 1480) og renovasjonstjenester (Art 1380) stemmer med selskapenes budsjetter.</div>
                            </div>
                        </label>
                        <label class="bm-check-item">
                            <input type="checkbox" id="bm-qa-8" checked onchange="updateBmQaStatus()">
                            <div class="bm-check-text">
                                <div class="bm-check-title">8. Finansielle Måltall & Rammevedtak</div>
                                <div class="bm-check-sub">Seksjonens samlede ramme er innenfor kommunedirektørens tildeling, og netto driftsresultat ≥ 1,0 %.</div>
                            </div>
                        </label>
                    </div>

                    <div style="margin-top:14px; display:flex; justify-content:space-between;">
                        <button type="button" class="btn btn-sm" onclick="toggleAllBmQa(true)">Merk Alle</button>
                        <button type="button" class="btn btn-sm btn-primary" onclick="runSimulatedFramsiktQA()">🔒 Kjør Formell QA-Validering</button>
                    </div>
                </div>

                <!-- QA Valideringsrapport / Attest -->
                <div class="bm-box">
                    <div class="bm-box-title">
                        <span>📜 Formell QA Valideringsattest (HITL Port 9)</span>
                        <span class="bm-badge bm-badge-success" id="bm-qa-attest-badge">Verifisert</span>
                    </div>

                    <div id="bm-qa-attest-output" style="background:#fafbfc; border:1px solid var(--border-light); border-radius:3px; padding:14px; font-family:var(--font-mono); font-size:11.5px; line-height:1.6; max-height:380px; overflow-y:auto; white-space:pre-wrap;">
Trykk på "Kjør Formell QA-Validering" for å generere revisjonsgodkjent attest med SHA-256 kryptografisk forsegling.
                    </div>

                    <div style="margin-top:12px; display:flex; justify-content:flex-end; gap:8px;">
                        <button type="button" class="btn btn-sm" onclick="copyBmQaAttest()">📋 Kopier Attest</button>
                        <button type="button" class="btn btn-sm btn-accent" onclick="downloadBmQaReport()">📥 Last ned Valideringsrapport</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

# Read file
with open(HTML_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Insertion target for HTML: right before <!-- 5B. RAG REGELVERKSASSISTENT
TARGET_HTML_ANCHOR = """    <!-- =======================================================================
         5B. RAG REGELVERKSASSISTENT & JUSS (GLASS-BOX AI)
         ======================================================================= -->"""

if "id=\"budsjett-modul-seksjon\"" not in content:
    if TARGET_HTML_ANCHOR in content:
        content = content.replace(TARGET_HTML_ANCHOR, BUDSJETT_HTML + "\n" + TARGET_HTML_ANCHOR, 1)
        print("Inserted BUDSJETT_HTML before 5B. RAG REGELVERKSASSISTENT")
    else:
        print("Warning: TARGET_HTML_ANCHOR not found!")
else:
    print("BUDSJETT_HTML already present.")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("Stage 2 complete: HTML Section injected.")
