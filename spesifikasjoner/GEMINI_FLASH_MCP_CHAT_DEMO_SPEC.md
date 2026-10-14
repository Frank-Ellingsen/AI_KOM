# Gemini Flash 3.6 Chat & MCP Integration Spec - Office Hub V2

## 1. Oversikt og Arkitektur

Dette dokumentet spesifiserer interaksjonsmodellen, MCP-verktøykoblingene (Model Context Protocol), og den operative spørreflaten for **Gemini Flash 3.6 Chat** i sidepanelet i **Office Hub V2**. 

Løsningen er designet for maksimal effisiens i en hektisk kommunal hverdag ved å kombinere lynrask AI-inferens (< 1,5 sekunders responstid) med **Glass-Box RAG** forankret i Kommuneloven, KOSTRA-kontoplanen og rådata fra Visma ERP.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      OFFICE HUB V2: GEMINI FLASH & MCP ARCHITECTURE              │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   [ 👤 Saksbehandler ] ──> ( Spørsmål i Streamlit Chat Sidebar )                │
│                                       │                                          │
│                                       ▼                                          │
│                         [ 🛡️ PII-Anonymiseringsmotor ]                          │
│                                       │                                          │
│                                       ▼                                          │
│                     [ ⚡ Google Gemini Flash 3.6 API ]                            │
│                                       │                                          │
│            ┌──────────────────────────┴──────────────────────────┐               │
│            │ (MCP Tool Call)                                     │ (RAG Context) │
│            ▼                                                     ▼               │
│  [ 🛠️ MCP Server: Finance Tools ]                       [ 📚 sqlite-vec RAG ]     │
│    • get_unit_financials()                              • Kommuneloven §         │
│    • get_eoy_prognosis()                                • KOSTRA Veileder        │
│    • calculate_action_effect()                          • Økonomireglement       │
│                                       │                                          │
│                                       ▼                                          │
│            [ 🔒 SHA-256 Audit Stempel & Visning i UI ]                          │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. MCP Tools (Model Context Protocol) Spesifikasjon

Gemini Flash 3.6 kommuniserer med kommunens databaser via Model Context Protocol (MCP). Modellen har **0 direkte skrive- eller SQL-tilgang**, men kaller strukturerte, skrivebeskyttede funksjoner:

### MCP Tool 1: `get_unit_financials`
* **Beskrivelse:** Henter ferske YTD-tall, budsjettrammer og transaksjonsspesifikasjoner fra Visma ERP/SQLite for en spesifikk enhet.
* **Parametre:** `unit_id` (str), `period` (str), `account_group` (optional[str]).
* **Returverdi:** JSON med YTD-forbruk, budsjett, avvik i kr/%, og topp 3 avvikskontoer.

### MCP Tool 2: `search_municipal_law`
* **Beskrivelse:** Søker i den lokale vektordatabasen (`sqlite-vec`) etter relevante lovhjemler, reglementer og KOSTRA-veiledere.
* **Parametre:** `query_text` (str), `top_k` (int).
* **Returverdi:** Ekstrakter fra Kommuneloven, Økonomireglementet og Bystyrevedtak med eksakte paragrafhenvisninger (§).

### MCP Tool 3: `calculate_eoy_impact`
* **Beskrivelse:** Beregner simulert helårseffekt (End-of-Year balance) dersom spesifikke tiltak iverksattes.
* **Parametre:** `unit_id` (str), `action_type` (str), `monthly_saving` (float), `start_month` (int).
* **Returverdi:** Monte Carlo-simulert EOY-balanse (P10, P50, P90).

---

## 3. Simulert Case-Studie: Enhet 202 Grunnskole

### A. Brukerforespørsel
> *"Hva er status på Enhet 202 Grunnskole per Q2, hva er hovedårsaken til avviket, og hvilken effekt vil tiltakene ha på helårsprognosen (EOY)?"*

### B. Eksekveringskjede
1. **PII-Sanitering:** Tekst analyseres og vaskes for ev. personnavn før ekstern API-sending.
2. **MCP Tool Call 1:** `get_unit_financials(unit_id="202", period="Q2")`
3. **MCP Tool Call 2:** `search_municipal_law(query_text="inndekning av merforbruk budsjettbalanse")`
4. **MCP Tool Call 3:** `calculate_eoy_impact(unit_id="202", action_type="vikar_stopp", monthly_saving=170000, start_month=8)`
5. **Generering:** Gemini Flash 3.6 formaterer svaret ihht. kommunens obligatoriske 4-punktsmønster.

### C. Generert Svar fra Gemini Flash Chat

```markdown
### 📊 1. Avvik hittil i år (YTD Variance)
• **Driftsbudsjett Q2:** 6 850 000 kr
• **Faktisk regnskap (Visma ERP):** 7 700 000 kr
• **YTD Avvik:** **+850 000 kr (+12,4 % merforbruk)** — *Rødt flagg utløst i triage-køen.*

---

### 🔍 2. Årsak til avvik (Root Cause)
Glass-Box RAG-analysen av kontoplanen viser at 88 % av avviket skyldes to spesifikke kontoer:
1. **Konto 1020 (Innkjøp av vikarer):** +620 000 kr over ramme som følge av 14,2 % sykefravær i mai/juni.
2. **Konto 1600 (NAV-sykepengerefusjoner):** −180 000 kr i etterslep (gjennomsnittlig saksbehandlingstid hos NAV er p.t. 48 dager).

---

### 🎯 3. Forslag til Action Plan
1. **Strakstiltak (0–30 dager):** Slå sammen parallellklasser ved korttidsfravær < 3 dager, samt sende samlepurring til NAV for utestående refusjonskrav.
2. **Strukturelt tiltak (30–90 dager):** Inngå avtale om deling av fast ansatte ressurspersoner på tvers av skoler i Oppvekstsektoren.

---

### 📈 4. Kvantifisert Effekt på Prognosebane og EOY Balanse
• **Uten tiltak (P90 / Worst Case):** Forventet helårsavvik per 31.12 blir **+1 720 000 kr**.
• **Med tiltak (P10 / Forventet bane):** EOY-avviket reduseres til **+350 000 kr**, som kan dekkes inn via sektorens omstillingsfond.
• **Lovhjemmel (§):** Oppfyller inndekningskravet i **Kommuneloven § 14-5** om budsjettbalanse innen inneværende økonomiplanperiode.

*(SHA-256 Audit Stempel: `a8f9c2e4...8b1e` | Status: Klar for sign-off av Kommunalsjef)*
```

---

## 4. Implementasjon i Streamlit UI (Python Snippet)

```python
import streamlit as st
import json
import hashlib
from datetime import datetime

def render_gemini_mcp_chat():
    st.sidebar.title("💬 Gemini Flash Chat (MCP)")
    st.sidebar.caption("Søk i regnskap, lover og prognoser")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Vis chat-historikk
    for msg in st.session_state.chat_history:
        with st.sidebar.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Brukerinput
    if user_prompt := st.sidebar.chat_input("Spør om økonomi eller lover..."):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.sidebar.chat_message("user"):
            st.markdown(user_prompt)

        with st.sidebar.chat_message("assistant"):
            with st.spinner("Henter data via MCP & RAG..."):
                # PII-vask og MCP-kall utføres her
                response_text = execute_gemini_mcp_query(user_prompt)
                st.markdown(response_text)
                
                # Generer SHA-256 stempel for audit
                audit_hash = hashlib.sha256(f"{datetime.now().isoformat()}:{user_prompt}:{response_text}".encode()).hexdigest()[:12]
                st.caption(f"🔒 SHA-256 Audit ID: `{audit_hash}`")
                
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

def execute_gemini_mcp_query(prompt: str) -> str:
    # Plassholder for ekte Gemini Flash API + MCP Tool Call-logikk
    return "Svar simulert i samsvar med MCP-spesifikasjonen."
```

---

## 5. Sikkerhet, Governance & Offline Fallback

1. **GDPR & PII-Skjerming:** Ingen fødselsnumre, ansattnavn eller enkeltstående elevdata sendes til Gemini Flash API.
2. **Kryptografisk Audit Trail:** Alle chat-sesjoner logges med SHA-256 fingeravtrykk i `Audit_AI_Actions`-databasen for ettersyn fra Kommunerevisjonen (Stage-Gate Port 9).
3. **Offline Fallback:** Dersom nettforbindelsen til Gemini Flash API opplever feil eller timeout (> 3,0 sekunder), kobler sidepanelet om automatisk til den lokale **Ollama `qwen2.5`**-modellen uten at brukeren mister økten.
