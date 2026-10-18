import sqlite3

from kommune_ai_guardrails.rag import init_audit_log, log_audit_trail


def test_log_audit_trail_creates_hash(tmp_path):
    db_path = tmp_path / "audit.db"
    conn = sqlite3.connect(db_path)
    try:
        init_audit_log(conn)
        hash_value = log_audit_trail(conn, "test query", [1, 2], "response")
        row = conn.execute(
            "SELECT user_query, retrieved_chunk_ids, llm_response, sha256_hash FROM Audit_AI_Actions"
        ).fetchone()
    finally:
        conn.close()

    assert row is not None
    assert row[0] == "test query"
    assert row[2] == "response"
    assert row[3] == hash_value


def test_rag_ollama_init_audit_and_tables(tmp_path):
    import sys
    from pathlib import Path
    root_dir = Path(__file__).resolve().parents[1]
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    import rag_ollama_init as r_init

    db_path = tmp_path / "rag_init_test.db"
    conn = sqlite3.connect(db_path)
    try:
        r_init.init_audit_log(conn)
        hash_val = r_init.log_audit_trail(conn, "budsjett regulering", [10, 20], "test svar")
        row = conn.execute(
            "SELECT user_query, retrieved_chunk_ids, llm_response, sha256_hash FROM Audit_AI_Actions"
        ).fetchone()

        assert row is not None
        assert row[0] == "budsjett regulering"
        assert row[2] == "test svar"
        assert row[3] == hash_val

        # Test ensure_legal_tables returns False on empty DB
        assert r_init.ensure_legal_tables(conn) is False
        # Test hybrid_search returns [] gracefully on empty DB without throwing
        class DummyModel:
            def encode(self, text, **kwargs):
                return [0.0] * 384

        results = r_init.hybrid_search(conn, "test", DummyModel())
        assert results == []
    finally:
        conn.close()


def test_sanitize_pii_masks_sensitive_data():
    from kommune_ai_guardrails.rag import sanitize_pii

    raw_text = (
        "Bruker Ola Nordmann med fnr 01029012345, dnr 41029012345, "
        "tlf 98765432 og epost ola@kommune.no søker dispensasjon."
    )
    cleaned = sanitize_pii(raw_text)

    assert "01029012345" not in cleaned
    assert "41029012345" not in cleaned
    assert cleaned.count("[SKJERMET FNR]") == 2
    assert "98765432" not in cleaned
    assert "[SKJERMET TLF]" in cleaned
    assert "ola@kommune.no" not in cleaned
    assert "[SKJERMET E-POST]" in cleaned


def test_validate_output_citation():
    from kommune_ai_guardrails.rag import validate_output_citation

    assert validate_output_citation("Jfr. Kommuneloven § 14-5 må budsjett endres.") is True
    assert validate_output_citation("Dette er bare en generell tekst uten hjemmel.") is False

