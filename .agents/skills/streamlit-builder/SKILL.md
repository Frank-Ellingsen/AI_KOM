---
name: streamlit-builder
description: >-
  Streamlit Web UI komponenter, Control Office Hub layout, Session State tilstandsbevaring og caching.
---

# 🛠️ Tool Skill: Streamlit UI & Component Rendering Driver

> **Teknisk driver for utvikling og vedlikehold av interaktive Streamlit web-portaler (`app/app.py`).**

---

## 1. Oversikt og Formål

Bygger og optimaliserer brukergrensesnitt for saksbehandlere, økonomirådgivere og ledere. Håndterer tilstandsbevaring (*Session State*), caching, dynamiske faner og direkte nedlasting av rapporter og Audit Logs.

---

## 2. Arkitekturmønster i Streamlit

```text
[ Streamlit App (app/app.py) ]
  ├── 1. Layout & Styling (st.set_page_config)
  ├── 2. Cached Modeller (@st.cache_resource)
  ├── 3. Session State (st.session_state)
  ├── 4. Hovedkomponenter (Søk, Tabeller, Avviks-cards)
  └── 5. Eksport & Nedlasting (st.download_button)
```

---

## 3. Beste Praksis & Kodeeksempel

```python
import streamlit as st

def init_ui_session():
    """Initialiserer session state for vedvarende spørrehistorikk."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama3.1"

def render_audit_download(audit_df):
    """Genererer en nedlastingsknapp for SHA-256 Audit Trail."""
    csv_data = audit_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Last ned SHA-256 Audit Log (CSV)",
        data=csv_data,
        file_name="audit_log_kristiansand_ai.csv",
        mime="text/csv"
    )
```

---

## 4. Ytelsesregler
* Bruk `@st.cache_resource` for tyngre modeller (SentenceTransformers) så de kun lastes én gang i minnet.
* Bruk `@st.cache_data` for SQL-spørringer mot `kommune_golden_record.db`.
