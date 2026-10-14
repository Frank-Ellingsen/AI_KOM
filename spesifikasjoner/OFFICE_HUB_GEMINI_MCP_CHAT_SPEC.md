# 💬 Spesifikasjon: Gemini Flash API & MCP Chat-Integrasjon i Office Hub

**Dokument-ID:** SPEC-OFFICE-HUB-CHAT-001  
**Versjon:** 1.0  
**Gjelder:** Økonomi og Virksomhetsstyring, Kristiansand kommune  
**Sikkerhetsnivå:** Internt / Skjermet sone (Med PII-vask og Model Context Protocol)

---

## 1. Formål og Oversikt

For å håndtere en hektisk hverdag med stor arbeidsbelastning, etableres en direkte chat-assistent i **Control Office Hub**. Saksbehandlere og økonomirådgivere kan stille spørsmål på vanlig norsk direkte til kommunens økonomiske data (Visma ERP, Framsikt EPM, KOSTRA, Økonomireglement og Kommuneloven).

Chat-funksjonen drives av **Google Gemini API (Flash-modellen)** for lynrask responstid (< 2 sekunder), kombinert med **MCP (Model Context Protocol)** for trygg, strukturert og skrivebeskyttet datatilgang.

---

## 2. Arkitektur og Hvorfor MCP (Model Context Protocol)?

### 2.1 Hvorfor bruke MCP?
Model Context Protocol (MCP) er en åpen standard som skiller AI-modellen fra fagsystemene. Dette sikrer:
1. **Streng skrivebeskyttelse:** Gemini kan kun *lese* og *spørre* databasene via definerte MCP-verktøy, uten risiko for feilaktige endringer i Visma/Framsikt.
2. **Kildekontroll og Schema-validering:** MCP-serverne validerer SQL-spørringer mot definerte tabeller (`Fact_Regnskap`, `Fact_Budsjett`, `Dim_*`) før kjøring.
3. **Modulær utvidelse:** Samme MCP-servere kan benyttes av både Streamlit UI, Excel-tillegg og fremtidige fagsystemer.

### 2.2 Systemarkitektur for Chat

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 🖥️ STREAMLIT OFFICE HUB UI (Chat-panel i høyre sidefelt / Drawer)                 │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 1. Brukerstilt spørsmål på norsk
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 🛡️ PII ANONYMISERINGSMOTOR (Local PII Masker)                                    │
│   • Vasker fødselsnumre, navn, e-post før sending ut                             │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 2. Vasket prompt
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ GEMINI API (Gemini Flash via Google GenAI SDK med API-nøkkel)                 │
│   • Genererer intent, SQL-utkast og kildeoppslag                                 │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 3. Tool Calls via MCP Client
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 🔌 MCP SERVERE (Model Context Protocol Hosts)                                     │
│   ├── 🗄️ SQLite MCP Server: Kjører henviste SQL-spørringer mot Star Schema       │
│   ├── 📚 KOSTRA & Legal RAG MCP Server: Henter lovhjemler (§) og rundskriv       │
│   └── 📊 Excel & EPM MCP Server: Henter Framsikt-rammer og periodisering         │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 4. Strukturert data- og kilderesultat
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 💬 GENERERT SVAR MED GLASS-BOX TRANSPARENS                                        │
│   • Viser svar, tabell/graf, benyttet SQL, paragrafhenvisning og SHA-256 hash    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Nøkkelkomponenter i Chat-løsningen

### 3.1 PII-Skjerming før API-kall
Ingen personopplysninger sendes til eksterne API-er. PII-motoren (`PIIMasker`) fanger opp og erstatter fødselsnumre og navn med anonyme tokens (`[PERSON_1]`, `[EPOST_MASKERT]`) i minnet på lokal server før prompten oversendes Gemini Flash.

### 3.2 Implementerte MCP-Verktøy (Tools) for Chat

| MCP Server | Verktøynavn (Tool Name) | Beskrivelse |
| :--- | :--- | :--- |
| **`mcp-sqlite-finance`** | `query_ytd_variance` | Henter YTD-avvik i kroner og prosent for gitt enhet/ansvar/art fra `Fact_Regnskap` vs `Fact_Budsjett`. |
| **`mcp-sqlite-finance`** | `get_eoy_prognosis` | Kjører prediktiv tidsserieanalyse og henvender p10/p50/p90 prognoser for end-of-year balanse. |
| **`mcp-rag-legal`** | `search_municipal_law` | Hybrid RAG-søk (BM25 + `sqlite-vec`) i Kommuneloven, KOSTRA-veileder og Økonomireglementet. |
| **`mcp-excel-framsikt`** | `get_budget_ramme` | Henter vedtatte og tertialjusterte rammer per kommunalsjefområde fra Framsikt API/Excel. |

---

## 4. Kildekode-eksempel: Streamlit Chat med Gemini API & MCP

```python
import streamlit as st
import google.generativeai as genai
import json
import os
from pii_masker import mask_pii
from mcp_client import MCPFinanceClient

# Konfigurer Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

st.title("💬 Office Hub AI-Chat -- Økonomi & Virksomhetsstyring")

# Tilstandsstyring for chat-historikk
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vis historiske meldinger
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_prompt := st.chat_input("Spør om regnskapstall, avvik, prognoser eller KOSTRA-regler..."):
    # 1. Vis brukers spørsmål
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. PII-Skjerming
    clean_prompt, _ = mask_pii(user_prompt)

    # 3. Kall Gemini Flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    with st.chat_message("assistant"):
        with st.spinner("Analyserer data via MCP..."):
            mcp = MCPFinanceClient()
            system_instruction = """
            Du er en senior økonomirådgiver i Kristiansand kommune.
            Besvar spørsmålet presist basert på hentet data.
            Oppgi alltid:
            1. Avvik i tall og prosent
            2. Årsak til avvik
            3. Korrekt lov- eller reglementsparagraf (§)
            4. Kvantifisert effekt på helårsbalansen (EOY).
            """
            
            response = model.generate_content(
                f"{system_instruction}\n\nBrukerspørsmål: {clean_prompt}"
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
```

---

## 5. Beredskap og Fallback

1. **Fallback ved manglende nett/API-nøkkel:** Om Gemini API ikke kan nås, kobles chatten automatisk over til den lokale **Ollama `qwen2.5`**-modellen uten avbrudd for saksbehandler.
2. **Revisjonsstempel:** Hvert chat-svar som benyttes inn i et saksnotat eller en tertialrapport får automatisk lagret en **SHA-256 hash** i databasens `Audit_AI_Actions`-tabell for Kommunerevisjonen.
