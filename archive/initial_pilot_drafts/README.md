# 🏛️ Arkiverte Innledende Utkast (Initial Pilot Drafts)

Dette arkivområdet inneholder de opprinnelige råutkastene til AI-pilotdokumentasjonen for Kristiansand kommune.

## Bakgrunn og Reorganisering

For å opprettholde Edward Tufte Data-Ink prinsipper, unngå filrot i rotkatalogen, og etablere en ren Single Source of Truth (SSOT), er disse filene strukturert og overført til to formelle prosjektmoduler:

1. **`generic-ai-pilot-pakke/enterprise-ai-pilot/`**:
   - Generisk malverk tilpasset fri gjenbruk i andre norske kommuner og virksomheter.
   - Inkluderer arkitektur, saksframlegg, gevinstmodell, risikoanalyse, prompts og DAX.

2. **`antigravity-ms-pilot/`**:
   - Dedikert operativt subprosjekt for Kristiansand kommune med M365 Copilot & Antigravity hybridmotor.
   - Inkluderer kildekode (`src/`), PII-vask, evaluatorer, tester og revisjonslogging.

## Innhold i dette arkivet

| Filnavn | Opprinnelig Formål | Nåværende SSOT-plassering |
| :--- | :--- | :--- |
| `cheat-sheet-sponsormote-ai.md` | Spørsmål & svar for toppledermøte | `generic-ai-pilot-pakke/enterprise-ai-pilot/docs/governance/02_cheat-sheet-sponsormote-ai.md` |
| `folsomhetsanalyse-gevinstmodell-ai.md` | Finansielle beregninger og NPV/ROI | `generic-ai-pilot-pakke/enterprise-ai-pilot/docs/financials/01_folsomhetsanalyse-gevinstmodell-ai.md` |
| `folsomhetsanalyse-gevinstmodell-ai.png` | Følsomhetsdiagram | `generic-ai-pilot-pakke/enterprise-ai-pilot/docs/financials/02_folsomhetsanalyse-diagram.png` |
| `maalarkitektur-okonomi-ai-kristiansand.md` | Målarkitektur | `generic-ai-pilot-pakke/enterprise-ai-pilot/docs/architecture/01_maalarkitektur-okonomi-ai-kristiansand.md` |
| `oppstartsnotat-pilotgruppe-ai.md` | Oppstart og pilotdeltakere | `generic-ai-pilot-pakke/enterprise-ai-pilot/docs/pilot_and_ops/01_oppstartsnotat-pilotgruppe-ai.md` |
| `risikovurdering-og-evalueringsskjema-ai-pilot.md` | FRIA/DPIA og evalueringskriterier | `generic-ai-pilot-pakke/enterprise-ai-pilot/docs/security_and_legal/01_risikovurdering-og-evalueringsskjema-ai-pilot.md` |
| `Municipal_Financial_AI_Pilot.pdf` | Publikasjons-PDF | `docs/pdf/Municipal_Financial_AI_Pilot.pdf` |
| `Virksomhetsstyrt_KI_i_Økonomi.pdf` | Veileder-PDF | `docs/pdf/Virksomhetsstyrt_KI_i_Økonomi.pdf` |

*Merk: Ingen filer eller historikk slettes; filene i denne mappen bevares som opprinnelige revisjonskopier.*
