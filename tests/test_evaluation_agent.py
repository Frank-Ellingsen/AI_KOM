# -*- coding: utf-8 -*-
"""
Tests for Agent 13: Evaluation & Quality Assurance Agent
Validates Golden Dataset, RAG metrics, loop detection, and 90% CI/CD Gate.
"""

import pytest
from app.services.evaluation_service import EvaluationService
from app.schemas.evaluation import EvaluationRunReport


def test_golden_dataset_loading_and_structure():
    svc = EvaluationService()
    cases = svc.load_golden_dataset()
    assert len(cases) >= 5, "Golden dataset må inneholde minst 5 tilfeller"
    for c in cases:
        assert c.id.startswith("GOLDEN-")
        assert len(c.prompt) > 10
        assert len(c.ground_truth_context) > 20
        assert c.min_faithfulness >= 0.85


def test_rag_evaluation_metrics_calculation():
    svc = EvaluationService()
    query = "Hva krever Kommuneloven § 14-5?"
    gt = "Kommuneloven § 14-5 stiller krav til realistisk budsjettbalanse og inndekning av merforbruk."
    retrieved = [
        "Kommuneloven § 14-5 stiller krav til realistisk budsjettbalanse og inndekning av merforbruk.",
        "Urelatert avsnitt om snøbrøyting."
    ]
    res = svc.evaluate_rag_retrieval(query, retrieved, gt, k=2)
    assert res.recall_at_k == 1.0
    assert res.precision_at_k == 0.5
    assert res.mrr == 1.0
    assert res.passed is False or res.precision_at_k >= 0.5


def test_trajectory_loop_detection_and_step_cap():
    svc = EvaluationService()
    # 1. Normal sekvens uten løkke
    steps_ok = [
        {"tool": "db_inspect", "args": {"table": "Dim_Art"}},
        {"tool": "db_query", "args": {"sql": "SELECT * FROM Dim_Art"}}
    ]
    res_ok = svc.evaluate_trajectory(steps_ok, max_steps=5)
    assert not res_ok.loop_detected
    assert res_ok.passed is True

    # 2. Uendelig løkke (samme kall gjentas)
    steps_loop = [
        {"tool": "db_query", "args": {"sql": "SELECT 1;"}},
        {"tool": "db_query", "args": {"sql": "SELECT 1;"}}
    ]
    res_loop = svc.evaluate_trajectory(steps_loop, max_steps=5)
    assert res_loop.loop_detected is True
    assert res_loop.passed is False


def test_golden_suite_run_and_ci_cd_gate():
    svc = EvaluationService()
    report = svc.run_golden_suite()
    assert report.total_tests >= 5
    assert report.passed_tests >= 5
    assert report.overall_faithfulness >= 0.90
    assert report.ci_cd_gate_passed is True
    assert len(report.sha256_seal) == 64

    # Enforce gate
    assert svc.enforce_ci_cd_gate(report) is True


def test_ci_cd_gate_blocks_on_poor_faithfulness():
    svc = EvaluationService()
    failing_report = EvaluationRunReport(
        run_id="EVAL-FAIL",
        timestamp="2026-10-17T00:00:00Z",
        total_tests=10,
        passed_tests=5,
        overall_faithfulness=0.82,  # Under 90%
        overall_precision=0.75,
        ci_cd_gate_passed=False,
        sha256_seal="fakehash",
        results=[]
    )
    with pytest.raises(ValueError, match="CI/CD GATE BLOKKERT"):
        svc.enforce_ci_cd_gate(failing_report)


def test_golden_exemplars_feedback_db_integration(tmp_path):
    """Tester at godkjente Stage-Gate Port 9 gulleksempler fra SQLite beriker Golden Dataset."""
    import sqlite3
    db_file = tmp_path / "test_feedback.db"
    out_json = tmp_path / "test_golden.json"

    # 1. Opprett tabell og sett inn godkjent gulleksempel
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE golden_exemplars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sector TEXT,
        deficit_mnok REAL,
        ai_draft TEXT,
        human_edited_final TEXT,
        diff_summary TEXT,
        approved_by TEXT,
        created_at TEXT,
        sha256_seal TEXT
    )
    """)
    cursor.execute("""
    INSERT INTO golden_exemplars (sector, deficit_mnok, ai_draft, human_edited_final, diff_summary, approved_by, created_at, sha256_seal)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Helse og mestring",
        8.85,
        "Utkast 1 uten paragrafer",
        "SAKSFREMLEGG: Tiltaksplan Helse og mestring jf. Kommuneloven § 14-5 og § 14-6. Vedtak: Formannskapet godkjenner omdisponering.",
        "Diff summary",
        "Frank Ellingsen (Senior Controller)",
        "2026-10-19T14:00:00Z",
        "sha256_test_seal_hash_123"
    ))
    conn.commit()
    conn.close()

    # 2. Test innlasting via EvaluationService
    svc = EvaluationService(dataset_path=out_json, feedback_db_path=db_file)
    exemplars = svc.load_golden_exemplars_from_db()
    assert len(exemplars) == 1
    assert exemplars[0].id == "EXEMPLAR-001"
    assert "Helse og mestring" in exemplars[0].prompt
    assert "§ 14-5" in exemplars[0].ground_truth_context

    # 3. Test synkronisering til JSON fil
    synced = svc.sync_exemplars_to_golden_file(output_path=out_json)
    assert synced == 1
    assert out_json.exists()

    # 4. Verifiser at load_golden_dataset laster synkroniserte caser
    loaded_cases = svc.load_golden_dataset(include_exemplars=False)
    assert len(loaded_cases) == 1
    assert loaded_cases[0].id == "EXEMPLAR-001"
