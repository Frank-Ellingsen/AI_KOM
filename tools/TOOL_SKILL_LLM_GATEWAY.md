# 🛠️ Tool Skill: Hybrid LLM Gateway & Driver (`TOOL_SKILL_LLM_GATEWAY`)

> **Teknisk integrasjonsmodul for hybrid LLM-inferens: Google Gemini 3.8 Flash som primærmodell (0 % CPU-last, 1–2s responstid) med sømløs fallback til lokal Ollama (`llama3.1`, `qwen2.5`) ved frakoblet/air-gapped drift.**

---

## 1. Oversikt og Formål

For å sikre maksimal responstid på standard PC-er uten dedikert GPU, ruter **LLM Gateway** spørringer intelligent:
1. **Primær rute:** Google Gemini (`gemini-3.8-flash`) via `google-genai` SDK.
   - Forutsetning: Client-side PII-vasking (Stage-Gate Port 4) utføres *før* forespørselen sendes.
   - Ytelse: 0 % lokal CPU-belastning, 1–2 sekunder svartid.
2. **Fallback rute:** Lokal Ollama-server (`http://localhost:11434`) med `qwen2.5` eller `llama3.1`.
   - Benyttes dersom internett er utilgjengelig eller for 100 % air-gapped miljøer.

---

## 2. Kjernefunksjonalitet & Hybrid Driver

```python
import os
import json
from typing import Optional

def generate_llm_response(
    system_prompt: str, 
    user_prompt: str, 
    prefer_gemini: bool = True,
    temperature: float = 0.1
) -> str:
    """Hybrid LLM driver med automatisk fallback."""
    gemini_key = os.getenv("GEMINI_API_KEY")

    # 1. Forsøk Gemini 3.8 Flash dersom nøkkel finnes
    if prefer_gemini and gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=f"System: {system_prompt}\n\nBruker: {user_prompt}",
                config={"temperature": temperature}
            )
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Gemini API feilet ({e}), faller tilbake til lokal Ollama...")

    # 2. Fallback til lokal Ollama
    try:
        import ollama
        resp = ollama.chat(
            model=os.getenv("OLLAMA_MODEL", "qwen2.5:latest"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": temperature, "num_ctx": 8192}
        )
        return resp["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Både Gemini og Ollama feilet. Ollama feil: {e}")
```

---

## 3. Parametere & Konfigurasjon
* **Temperatur:** `0.0 – 0.1` for strenge juridiske og regnskapsmessige vurderinger.
* **Maks kontekst:** 8 192 / 16 384 tokens for omfattende KOSTRA-paragrafer og tertialrapporter.
* **PII-sjekk:** PII-scrubber (`PIIScrubber.sanitize`) må kalles før kall til eksterne API-er.
