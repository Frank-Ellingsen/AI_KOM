# De 5 Nivåene i AI Engineering for Kristiansand Kommune (`AI_KOM`)

Dette dokumentet definerer den komplette 5-lags arkitekturstakken for **`AI_KOM` (Kristiansand Kommune Control Office Hub)**. Modellen beskriver evolusjonen fra enkle systemprompter til autonome, fleragentiske og lovmessig forankrede styringssystemer for kommunesektoren.

---

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 5: GRAPH ENGINEERING                                                   │
│ Fleragent-topologier, DAG-arbeidsflyter, tilstandsmaskiner & HITL-avbrudd  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 4: LOOP ENGINEERING                                                    │
│ Generator-Evaluator sykluser, selvrettende kvalitets- og lovlighetsporter   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 3: HARNESS ENGINEERING                                                 │
│ Sandkasse-kjøring, MCP-integrasjon, OS-sikkerhetsgrenser & OWASP-vern       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 2: CONTEXT ENGINEERING                                                 │
│ Hybrid RAG, progressiv avdekking, PII-skjerming & Context Paging            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ NIVÅ 1: PROMPT ENGINEERING                                                  │
│ Systemprompter, Rolledefinisjoner, Few-Shot eksempler & Pydantic Schemas     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Nivå 1: Prompt Engineering (Fundamentet)

Prompt Engineering handler om å instruere grunnmodellen (LLM) presist til å utføre isolerte oppgaver med lavest mulig usikkerhet.

### Kjernemekanismer i `AI_KOM`:
* **Rolledefinisjon**: Instruerer modellen til å opptre som en **Seniorkommunecontroller** med dyp kunnskap om statlig og kommunalt økonomiregelverk.
* **Strukturert Utdata (JSON Schema / Pydantic)**: Sikrer at alle svar følger faste datamodeller i stedet for fritekst, slik at tall kan leses direkte av ERP-systemer (Visma / Unit4 / Framsikt).
* **Chain-of-Thought (CoT)**: Tvinger modellen til å vise trinnvise beregninger av avvik og prosentvis rammeavvik før den konkluderer med RAG-status (Rød/Rav/Grønn).

---

## 2. Nivå 2: Context Engineering (Minne & Datatilgang)

Context Engineering omtales som *"Feature Engineering for LLM-er"*. Det handler om å kuratere, komprimere og strukturere data slik at modellen til enhver tid har akkurat riktig kontekst i sitt aktive kontekstvindu.

### Kjernemekanismer i `AI_KOM`:
* **Progressiv Avdekking (Progressive Disclosure)**:
  * **L1 (Metadata)**: Kun enhetsnavn og ansvarssammendrag er synlig ved oppstart (~100 tokens per enhet).
  * **L2 (Instruksjoner)**: Faste konteringsregler og KOSTRA-retningslinjer lastes inn ved aktivering.
  * **L3 (Data/Skript)**: Detaljerte regnskapsdata og Python-analyseskript kjøres direkte via terminal uten å fylle kontekstvinduet med råkode.
* **Hybrid-RAG (BM25 + Vektorsøk)**: Nøyaktig oppslag på ansvarsnumre (*f.eks. Ansvar 5200 - Sykehjem*) kombinert med semantisk søk i *Kommuneloven* og *Økonomiplan 2026–2029*.
* **GDPR Port 4 PII-Skjerming**: Automatisk sladding av fødselsnumre (11 siffer), bankkonti og helseopplysninger *før* teksten settes sammen i kontekstvinduet.

---

## 3. Nivå 3: Harness Engineering (Kjøremiljø & Sikkerhet)

Harness Engineering etablerer det sikre, isolerte kjøremiljøet (*runtime architecture*) rundt modellen. Det kobler modellen trygt til omverdenen via kontrollerte grensesnitt.

### Kjernemekanismer i `AI_KOM`:
* **Model Context Protocol (MCP)**: Standardisert integrasjonslag ("USB-C for AI") som kobler modellen til Framsikt, SSB KOSTRA og kommunale databaser via sikre API-endepunkter (`Tools` og `Resources`).
* **Luftisolert Sandkasse (Air-Gapped Sandbox)**: Kodeeksekvering og beregninger kjøres i isolerte miljøer uten direkte tilgang til eksterne nettverk, noe som forhindrer utilsiktet datalekkasje.
* **Sikkerhet mot Prompt-Injeksjon (OWASP LLM01/LLM02)**: Inngående bilagstekster og eksterne fakturadata skannes og nøytraliseres for å hindre indirekte prompt-injeksjoner.

---

## 4. Nivå 4: Loop Engineering (Selvkorrigering & Kvalitet)

Loop Engineering erstatter manuelle "re-prompting"-løkker med **autonome, selvkorrigerende tilbakemeldingssløyfer** basert på et **Generator vs. Evaluator**-mønster.

### Kjernemekanismer i `AI_KOM`:
* **Evaluator-Optimizer Løkke**:
  1. **Generator-node**: Lager utkast til saksfremlegg eller avviksnotat.
  2. **Evaluator-node**: Sjekker utkastet mot **3 udiskutable kvalitetsporter**:
     * ⚖️ Eksplisitt henvisning til *Kommuneloven § 14-5* (Handlingsplikt ved merforbruk).
     * ⚖️ Eksplisitt henvisning til *Kommuneloven § 14-6* (Bruttoprinsippet).
     * 🔒 100 % skjerming for PII (GDPR).
  3. **Refinement Turn**: Ved avvik sendes spesifikk tilbakemelding tilbake til Generator for retting (maks 3 iterasjoner).
* **Stage-Gate Port 9 & SHA-256 Revisjonsstempel**: Når Evaluator godkjenner utkastet, påføres et kryptografisk tidsstempel og SHA-256 segl jf. *EU AI Act Art. 14* for *Kommunerevisjonen*.

---

## 5. Nivå 5: Graph Engineering (Orkestrering & Fleragent)

Graph Engineering koordinerer komplekse, sammensatte saksbehandlingsprosesser ved å koble spesialiserte agenter sammen i en **rettet asyklisk graf (DAG)** med dyp tilstandskontroll (*Statecharts / LangGraph*).

### Kjernemekanismer i `AI_KOM`:
```text
                  ┌────────────────────────┐
                  │ INNKOMMENDE HENDELSE  │
                  │ (F.eks. M8-Avviksrapport)
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │    TRIAGE ROUTER       │ (Ruter saken til rett agent)
                  └─────┬────────────┬─────┘
                        │            │
            ┌───────────┘            └───────────┐
            ▼                                    ▼
┌───────────────────────┐            ┌───────────────────────┐
│   CONTROLLER-AGENT    │            │    JURIDISK AGENT     │
│ (Regnskap & Avvik)    │            │ (Kommunelov & Vedtak) │
└───────────┬───────────┘            └───────────┬───────────┘
            │                                    │
            └───────────┐            ┌───────────┘
                        ▼            ▼
                  ┌────────────────────────┐
                  │    REVISJONS-AGENT     │ (Sjekker bruttoprinsipp & PII)
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │  HUMAN-IN-THE-LOOP     │ (Endelig sign-off fra leder)
                  │ (Stage-Gate Port 9)    │
                  └────────────────────────┘
```

* **Rollefordeling i Grafen**:
  * **Triage Router**: Lynrask sortering basert på risikonivå (🔴 Rød / 🟠 Rav / 🟢 Grønn).
  * **Controller-Agent**: Analyserer regnskapstall fra Visma og beregner avvik.
  * **Juridisk Agent**: Utformer formelle vedtakspunkter og sikrer hjemmelsgrunnlag.
  * **Revisjons-Agent**: Kjører sluttkontroll jf. Kommuneloven.
* **Human-In-The-Loop (HITL) Avbrudd**: Grafen stanser automatisk ved kritiske beslutningspunkter og krever godkjenning fra enhetsleder eller controller før notater journalføres.

---

## Oppsummering og Verdiløfte

| Nivå | Hva det løser i Kristiansand kommune |
| :--- | :--- |
| **1. Prompt** | Sikrer presise og strukturerte svar fra AI-modellen. |
| **2. Context** | Forhindrer at 81 enheters regnskap fyller minnet (sparer 90 %+ tokens). |
| **3. Harness** | Gir trygg tilkobling til Framsikt og ERP i isolerte sandkasser. |
| **4. Loop** | Garanterer at ingen utkast sendes til leder før lovkrav og GDPR er sjekket. |
| **5. Graph** | Automatiserer hele saksbehandlingskjeden fra avvik til politisk vedtak. |
