# AI_KOM Portallayout og Navigasjonsstruktur
**Kristiansand kommune — Control Office Hub (AI_KOM)**

---

## 1. Målsetting og Designprinsipper

AI_KOM-portalen inneholder omfattende funksjonalitet innen EVM-nøkkeltall, KOSTRA-avvik, Framsikt/Visma-integrasjon, Power BI, saksgenerator og AI-assistanse. For å forhindre **kognitiv overbelastning (cognitive overload)** og gjøre portalen intuitiv for alle brukergrupper, bygger layouten på tre hovedprinsipper:

1. **Rollebasert inngang (Personas):** Brukeren ser kun det som er relevant for sin rolle ved første øyekast.
2. **Progressiv avsløring (Progressive Disclosure):** Avansert statistikk, DAX-koder, MLOps og kryptografiske Hasher skjules i nedtrekkselementer (accordions) eller dedikerte controllermoduler.
3. **Universell utforming & Tydelig visuell kontekst:** Trafikklys (Rød/Gul/Grønn), standardiserte statusbjelker og ryddig typografi.

---

## 2. Global Navigasjonsstruktur

```
+---------------------------------------------------------------------------------------------------+
| AI_KOM | Kristiansand kommune — Control Office Hub      [Søk...]  [M9 September: Dag 6-10] [Profil] |
+---------------------------------------------------------------------------------------------------+
| 🏫 Min Enhet & Min Måned  |  🏛️ Sektor & Konsern  |  📊 Controller Hub  |  📚 Veiledere & Maler   |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Detaljert Inndeling per Fane

### 🏫 Fane 1: Min Enhet & Min Måned
**Målgruppe:** Enhetsledere, rektorer, styrere, avdelingsledere og seksjonsledere.  
**Fokus:** Enkel, "nettbank-aktig" oversikt over egen enhet uten teknisk sjargong.

* **1.1 Hovedkort (Nettbankvisning):**
  * Tildelt Årsramme, Forbrakt YTD, Disponibel Saldo ut året, Forventet Årsavvik (Trafikklys).
* **1.2 Månedens status & Årshjul (M9 September):**
  * Hvor er vi i prosessen? (f.eks. *Dag 6–10: Avviksdeteksjon & Triage*).
  * Nedtellingsur til rapporteringsfrist.
* **1.3 Budsjettfordeling per kontogruppe:**
  * Fastlønn (Stillingsoversikt)
  * Variabel lønn & Overtid (Art 1020 / 1090)
  * NAV-refusjoner & Sykelønn (Art 1600 / 1690)
  * Kjøp av varer og driftstjenester
* **1.4 Interaktive Lederverktøy:**
  * **Tiltakssimulator:** Hva skjer med årsresultatet hvis jeg reduserer vikarinnleie med 15 %?
  * **1-Klikk Avviksnotat:** Automatisk generering av 4-punkts forklaringsnotat til kommunalsjef.

---

### 🏛️ Fane 2: Sektor & Konsernstyring
**Målgruppe:** Kommunalsjefer, direktører, Kommunedirektør, Formannskap og Bystyre.  
**Fokus:** Strategisk helhetsbilde, måltallsoppfølging og beslutningsklare politiske saker.

* **2.1 Konsernets Kritiske Måltall:**
  * **Korrigert Netto Driftsresultat:** Reelt anslag vs. Måltall (≥ 1,0 %).
  * **Sentralt Disposisjonsfond:** Nåværende dekning vs. Måltall (≥ 4,0 %).
  * **Netto Lånegjeld:** Gjeldende nivå vs. Lånetak (8,8 mrd. kr).
* **2.2 Konsernets Triage-matrise:**
  * Rødflagg-oversikt over kommunalområdene (Oppvekst, Helse & mestring, By- & stedsutvikling osv.).
  * Rangering av de 16 mest avviksutsatte enhetene.
* **2.3 Politisk Saksgenerator & Vedtaksmodul:**
  * Omfordelings- og budsjettendringssaker jf. Kommuneloven § 14-5.
  * Eksport av ferdig formaterte sakspakker:
    * 📄 Word-saksfremlegg (`.docx`)
    * 📊 PowerPoint til bystyret (`.pptx`)

---

### 📊 Fane 3: Controller Hub & Analyse
**Målgruppe:** Økonomirådgivere, senior controllere, IT/data-engineers og superbrukere.  
**Fokus:** Dypdykk i data, Framsikt/Visma-avstemming, DAX-koder, MLOps og RAG/AI-assistent.

* **3.1 KOSTRA & Framsikt Engine:**
  * Detaljert stillings- og lønnsberegner (bruttoføring, AGA Sone 1, SPK/KLP pensjon).
  * Selvkostmodellering for VAR og Byggesak (5-års fremføring av selvkostfond).
* **3.2 Power BI & Enterprise Data Hub:**
  * Embedded Power BI-rapporter med drill-down til transaksjonsnivå.
  * DAX-kodebibliotek og Power Query M-koder for gjenbruk.
* **3.3 Stage-Gate Port 9 & AI Governance:**
  * Controller Sign-off (APPROVED / MODIFIED / REJECTED) med SHA-256 kryptografisk stempel.
  * MLOps-dashboard, RAG-vektordatabase og AI-chatbot for dypdykk i kommunelov og forskrifter.

---

### 📚 Fane 4: Veiledere, Maler & Regelverk
**Målgruppe:** Felles for alle brukere.  
**Fokus:** Én samlet ressursportal for retningslinjer, opplæring og maler.

* **4.1 Malbank (Filnedlasting):**
  * Excel FAST-modeller (`.xlsx`)
  * Word-saksfremlegg (`.docx`)
  * PowerPoint-dekk (`.pptx`)
  * Power BI-prosjekter (`.pbip`)
* **4.2 Regelverk & Oppslagsverk:**
  * Kommuneloven (2018) Kap. 14
  * Økonomireglement for Kristiansand kommune
  * KOSTRA Kontoplan 2026/2027
  * EVM & Nøkkeltallsordbok
* **4.3 Interaktiv Styringskalender (Årshjul):**
  * Tidslinje for T1, T2, HØP, årsoppgjør og KOSTRA-rapportering.

---

## 4. Implementasjonsforslag for GitHub Pages (HTML/Markdown Layout)

```markdown
<!-- Eksempel på fanevelger i Markdown / HTML for GitHub Pages -->
<div class="nav-tabs">
  <button class="tab-button active" onclick="openTab('min-enhet')">🏫 Min Enhet & Min Måned</button>
  <button class="tab-button" onclick="openTab('sektor-konsern')">🏛️ Sektor & Konsernstyring</button>
  <button class="tab-button" onclick="openTab('controller-hub')">📊 Controller Hub & Analyse</button>
  <button class="tab-button" onclick="openTab('veiledere-maler')">📚 Veiledere & Maler</button>
</div>
```

---

## 5. Oppsummering og Anbefalte Neste Steg
1. **Bruk rollebaserte visninger** som standard for å forenkle hverdagen til enhetslederne.
2. **Plasser avanserte AI- og MLOps-verktøy** i *Controller Hub*-fanen.
3. **Hold malbanken oppdatert** med direkte nedlastingslenker til `.xlsx`, `.docx` og `.zip`-pakker.
