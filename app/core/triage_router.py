"""
Kristiansand Kommune AI Hub — Fast-Path Triage Router
Klassifiserings- og ruteringsmotor for innkommende henvendelser.
Ruter mellom Direct MCP, RAG Lookup, Skill Workflow og Memory Context.
"""

import re
import hashlib
import json
import asyncio
from typing import Optional

from app.schemas.triage import (
    TriageRequest,
    TriageDecision,
    TriageCategory,
    ExecutionPriority,
    ToolTarget,
)


class TriageRouter:
    """
    Fast-path triage router som klassifiserer brukerhenvendelser på under 2ms
    og ruter til optimal utførelseskanal med SHA-256 revisjonsstempel.
    """

    def __init__(self, vector_store_client=None, redis_client=None):
        self.vector_store = vector_store_client
        self.redis = redis_client

        # Fast-Path Regex mønstre
        self.mcp_patterns = [
            re.compile(r"hent regnskap", re.IGNORECASE),
            re.compile(r"visma|framsikt|websak", re.IGNORECASE),
            re.compile(r"saldo|forbrakt|utgifter", re.IGNORECASE),
            re.compile(r"hovedbok|bilagsjournal", re.IGNORECASE),
        ]
        self.rag_patterns = [
            re.compile(r"kommunelov|økonomireglement|forskrift|høp|hjemmel", re.IGNORECASE),
            re.compile(r"paragraf|§|selvkostforskrift", re.IGNORECASE),
            re.compile(r"arbeidsmiljølov|hta|hovedtariffavtale", re.IGNORECASE),
        ]
        self.skill_patterns = [
            re.compile(r"ompostering|korreksjon|generer|lag excel|lag word|saksfremlegg|mva-test|mva-balanse", re.IGNORECASE),
            re.compile(r"trigg|push button|run ingestion|ingester", re.IGNORECASE),
            re.compile(r"prognose|monte carlo|p10|p50|p90|eac", re.IGNORECASE),
        ]

    def _generate_audit_hash(self, request: TriageRequest, category: str) -> str:
        raw_str = f"{request.session_id}:{request.prompt}:{category}:{request.active_period}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    async def classify_and_route(self, request: TriageRequest) -> TriageDecision:
        """Klassifiserer og ruter henvendelsen asynkront."""
        return self._classify_internal(request)

    def classify_and_route_sync(self, request: TriageRequest) -> TriageDecision:
        """Synkron versjon av klassifiseringsmotoren."""
        return self._classify_internal(request)

    def _classify_internal(self, request: TriageRequest) -> TriageDecision:
        prompt_text = request.prompt.strip()

        # 1. FAST-PATH RULE MATCHING (< 2ms execution)
        is_mcp = any(p.search(prompt_text) for p in self.mcp_patterns)
        is_rag = any(p.search(prompt_text) for p in self.rag_patterns)
        is_skill = any(p.search(prompt_text) for p in self.skill_patterns)

        tools = []

        if is_skill and (is_mcp or is_rag):
            category = TriageCategory.HYBRID_COMPOSITE
            reasoning = "Sammensatt henvendelse: Krever både datainnhenting, regelsoppslag og automatisert arbeidsflyt (Skill)."
            mcp_list = ["visma_erp", "framsikt_graphql"] if is_mcp else []
            rag_filters = {"jurisdiction": "Kristiansand", "document_type": "REGLEMENT"} if is_rag else {}
            if "ompostering" in prompt_text.lower():
                skill_target = "ompostering_v2_workflow"
                tools.append(ToolTarget(tool_name="ompostering_engine", action="validate_and_repost"))
            elif "mva" in prompt_text.lower():
                skill_target = "mva_balanse_validator"
                tools.append(ToolTarget(tool_name="test_mva_balanse_2130", action="verify_konto_2130"))
            else:
                skill_target = "case_proposal_generator"
                tools.append(ToolTarget(tool_name="saksfremlegg_generator", action="generate_note"))

        elif is_skill:
            category = TriageCategory.SKILL_WORKFLOW
            reasoning = "Direkte flerstegs arbeidsflyt eller dokumentgenerering i henhold til kommunale maler."
            mcp_list = []
            rag_filters = {}
            if "ompostering" in prompt_text.lower():
                skill_target = "ompostering_v2_workflow"
            elif "mva" in prompt_text.lower():
                skill_target = "mva_balanse_validator"
            elif "prognose" in prompt_text.lower() or "eac" in prompt_text.lower():
                skill_target = "predictive_forecasting_engine"
            elif "ingestion" in prompt_text.lower() or "push button" in prompt_text.lower():
                skill_target = "m10_ingestion_runner"
            else:
                skill_target = "generic_artifact_skill"

        elif is_rag:
            category = TriageCategory.RAG_LOOKUP
            reasoning = "Kunnskaps- eller lovoppslag forankret i juridisk kildemateriale (Kommuneloven / Økonomireglementet)."
            mcp_list = []
            tags = ["okonomireglement"]
            if "kommunelov" in prompt_text.lower() or "§" in prompt_text:
                tags.append("kommuneloven")
            if "arbeidsmiljølov" in prompt_text.lower() or "hta" in prompt_text.lower():
                tags.append("hta_aml")
            rag_filters = {"jurisdiction": "Kristiansand", "tags": tags}
            skill_target = None

        elif is_mcp:
            category = TriageCategory.DIRECT_MCP
            reasoning = "Reelt sanntidsoppslag i kommunens fagsystemer (Visma ERP / Framsikt EPM)."
            mcp_list = ["visma_erp", "framsikt_graphql"]
            rag_filters = {}
            skill_target = None

        else:
            category = TriageCategory.MEMORY_CONTEXT
            reasoning = "Konversasjon og kontekstsoppslag fra pågående økt og aktiv persona."
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
            target_tools=tools,
            reasoning_trace=reasoning,
            sha256_audit_hash=audit_hash,
        )
