# 📐 Systemarkitektur & Multi-Agent Veikart

Dette dokumentet beskriver den tekniske arkitekturen for **AI Økonomirådgiver i Kristiansand kommune** samt overgangen fra nåværende MVP til et **LangGraph Multi-Agent System**.

---

## 1. 6-Nivås Budsjetthierarki (Data Architecture)

Løsningen strukturerer kommunens økonomidata i seks hierarkiske nivåer:

Sektor (1) -> Kommunalsjefområde (2) -> Ansvar/Enhet (3) -> KOSTRA-Funksjon (4) -> KOSTRA-Art (5) -> Bilag (6)

* **Sektor (Nivå 1):** F.eks. Helse og Mestring.
* **Kommunalsjefområde (Nivå 2):** F.eks. Omsorgssentre, Hjemmetjenester, Mestring.
* **Ansvar / Enhet (Nivå 3):** F.eks. Ansvar `2530` (Randesund Omsorgssenter).
* **KOSTRA-Funksjon (Nivå 4):** F.eks. Funksjon `253` (Pleie og omsorg i institusjon).
* **KOSTRA-Art (Nivå 5):** F.eks. Art `10000` (Fast lønn) eller Art `10900` (Overtid).
* **Bilag (Nivå 6):** Enkelttransaksjoner i ERP-databasen (`stg_erp_transactions`).

---

## 2. Hybrid RAG + Parameterisert SQL Engine

```text
                        ┌──────────────────────────────┐
                        │   Brukerforespørsel (Chat)   │
                        └──────────────┬───────────────┘
                                       │
                        ┌──────────────▼───────────────┐
                        │  Gemini 2.0 Agent Orkestrator │
                        └──────┬───────────────┬───────┘
                               │               │
            ┌──────────────────┴──┐         ┌──┴──────────────────┐
            ▼                     ▼         ▼                     ▼
┌───────────────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ query_erp_transactions│ │  rag_search   │ │  eoy_forecast │ │ process_realloc│
│     (SQL + RBAC)      │ │ (Vektorsøk)   │ │ (Lønnsmotor)  │ │ (Juss §14-5)  │
└───────────┬───────────┘ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                     │                 │                 │
            └─────────────────────┴────────┬────────┴─────────────────┘
                                           ▼
                            ┌──────────────────────────────┐
                            │  Uforanderlig Audit Log Entry│
                            │   (audit_log i SQLite/PG)    │
                            └──────────────────────────────┘
```

---

## 3. Sikkerhet, RBAC og Audit Trail

* **RBAC (Role-Based Access Control):** Enhetsledere får automatisk lagt på `WHERE ansvar = '...'` på alle SQL-spørringer.
* **GDPR & K-Anonymitet:** Transaksjoner skjermes på aggregert artsnivå uten personidentifikatorer.
* **Audit Trail (Arkivlova):** Alle spørringer, agentutkast og omdisponeringer logges i databasen med tidsstempel, bruker-ID og handling.

---

## 4. Multi-Agent Veikart (LangGraph Subgraphs)

Neste steg i produksjonsskaleringen er å splitte den monolittiske agenten inn i **fire spesialiserte undergrafer (subgraphs)**:

1. **Supervisor / Router Agent:** Analyserer henvendelsen og ruter til rett agent.
2. **Regnskapsagent (ERP/MVA):** Kjører presise SQL-spørringer og avstemminger.
3. **Budsjett- & EOY-Agent:** Integrert mot Framsikt for årsprognoser og avvik.
4. **Saksbehandlingsagent:** Utarbeider formelle saksframlegg jf. Kommuneloven § 14-5.
