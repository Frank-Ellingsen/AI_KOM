# 🛠️ Tool Skill: Ollama API Bridge & LLM Driver

> **Teknisk integrasjonsmodul for lokalt Ollama-runtimemiljø (`llama3.1`, `qwen2.5`, `mistral`) med JSON-schema validering og feilhåndtering.**

---

## 1. Oversikt og Formål

Denne verktøy-skillen styrer kommunikasjonen mellom agenten og den lokale Ollama-serveren (`http://localhost:11434`). Den sørger for 100 % lokal, skjermet AI-inferens uten at data forlater kommunens nettverk.

---

## 2. Kjernefunksjonalitet

1. **Modellstyring:**
   * Automatisk sjekk av tilgjengelige modeller via `ollama.list()`.
   * Dynamisk fallback fra `llama3.1` til `qwen2.5` eller `mistral` dersom foretrukket modell ikke svarer.
2. **Strukturert Output (JSON Schema Mode):**
   * Tvinger Ollama til å returnere gyldig, parsbar JSON for saksfremlegg og strukturert avviksanalyse.
3. **Innebygd Parametersetting:**
   * Temperaturkontroll: `0.0` – `0.1` for fakta/juss; `0.3` – `0.5` for oppsummeringer og fagspråk.
   * `num_ctx`: Utvidet kontekstvindu (8192 / 16384 tokens) for store kildeblokker.

---

## 3. Eksempel på Kjørekode

```python
import ollama

def call_local_ollama(system_prompt: str, user_prompt: str, model="llama3.1", json_mode=False):
    options = {
        "temperature": 0.1,
        "num_ctx": 8192
    }
    format_type = "json" if json_mode else None
    
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options=options,
            format=format_type
        )
        return response["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Ollama API Feil: {str(e)}. Sjekk at 'ollama serve' kjører.")
```

---

## 4. Sikkerhet og Ytelse
* **Air-gapped verification:** Ingen utgående nettverkskall.
* **Timeout & Retry:** Håndterer modelloppvarming og caching av minne.
