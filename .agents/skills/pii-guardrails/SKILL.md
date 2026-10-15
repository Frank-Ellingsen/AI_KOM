---
name: pii-guardrails
description: >-
  Skjerming av personopplysninger (FNR, DNR, tlf +47, e-post) og SHA-256 revisjonslogging i samsvar med Stage-Gate Port 4 og Port 9.
---

# 🛠️ Agent Skill: PII Scrubbing & Guardrails (`pii-and-guardrails`)

> **Formål:** Skjerming av personopplysninger (PII), sikkerhetsvalidering og SHA-256 revisjonslogging i samsvar med Stage-Gate Port 4 (Datastyring) og Port 9 (Operativ Drift).

---

## 📋 Skill Spesifikasjon & Metadata

| Egenskap | Verdi |
| :--- | :--- |
| **Skill Name** | `pii-and-guardrails` |
| **Versjon** | `1.0.0` |
| **Standarder** | GDPR Art. 5/32, EU AI Act Art. 27 |

---

## ⚙️ Implementasjonsmønster i Python

```python
import re
import hashlib
import json

class PIIScrubber:
    PATTERNS = {
        'FNR_DNR': r'\b([0-3][0-9]|[4-7][0-9])(0[1-9]|1[0-2])\d{7}\b',
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'PHONE': r'\b(?:\+47[\s-]?)?(?:[49]\d{7}|(?:\d{2}[\s-]?){4})\b'
    }

    @classmethod
    def sanitize(cls, text: str) -> str:
        clean_text = text
        for p_type, pattern in cls.PATTERNS.items():
            clean_text = re.sub(pattern, f"[{p_type}_MASKED]", clean_text)
        return clean_text

def create_audit_hash(user_query: str, chunk_ids: list, response: str) -> str:
    payload = f"{user_query}|{json.dumps(chunk_ids)}|{response}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()
```
