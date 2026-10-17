# Antigravity Backend — API Specification & Deployment Guide
**Project:** AI_KOM (Kristiansand Kommune — Control Office Hub)  
**Module:** Antigravity API & DevOps (`/api/v1` & `/deploy`)  

---

## 1. REST API Endpoints Overview (`/api/v1`)

Antigravity exposes a RESTful OpenAPI 3.1 interface protected by OAuth2 Bearer tokens.

### 1.1 Financial & Budget Endpoints (`/api/v1/finance`)

| Method | Endpoint | Description | Auth Scope |
| :--- | :--- | :--- | :--- |
| `GET` | `/finance/overview` | Fetches municipal high-level financial health (Netto driftsresultat, Disposisjonsfond, Lånetak) | `read:finance` |
| `GET` | `/finance/units/{unit_id}/m9` | Fetches Month 9 YTD actuals, budget, and variance for a specific unit | `read:unit` |
| `POST` | `/finance/selvkost/calculate` | Runs 5-year selvkost calculation for VAR / Building permits | `calc:selvkost` |
| `POST` | `/finance/payroll/simulate` | Simulates impact of staffing/absence changes on salary accounts (Art 1010-1090) | `write:payroll` |

### 1.2 RAG & AI Endpoints (`/api/v1/ai`)

| Method | Endpoint | Description | Auth Scope |
| :--- | :--- | :--- | :--- |
| `POST` | `/ai/variance-note/generate` | Generates a 4-point variance explanation note grounded in Visma data | `write:reports` |
| `POST` | `/ai/rag/query` | Queries municipal statutes, Økonomireglement, and HØP vector store | `read:rag` |
| `GET` | `/ai/audit/verify/{hash}` | Verifies SHA-256 audit signature of a generated document | `read:audit` |

### 1.3 Stage-Gate Port 9 Endpoints (`/api/v1/governance`)

| Method | Endpoint | Description | Auth Scope |
| :--- | :--- | :--- | :--- |
| `POST` | `/governance/port9/sign` | Controller sign-off (APPROVED/REJECTED) with SHA-256 cryptographic stamp | `admin:controller` |
| `GET` | `/governance/port9/logs` | Fetches audit log history for Kommunerevisjonen | `read:audit` |

---

## 2. OpenAPI Payload Examples

### Request: Generate Variance Note (`POST /api/v1/ai/variance-note/generate`)

```json
{
  "unit_id": "2020_Grunnskole_Sentrum",
  "period": "2026M09",
  "variance_threshold_nok": 100000,
  "include_action_plan": true,
  "language": "no"
}
```

### Response:

```json
{
  "unit_id": "2020_Grunnskole_Sentrum",
  "period": "2026M09",
  "status": "DRAFT_GENERATED",
  "summary": "Enheten har et merforbruk på 1,42 mill. kr per M9, hovedsakelig knyttet til vikarbruk ved sykefravær (Art 1020) [1].",
  "points": [
    "1. Regnskapsstatus: Høyere vikarkostnader enn budsjettert (Art 1020) sammmenholdt med HTA-tillegg [1].",
    "2. Årsaksanalyse: Sykelønnsrefusjoner fra NAV (Art 1690) har et etterslep på 60 dager [2].",
    "3. Prognose ut året: Forventet årsavvik på -1,1 mill. kr hvis tiltak ikke iverksettes [1].",
    "4. Korrigerende tiltak: Ansettelsesstopp videreføres og vikarinnleie strammes inn [3]."
  ],
  "sources_cited": [
    {"id": 1, "title": "Visma GL M9 Extract - Unit 2020"},
    {"id": 2, "title": "NAV Refusjonsregister Q3"},
    {"id": 3, "title": "Kristiansand Kommune Ansettelsesretningslinjer 2026"}
  ],
  "sha256_hash": "a4523fff19ea44bc88f95882936f75afa4523fff19ea44bc88f95882936f75af"
}
```

---

## 3. Production Deployment Specification (Docker & Kubernetes)

### Production `Dockerfile`:

```dockerfile
FROM python:3.12-slim as base

ENV PYTHONUNBUFFERED=1     PYTHONDONTWRITEBYTECODE=1     PIP_NO_CACHE_DIR=off     PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential curl libpq-dev     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### GitHub Actions CI/CD Pipeline (`.github/workflows/deploy-backend.yml`):
* **Step 1:** Run `pytest` and `flake8` linting.
* **Step 2:** Build multi-arch Docker image.
* **Step 3:** Push to Azure Container Registry (ACR) / Private Registry.
* **Step 4:** Deploy to Kubernetes / Azure App Service with zero-downtime rolling update.
