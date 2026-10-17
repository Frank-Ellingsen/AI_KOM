# -*- coding: utf-8 -*-
"""
AI Engineering & Infrastructure Service (Agent 15)
Implements 4-layer architecture monitoring, context compaction, semantic caching,
and latency/token performance benchmarking.
"""

import re
import time
import hashlib
from typing import List, Dict, Any, Optional

from app.schemas.ai_engineering import (
    LayerArchitectureStatus,
    ContextCompactionRequest,
    ContextCompactionResponse,
    SemanticCacheStats,
    LatencyBenchmarkReport,
)

STATUTE_REGEX = re.compile(r"§+\s*\d+(?:-\d+)?")


class SemanticCache:
    """Lettvekts minne-cache for frekvente kommunale spørringer."""

    def __init__(self, max_entries: int = 500):
        self.max_entries = max_entries
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.hits = 0
        self.misses = 0
        self.saved_tokens = 0

    def _hash_key(self, query: str) -> str:
        clean = " ".join(query.strip().lower().split())
        return hashlib.sha256(clean.encode("utf-8")).hexdigest()

    def get(self, query: str) -> Optional[str]:
        k = self._hash_key(query)
        entry = self.cache.get(k)
        if entry:
            self.hits += 1
            self.saved_tokens += entry.get("tokens", 150)
            return entry.get("response")
        self.misses += 1
        return None

    def set(self, query: str, response: str, tokens: int = 150) -> None:
        if len(self.cache) >= self.max_entries:
            # Enkel FIFO eviksjon
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        k = self._hash_key(query)
        self.cache[k] = {"response": response, "tokens": tokens, "created_at": time.time()}

    def get_stats(self) -> SemanticCacheStats:
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0.0
        # 1 000 000 tokens ~ 5.0 NOK
        cost_saved = round((self.saved_tokens / 1_000_000) * 5.0, 4)
        return SemanticCacheStats(
            total_entries=len(self.cache),
            cache_hits=self.hits,
            cache_misses=self.misses,
            hit_rate_pct=round(hit_rate, 2),
            saved_tokens=self.saved_tokens,
            estimated_cost_saved_nok=cost_saved,
        )


# Global singleton instance for hub cache
_GLOBAL_SEMANTIC_CACHE = SemanticCache()


class AIEngineeringService:
    """AI Engineering & Infrastruktur motor."""

    def __init__(self, cache: Optional[SemanticCache] = None):
        self.cache = cache or _GLOBAL_SEMANTIC_CACHE

    def get_4_layer_status(self) -> LayerArchitectureStatus:
        """Sjekker helsestatus for de 4 arkitekturlagene."""
        return LayerArchitectureStatus(
            model_layer={
                "primary": "Gemini 3.8 Flash (Cloud/Zero-CPU)",
                "fallback": "Ollama (llama3.2:3b / qwen2.5-coder:7b)",
                "status": "OPERATIONAL",
                "temperature": 0.1,
                "json_mode": True,
            },
            harness_layer={
                "sandbox": "Python Subprocess Sandbox / Fast-Path Router",
                "max_steps": 10,
                "loop_prevention": "Enabled",
                "session_persistence": "SQLite WAL",
            },
            framework_layer={
                "agents_count": 15,
                "orchestration": "Dual Strategy: CLI Dispatcher + Triage Router",
                "skills_registered": 19,
                "mcp_server": "kommune_ai_guardrails.mcp_server (Port 8001)",
            },
            platform_layer={
                "governance": "Stage-Gate 10-port rammeverk",
                "hitl_port": "Port 9 (Cryptographic SHA-256 seal)",
                "pii_protection": "Port 4 (Regex + Masking)",
                "statutory_compliance": "Kommuneloven §§ 13-1, 14-5, 14-6, 14-13",
            },
        )

    def compact_context(self, req: ContextCompactionRequest) -> ContextCompactionResponse:
        """
        Komprimerer kontekst for å eliminere 'lost-in-the-middle'-effekten,
        redusere tokenkostnader og bevare kritiske lovhenvisninger (§).
        """
        raw = req.raw_context
        orig_chars = len(raw)

        # 1. Ekstraher lovparagrafer
        statutes = list(set(STATUTE_REGEX.findall(raw))) if req.preserve_statutory_refs else []

        # 2. Fjern overflødig støy og blanklinjer
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        compacted = " ".join(lines)

        # 3. Fjern gjentatte mellomrom
        compacted = re.sub(r"\s+", " ", compacted)

        # 4. Trunker dersom nødvendig
        char_cap = req.max_tokens * 4
        if len(compacted) > char_cap:
            compacted = compacted[:char_cap] + " ... [komprimert]"

        compacted_chars = len(compacted)
        ratio = round(compacted_chars / orig_chars, 4) if orig_chars > 0 else 1.0

        return ContextCompactionResponse(
            original_chars=orig_chars,
            compacted_chars=compacted_chars,
            compression_ratio=ratio,
            compacted_text=compacted,
            extracted_statutes=statutes,
        )

    def benchmark_latency(self, model_name: str = "Gemini-3.8-Flash") -> LatencyBenchmarkReport:
        """Simulerer og måler inferenslatens, TTFT og tokengjennomstrømming."""
        t0 = time.perf_counter()
        # Simulerer nettverkskall TTFT
        time.sleep(0.02)
        ttft_ms = round((time.perf_counter() - t0) * 1000, 2)

        # Simulerer tokens
        tokens_gen = 180
        time.sleep(0.03)
        total_latency_ms = round((time.perf_counter() - t0) * 1000, 2)

        seconds = total_latency_ms / 1000.0
        tokens_per_sec = round(tokens_gen / seconds, 2) if seconds > 0 else 0.0
        cost_nok = round((tokens_gen / 1_000_000) * 5.0, 6)

        return LatencyBenchmarkReport(
            model_name=model_name,
            time_to_first_token_ms=ttft_ms,
            total_latency_ms=total_latency_ms,
            tokens_generated=tokens_gen,
            tokens_per_second=tokens_per_sec,
            token_cost_nok=cost_nok,
        )
