# GitHub Actions CI/CD Pipeline for MVA & M10 Omposteringsvalidering
**Antigravity Backend Engine — Kristiansand kommune (AI_KOM)**

---

## 1. Oversikt over CI/CD-arbeidsflyten

Denne GitHub Actions-arbeidsflyten (`mva_validering_ci.yml`) automatisere kvalitetssikringen av MVA-kompensasjon og avstemming mot **Balansekonto 2130 (Momsrefusjon)** hver gang nye korreksjonsfiler eller omposteringer skyves til repositoriet, eller når en controller trykker på "Push Button Ingestion" i portalen.

```
[ Git Push / Push Button Trigger ]
             │
             ▼
[ GitHub Actions Runner (Ubuntu-latest) ]
             │
             ├─► 1. Sjekk ut kildekode & sett opp Python 3.12
             ├─► 2. Installer pandas, openpyxl & pydantic
             ├─► 3. Kjør `test_mva_balanse_2130.py`
             │      └─► Sjekk at Differanse(MVA_Komp - Konto_2130) == 0.00 NOK
             ├─► 4. Generer SHA-256 kryptografisk revisjonsstempel
             └─► 5. Last opp Audit Trail Artifact (retensjon 90 dager)
```

---

## 2. Trigger-betingelser

1. **Automatisk ved endringer:** Kjøres automatisk dersom nye `.xlsx`-korreksjonsfiler legges til under `data/repostings/` eller dersom backend-tjenesten for ompostering endres.
2. **Manuell kjøring (workflow_dispatch):** Controllers kan utløse testen direkte fra GitHub UI eller via Antigravity API-et ved M10-månedsslutt.

---

## 3. Integrasjon med Antigravity Stage-Gate Port 9

Ved vellykket kjøring (`PASSED`):
* MVA-kompensasjonsbeløpet er verifisert i henhold til *Momskompensasjonsloven*.
* Filen stemples med en unikk **SHA-256 checksum**.
* Godkjenningsstatus blir tilgjengelig for **Stage-Gate Port 9 Audit Trail** og Kommunerevisjonen.
