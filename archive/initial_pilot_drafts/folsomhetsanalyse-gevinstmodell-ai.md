# Følsomhetsanalyse for Gevinstmodell: AI i Økonomistyring

**Virksomhet:** Kristiansand kommune — Økonomi og virksomhetsstyring  
**Formål:** Vurdere lønnsomhet, risiko, break-even og nedbetalingstid (*Payback*) under ulike forutsetninger om antall brukere, tidsinnsparing, utaksgrad og timekostnad.

---

## 1. Hovedkonklusjon og Risiko-oppsummering

Følsomhetsanalysen viser at investeringen i en **Bølge 1 AI-pilot og utrulling** har en **svært lav finansiell risikoprofil**:

1. **Rask tilbakebetaling (*Base Case*):** Med 30 økonomirådgivere, 2,0 timer spart per uke og en utaksgrad på 70 %, oppnås en **netto årlig gevinst på ca. 1,06 mill. kr** og en nedbetalingstid (*Payback*) på **4,9 måneder**.
2. **Lav kritisk utaksgrad (Break-even på drift):** Det kreves at avdelingen klarer å hente ut kun **12,9 %** av den teoretisk innsparte tiden for at AI-satsingen skal dekke sine egne årlige drifts- og lisenskostnader (240 000 kr/år).
3. **Break-even på alt (Investering + 3 års drift):** Det kreves en utaksgrad på kun **20,7 %** for å nedbetale både engangsinvesteringen (435 000 kr) og alle årlige driftskostnader over en 3-årsperiode.
4. **Skaleringseffekt:** Ved utrulling til 50 rådgivere synker nedbetalingstiden til **under 3 måneder**, selv om utaksgraden skulle være så lav som 50 %.

---

## 2. Scenariomatrise: Konservativt vs. Base Case vs. Optimistisk

| Parameter / Resultat | Konservativt scenario | Base Case (Forventet) | Optimistisk scenario |
| :--- | :--- | :--- | :--- |
| **Antall aktive rådgivere** | 15 rådgivere | **30 rådgivere** | 30 rådgivere |
| **Innspart tid per rådgiver** | 1,0 time/uke | **2,0 timer/uke** | 3,5 timer/uke |
| **Utaksgrad / Realiseringsgrad (%)** | 40 % | **70 %** | 85 % |
| **Timekostnad inkl. AGA & pensjon** | 600 kr/t | **650 kr/t** | 700 kr/t |
| **Totalt frigjort tid (timer/år)** | 675 timer/år | **2 861 timer/år** | 4 725 timer/år |
| **Frigjorte årsverk** | 0,41 årsverk | **1,73 årsverk** | 2,86 årsverk |
| **Realisert kronegevinst (brutto)** | 162 000 kr/år | **1 301 664 kr/år** | 2 811 375 kr/år |
| **Årlige driftskostnader (FinOps)** | 240 000 kr/år | **240 000 kr/år** | 240 000 kr/år |
| **NETTO ÅRLIG GEVINST (kr/år)** | **-78 000 kr/år** | **+1 061 664 kr/år** | **+2 571 375 kr/år** |
| **3-ÅRS ROI (%)** | -153,8 % | **+632,2 %** | +1 673,4 % |
| **PAYBACK-PERIODE (måneder)** | Ikke inntjent | **4,9 måneder** | **2,0 måneder** |

---

## 3. Følsomhetstabell 1: Payback-periode (måneder) basert på Utaksgrad og Teamstørrelse

*(Forutsetninger: 2,0 timer spart per rådgiver/uke, 650 kr/t timekostnad, 435 000 kr etablering, 240 000 kr/år drift)*

| Realiseringsgrad / Utaksgrad (%) | 10 rådgivere | 15 rådgivere | 20 rådgivere | 30 rådgivere (Base) | 50 rådgivere |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **20 %** | Negativ | Negativ | 261,0 mnd | **34,8 mnd** | 10,9 mnd |
| **30 %** | Negativ | Negativ | 29,0 mnd | **13,1 mnd** | 6,3 mnd |
| **40 %** | Negativ | 58,0 mnd | 15,3 mnd | **8,3 mnd** | 4,4 mnd |
| **50 %** | Negativ | 29,0 mnd | 10,4 mnd | **6,1 mnd** | 3,4 mnd |
| **60 %** | 72,5 mnd | 18,3 mnd | 7,8 mnd | **4,8 mnd** | 2,7 mnd |
| **70 % (Forventet)** | 30,8 mnd | 13,1 mnd | 6,3 mnd | **4,0 mnd** | 2,3 mnd |
| **80 %** | 19,3 mnd | 10,1 mnd | 5,2 mnd | **3,4 mnd** | 2,0 mnd |
| **90 %** | 14,0 mnd | 8,2 mnd | 4,4 mnd | **2,9 mnd** | 1,7 mnd |

*Merk: Ved Base Case (30 rådgivere og 70 % utaksgrad) oppnås full nedbetaling etter ca. 4–5 måneder.*

---

## 4. Følsomhetstabell 2: Netto årlig gevinst (kr/år) basert på Innspart tid og Utaksgrad

*(Forutsetninger: Base Case med 30 rådgivere, 650 kr/t timekostnad, 240 000 kr/år drift)*

| Innspart tid per uke | Utaksgrad 40 % | Utaksgrad 50 % | Utaksgrad 70 % (Base) | Utaksgrad 85 % | Utaksgrad 100 % |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1,0 time/uke** | -32 320 kr | +19 600 kr | **+123 440 kr** | +201 320 kr | +279 200 kr |
| **1,5 timer/uke** | +71 520 kr | +149 400 kr | **+305 160 kr** | +422 000 kr | +538 800 kr |
| **2,0 timer/uke (Base)**| +175 360 kr | +279 200 kr | **+1 061 664 kr** | +1 228 120 kr | +1 443 200 kr |
| **2,5 timer/uke** | +279 200 kr | +409 000 kr | **+668 600 kr** | +863 350 kr | +1 058 100 kr |
| **3,0 timer/uke** | +383 040 kr | +538 800 kr | **+850 320 kr** | +1 084 000 kr | +1 317 700 kr |

---

## 5. De Tre Utaksmekanismene for Å Hente Ut Kronene

En innspart time er kun en teoretisk kapasitetsgevinst inntil ledelsen fatter et aktivt valg om hvordan den skal tas ut i kommuneregnskapet:

1. **Re-allokering til analysestøtte (Kapasitetsgevinst):** Tiden frigjøres fra manuelle reglementsoppslag og råutkast til rapporter, og flyttes over til dypere virksomhetsanalyser og direkte beslutningsstøtte for enhetslederne. Kommunen håndterer økt saksmengde uten å ansette flere rådgivere.
2. **Direkte kostnadsreduksjon (Unngåtte utgifter):** Redusert overtid ved rapporteringstopper (T1, T2, Årsregnskap) og unngått innleie av eksterne konsulenter til utrednings- og analysenarbeid.
3. **Strukturelt rammekutt (Bemanningstilpasning):** Inndragning av årsverk eller reduksjon i erstatningsrekruttering ved naturlig avgang (pensjon/oppsigelser), i tråd med kommunens langsiktige innsparingskrav (slik Kristiansand kommune har lagt inn et innsparingskrav på 2 mill. kr fra 2029 under *Teknologiløftet*).
