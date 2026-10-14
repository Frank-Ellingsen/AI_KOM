# Power BI Enterprise Architecture, Fabric & AI Copilot Integration

## 1. Datakilder og DirectQuery vs. Import Mode
- **Import Mode:** Benyttes for `Fact_Regnskap` og historiske data for maksimal DAX-ytelse og avansert RLS.
- **DirectQuery / Fabric Direct Lake:** Benyttes for live avvikssoek i Visma ERP transaksjonstabeller.

## 2. Microsoft Fabric & Copilot Integration
- Integration med Copilot i Power BI for å generere DAX-utkast og automatiske avvikssammendrag.
- Syntese av AI Insights direkte inn i Streamlit / Office Hub.

## 3. Governance, RLS & Deployment Pipeline
- Dev -> Test -> Prod deployment pipelines i Power BI Service.
- Algoritmeregistering og EU AI Act samsvar for AI-visuals.
