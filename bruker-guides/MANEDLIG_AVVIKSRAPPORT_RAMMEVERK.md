# 📊 Rammeverk for Månedlig Avviks- og Tiltaksrapportering
**Kristiansand Kommune -- Økonomi og Virksomhetsstyring**

---

## 🏛️ 1. Formål og Innledning
Dette rammeverket definerer den månedlige rutinen for automatisk og automatisert avviksrapportering med tilhørende tiltaksforslag (*Action Plans*) på fem organisatoriske nivåer i Kristiansand kommune:
1. **Kommunestyret / Bystyret** (Politisk overordnet)
2. **Kommunedirektør** (Toppadministrasjon)
3. **Kommunalsjef** (Sektorleder)
4. **Seksjonsleder / Stabssjef** (Fag- og stabsfunksjon)
5. **Avdelingsleder / Enhetsleder** (Operativ virksomhet)

Systemet kombinerer regnskapstransaksjoner fra **Visma ERP**, budsjettrammer fra **Framsikt EPM**, KOSTRA-nøkkeltall fra **SSB**, samt AI-genererte tiltaksforslag forankret i **Kommuneloven** og kommunens **Økonomireglement**.

---

## 📐 2. Avviksterskler og Gradering per Nivå

For å unngå informasjonsoverflod filtreres og eskalerers avvik basert på definerte terskelverdier:

| Nivå | Avviksterskel (Kroner) | Avviksterskel (%) | Kriterie for Eskalering |
| :--- | :--- | :--- | :--- |
| **1. Bystyret** | Avvik > 5 000 000 kr | > 3.0 % av sektorramme | Prinsipielle avvik, fondstapping, endring av låneramme (Kommuneloven § 14-5). |
| **2. Kommunedirektør** | Avvik > 2 000 000 kr | > 2.0 % av kommunens samlede drift | Tverrsektorielle avvik, behov for ansettelsesstopp eller administrative strakstiltak. |
| **3. Kommunalsjef** | Avvik > 500 000 kr | > 5.0 % av enhetens ramme | Systemiske avvik på tvers av underliggende enheter, vikar- og overtidseksplosjon. |
| **4. Seksjonsleder** | Avvik > 200 000 kr | > 5.0 % av seksjonens ramme | Avvik på fellesprosjekter, fagsystemer, fellesavtaler eller stabsressurser. |
| **5. Enhetsleder** | Avvik > 50 000 kr | > 5.0 % på enkeltkonto/art | Linjeavvik på lønn (art 1020/1090), vikarer, sykefravær eller driftsavtaler. |

---

## 🔄 3. Den Månedlige Rapporteringssløyfen (Månedshjulet)

```text
[ Dag 1-3: Månedsoppgjør i Visma ERP ]
                 │
                 ▼
[ Dag 4: ETL-Kjøring & PII-vask til SQLite ]
                 │
                 ▼
[ Dag 5: Automatisk Avviksdeteksjon & AI-Tiltaksgenerering ]
                 │
                 ▼
[ Dag 6-7: Controller-gjennomgang & HITL Sign-Off (APPROVED/MODIFIED) ]
                 │
                 ▼
[ Dag 8: Distribusjon av Månedlige Rapporter til Leder 1–5 ]
```

---

## 🤖 4. AI-Generering av "Forslag til Action"

For hvert identifiserte kritiske avvik utarbeider systemet en strukturert tiltakspakke bestående av:
1. **Årsaksdiagnose:** Kobling mellom regnskapstall, NAV-refusjonsetterslep og fraværsdata.
2. **Standardiserte Tiltaksalternativer:**
   * *Strakstiltak (0–30 dager):* Innkjøpsstopp, overtidskontroll, vikarrestriksjon.
   * *Strukturelle tiltak (30–90 dager):* Bemanningsplanjustering, tildelingsmodell-revidering.
   * *Politiske tiltak (> 90 dager):* Sak om tilleggsbevilgning eller omdisponering i Bystyret.
3. **Konsekvensberegning:** Forventet innsparing i NOK og beregnet effekt på EOY (End-of-Year) helårsprognose.
4. **Kilde- & Paragrafhenvisning (§):** Forankring i Kommuneloven, KOSTRA-veiledere og Økonomireglement.

---

## 🛡️ 5. Sporbarhet, Transparens og Audit Trail (Port 9)

Alle månedlige rapporter og tiltaksforslag behandles i henhold til **Human-in-the-Loop (HITL)**-prinsippet:
* Saksbehandler/Controller må aktivt gjennomgå og godkjenne rapporten.
* Rapportens innhold, AI-genererte forslag og saksbehandlers endringer stemples med en uforanderlig **SHA-256 hash** i `Audit_AI_Actions`-databasen for **Kommunerevisjonen**.
