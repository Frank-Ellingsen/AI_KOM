# Antigravity Triage Router Specification & Implementation
**Modul:** `app/core/triage_router.py`  
**System:** AI_KOM / Antigravity Backend Engine  
**Dato:** 17. oktober 2026  

---

## 1. Oversikt og Arkitektur

Triage Routeren fungerer som den sentrale **forespørselshåndtereren (Request Classifier & Router)** i Antigravity-backendet. Dens oppgave er å analysere innkommende brukerhenvendelser, kontekst og gjeldende persona, for deretter å rute oppgaven til den mest effektive og presise behandlingsmekanismen:

```
                          [ Brukerhenvendelse ]
                                    │
                                    ▼
                       [ Fast-Path Triage Router ]
                      (app/core/triage_router.py)
                                    │
      ┌─────────────────────┼─────────────────────┬─────────────────────┐
      ▼                     ▼                     ▼                     ▼
[ 1. Direct MCP ]    [ 2. RAG Lookup ]    [ 3. Skill Workflow ] [ 4. Memory Lookup ]
  - Visma / ERP        - Qdrant Vector      - Python Sandbox      - Session State
  - Framsikt API       - Legal / HØP Docs   - File Generators     - Active Persona
      │                     │                     │                     │
      └─────────────────────┼─────────────────────┴─────────────────────┘
                            │
                            ▼
              [ Orchestrated Response / Artifact ]
```

---

## 2. Pydantic Datamodeller (`app/schemas/triage.py`)

```python
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TriageCategory(str, Enum):
    DIRECT_MCP = "DIRECT_MCP"
    RAG_LOOKUP = "RAG_LOOKUP"
    SKILL_WORKFLOW = "SKILL_WORKFLOW"
    MEMORY_CONTEXT = "MEMORY_CONTEXT"
    HYBRID_COMPOSITE = "HYBRID_COMPOSITE"

class ExecutionPriority(str, Enum):
    HIGH_REALTIME = "HIGH_REALTIME"
    STANDARD = "STANDARD"
    BACKGROUND_BATCH = "BACKGROUND_BATCH"

class TriageRequest(BaseModel):
    prompt: str = Field(..., description="Innkommende tekst eller spørsmål fra brukeren")
    session_id: str = Field(..., description="Unik økt-ID fra Redis session store")
    user_persona: str = Field(default="ENHETSLEDER", description="Aktiv persona: ENHETSLEDER, CONTROLLER, TOPPLEDELSE")
    active_unit_id: Optional[str] = Field(None, description="Aktivert enhets-ID, f.eks. 120100 Vågsbygd skole")
    active_period: str = Field(default="M10_2026", description="Gjeldende regnskapsperiode")

class ToolTarget(BaseModel):
    tool_name: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class TriageDecision(BaseModel):
    primary_category: TriageCategory
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    priority: ExecutionPriority = ExecutionPriority.STANDARD
    required_mcp_connectors: List[str] = Field(default_factory=list)
    rag_search_filters: Dict[str, Any] = Field(default_factory=dict)
    skill_workflow_target: Optional[str] = None
    target_tools: List[ToolTarget] = Field(default_factory=list)
    reasoning_trace: str = Field(..., description="Forklaring på hvorfor denne ruten ble valgt")
    sha256_audit_hash: str = Field(..., description="Kryptografisk stempel for audit log")
```

---

## 3. Triage Router Kjerne Engine (`app/core/triage_router.py`)

```python
import re
import hashlib
import json
from typing import TriageDecision, TriageRequest, TriageCategory, ExecutionPriority, ToolTarget

class TriageRouter:
    def __init__(self, vector_store_client=None, redis_client=None):
        self.vector_store = vector_store_client
        self.redis = redis_client
        
        # Fast-Path Regex mønstre
        self.mcp_patterns = [
            re.compile(r"hent regnskap", re.IGNORECASE),
            re.compile(r"visma|framsikt|websak", re.IGNORECASE),
            re.compile(r"saldo|forbrakt|utgifter", re.IGNORECASE)
        ]
        self.rag_patterns = [
            re.compile(r"kommunelov|økonomireglement|forskrift|høp|hjemmel", re.IGNORECASE),
            re.compile(r"paragraf|§|selvkostforskrift", re.IGNORECASE)
        ]
        self.skill_patterns = [
            re.compile(r"ompostering|korreksjon|generer|lag excel|lag word|saksfremlegg|mva-test", re.IGNORECASE),
            re.compile(r"trigg|push button|run ingestion", re.IGNORECASE)
        ]

    def _generate_audit_hash(self, request: TriageRequest, category: str) -> str:
        raw_str = f"{request.session_id}:{request.prompt}:{category}:{request.active_period}"
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

    async def classify_and_route(self, request: TriageRequest) -> TriageDecision:
        prompt_text = request.prompt.strip()
        
        # 1. FAST-PATH RULE MATCHING (< 2ms execution)
        is_mcp = any(p.search(prompt_text) for p in self.mcp_patterns)
        is_rag = any(p.search(prompt_text) for p in self.rag_patterns)
        is_skill = any(p.search(prompt_text) for p in self.skill_patterns)

        if is_skill and (is_mcp or is_rag):
            category = TriageCategory.HYBRID_COMPOSITE
            reasoning = "Sammensatt henvendelse: Krever både datainnhenting, regelsoppslag og arbeidsflyt (Skill)."
            mcp_list = ["visma_erp", "framsikt_graphql"] if is_mcp else []
            rag_filters = {"jurisdiction": "Kristiansand", "document_type": "REGLEMENT"} if is_rag else {}
            skill_target = "ompostering_v2_workflow" if "ompostering" in prompt_text.lower() else "case_proposal_generator"
            
        elif is_skill:
            category = TriageCategory.SKILL_WORKFLOW
            reasoning = "Direkte flerstegs arbeidsflyt eller dokumentgenerering."
            mcp_list = []
            rag_filters = {}
            skill_target = "ompostering_v2_workflow" if "ompostering" in prompt_text.lower() else "generic_artifact_skill"

        elif is_rag:
            category = TriageCategory.RAG_LOOKUP
            reasoning = "Kunnskaps- eller lovoppslag forankret i juridisk kildemateriale."
            mcp_list = []
            rag_filters = {"jurisdiction": "Kristiansand", "tags": ["kommuneloven", "okonomireglement"]}
            skill_target = None

        elif is_mcp:
            category = TriageCategory.DIRECT_MCP
            reasoning = "Reelt sanntidsoppslag i kommunens fagsystemer (Visma / Framsikt)."
            mcp_list = ["visma_erp", "framsikt_graphql"]
            rag_filters = {}
            skill_target = None

        else:
            category = TriageCategory.MEMORY_CONTEXT
            reasoning = "Konversasjon og kontekstsoppslag fra pågående økt."
            mcp_list = []
            rag_filters = {}
            skill_target = None

        audit_hash = self._generate_audit_hash(request, category.value)

        return TriageDecision(
            primary_category=category,
            confidence_score=0.95,
            priority=ExecutionPriority.HIGH_REALTIME if is_mcp else ExecutionPriority.STANDARD,
            required_mcp_connectors=mcp_list,
            rag_search_filters=rag_filters,
            skill_workflow_target=skill_target,
            reasoning_trace=reasoning,
            sha256_audit_hash=audit_hash
        )
```

---

## 4. Testsuitedokumentasjon (`tests/test_triage_router.py`)

```python
import pytest
from app.schemas.triage import TriageRequest, TriageCategory
from app.core.triage_router import TriageRouter

@pytest.mark.asyncio
async def test_triage_ompostering_hybrid():
    router = TriageRouter()
    req = TriageRequest(
        prompt="Kjør ompostering for feilførte IT-lisenser på Vågsbygd skole og sjekk MVA-balansen.",
        session_id="test-session-123",
        user_persona="CONTROLLER",
        active_unit_id="120100"
    )
    decision = await router.classify_and_route(req)
    assert decision.primary_category in [TriageCategory.SKILL_WORKFLOW, TriageCategory.HYBRID_COMPOSITE]
    assert decision.sha256_audit_hash is not None
    assert len(decision.sha256_audit_hash) == 64

@pytest.mark.asyncio
async def test_triage_rag_legal_lookup():
    router = TriageRouter()
    req = TriageRequest(
        prompt="Hva sier Kommuneloven § 14-5 om overskridelse av årsbudsjett?",
        session_id="test-session-456",
        user_persona="ENHETSLEDER"
    )
    decision = await router.classify_and_route(req)
    assert decision.primary_category == TriageCategory.RAG_LOOKUP
    assert "kommuneloven" in decision.rag_search_filters["tags"]
```
