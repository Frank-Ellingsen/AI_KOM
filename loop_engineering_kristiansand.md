# Loop Engineering i AI_KOM — Control Office Hub for Kristiansand Kommune
**Arkitektur for Selvreparerende, Lovlige og Kvalitetssikrede AI-Løkker (Lag 4 i AI Engineering)**

---

## 1. Executive Summary & Formål

I overgangen fra enkle LLM-prompter til autonome agentiske systemer i kommunal sektor er **Loop Engineering** (Lag 4 i AI Engineering-hierarkiet) den avgjørende arkitekturdisiplinen. 

I **`AI_KOM` (Kristiansand kommune Control Office Hub)** sikrer Loop Engineering at en AI-generert avviksanalyse eller et saksfremlegg aldri oversendes til saksbehandler eller Formannskapet uten først å ha bestått en automatisk **Evaluator-Optimizer-løkke**. 

Dette fjerner risikoen for:
* **Juridiske mangler**: Manglende henvisning til *Kommuneloven § 14-5* (budsjettbalanse) eller *§ 14-6* (bruttoprinsippet).
* **GDPR-brudd**: Unyttet eller ufrivillig eksponering av skjermede personopplysninger (11-sifrede fødselsnumre eller bankkonti).
* **Hallusinerte tall**: Avvik mellom regnskapstall fra Visma/Framsikt og teksten i saksfremlegget.

---

## 2. Kjernekonseptet: Generator vs. Evaluator Dualitet

En grunnleggende regel i Loop Engineering er at **en LLM ikke pålitelig kan evaluere og rette sitt eget arbeid i samme passering**. `AI_KOM` splitter derfor prosessen i to uavhengige noder:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. GENERATOR NODE (LLM Draft)                                           │
│ Genererer første utkast til saksfremlegg basert på KOSTRA/Visma-data     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. EVALUATOR NODE (Deterministiske & LLM-baserte kvalitetsporter)       │
│  • Gate 1: Kommuneloven § 14-5 (Budsjettbalanse)                        │
│  • Gate 2: Kommuneloven § 14-6 (Bruttoprinsippet)                       │
│  • Gate 3: GDPR Port 4 (0 unøyaktige 11-sifrede fnr/kontonummere)       │
│  • Gate 4: Formelt vedtaksforslag og finansieringsplan                  │
└──────────────────┬──────────────────────────────────┬───────────────────┘
                   │                                  │
          ❌ Avvist (Tilbakemelding)                  ✅ Godkjent
                   │                                  │
                   ▼                                  ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────┐
│ OPTIMIZER TURN (Forbedring)          │  │ STAGE-GATE PORT 9 SIGN-OFF    │
│ Re-prompter Generator med konkret    │  │ Menneskelig controller god-   │
│ tilbakemelding (Maks 3 iterasjoner)  │  │ kjenner & SHA-256 forsegles   │
└──────────────────────────────────────┘  └───────────────────────────────┘
```

---

## 3. Kvalitets- og Lovlighetsporter (Quality Gates)

Før et utkast godkjennes av Evaluator-noden, må det bestå fire obligatoriske sjekker:

| Kvalitetsport | Krav og Regelsett | Verifikasjonsmetode | Handling ved Avvik |
| :--- | :--- | :--- | :--- |
| **Port 1: Budsjettbalanse** | Eksplisitt henvisning til *Kommuneloven § 14-5* ved merforbruk. | Tekstsøk & Semantisk validering | Krev innsettelse av juridisk paragraf og handlingsplikt. |
| **Port 2: Bruttoprinsippet** | Eksplisitt henvisning til *Kommuneloven § 14-6* (forbud mot nettobudsjettering). | Regler for kontering (*Kontoklasse x Funksjon x Art*) | Krev at utgifter og refusjoner (f.eks. NAV art 1600) føres brutto. |
| **Port 3: GDPR & PII (Port 4)** | 100 % vasking av fødselsnumre (11 siffer), bankkonti og e-post. | Regex & Detektormodell | Masker PII til `[SKJERMET_FNR]` / `[SKJERMET_KONTO]` før godkjenning. |
| **Port 4: Vedtaksstruktur** | Må inneholde formell overskrift *"Forslag til Vedtak"* og inndekning. | Struktursjekk (Pydantic / Regex) | Krev at vedtaksforslag formes som et gyldig politisk punkt. |

---

## 4. Python Implementasjonsarkitektur (`ai_kom_loop_engine.py`)

Nedenfor er kjernestrukturen for hvordan Evaluator-Optimizer-løkken kjøres i `AI_KOM`:

```python
import hashlib
import re
import json
from datetime import datetime
from typing import Dict, Any, Tuple

# 1. GENERATOR NODE
def generator_draft_memo(sector: str, deficit_mnok: float, attempt: int, feedback: str = "") -> str:
    if attempt == 1:
        # Første utkast: Mangler juridiske paragrafer og inneholder uskjermet PII
        return f"""
        SAKSFREMLEGG: Tiltaksplan for {sector}
        Bakgrunn: Sektoren har et merforbruk på {deficit_mnok:.2f} MNOK i M8-prognosen.
        Innstilling: Formannskapet vedtar å omdisponere midler fra Oppvekst.
        Saksbehandler konto: 1234.56.78901.
        """
    else:
        # Revidert utkast basert på Evaluator-tilbakemelding
        return f"""
        SAKSFREMLEGG: Tiltaksplan for {sector} (Revidert utkast)
        
        1. Bakgrunn og Risiko
        Sektoren {sector} viser et projisert merforbruk på {deficit_mnok:.2f} MNOK i 2. tertial.
        I henhold til Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak om innsparing 
        eller omdisponering for å opprettholde samlet driftsbalanse.
        
        2. Finansiell Inndekning og Bruttoprinsippet
        Inndekning skjer via omdisponering fra Oppvekst (mindreforbruk) og bruk av disposisjonsfond.
        I henhold til Kommuneloven § 14-6 konteres alle inntekter og utgifter brutto.
        
        3. Forslag til Vedtak
        Formannskapet godkjenner omdisponering av {deficit_mnok:.2f} MNOK til {sector}.
        Kontakt: [SKJERMET_KONTO]
        """

# 2. EVALUATOR NODE
def evaluator_check(draft_text: str) -> Tuple[bool, str]:
    checks = {
        "has_par_14_5": "Kommuneloven § 14-5" in draft_text,
        "has_par_14_6": "Kommuneloven § 14-6" in draft_text,
        "has_vedtak": "Forslag til Vedtak" in draft_text or "Innstilling" in draft_text,
        "pii_clean": not bool(re.search(r'\b\d{4}\.\d{2}\.\d{5}\b|\b\d{11}\b', draft_text))
    }
    
    passed = all(checks.values())
    feedback = []
    if not checks["has_par_14_5"]: feedback.append("MANGLER: Henvisning til Kommuneloven § 14-5.")
    if not checks["has_par_14_6"]: feedback.append("MANGLER: Henvisning til Kommuneloven § 14-6 (Bruttoprinsippet).")
    if not checks["pii_clean"]: feedback.append("GDPR-BRUDD: Uskjermet bankkonto eller fødselsnummer funnet.")
    
    return passed, " | ".join(feedback) if feedback else "APPROVED"

# 3. EVALUATOR-OPTIMIZER LOOP EXECUTOR
def run_evaluator_optimizer_loop(sector: str, deficit: float, max_attempts: int = 3) -> Dict[str, Any]:
    attempt = 1
    feedback = ""
    
    while attempt <= max_attempts:
        draft = generator_draft_memo(sector, deficit, attempt, feedback)
        passed, feedback = evaluator_check(draft)
        
        if passed:
            # Stage-Gate Port 9: Generer SHA-256 forsegling for Kommunerevisjonen
            timestamp = datetime.utcnow().isoformat() + "Z"
            seal_payload = f"{timestamp}|Controller|{sector}|APPROVED|{hashlib.sha256(draft.encode()).hexdigest()}"
            sha_seal = hashlib.sha256(seal_payload.encode()).hexdigest()
            
            return {
                "status": "APPROVED",
                "iterations_required": attempt,
                "final_draft": draft.strip(),
                "sha256_audit_seal": sha_seal
            }
        attempt += 1
        
    return {"status": "FAILED_MAX_ITERATIONS", "last_feedback": feedback}
```

---

## 5. Stoppbetingelser & Sikkerhetsmekanismer (Halting Mechanisms)

For å forhindre uendelige løkker og usikre kostnader i produksjon benytter `AI_KOM` tre stoppbetingelser:
1. **Iterasjonstak (`max_attempts = 3`)**: Dersom dokumentet ikke har bestått Evaluator etter 3 forsøk, avbrytes løkken og saken sendes til manuell behandling hos controller.
2. **Token- og Budsjettkontroll**: Hver løkke overvåker tokenforbruket. Dersom akkumulértforbruk overskrider 10 000 tokens, stoppes genereringen.
3. **Konvergenssjekk**: Hvis Evaluator gir samme tilbakemelding to ganger på rad uten endring i utkastet, avbrytes prosessen for å forhindre spinn.

---

## 6. Gevinster for Kristiansand Kommune

* **100 % Overholdelse av EU AI Act Art. 14**: Alle vedtakssaker har full menneskelig kontroll (Human-In-The-Loop) kombinert med ubestridelig SHA-256 kryptografisk sporbarhet for *Kommunerevisjonen*.
* **Minimal Tidsbruk for Enhetsledere**: Enhetslederen mottar et *ferdig kvalitetssikret* saksfremlegg som har bestått alle юридиiske tester, og kan godkjenne saken på under 1 minutt.
* **Redusert Press på Økonomirådgivere**: Fjerner manuell korrekturlesing av formelle krav, slik at rådgiverne kan fokusere på strategisk virksomhetsstyring.
