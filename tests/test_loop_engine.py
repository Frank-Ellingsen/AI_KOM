# -*- coding: utf-8 -*-
"""
Master Test Suite: Loop Engineering & Evaluator-Optimizer Engine (Lag 4)
Tester kvalitetsportene (§ 14-5, § 14-6, GDPR Port 4, Vedtaksstruktur) og SHA-256 revisjonssegl.
"""

import pytest
from tools.loop_engine import LoopEngine, mask_pii_text, EvaluatorReport


def test_pii_masking():
    raw_text = "Saksbehandler Ola Nordmann (12058812345, ola@kristiansand.kommune.no) konto 1234.56.78901."
    masked = mask_pii_text(raw_text)
    assert "12058812345" not in masked
    assert "[SKJERMET_FNR]" in masked
    assert "1234.56.78901" not in masked
    assert "[SKJERMET_KONTO]" in masked
    assert "ola@kristiansand.kommune.no" not in masked
    assert "[SKJERMET_EPOST]" in masked


def test_evaluator_flags_missing_gates():
    engine = LoopEngine()
    bad_draft = "Dette er et notat uten paragrafer, uten vedtak og med konto 1234.56.78901."
    report = engine.evaluate_draft(bad_draft)
    assert not report.passed
    assert not report.gate_1_14_5
    assert not report.gate_2_14_6
    assert not report.gate_3_gdpr
    assert not report.gate_4_vedtak
    assert len(report.feedback) == 4


def test_evaluator_passes_compliant_draft():
    engine = LoopEngine()
    compliant_draft = """
    SAKSFREMLEGG: Tiltak for Helse og Mestring
    I henhold til Kommuneloven § 14-5 fremmes sak om budsjettbalanse.
    I henhold til Kommuneloven § 14-6 budsjetteres inntekter og utgifter brutto.
    Kontakt: [SKJERMET_KONTO]
    
    Forslag til Vedtak:
    1. Formannskapet godkjenner omdisponering.
    """
    report = engine.evaluate_draft(compliant_draft)
    assert report.passed
    assert report.gate_1_14_5
    assert report.gate_2_14_6
    assert report.gate_3_gdpr
    assert report.gate_4_vedtak
    assert len(report.feedback) == 0


def test_loop_engine_approval_and_sha256_seal():
    engine = LoopEngine(max_attempts=3)
    res = engine.run_loop(sector="Helse og mestring", deficit_mnok=8.85, unit_name="5200 - Sykehjem")
    assert res["status"] == "APPROVED"
    assert res["iterations_required"] == 2
    assert "sha256_audit_seal" in res
    assert len(res["sha256_audit_seal"]) == 64
    assert res["quality_gates"]["port_1_14_5"] == "PASSED"
    assert res["quality_gates"]["port_2_14_6"] == "PASSED"
    assert res["quality_gates"]["port_3_gdpr"] == "PASSED"
    assert res["quality_gates"]["port_4_vedtak"] == "PASSED"
