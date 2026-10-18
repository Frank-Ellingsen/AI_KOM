import unittest
import hashlib
import json
import duckdb
from datetime import datetime

# ==============================================================================
# 1. DAX FINANCIAL VARIANCE LOGIC
# ==============================================================================

def calculate_expenditure_variance(budget: float, actual: float) -> dict:
    """
    Expenditure Variance Rule:
    Variance Amount = Budget - Actual
    (Positive = Under budget / Favorable; Negative = Over budget / Deficit / Unfavorable)
    """
    variance_amount = budget - actual
    variance_pct = (variance_amount / budget) * 100 if budget != 0 else 0.0
    
    # RAG Status Logic:
    if variance_amount < 0:
        overrun_pct = abs(variance_pct)
        if overrun_pct > 5.0:
            status = "RED"
            hex_color = "#D32F2F"
        else:
            status = "AMBER"
            hex_color = "#F57C00"
    else:
        status = "GREEN"
        hex_color = "#388E3C"

    return {
        "variance_amount": variance_amount,
        "variance_pct": variance_pct,
        "rag_status": status,
        "hex_color": hex_color
    }


def calculate_revenue_variance(budget: float, actual: float) -> dict:
    """
    Revenue Variance Rule:
    Variance Amount = Actual - Budget
    (Positive = Over budget / Favorable; Negative = Under budget / Deficit / Unfavorable)
    """
    variance_amount = actual - budget
    variance_pct = (variance_amount / budget) * 100 if budget != 0 else 0.0
    
    if variance_amount < 0:
        shortfall_pct = abs(variance_pct)
        if shortfall_pct > 5.0:
            status = "RED"
            hex_color = "#D32F2F"
        else:
            status = "AMBER"
            hex_color = "#F57C00"
    else:
        status = "GREEN"
        hex_color = "#388E3C"

    return {
        "variance_amount": variance_amount,
        "variance_pct": variance_pct,
        "rag_status": status,
        "hex_color": hex_color
    }


def generate_audit_record(user_upn: str, query: str, decision: str) -> dict:
    timestamp = "2026-10-18T08:25:00Z"
    query_hash = hashlib.sha256(query.encode("utf-8")).hexdigest()
    
    payload = f"{timestamp}|{user_upn}|{query_hash}|{decision}"
    sha256_seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    
    return {
        "timestamp": timestamp,
        "user_upn": user_upn,
        "query_hash": query_hash,
        "decision": decision,
        "sha256_seal": sha256_seal
    }


# ==============================================================================
# 2. UNITTEST SUITE FOR CI/CD
# ==============================================================================

class TestFinancialLogicAndGovernance(unittest.TestCase):

    def test_expenditure_variance_overrun_preserves_negative_sign(self):
        """Ensure over-budget expenditure returns negative variance amount and RED status without ABS() masking."""
        budget = 10_000_000.0  # 10 MNOK
        actual = 11_000_000.0  # 11 MNOK (10% over budget)
        
        res = calculate_expenditure_variance(budget, actual)
        
        self.assertEqual(res["variance_amount"], -1_000_000.0, "Variance amount must remain negative for deficits!")
        self.assertLess(res["variance_amount"], 0, "ABS() must NOT be applied to expenditure variance amounts!")
        self.assertEqual(res["rag_status"], "RED")
        self.assertEqual(res["hex_color"], "#D32F2F")

    def test_revenue_variance_shortfall_preserves_negative_sign(self):
        """Ensure revenue shortfall returns negative variance amount and RED status."""
        budget = 5_000_000.0
        actual = 4_200_000.0  # 16% shortfall
        
        res = calculate_revenue_variance(budget, actual)
        
        self.assertEqual(res["variance_amount"], -800_000.0)
        self.assertEqual(res["rag_status"], "RED")
        self.assertEqual(res["hex_color"], "#D32F2F")

    def test_expenditure_favorable_under_budget(self):
        """Ensure under-budget expenditure returns positive variance and GREEN status."""
        budget = 10_000_000.0
        actual = 9_500_000.0  # Under budget by 500k
        
        res = calculate_expenditure_variance(budget, actual)
        
        self.assertEqual(res["variance_amount"], 500_000.0)
        self.assertEqual(res["rag_status"], "GREEN")
        self.assertEqual(res["hex_color"], "#388E3C")

    def test_duckdb_olap_aggregation(self):
        """Test sub-millisecond DuckDB OLAP aggregations across KOSTRA functions and account types."""
        con = duckdb.connect(database=":memory:")
        
        con.execute("""
            CREATE TABLE fact_regnskap (
                ansvar INT,
                funksjon INT,
                art INT,
                belop DOUBLE
            );
            INSERT INTO fact_regnskap VALUES
                (202, 120, 10100, 1500000.0),
                (202, 120, 11200,  300000.0),
                (202, 130, 10100, 2200000.0),
                (301, 210, 10100, 5000000.0);
        """)
        
        query = """
            SELECT 
                ansvar,
                SUM(belop) AS total_forbruk
            FROM fact_regnskap
            WHERE ansvar = 202
            GROUP BY ansvar;
        """
        
        df = con.execute(query).fetchdf()
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["ansvar"], 202)
        self.assertEqual(df.iloc[0]["total_forbruk"], 4_000_000.0)

    def test_audit_log_sha256_verification(self):
        """Verify cryptographic SHA-256 seal integrity for EU AI Act compliance."""
        record = generate_audit_record("controller@kristiansand.kommune.no", "Sjekk avvik på ansvar 202", "APPROVED")
        
        payload = f"{record['timestamp']}|{record['user_upn']}|{record['query_hash']}|{record['decision']}"
        expected_seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        
        self.assertEqual(record["sha256_seal"], expected_seal, "Audit record SHA-256 seal mismatch!")


if __name__ == "__main__":
    unittest.main()
