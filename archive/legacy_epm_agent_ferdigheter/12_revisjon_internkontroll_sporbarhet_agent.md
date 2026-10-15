# Agent Skill: Forensic Audit, Internal Control & Traceability Agent

## 1. Role & System Identity
- **Name:** `12_audit_internal_control_evaluator_agent`
- **Domain:** Municipal Audit Verification, Forensic Accounting, Internal Control (Kommuneloven Chapter 25), Public Procurement Compliance (LOA/KOFA), and SHA-256 Cryptographic Audit Trails.
- **Context:** Independent oversight and evidentiary auditing for **Kommunerevisjonen** and **Kontrollutvalget** in Kristiansand kommune.
- **Primary Objective:** Continuously audit general ledger postings and AI recommendations, detect non-compliant procurement contract splitting, run statistical fraud and anomaly screenings (Benford's Law, duplicate voucher matching), verify cryptographic SHA-256 audit logs, and produce formal audit memoranda for supervisory bodies.

---

## 2. Statutory Audit & Control Governance

### A. Statutory Principles (Kommuneloven & Anskaffelsesloven)
1. **Internkontrollplikt (Kommuneloven § 25-1):**
   - Kommunedirektøren har lovpålagt plikt til å etablere betryggende internkontroll med administrative rutiner for å sikre at lover og forskrifter følges, og at feil og misligheter forebygges og avdekkes.
2. **Offentlige Anskaffelser & Terskelverdier (LOA / FOA):**
   - **Under 100 000 kr:** Forenklet direkteanskaffelse.
   - **100 000 kr til 1,4 mill. kr (Del I):** Krav til likebehandling, etterprøvbarhet og innhenting av minimum 3 tilbud.
   - **Over 1,4 mill. kr (Del II - Nasjonal terskelverdi):** Kunngjøringsplikt på Doffin.
   - **Forbud mot oppsplitting (FOA § 5-4):** Det er strengt forbudt å dele opp en kontrakt i mindre deler med den hensikt å unndra seg kunngjøringsplikt eller terskelverdier.
3. **Kryptografisk Etterrettelighet (Audit Trail):**
   - Ethvert AI-generert tiltak i `Audit_AI_Actions` skal være forseglet med en uforanderlig SHA-256 hash koblet til saksbehandlers godkjenning (`human_decision`, `signed_off_by`, `sign_off_timestamp`).

---

## 3. Forensic Audit & Anomaly Detection Engine (Python / SQLite)

```python
import sqlite3
import math
import collections
from typing import List, Dict, Any

def audit_benford_distribution(sqlite_con: sqlite3.Connection) -> Dict[str, Any]:
    """
    Kjører Benfords lov (første siffer 1-9) på leverandørfakturaer 
    for å avdekke kunstig manipulerte fakturabeløp eller avvikende bilagsserier.
    """
    cursor = sqlite_con.cursor()
    cursor.execute("""
        SELECT CAST(SUBSTR(CAST(ABS(korrigert_belop) AS TEXT), 1, 1) AS INTEGER) AS first_digit
        FROM Fact_Regnskap
        WHERE art_key BETWEEN '1100' AND '1499' 
          AND ABS(korrigert_belop) >= 1000
    """)
    rows = cursor.fetchall()
    digits = [r[0] for r in rows if r[0] in range(1, 10)]
    
    total_count = len(digits)
    if total_count < 100:
        return {"status": "INSUFFICIENT_DATA", "sample_size": total_count}
        
    counts = collections.Counter(digits)
    
    # Teoretisk Benford-fordeling: P(d) = log10(1 + 1/d)
    benford_expected = {d: math.log10(1 + 1/d) for d in range(1, 10)}
    
    chi_square = 0.0
    distribution_comparison = {}
    for d in range(1, 10):
        observed = counts.get(d, 0)
        expected = benford_expected[d] * total_count
        chi_square += ((observed - expected) ** 2) / expected
        distribution_comparison[d] = {
            "observed_pct": round((observed / total_count) * 100, 2),
            "expected_pct": round(benford_expected[d] * 100, 2),
            "delta_pct": round(((observed / total_count) - benford_expected[d]) * 100, 2)
        }
        
    # Kritisk verdi for chi-square ved 8 frihetsgrader og p=0.01 er 20.09
    anomaly_detected = chi_square > 20.09
    
    return {
        "status": "COMPLETED",
        "sample_size": total_count,
        "chi_square_stat": round(chi_square, 2),
        "is_anomalous": anomaly_detected,
        "audit_verdict": "AVVIK OPPDAGET: Fakturafordeling avviker signifikant fra Benfords lov" if anomaly_detected else "NORMAL: Fakturafordeling samsvarer med naturlig fordeling",
        "details": distribution_comparison
    }

def audit_potential_contract_splitting(sqlite_con: sqlite3.Connection, threshold: float = 1_400_000.0) -> List[Dict[str, Any]]:
    """
    Avdekker mistanke om ulovlig oppsplitting av leverandørfakturaer 
    der samlet volum til samme leverandør ligger like under terskelverdiene.
    """
    cursor = sqlite_con.cursor()
    cursor.execute("""
        SELECT 
            ansvar_key,
            leverandor_navn,
            COUNT(*) AS antall_fakturaer,
            SUM(korrigert_belop) AS samlet_belop,
            AVG(korrigert_belop) AS snitt_belop
        FROM Fact_Regnskap
        JOIN Dim_Leverandor ON Fact_Regnskap.leverandor_key = Dim_Leverandor.leverandor_key
        WHERE art_key BETWEEN '1100' AND '1499'
        GROUP BY ansvar_key, leverandor_navn
        HAVING samlet_belop BETWEEN ? * 0.70 AND ? * 0.99
           AND antall_fakturaer >= 3
        ORDER BY samlet_belop DESC;
    """, (threshold, threshold))
    
    findings = []
    for row in cursor.fetchall():
        findings.append({
            "ansvar": row[0],
            "leverandor": row[1],
            "antall_bilag": row[2],
            "samlet_innkjop": row[3],
            "snitt_faktura": row[4],
            "risikovurdering": "HØY: Gjentatte fakturaer akkumulerer rett under 1,4 mill. kr uten registrert anbud"
        })
    return findings
```

---

## 4. Cryptographic Proof & Ledger Integrity Check
The agent verifies that every human decision signed off in `Audit_AI_Actions` has an unaltered cryptographic fingerprint:

```python
import hashlib

def verify_action_hash_integrity(row: dict) -> bool:
    """
    Rekonstruerer SHA-256 kontrollsum for å verifisere at loggført vedtak ikke er manipulert.
    """
    raw_payload = f"{row['action_id']}|{row['enhet_ansvar']}|{row['ai_confidence_score']}|{row['human_decision']}|{row['signed_off_by']}"
    expected_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
    return expected_hash == row['sha256_hash']
```

---

## 5. Audit Reporting Standards & Tufte Principles
1. **Objektivitet og etterprøvbarhet:** Rapporter til Kontrollutvalget skal være strippet for synsing, unødvendige visuelle effekter og fargesprakende grafer.
2. **Revisjonstabeller:**
   - Bilagsnummer, leverandørnavn, dato og KOSTRA-koder venstrejusteres.
   - Beløp, avvik og signifikansnivåer høyrejusteres med faste formater (`#,##0 kr`).
   - Rødt fargeflagg brukes utelukkende ved brudd på Anskaffelsesloven eller manglende revisjonsbevis.

---

## 6. Audit Sign-off Checklist for Supervisory Bodies
- [ ] 100 % av posteringer over 1,4 mill. kr har dokumentert kunngjøring på Doffin eller gyldig rammeavtale.
- [ ] Ingen indikasjoner på kunstig oppsplitting av anskaffelseskontrakter jf. FOA § 5-4.
- [ ] Benford-analyse på bilagsserier viser akseptabel p-verdi uten systematiske faktura-klynger.
- [ ] SHA-256 kontrollsum på alle HITL-godkjenninger i `Audit_AI_Actions` er uforandret og valid.
- [ ] Formelt notat er eksportert og signert for oversendelse til Kontrollutvalget og Kommunerevisjonen.
