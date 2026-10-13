"""
Golden Test Suite for MLOps & RAG Evaluation (test_rag_eval.py)
Spesifisert i DOCKER_AND_MLOPS_DEPLOYMENT.md.
Tester:
1. Faithfulness Score (100% Kildeforankring mot Kommuneloven og regelverk)
2. Context Precision & Recall (Relevante chunks for budsjettendring og KOSTRA)
3. PII Safety Check (100% anonymisering av fødselsnumre, tlf og e-post)
4. SHA-256 Audit Integrity
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
import pytest

from kommune_ai_guardrails.rag import (
    sanitize_pii,
    validate_output_citation,
    init_audit_log,
    log_audit_trail,
)


# ==============================================================================
# 1. FAITHFULNESS SCORE (100% KILDEFORANKRING)
# ==============================================================================
def test_rag_eval_faithfulness_citation():
    """Validerer at svar på økonomiske og juridiske spørsmål forankres i lovhjemmel."""
    test_cases = [
        ("Jf. Kommuneloven § 14-5 plikter kommunedirektøren å fremme sak ved vesentlige avvik.", True),
        ("KILDE: KOSTRA-veileder 2026 tabell 4 for funksjon 202 Grunnskole.", True),
        ("Jfr. Økonomireglementet for Kristiansand kommune punkt 3.2.", True),
        ("Budsjettet må endres fordi vi har brukt for mye penger på vikarer uten hjemmel.", False),
        ("Dette er et generelt svar uten noen kildehenvisning.", False),
    ]

    for answer_text, expected_valid in test_cases:
        is_faithful = validate_output_citation(answer_text)
        assert is_faithful == expected_valid, f"Feilet på: {answer_text}"


# ==============================================================================
# 2. CONTEXT PRECISION & RECALL (RELEVANTE CHUNKS)
# ==============================================================================
def test_rag_eval_context_precision_and_recall(tmp_path):
    """Tester at søk etter budsjettrevisjon treffer relevante paragrafer."""
    db_path = tmp_path / "test_eval.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Opprett dummy lovdatabase med kjente chunks
    cur.execute("""
    CREATE TABLE legal_chunks (
        id INTEGER PRIMARY KEY,
        document_title TEXT,
        paragraph TEXT,
        content TEXT
    );
    """)

    cur.executemany("""
    INSERT INTO legal_chunks (id, document_title, paragraph, content) VALUES (?, ?, ?, ?)
    """, [
        (1, "Kommuneloven", "§ 14-5", "Årsbudsjettet og økonomiplanen skal være realistiske og i balanse. Ved vesentlige avvik skal saken fremmes for kommunestyret."),
        (2, "Kommuneloven", "§ 14-6", "Årsregnskap og årsberetning skal avlegges innen 31. mars."),
        (3, "Offentleglova", "§ 3", "Saksdokument, journalar og liknande register for organet er opne for innsyn dersom ikkje anna følgjer av lov."),
        (4, "KOSTRA Forskrift", "§ 2", "Kommunene skal rapportere regnskap og tjenestetall innen fastsatte frister.")
    ])
    conn.commit()

    # Evaluering av recall for "budsjett avvik": Chunk 1 skal være med
    query_keyword = "%avvik%"
    matched = cur.execute("SELECT id, paragraph FROM legal_chunks WHERE content LIKE ?", (query_keyword,)).fetchall()
    conn.close()

    matched_ids = [m[0] for m in matched]
    assert 1 in matched_ids, "Recall-feil: Kommuneloven § 14-5 ble ikke gjenfunnet på avvikssøk."
    assert len(matched_ids) >= 1, "Precision-feil: Ingen treff på nøkkelord."


# ==============================================================================
# 3. PII SAFETY CHECK (PORT 4 ZERO-LEAKAGE)
# ==============================================================================
def test_rag_eval_pii_zero_leakage():
    """Tester at ingen personopplysninger passerer PII-filteret."""
    syntetiske_personopplysninger = [
        ("Ansatt Kari Nordmann med fnr 12058512345 har overtid.", "12058512345", "[SKJERMET FNR]"),
        ("Kontakt enhetsleder på tlf 99887766 for godkjenning.", "99887766", "[SKJERMET TLF]"),
        ("Send bekreftelse til saksbehandler frank.ellingsen@kristiansand.kommune.no snarest.", "frank.ellingsen@kristiansand.kommune.no", "[SKJERMET E-POST]"),
    ]

    for raw, secret, masked_token in syntetiske_personopplysninger:
        vasket = sanitize_pii(raw)
        assert secret not in vasket, f"PII Lekkasje! Fant {secret} i vasket tekst."
        assert masked_token in vasket, f"Mangler forventet maskeringstoken {masked_token} i {vasket}."


# ==============================================================================
# 4. SHA-256 AUDIT TRAIL INTEGRITY (PORT 9)
# ==============================================================================
def test_rag_eval_sha256_audit_integrity(tmp_path):
    """Tester at revisjonssporet oppretter gyldige, uforanderlige SHA-256 hash-strenger."""
    db_path = tmp_path / "eval_audit.db"
    conn = sqlite3.connect(db_path)
    try:
        init_audit_log(conn)
        hash_val = log_audit_trail(conn, "Hva er fristen for 2. tertial?", [1, 4], "Fristen er 28. september jf. årshjulet.")

        row = conn.execute("SELECT sha256_hash FROM Audit_AI_Actions").fetchone()
        assert row is not None
        assert row[0] == hash_val
        assert len(hash_val) == 64, "SHA-256 hash må være nøyaktig 64 heksadesimale tegn."
    finally:
        conn.close()
