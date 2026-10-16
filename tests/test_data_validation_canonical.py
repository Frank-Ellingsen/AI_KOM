"""
Unit & Integration Tests for Canonical Data Model & Pydantic Data Validation
=============================================================================
Kristiansand Kommune AI Hub — Single Source of Truth (SSOT) Verifikasjon
"""

from pathlib import Path
import pytest
import sqlite3
import re

from tools.data_quality_validator import DataQualityValidator
from erp_data.canonical_models import (
    KontoklasseCanonical,
    FunksjonCanonical,
    ArtCanonical,
    AnsvarCanonical,
    DatoCanonical,
    BudsjettansvarligCanonical,
    ErpTransactionStaging,
    FactRegnskapCanonical,
    FactBudsjettCanonical,
    AuditAiActionCanonical,
    FactPrognoseLoggCanonical,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "erp_data" / "kommune_golden_record.db"


@pytest.fixture(scope="module")
def validator():
    v = DataQualityValidator(DB_PATH)
    v.connect()
    yield v
    v.close()


def test_validator_master_run(validator):
    """Kjører alle 6 valideringssuiter og forventer 100 % suksess."""
    all_ok = validator.run_all()
    assert all_ok is True, f"Data Quality Validation feilet: {validator.results['failed_suites']} suiter med feil"
    assert validator.results["passed_suites"] == 6


def test_pydantic_contracts_coverage(validator):
    """Validerer at alle 11 tabeller har 100 % samsvar mot sine Pydantic v2-kontrakter."""
    ok = validator.validate_pydantic_contracts()
    assert ok is True
    stats = validator.results["suite_details"]["Suite 1: Pydantic v2 Canonical Data Contracts"]["stats"]
    for tbl, s in stats.items():
        assert s["invalid_rows"] == 0, f"Ugyldige rader funnet i {tbl}: {s['invalid_rows']}"
        assert s["compliance_rate"] == "100.0%", f"{tbl} har lavere compliance enn 100%: {s['compliance_rate']}"


def test_zero_orphaned_foreign_keys(validator):
    """Tester Star Schema referensiell integritet (0 foreldreløse fremmednøkler)."""
    ok = validator.validate_referential_integrity()
    assert ok is True
    fk_checks = validator.results["suite_details"]["Suite 2: Star Schema Referential Integrity (Zero Orphans)"]["foreign_key_checks"]
    for name, res in fk_checks.items():
        assert res["orphan_count"] == 0, f"Orphans funnet i {name}: {res['orphan_count']}"
        assert res["status"] == "PASS"


def test_pii_guardrails_port_4(validator):
    """Verifiserer at ingen 11-sifrede fødselsnumre eller personopplysninger lekker inn i staging."""
    ok = validator.validate_pii_security()
    assert ok is True
    assert validator.results["suite_details"]["Suite 3: PII Security & GDPR Art. 5 (Stage-Gate Port 4)"]["violations_detected"] == 0


def test_financial_governance_rules(validator):
    """Verifiserer Kommuneloven § 14-5 (budsjettbalanse) og Monte Carlo orden P10 <= P50 <= P90."""
    ok = validator.validate_financial_governance()
    assert ok is True
    assert validator.results["suite_details"]["Suite 4: Statutory & Financial Governance (§ 14-5, § 14-6, EVM)"]["findings_count"] == 0


def test_cryptographic_audit_trail_port_9(validator):
    """Verifiserer SHA-256 forsegling og Human-in-the-Loop saksbehandlingsvedtak."""
    ok = validator.validate_audit_trail_integrity()
    assert ok is True
    details = validator.results["suite_details"]["Suite 5: Stage-Gate Port 9 HITL Cryptographic Audit Verification"]["details"]
    assert details["Fact_Prognose_Logg"]["status"] == "PASS"
    assert details["Audit_AI_Actions"]["status"] == "PASS"
    assert details["Fact_Prognose_Logg"]["total_records"] > 0
    assert details["Audit_AI_Actions"]["total_records"] > 0


def test_multi_tier_reconciliation(validator):
    """Verifiserer at sum og radantall stemmer eksakt mellom SQLite Golden Record og DuckDB Parquet."""
    ok = validator.validate_multi_tier_reconciliation()
    assert ok is True
    rec = validator.results["reconciliation"]
    sq = rec["SQLite_Golden_Record"]
    dk = rec["DuckDB_Parquet"]
    assert sq["regnskap_rows"] == dk["regnskap_rows"]
    assert sq["budsjett_rows"] == dk["budsjett_rows"]
    assert abs(sq["regnskap_sum_nok"] - dk["regnskap_sum_nok"]) < 0.01
    assert abs(sq["budsjett_sum_nok"] - dk["budsjett_sum_nok"]) < 0.01
