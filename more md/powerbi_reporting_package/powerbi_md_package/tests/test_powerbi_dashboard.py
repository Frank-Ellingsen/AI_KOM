import unittest
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import mask_pii, run_monte_carlo, generate_sha256_seal

class TestPowerBIDashboard(unittest.TestCase):
    def test_pii_masking(self):
        raw = "Saksbehandler Ola Nordmann 12058812345 har konto 1234.56.78901."
        masked = mask_pii(raw)
        self.assertNotIn("12058812345", masked)
        self.assertIn("[SKJERMET_FNR]", masked)

    def test_dataset_coverage(self):
        df = pd.read_csv("data/kristiansand_81_enheter.csv")
        self.assertEqual(len(df), 81)
        self.assertEqual(df["Virksomhetsomrade"].nunique(), 6)

    def test_sha256_seal(self):
        seal = generate_sha256_seal("user@kristiansand.kommune.no", "Sykehjem Enhet 1", "OK", "APPROVED")
        self.assertEqual(len(seal["sha256_seal"]), 64)

if __name__ == '__main__':
    unittest.main()
