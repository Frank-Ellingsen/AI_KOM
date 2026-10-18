"""
Enhetstestsuite for MVP Helse og Mestring (Ansvar 5200)
Verifiserer:
1. Stage-Gate Port 4 PII-skjerming (FNR, D-nr, kontonummer, telefon +47, e-post)
2. DuckDB OLAP & ISO 21508 EVM-beregninger (PV, CV, periodisert Avvik_Pct, CPI, EAC, VAC)
3. Monte Carlo Q4-sesongprognoser (P10 <= P50 <= P90)
4. NAV-refusjonsgap (Art 1600) og Kommuneloven § 14-6 Bruttoprinsippet
5. Juridisk saksfremlegg (§ 14-5, § 14-6 og HTA § 4 / AML § 10-12)
6. Stage-Gate Port 9 & Port 10 SHA-256 revisorstempel og SQLite-persistens (APPROVED, MODIFIED, REJECTED)
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import (
    build_legal_recommendation,
    calculate_nav_refund_gap,
    generate_audit_seal,
    load_audit_history,
    load_helse_data,
    mask_pii,
    run_monte_carlo,
)


class TestHelseMestringMVP(unittest.TestCase):

    def test_port4_pii_masking_fnr_dnr_account_phone_email(self):
        raw_text = (
            "Saksbehandler Ola Nordmann, fnr 120588 12345, D-nr 52058812345, "
            "konto 1234.56.78901, tlf +47 987 65 432, epost: test@kristiansand.kommune.no"
        )
        masked = mask_pii(raw_text)
        self.assertNotIn("120588 12345", masked)
        self.assertNotIn("52058812345", masked)
        self.assertNotIn("1234.56.78901", masked)
        self.assertNotIn("987 65 432", masked)
        self.assertNotIn("test@kristiansand.kommune.no", masked)
        self.assertIn("[SKJERMET_FNR]", masked)
        self.assertIn("[SKJERMET_KONTO]", masked)
        self.assertIn("[SKJERMET_TLF]", masked)
        self.assertIn("[SKJERMET_EPOST]", masked)

    def test_duckdb_evm_and_periodized_variance_calculations(self):
        df = load_helse_data()
        self.assertEqual(len(df), 3)
        for _, row in df.iterrows():
            expected_ytd = round(row["Budsjett_MNOK"] * (8.0 / 12.0), 2)
            self.assertEqual(row["Forventet_YTD_MNOK"], expected_ytd)

            calculated_variance = round(expected_ytd - row["Regnskap_YTD_MNOK"], 2)
            self.assertEqual(row["Avvik_MNOK"], calculated_variance)

            # Verify Avvik_Pct is measured against periodized YTD budget (Forventet_YTD_MNOK)
            expected_pct = round((calculated_variance / expected_ytd) * 100.0, 2)
            self.assertEqual(row["Avvik_Pct"], expected_pct)

            # Verify ISO 21508 CPI and EAC
            expected_cpi = round(expected_ytd / row["Regnskap_YTD_MNOK"], 3)
            self.assertEqual(row["CPI"], expected_cpi)
            expected_eac = round(row["Budsjett_MNOK"] / expected_cpi, 2)
            self.assertEqual(row["EAC_MNOK"], expected_eac)

    def test_monte_carlo_projections(self):
        budget = 145.0
        ytd = 104.4
        p10, p50, p90 = run_monte_carlo(budget, ytd)

        self.assertLessEqual(p10, p50)
        self.assertLessEqual(p50, p90)
        self.assertGreater(p50, 130.0)
        self.assertLess(p50, 180.0)

    def test_nav_refund_gap_and_bruttoprinsippet(self):
        df = load_helse_data()
        row_254 = df[df["KOSTRA_Funksjon"] == 254].iloc[0]
        nav_info = calculate_nav_refund_gap(row_254)

        self.assertEqual(nav_info["actual_nav_mnok"], 5.20)
        self.assertEqual(nav_info["expected_nav_mnok"], 8.87)
        self.assertEqual(nav_info["refund_gap_mnok"], 3.67)
        self.assertTrue(nav_info["bruttoprinsipp_ok"])

    def test_legal_recommendation_includes_14_5_14_6_and_hta_4(self):
        df = load_helse_data()
        row_254 = df[df["KOSTRA_Funksjon"] == 254].iloc[0]
        _, p50, _ = run_monte_carlo(float(row_254["Budsjett_MNOK"]), float(row_254["Regnskap_YTD_MNOK"]))
        rec = build_legal_recommendation(row_254, p50)

        self.assertIn("Kommuneloven § 14-5", rec)
        self.assertIn("Kommuneloven § 14-6", rec)
        self.assertIn("HTA", rec)
        self.assertIn("AML", rec)

    def test_sha256_audit_seal_and_sqlite_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_db = Path(tmpdir) / "test_audit.db"
            user = "test.controller@kristiansand.kommune.no"
            funksjon = "254"
            rec = "TEST_RECOMMENDATION"
            note = "Kontakt fnr 120588 12345 kontrollert."

            for decision in ("APPROVED", "MODIFIED", "REJECTED"):
                audit = generate_audit_seal(
                    user, funksjon, rec, decision, user_note=note, db_path=tmp_db
                )
                self.assertIn("sha256_seal", audit)
                self.assertEqual(len(audit["sha256_seal"]), 64)
                self.assertEqual(audit["human_decision"], decision)
                self.assertNotIn("120588 12345", audit["user_note"])
                self.assertIn("[SKJERMET_FNR]", audit["user_note"])

            df_log = load_audit_history(limit=10, db_path=tmp_db)
            self.assertEqual(len(df_log), 3)
            self.assertEqual(set(df_log["Beslutning"].tolist()), {"APPROVED", "MODIFIED", "REJECTED"})


if __name__ == "__main__":
    unittest.main()
