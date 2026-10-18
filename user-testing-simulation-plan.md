# User Testing & Pre-Deployment Simulation Blueprint
**Kristiansand Kommune — AI Project Controller Hub (`AI_KOM`)**

A comprehensive, production-ready guide to simulating user interactions, identifying UX friction points, and automating quality gates across municipal roles before deploying changes to [index.html](file:///C:/Users/frank/Desktop/AI_KOM/index.html) and underlying AI services.

---

## 1. Overview & Strategy

Simulating user interactions before deploying financial AI tools to Kristiansand Kommune (6 virksomhetsområder, 81 enheter, 7,24 milliarder NOK årsbudsjett) prevents navigation dead-ends, miscalculated variances, legal compliance breaches (*Kommuneloven § 14-5*), and user frustration.

This blueprint combines five complementary testing vectors:
1. **Municipal Synthetic Persona Simulation**: Headless Playwright agents acting as distinct municipal personas (Enhetsleder, Kommunalsjef, Controller, Revisor).
2. **Unmoderated Quantitative UX Analytics**: Task completion rate, direct path ratio, and misclick tracking.
3. **AI-Moderated Qualitative Probing**: Real-time contextual follow-ups triggered by user hesitation (> 5s pause) or repetitive clicking.
4. **Small-Cohort Human Validation**: The 5-user Nielsen Norman rule executed with actual municipal stakeholders.
5. **Automated CI/CD Golden Dataset Evaluation Gates**: Regression testing against ground-truth datasets via **Agent 13** (`python tools/run_tool.py eval --gate`).

---

## 2. Phase 1: Synthetic Persona Simulation

Synthetic AI User Personas execute scripted and exploratory user journeys against [index.html](file:///C:/Users/frank/Desktop/AI_KOM/index.html) using browser automation (Playwright / Browser Subagent).

### Municipal Persona Matrix

| Persona ID | Municipal Role & Profile | Behavior Pattern | Validation Focus |
| :--- | :--- | :--- | :--- |
| `P1_ENHETSLEDER` | **Leder Hjemmetjenesten Vågsbygd (Enhet 202)**<br>Lav teknisk toleranse, operativt travel, lite tid. | Forventer 1-klikks månedsoversikt, trykker kun primærknapper, leser ikke veiledninger. | Min Enhet-fane, fravær av teknisk IT-sjargong, rask avklaring av sykefravær og NAV-refusjon (art 1690). |
| `P2_KOMMUNALSJEF` | **Virksomhetsdirektør Oppvekst / Helse**<br>Strategisk overblikk, forbereder formannskapssaker. | Veksler mellom virksomhetsområder, analyserer Top 3-takometre, ber om Bystyret PPTX-eksport. | Sektor & Konsern-fane, konsistent oppdatering av takometre, direkte kobling til saksfremlegg. |
| `P3_CONTROLLER` | **Senior Project Controller (Frank Ellingsen)**<br>Avansert BI-bruker, dyp økonomiforståelse. | Kjører DuckDB-spørringer, verifiserer Earned Value (CPI, EAC/ETC), bruker hurtigtaster, godkjenner i Port 9. | Datakonsistens, revisjonsspor, FAST Excel-eksport, Stage-Gate Port 9 sign-off (APPROVED/MODIFIED/REJECTED). |
| `P4_REVISOR` | **Kommunerevisjonen / Kontrollutvalget**<br>Ekstern kontrollør, juridisk fokus (§ 14-5). | Leter etter avvik > 5 %, kontrollerer lovhenvisninger, etterspør SHA-256 forsegling. | Sporbarhet, uforanderlige revisjonslogger, juridisk siteringsnøyaktighet, kilde-ID i RAG-svar. |
| `P5_CHAOS` | **Adversarial & Stress Tester**<br>Sikkerhets- og robusthetstesting. | Injisering av ugyldige tegn, klikker 10 ganger raskt, tester feilhåndtering ved nettverksbrudd. | OWASP ASI06 (Indirect Prompt Injection), skjerming av feilmeldinger, ingen eksponering av interne stack traces. |

---

### Persona Prompt Templates

#### Template: `P1_ENHETSLEDER`
```markdown
Du simulerer en enhetsleder i Kristiansand kommune (Hjemmetjenesten Vågsbygd, Enhet 202).
- Teknisk kompetanse: Lav til middels (bruker primært Visma og Teams).
- Mål: Finne avviket for Enhet 202 i M10, forstå hvorfor vikarbudsjettet er overskredet, og bekrefte månedsrapportering.
- Atferdsregler:
  1. Gå direkte til fanen "Min Enhet & Min Måned".
  2. Hvis et tall krever mer enn to klikk for å forklares, noter dette som "FRUSTRAASJON_NAVIGASJON".
  3. Klikk "Godkjenn Månedsstatus" og bekreft at det vises en tydelig kvittering.
  4. Loggfør alle steg og uklare faguttrykk i JSON-format.
```

#### Template: `P3_CONTROLLER` (Frank Ellingsen)
```markdown
Du simulerer en senior project controller med ansvar for konsernprognoser og EVM-styring.
- Teknisk kompetanse: Svært høy (SQL, DAX, EVM, Kommuneloven § 14-5).
- Mål: Gjennomføre rullende EAC-beregning for Helse og mestring, validere CPI-terskler (< 0.95 = rød alarm), og forsegle tertialnotat.
- Atferdsregler:
  1. Åpne "Sektor & Konsernstyring", sjekk at Top 3 takometrene oppdateres når Oppvekst og Helse velges.
  2. Verifiser at bruttoprinsippet (§ 14-6) overholdes (ingen netting av refusjoner mot lønn).
  3. Utfør Stage-Gate Port 9 sign-off med kryptografisk SHA-256 hash.
  4. Verifiser at FAST Excel-modellen stemmer med tallene i konsernoversikten.
```

---

## 3. Phase 2: Unmoderated Prototype Testing & UX Metrics

Ved automatisert eller assistert testing måles kvantitative brukeropplevelses-KPI-er:

* **Task Success Rate (TSR)**: Mål $\ge 95\,\%$ for kritiske oppgaver (månedsslutt, saksfremlegg).
* **Direct Path Ratio**: Andel brukere som finner direkte vei til målet uten å gå omveier via feil faner. Mål $\ge 80\,\%$.
* **Misclick Rate**: Klikk på ikke-interaktive elementer (f.eks. statiske etiketter). Mål $< 3\,\%$.
* **System Usability Scale (SUS)**: Standardisert 10-spørsmåls benchmark tilpasset offentlig sektor. Mål $> 75$ (Klasse A / "Excellent").
* **Edward Tufte Data-Ink Score**: Null vertikale linjer i tabeller, ingen unødige 3D-elementer, og fargebruk kun ved aktive avvik.

---

## 4. Phase 3: AI-Moderert Kvalitativ Probing

Under live testøkter eller automatiserte nettleserlogger overvåker en AI-observatør interaksjonsflyten:

```
[Brukermus- og Klikkstrøm]
           │
           ▼
[Nølingsdetektor (Pause > 5s eller > 3 feilklikk i samme seksjon)]
           │
           ▼
[Kontekstuell Spørring i Chatbot]
           │
           ▼
"Jeg la merke til at du stoppet ved Takometeret for Netto Driftsresultat.
 Var det uklart om avviket gjaldt hele kommunen eller kun din sektor?"
```

---

## 5. Phase 4: Menneskelig Validering (5-Bruker Regelen)

Ifølge Nielsen Norman Group avdekker **5 representative brukere ~85 % av alle kritiske brukervennlighetsproblemer**.

### Testprotokoll for Kristiansand Kommune:
1. **Deltakere**:
   * 2 enhetsledere (1 Helse, 1 Oppvekst)
   * 1 kommunalsjef / rådgiver
   * 1 økonomikonsulent / regnskapsfører
   * 1 representant fra Kommunerevisjonen
2. **Gjennomføring**:
   * "Tenk høyt"-metodikk mens deltakeren løser 3 reelle driftsscenarier (f.eks. uventet budsjettsprekk, NAV-refusjonsgap, forberedelse til formannskapet).
3. **Kategorisering av avvik**:
   * 🔴 **Blokkere**: Brukeren klarer ikke fullføre oppgaven uten ekstern hjelp.
   * 🟡 **Betydelig friksjon**: Brukeren nøler > 30 sekunder eller velger feil fane.
   * 🟢 **Kosmetisk forbedring**: Tekstjustering, skriftstørrelse eller etikettpresisering.

---

## 6. Phase 5: CI/CD Golden Dataset & Pre-Deployment Gates

Ingen oppdatering av [index.html](file:///C:/Users/frank/Desktop/AI_KOM/index.html) eller API-serveren settes i produksjon uten at automatiserte kvalitetsporter er passert.

### 6.1 Operative Testkommandoer i Repoet

```powershell
# 1. Kjør full evaluering mot Golden Evaluation Dataset (Agent 13)
python tools/run_tool.py eval --gate

# 2. Kjør integrasjonstester for Top 3 KPIs og takometre
python -m pytest tests/test_top3_kpi.py -v

# 3. Kjør sikkerhets- og valideringssjekk
python tools/run_tool.py ai-eng --benchmark
```

### 6.2 Pre-Deployment Quality Gate Matrix

```yaml
quality_gates:
  min_task_completion_rate: 0.95
  max_allowed_error_rate: 0.01
  evaluation_metrics:
    - name: "factual_consistency"
      min_score: 0.90
      description: "Ingen hallusinerte tall eller feilaktige lovhenvisninger jf. Kommuneloven § 14-5"
    - name: "legal_citation_precision"
      min_score: 0.95
      description: "Korrekt henvisning til § og ledd med kilde-ID"
    - name: "tufte_ui_compliance"
      min_score: 1.00
      description: "Fravær av vertikale linjer og korrekt bruk av fargene #c0392b, #d35400, #27ae60"
    - name: "pii_leakage_rate"
      max_score: 0.00
      description: "Null umaskerte personopplysninger (FNR, navn) i ekstern LLM-dispatch"
  block_deployment_on_failure: true
```

---

## 7. Operativ Sjekkliste før Produksjonssetting

- [ ] **Syntetisk Persona-kjøring**: Kjørt simuleringer for `P1_ENHETSLEDER`, `P2_KOMMUNALSJEF` og `P3_CONTROLLER` via Playwright.
- [ ] **Top 3-Layout & Fanebytte**: Verifisert at `#top3-kpi-seksjon` vises øverst i fanen Sektor & Konsernstyring og oppdateres ved sektorbytte.
- [ ] **Golden Dataset Evaluering**: Verifisert at `python tools/run_tool.py eval --gate` oppnår $\ge 90\,\%$.
- [ ] **Pytest Regresjonstest**: Verifisert at alle tester i `tests/` kjører 100 % grønt.
- [ ] **PII & OWASP Sikkerhetssjekk**: Bekreftet at Stage-Gate Port 4 (sladding) og Port 9 (SHA-256 HITL) er intakte.
- [ ] **Faglig Sign-off**: Senior Controller (Frank Ellingsen) har godkjent funksjonaliteten.
