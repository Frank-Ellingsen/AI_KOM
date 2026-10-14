# Finansiell Håndbok og Brukermanual for AI Gevinstmodell

Dette dokumentet beskriver oppbyggingen av regnearkmodellen `gevinstmodell-ai-okonomi.xlsx` og gir veiledning i hvordan økonomirådgivere kan beregne ROI og gevinster for kommunale AI-piloter.

---

### 1. Structure i Regnearkmodellen (`gevinstmodell-ai-okonomi.xlsx`)

Regnearket er bygget med fire sammenlinked faneblader:

1. **`ROI & Sammendrag`:** Hoveddashbord som oppsummerer brutto og netto gevinster, 3-års ROI (%) og tilbakebetalingstid (*Payback-periode* i måneder).
2. **`Use-Case Kalkulator`:** Tidsbrukskalkulator for fem spesifikke prosessområder (RAG-oppslag, tertialrapportering, bilagskontroll, budsjettstøtte og innkjøpsanalyse).
3. **`Kostnader & FinOps`:** Komplett oversikt over engangsinvesteringer (etablering, AI Gateway, DPIA) og løpende drift (SaaS-lisenser, token-forbruk, support).
4. **`Gevinstutaksplan`:** Organisatorisk plan for omsetting av frigjort tid til re-allokering, konsulentreduksjon eller rammekutt.

---

### 2. Standard Parametere og Antakelser (Baseline)

* **Timekostnad rådgiver:** 650 kr/t (ca. 1,07 mill. kr per årsverk inkl. sosiale kostnader og overhead).
* **Standard årsverk:** 1 650 arbeidstimer per år.
* **Realiseringsgrad (Utaksgrad):** Sett til **70 %** i standardmodellen (tar hensyn til at ikke all frigjort tid umiddelbart kan tas ut i kronesparing).
* **Analyseperiode:** 3 år.

---

### 3. Beregningsformler i Modellen

$$\text{Brutto produktivitetsgevinst} = \text{Innsparte timer} \times \text{Timekostnad}$$

$$\text{Realisert gevinst} = \text{Brutto gevinst} \times \text{Realiseringsgrad (70\%)}$$

$$\text{Netto årlig gevinst} = \text{Realisert gevinst} - \text{Årlige driftskostnader}$$

$$\text{3-Års ROI (\%)} = \frac{(\text{Netto årlig gevinst} \times 3) - \text{Engangsinvestering}}{\text{Engangsinvestering}} \times 100$$

$$\text{Payback-periode (måneder)} = \frac{\text{Engangsinvestering}}{\text{Netto årlig gevinst}} \times 12$$

---

### 4. Fargekoder for Redigering i Excel

* **Blå celler (`#DCE6F1`):** Redigerbare inndata. Endre disse for å tilpasse modellen til din kommune.
* **Grønne celler (`#E2EFDA`):** Formler og beregnede resultater. Skal ikke overskrives.
* **Grå celler (`#D6DCE4`):** Delsummer og totalsummer.
