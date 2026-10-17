# -*- coding: utf-8 -*-
"""
Tests for Agent 15: AI Engineering & Infrastructure Agent
Validates 4-layer architecture status, context compaction, semantic cache,
and latency benchmarking.
"""

from app.services.ai_engineering_service import AIEngineeringService, SemanticCache
from app.schemas.ai_engineering import ContextCompactionRequest


def test_4_layer_architecture_status():
    svc = AIEngineeringService()
    status = svc.get_4_layer_status()
    assert "primary" in status.model_layer
    assert "Gemini" in status.model_layer["primary"]
    assert "Ollama" in status.model_layer["fallback"]
    assert status.harness_layer["max_steps"] == 10
    assert status.framework_layer["agents_count"] == 15
    assert "Stage-Gate" in status.platform_layer["governance"]


def test_context_compaction_preserves_statutes():
    svc = AIEngineeringService()
    raw = """
    Kommuneloven § 14-5 krever at årsbudsjettet er i balanse.
    
    
    Det stilles også krav til bruttoprinsippet jf. § 14-6.
    
    Mange tomme linjer og padding.
    """
    req = ContextCompactionRequest(raw_context=raw, max_tokens=500, preserve_statutory_refs=True)
    res = svc.compact_context(req)
    assert res.compacted_chars < res.original_chars
    assert res.compression_ratio < 1.0
    assert any("14-5" in s for s in res.extracted_statutes)
    assert any("14-6" in s for s in res.extracted_statutes)


def test_semantic_cache_hits_and_cost_savings():
    cache = SemanticCache(max_entries=10)
    query = "Hva krever § 14-5 om budsjettbalanse?"
    response = "Årsbudsjettet skal være realistisk og i balanse."

    # First access: Miss
    assert cache.get(query) is None
    assert cache.misses == 1

    # Store
    cache.set(query, response, tokens=200)

    # Second access: Hit
    cached_val = cache.get(query)
    assert cached_val == response
    assert cache.hits == 1

    stats = cache.get_stats()
    assert stats.total_entries == 1
    assert stats.hit_rate_pct == 50.0
    assert stats.saved_tokens == 200
    assert stats.estimated_cost_saved_nok > 0.0


def test_latency_benchmark():
    svc = AIEngineeringService()
    bench = svc.benchmark_latency("Gemini-3.8-Flash")
    assert bench.time_to_first_token_ms > 0.0
    assert bench.total_latency_ms >= bench.time_to_first_token_ms
    assert bench.tokens_generated > 0
    assert bench.tokens_per_second > 0.0
    assert bench.token_cost_nok >= 0.0
