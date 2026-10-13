# 🐳 Docker Kontainerarkitektur & MLOps / RAG Eval Specification

## 1. Oversikt over Kontainerarkitekturen

For å sikre 100 % isolert, skalerbar og reproduserbar drift i kommunens IKT-miljø (IKT Agder / intern server), pakkes **Kommune AI Guardrails** i en isolert Docker-kontainer koblet sammen med den lokale **Ollama AI-motoren**.

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 🌐 DOCKER COMPOSE MELDINGS- & NETTVERKSSONER                          │
├───────────────────────────────────────┬────────────────────────────────┤
│ 📦 KONTAINER 1: kommune_ai_app        │ 📦 KONTAINER 2: kommune_ai_ollama│
│ • Streamlit Web UI (Port 8501)        │ • Ollama AI Engine (Port 11434)│
│ • SQLite (sqlite-vec 384D + FTS5)     │ • Llama 3.1 / Qwen 2.5 modeller│
│ • Python 3.12 Runtime & PII-Vasker    │ • GPU- / CPU-Akselerasjon      │
└───────────────────────────────────────┴────────────────────────────────┘
```

---

## 2. Kontainerfiler & Konfigurasjon

### 📜 `Dockerfile`
```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl sqlite3 libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY app/ /app/app/
COPY data/ /app/data/
COPY config/ /app/config/

EXPOSE 8501
CMD ["streamlit", "run", "app/app.py", "--server.headless=true"]
```

### 📜 `docker-compose.yml`
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: kommune_ai_ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_storage:/root/.ollama

  kommune_ai_app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kommune_ai_app
    restart: unless-stopped
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama

volumes:
  ollama_storage:
```

---

## 3. Light-weight MLOps & Automatisert RAG Evaluation

I stedet for et tungt MLflow-rigg benyttes en **Golden Test Suite** (`tests/test_rag_eval.py`) som måler tre nøkkelindikatorer før ny utrulling:

1. **Faithfulness Score (100 % Kildeforankring):** Sjekker at AI-svaret utelukkende er basert på hentede kilde-chunks (§).
2. **Context Precision & Recall:** Sjekker at vektorsøket faktiske henter opp riktig paragraf i Kommuneloven, KOSTRA eller Økonomireglementet.
3. **PII Safety Check:** Sjekker at fødselsnumre, e-postadresser og navn vaskes bort før søk og loggføring.

---

## 🚀 Oppstartskommandoer for IT-drift

For å starte hele løsningen på serveren:

```bash
# 1. Bygg og start kontainerne i bakgrunnen
docker compose up -d --build

# 2. Last ned valgt Ollama-modell inn i Ollama-kontaineren
docker exec -it kommune_ai_ollama ollama pull llama3.1

# 3. Kjøre automatisert RAG-evaluering
docker exec -it kommune_ai_app python tests/test_rag_eval.py
```
