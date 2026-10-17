# M10 October Month-End Monitoring, Staging & Manual Ingestion Approval
**Kristiansand kommune — Control Office Hub (AI_KOM) / Antigravity Engine**

---

## 1. Month-End Arrival Monitoring Architecture

To detect when new month-ending financial reports (e.g., M10 October data) are produced by ERP/Visma and Framsikt, the Antigravity engine implements a dual detection strategy:

```
+-----------------------------------------------------------------------------------+
|                            SOURCE PRODUCTION EVENT                                |
|  Visma / Unit4 ERP / Framsikt completes M10 month-end closing (10th of November)   |
+-----------------------------------------------------------------------------------+
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
+------------------------------------+       +------------------------------------+
| OPTION A: Webhook Event Listener   |       | OPTION B: Automated File Watcher   |
| POST /api/v1/events/month-end      |       | Polls Azure Blob / SFTP / Shared   |
| Event: `month_close.completed`     |       | Pattern: `visma_m10_2026_*.csv`    |
+------------------------------------+       +------------------------------------+
                   │                                           │
                   └─────────────────────┬─────────────────────┘
                                         ▼
+-----------------------------------------------------------------------------------+
|                           STAGING & HOLDING QUEUE                                 |
|  Status: `STAGED_AWAITING_HUMAN_APPROVAL`                                         |
|  Notification: Banner on Portal & Teams Webhook ("M10 Files Produced & Ready")    |
|  Pipeline Action: PAUSED (No data ingested into vector DB or Power BI yet)        |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                    HUMAN-IN-THE-LOOP APPROVAL ("PUSH BUTTON")                     |
|  Controller pushes: [ 🚀 TRIGGER M10 INGESTION & PIPELINE ]                      |
|  API Call: `POST /api/v1/ingestion/m10/execute`                                   |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        EXECUTION & DATA PROCESSING                                |
|  1. SHA-256 Checksum Verification                                                 |
|  2. PII Scrubbing & KOSTRA Validation                                             |
|  3. Polars Aggregation & Power BI Model Refresh                                   |
|  4. Stage-Gate Port 9 Audit Stamping                                              |
+-----------------------------------------------------------------------------------+
```

---

## 2. API Specifications for Staging & Human Trigger

### A. Webhook / Event Detection Endpoint
```http
POST /api/v1/events/month-end
Content-Type: application/json

{
  "event": "month_end.files_produced",
  "periode": "2026-M10",
  "source_system": "Visma_ERP_Framsikt",
  "timestamp": "2026-11-10T06:00:00Z",
  "files": [
    {
      "filename": "M10_Oktober_2026_Regnskap_Fiktiv.csv",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "records_count": 10,
      "size_bytes": 1450
    }
  ]
}
```

**Response Status:** `202 Accepted`  
**Internal State Updated:** `M10_STATUS = STAGED_AWAITING_HUMAN_APPROVAL`

---

### B. Controller Portal "Push Button" Ingestion Trigger Endpoint
```http
POST /api/v1/ingestion/m10/execute
Content-Type: application/json
Authorization: Bearer <Controller_JWT_Token>

{
  "periode": "2026-M10",
  "approved_by": "frank.ellingsen@kristiansand.kommune.no",
  "role": "Senior_Controller",
  "run_options": {
    "scrub_pii": true,
    "validate_kostra": true,
    "rebuild_vector_rag": true,
    "notify_teams_channel": true
  }
}
```

**Response Status:** `200 OK`  
```json
{
  "status": "PROCESSING",
  "job_id": "job_m10_ingest_20261110_001",
  "message": "M10 Ingestion pipeline initiated successfully by Frank Ellingsen.",
  "sha256_audit_seal": "8f4e2a1b9c3d7e5f6a0b1c2d3e4f5a6b7c8d9e0f"
}
```

---

## 3. Fictive October (M10) Dataset Summary

The fictive October dataset (`M10_Oktober_2026_Regnskap_Fiktiv.csv`) reflects realistic municipal financial conditions in Kristiansand for October 2026:

| Virksomhetsområde | Enhetsnavn | KOSTRA Art & Navn | Budsjett YTD (NOK) | Regnskap YTD (NOK) | Avvik YTD (NOK) | Triage | Hovedårsak / Merknad |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Område 2 Oppvekst** | Vågsbygd Skole | 1020 Lønn vikarer | 3 200 000 | 4 850 000 | **+1 650 000** | 🔴 RØD | Høyt sykefravær og vikarbruk |
| **Område 2 Oppvekst** | Vågsbygd Skole | 1690 NAV Refusjon | -1 200 000 | -850 000 | **+350 000** | 🟡 GUL | Etterslep på NAV-refusjonskrav |
| **Område 3 Helse/Mestring** | Oddernes Omsorg | 1090 Overtid/ubekvem | 4 100 000 | 6 200 000 | **+2 100 000** | 🔴 RØD | Press på turnus og vakanser |
| **Område 5 By/Sted** | Kommunalteknikk | 1270 Snøbrøyting | 8 900 000 | 10 400 000 | **+1 500 000** | 🟡 GUL | Tidlig snøfall og vinterberedskap |
| **Område 5 By/Sted** | VAR Selvkost | 1620 Vanngebyrer | -35 000 000 | -35 200 000 | **-200 000** | 🟢 GRØNN | Selvkost i balanse |

---

## 4. UI Component for "Push Button" Ingestion Staging

```html
<!-- HTML/React Snippet for Control Hub Banner -->
<div class="staging-banner pending-approval">
  <div class="banner-icon">🔔</div>
  <div class="banner-content">
    <h4>M10 Oktober-data er produsert og ligger klar i Staging Queue</h4>
    <p>Fil: <code>M10_Oktober_2026_Regnskap_Fiktiv.csv</code> | Generert: 10. nov 2026 06:00 | Kilde: Visma ERP / Framsikt</p>
    <p class="status-badge">Status: AWAITING_HUMAN_TRIGGER</p>
  </div>
  <div class="banner-action">
    <button class="btn-trigger-ingest" onclick="triggerM10Ingestion()">
      🚀 PUSH BUTTON TO START M10 INGESTION
    </button>
  </div>
</div>
```

---

## 5. Instructions to Deploy File Package

1. Unzip `antigravity_m10_monthend_pack.zip`.
2. Move `M10_Oktober_2026_Regnskap_Fiktiv.csv` to your backend staging folder (`/backend/data/staging/`).
3. Commit `ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md` to your repository documentation.
4. Execute `POST /api/v1/ingestion/m10/execute` via Postman or the portal interface to trigger processing.
