"""
Enhetstestsuite for MVP Helse og Mestring
Verifiserer PII-skjerming, DAX-beregninger, Monte Carlo-grenser og SHA-256 revisorstempel.
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import mask_pii, run_monte_carlo, generate_audit_seal, load_helse_data


class TestHelseMestringMVP(unittest.TestCase):

    def test_port4_pii_masking(self):
        raw_text = "Saksbehandler Ola Nordmann, fnr 120588 12345, konto 1234.56.78901, epost: test@kristiansand.kommune.no"
        masked = mask_pii(raw_text)
        self.assertNotIn("120588 12345", masked)
        self.assertNotIn("1234.56.78901", masked)
        self.assertNotIn("test@kristiansand.kommune.no", masked)
        self.assertIn("[SKJERMET_FNR]", masked)
        self.assertIn("[SKJERMET_KONTO]", masked)
        self.assertIn("[SKJERMET_EPOST]", masked)

    def test_dax_variance_calculations(self):
        df = load_helse_data()
        self.assertEqual(len(df), 3)
        for _, row in df.iterrows():
            # Check expected budget formula
            expected_ytd = round(row["Budsjett_MNOK"] * (8.0 / 12.0), 2)
            self.assertEqual(row["Forventet_YTD_MNOK"], expected_ytd)
            
            # Check variance formula
            calculated_variance = round(expected_ytd - row["Regnskap_YTD_MNOK"], 2)
            self.assertEqual(row["Avvik_MNOK"], calculated_variance)

    def test_monte_carlo_projections(self):
        budget = 145.0
        ytd = 104.4
        p10, p50, p90 = run_monte_carlo(budget, ytd)
        
        # P10 <= P50 <= P90
        self.assertLessEqual(p10, p50)
        self.assertLessEqual(p50, p90)
        
        # Check sanity bounds (should be around 140 - 170 MNOK for full year)
        self.assertGreater(p50, 130.0)
        self.assertLess(p50, 180.0)

    def test_sha256_audit_seal_integrity(self):
        user = "test.controller@kristiansand.kommune.no"
        funksjon = "254"
        rec = "TEST_RECOMMENDATION"
        decision = "APPROVED"
        
        audit = generate_audit_seal(user, funksjon, rec, decision)
        
        self.assertIn("sha256_seal", audit)
        self.assertEqual(len(audit["sha256_seal"]), 64)
        self.assertEqual(audit["human_decision"], "APPROVED")


if __name__ == "__main__":
    unittest.main()
