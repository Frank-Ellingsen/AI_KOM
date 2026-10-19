# Mål, Hensikt og Menneskelig Tilsyn (Human-in-the-Loop)
## AI_KOM: Control Office Hub for Kristiansand Kommune

**Dokument-ID:** `AI_KOM-GOAL-HITL-2026-V1`  
**Dato:** 19. oktober 2026  
**Prosjekt:** AI_KOM (Control Office Hub)  
**Målgruppe:** Kommunedirektøren, Formannskapet, Enhetsledere og Kommunerevisjonen  

---

## 1. Hovedmål (Primary Goal)

Hovedmålet med **`AI_KOM`** er å transformere den kommunale virksomhetsstyringen i Kristiansand kommune (som omfatter et årlig driftsbudsjett på **7,24 milliarder kroner** fordelt på **81 enheter** og **6 virksomhetsområder**) ved å erstatte tunge, manuelle rapporteringsrutiner med en **selvbetjent, AI-assistert og unntaksbasert styringsplattform**.

---

## 2. Strategisk Hensikt (Strategic Intent)

Prosjektet bygger på fem strategiske pillere som sikrer at digitaliseringen gir reell gevinstrealisering uten å gå på bekostning av rettssikkerhet eller økonomisk kontroll:

### 2.1 Makt til Enhetslederne (Self-Service Autonomy)
* **Selvbetjening**: Gi alle 81 enhetsledere verktøy til selvstendig å håndtere månedslukking, KOSTRA-kontering, vertskommuneoppgjør og selvkostberegninger.
* **Avlastning av Økonomirådgiverne**: Endre rollen til kommunens økonomirådgivere og controllere fra manuelle "tallknusere" og oppslagsverk til strategiske kvalitetssikrere.

### 2.2 Unntaksbasert Styring (Management by Exception)
* **"Silence is Consent" (🟢 Grønn sti)**: For enheter i balanse (avvik $< 2,0\,\%$) skjer datainnsamling, KOSTRA-avstemming og journalføring **100 % automatisk** uten at lederen forstyrres.
* **"One-Click Triage" (🔴 Rød sti)**: Ved budsjettavvik over terskel henter systemet data fra Visma/Framsikt, sjekker lovkrav, maskerer personopplysninger og genererer et ferdig utkast til saksfremlegg. Lederen gjennomgår og godkjenner notatet på under 30 sekunder.

### 2.3 "Null-Manual" Brukervennlighet (Zero-Guide UX)
* **SSO og Kontekst**: Automatisk gjenkjenning av lederens ansvarsnummer ved innlogging via Microsoft Entra ID.
* **Innbakte Mikro-tooltips (ℹ️)**: Forklaring av KOSTRA-regler, kalkylerekker og lovbestemmelser direkte i skjemaet idet handlingen utføres.

---

## 3. Menneskelig Tilsyn (Human-in-the-Loop / HITL)

AIL-arkitekturen i `AI_KOM` er utformet slik at **kunstig intelligens aldri fatter autonome juridiske eller økonomiske vedtak**. Menneskelig tilsyn er bygget inn som et ufrakvikelig kontrollpunkt.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. AI DATA INGESTION & VARIANCE ANALYSIS (AUTOMATISK)                  │
│ AI henter data fra Visma/Framsikt og kjører sjekk mot KOSTRA          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. EVALUATOR-OPTIMIZER LOOP (AUTOMATISK KVALITETSKONTROLL)              │
│ Sjekker Kommuneloven § 14-5/14-6, GDPR Port 4 PII og format             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. STAGE-GATE PORT 9 (MENNESKELIG SIGN-OFF / HITL)                      │
│ Enhetsleder/Controller gjennomgår, overprøver og godkjenner             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. KRYPTOGRAFISK FORSEGLET JOURNALFØRING (SHA-256)                       │
│ Genererer uforanderlig revisjonsstempel for Kommunerevisjonen           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Hvorfor 100 % Autonomi er Ulovlig
1. **EU AI Act Artikkel 14 (Menneskelig tilsyn)**: Høyrisiko AI-systemer som benyttes i offentlig forvaltning og ressurstildeling krever kontinuerlig menneskelig overvåking (*Human-in-the-Loop*).
2. **Kommuneloven § 14-5 (Handlingsplikt)**: Den rettslige plikten til å iverksette tiltak og legge frem sak om inndekning ved merforbruk ligger personlig hos Kommunedirektøren og delegertes enhetsledere, ikke hos en algoritme.
3. **Kommuneloven § 14-6 (Bruttoprinsippet)**: Forbudet mot nettobudsjettering krever at menneskelige beslutningstakere har full visibilitet over alle brutto inntekter og utgifter.
4. **Kommuneloven § 13-1 & Forvaltningsloven § 17 (Utredningsplikt)**: Kommunedirektøren har et personlig, lovpålagt ansvar for at saker som fremmes for folkevalgte organer er saklig, fullstendig og objektivt utredet. AI fungerer utelukkende som saksforberedende assistent; det endelige politiske saksfremlegget må alltid forankres under en navngitt leders godkjenning.
5. **Hovedtariffavtalen (HTA) § 4 & Arbeidsmiljøloven § 10-12 (Drøftingsplikt)**: Dersom et avviks- eller innsparingstiltak berører bemanning, overtid eller vaktturnus (f.eks. ved innleiestopp for vikarer), kreves obligatorisk drøfting med tillitsvalgte før iverksettelse (jf. `MAL_HTA_PARAGRAF_4_DROFTINGSPROTOKOLL`).

### 3.2 Implementasjon i Stage-Gate Port 9
* **Menneskelig Godkjenningsknapp**: Ingen AI-genererte saksfremlegg, omdisponeringer eller utgående fakturaer publiseres eller sendes til politisk behandling før ansvarlig leder har trykket "Godkjenn" i Stage-Gate Port 9.
* **Evaluator-Optimizer Løkke ([tools/loop_engine.py](file:///C:/Users/frank/Desktop/AI_KOM/tools/loop_engine.py))**: Før et utkast når lederens bord, kjøres den automatiserte kvalitetskontrollen (`python tools/run_tool.py loop`) som garanterer at §§ 14-5, 14-6, GDPR og vedtaksstruktur er 100 % oppfylt.
* **Kryptografisk SHA-256 Revisjonsstempel & Arkivloven § 6**: Ved godkjenning slås lederens identitet, tidsstempel, sektor og dokumentets innhold sammen til et unikt SHA-256 stempel. Loggen lagres som et uforanderlig revisjonsregister (WORM / Write Once Read Many) i tråd med arkivlovens krav for *Kommunerevisjonen*.
* **Lokal PII-skjerming (Port 4)**: Fødselsnumre (11 siffer) og kontonumre sladdes automatisk før AI-behandling, slik at lederen kun forholder seg til kvalitetssikrede, skjermede data.

---

## 4. Tids- og Innsatsmatrise for Enhetsledere

| Operasjonstype | Tradisjonell Manuell Prosess | AI_KOM med HITL (Self-Automator) | Menneskelig Innsats |
| :--- | :--- | :--- | :--- |
| **Månedsoppgjør i balanse (🟢)** | 1–2 timer rapportskriving | Automatisk generering og arkivering | **0 minutter** (Silence is Consent) |
| **Budsjettavvik / Saksfremlegg (🔴)** | 3–5 timer datainnsamling og notat | AI lager utkast via Evaluator-loop | **30 sekunder** (Review & Approval) |
| **Selvkost & Vertskommunekalkyle** | Excel-ark med fare for formelfeil | Ferdig utfylt modell med sjekk | **2 minutter** (Verifisering) |

---

## 5. Oppsummering

**Målet** er 100 % selvbetjening og dramatisk tidsinnsparing.  
**Hensikten** er unntaksbasert styring og sømløs saksbehandling.  
**Menneskelig tilsyn (HITL)** sikrer at kommunen etterlever EU AI Act, Kommuneloven og god forvaltningsskikk med full revisjonssporbarhet.
