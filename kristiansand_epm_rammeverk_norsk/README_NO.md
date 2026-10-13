# Kristiansand Kommune — Agentisk EPM & AI Rammeverk (Norsk Versjon)

Dette rammeverket utgjør en komplett, ansvarlig og RAG-forankret Enterprise Performance Management (EPM) arkitektur for Kristiansand kommune.

## 📁 Komplett Mappestruktur (Norsk)

```text
kristiansand_epm_rammeverk_norsk/
├── README_NO.md                                      <- Hovedveileder for rammeverket
├── agent_ferdigheter/                                <- Spesialiserte agent-instruksjoner (.md)
│   ├── 01_dataintegrasjon_etl_agent.md               <- Integrasjon og KOSTRA-harmonisering
│   ├── 02_bi_dax_modellering_agent.md                <- DAX-måltall og stjernemodell
│   ├── 03_prediktiv_anomali_agent.md                 <- Sesongdekomponering og tidligvarsling
│   ├── 04_preskriptiv_hitl_agent.md                  <- Tiltak og beslutningsstøtte
│   ├── 05_etikk_styring_portvakt_agent.md            <- Kommuneloven & EU AI Act (FRIA)
│   ├── 06_ledelsesrapport_skribent_agent.md          <- Saksfremlegg og tertialnotater
│   ├── 07_excel_powerbi_rapportering_agent.md        <- Tufte/IBCS dashboard-design
│   └── 08_flerniva_interessent_rapportering_agent.md <- Rollebasert interessentrapportering
├── dokumentasjon/                                    <- Systemdokumentasjon, saksfremlegg og analyser
│   ├── antigravity_brukstilfelle_epm.md              <- Fullstendig teknisk arkitekturbeskrivelse
│   ├── dax_kostra_kpi_pakke.md                       <- Full KOSTRA DAX-pakke
│   ├── epm_fullstendig_arbeidsflyt.md                <- End-to-end agentisk arbeidsflyt
│   ├── rag_kunnskapsbase_spesifikasjon.md            <- RAG-kontekst, embeddings og kildekrav
│   ├── saksfremlegg_epm_okonomidirektor.docx         <- Formelt saksfremlegg til økonomidirektøren
│   ├── Rapport om innføring AI i offentlig sektor.docx<- Risiko-, etikk- og styringsrapport
│   ├── tildelingsskjema_ai_anbud.xlsx                <- Evalueringsmatrise for anskaffelse
│   └── epm_sammendrag_kristiansand.pdf               <- Ledelsessammendrag (1-sides executive memo)
├── data/                                             <- Datagrunnlag og SQLite Golden Record
│   ├── BoMiljø.csv                                   <- Anonymiserte regnskapsdata (Kommunal Boenhet)
│   ├── Komskole.csv                                  <- Anonymiserte regnskapsdata (Kommunal Skole)
│   ├── kostra_kontoplan.csv                          <- Komplett KOSTRA kontoplanhierarki (SSB)
│   ├── kontor_oversikt_og_arshjul.xlsx               <- Årshjul og prosessoversikt for økonomistyring
│   └── kristiansand_golden_record.db                 <- SQLite Golden Record database
├── kildekode/                                        <- Produksjonsklar kildekode og scripts
│   ├── datalinje/
│   │   └── epm_agent_pipeline.py                     <- Python ETL, Golden Record & Audit Log
│   ├── powerbi/
│   │   └── fxOpenAI_RAG.m                            <- Power Query M-funksjon for RAG-oppslag
│   ├── brukergrensesnitt/
│   │   └── hitl_skriveback_ui.py                     <- Streamlit Glass-Box Controller UI
│   └── sikkerhet/
│       └── pii_scrubber.py                           <- Lokal PII-anonymisering for fritekst/bilag
└── ressurser/                                        <- Visuelle diagrammer og illustrasjoner
    ├── epm_arbeidsflyt_diagram.png                   <- Komplett arkitekturflyt
    └── kontor_arbeidsflyt_diagram.png                <- Kontorarbeidsflyt diagram
```

## 🛡️ Sikkerhet, Personvern & RAG-arkitektur

- **Manuell utløsning (Human-in-the-Loop):** Ingen uønskede automatiserte køer eller API-kall uten eksplisitt lederbeslutning.
- **Enterprise AI Provider & Lokal Klargjøring:** Azure OpenAI (Norge/EU) med DPA og Zero Data Retention (ZDR), alternativt lokal LLM (f.eks. Ollama / LM Studio).
- **Lokal PII-anonymisering:** `pii_scrubber.py` fjerner automatisk fødselsnumre, kontonumre, telefonnumre, e-poster og personnavn før data eventuelt sendes til ekstern analyse.
- **RAG-forankring:** Preskriptive tiltak forankres mot økonomireglement, delegeringsreglement og KOSTRA-veiledere.
