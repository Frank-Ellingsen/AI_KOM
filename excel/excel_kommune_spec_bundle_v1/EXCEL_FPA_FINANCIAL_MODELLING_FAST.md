# 📊 Excel FP&A Finansiell Modellering & FAST-Standard

**Virksomhetsområde:** Økonomi og Virksomhetsstyring, Kristiansand kommune  
**Standard:** FAST Standard (Flexibility, Appropriateness, Structured, Transparent) & ICAEW Principles  
**Målgruppe:** Økonomirådgivere, Controllere, Finansanalytikere  

---

## 1. Hovedprinsipper for Kommunal Finansiell Modellering i Excel

1. **Fleksibilitet (Flexibility):** Modeller må tåle strukturelle endringer i KOSTRA-kontoplanen, organisasjonsendringer (ansvar/tjeneste) og endrede rammebetingelser fra Statsbudsjettet.
2. **Hensiktsmessighet (Appropriateness):** Unngå overkompliserte matriseformler der enkle, dynamiske matrisefunksjoner (`XLOOKUP`, `FILTER`, `UNIQUE`, `LET`, `LAMBDA`) løser oppgaven mer robust.
3. **Struktur (Structured):**
   * **Strenge fargekoder:**
     * **Mørkeblå tekst (`#000080` / RGB 0,0,128):** Hardkodede inndata/forutsetninger.
     * **Svart tekst (`#000000` / RGB 0,0,0):** Beregnede formler og summer.
     * **Mørkegrønn tekst (`#006100` / RGB 0,97,0):** Interne lenker/referanser innen samme ark.
     * **Mørkerød tekst (`#800000` / RGB 128,0,0):** Eksterne lenker/referanser til andre arbeidsbøker.
     * **Lys grå bakgrunn (`#F2F2F2`):** Inndataceller som krever saksbehandlers overprøving.
4. **Transparens (Transparent):** Én formelrekke per linje. Ingen skjulte rader/kolonner uten tydelig merking. Ingenting "hardkodes" inne i formler (f.eks. aldri `=A1*1.025`, men `=A1*(1 + Index_Prisstigning)`).

---

## 2. Kommunal Custom Number Formatting

For å sikre at negative avvik framstår umiddelbart tydelige for økonomiledelsen:

```text
Formatkode for regnskapsavvik:
_(* #,##0_);[Red]_(* (#,##0);_(* "-"_);_(@_)
```

* **Positive tall:** Svarte, høyrejustert med tusenskille.
* **Negative tall:** Røde med parentes `(1 234 500)`.
* **Nullverdier:** Vises som en ren bindestrek `-`.
* **Tekst:** Venstrejustert standard.

---

## 3. Standardisert Modellarkitektur (Tab-struktur)

```text
[ 00_Forside_og_Logg ] ==> [ 01_Forutsetninger_Rammer ] ==> [ 02_Data_Visma_Import ] 
                         ==> [ 03_Beregninger_Prognose ] ==> [ 04_Rapport_Bystyret ]
```

1. **`00_Forside_og_Logg`:** Prosjekttittel, versjonskontroll, saksbehandler, SHA-256 kontrollstempel og endringslogg.
2. **`01_Forutsetninger_Rammer`:** Definisjon av lønnsvekst (KS-oppgjør), deflatorer, deflasjonsrater og demografiparametere.
3. **`02_Data_Visma_Import`:** Rådata fra Visma ERP hentet via Power Query (Read-only).
4. **`03_Beregninger_Prognose`:** Fremskrivingslogikk (EOY-prognoser, vikarfremskriving, NAV-etterslep).
5. **`04_Rapport_Bystyret`:** Utskriftsklar rapport tilpasset A4/Liggende med saksbehandlers sammendrag og aksjonspunkter.
