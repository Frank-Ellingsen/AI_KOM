"""
Subproject Unit & Integration Tests for Antigravity MS Pilot
Kristiansand Kommune — AI Guardrails & M365 Copilot Pilot
"""

import json
import pytest
from pathlib import Path
import sys

PILOT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PILOT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gateway.pii_scrubber import sanitize_pii, TokenRateLimiter
from rag.hybrid_retriever import HybridRetriever, TableAwareChunker, Chunk
from utils.audit_logger import AuditLogger


def test_pii_scrubbing_fnr_and_phone():
    raw_prompt = "Attestasjon for saksbehandler Ola Nordmann, FNR 01020312345, tlf 99887766, epost test@kristiansand.kommune.no"
    clean = sanitize_pii(raw_prompt)
    assert "01020312345" not in clean
    assert "99887766" not in clean
    assert "test@kristiansand.kommune.no" not in clean
    assert "[SKJERMET_FNR]" in clean
    assert "[SKJERMET_TLF]" in clean
    assert "[SKJERMET_EPOST]" in clean


def test_token_rate_limiter_finops():
    limiter = TokenRateLimiter(capacity=1000, refill_rate_per_sec=100)
    ok, rem = limiter.acquire("user_test", estimated_tokens=400)
    assert ok is True
    assert rem == pytest.approx(600, abs=1.0)

    # Overforbruk
    ok_excess, rem_excess = limiter.acquire("user_test", estimated_tokens=700)
    assert ok_excess is False
    assert rem_excess == pytest.approx(600, abs=1.0)


def test_table_aware_chunker():
    markdown_doc = """# Økonomirapportering
Dette er innledende avsnitt.

| Enhet | Budsjett | Regnskap | Avvik |
| :--- | :--- | :--- | :--- |
| 202 | 1000000 | 1200000 | +200000 |
| 401 | 2000000 | 1900000 | -100000 |

Avsluttende merknader jf. Kommuneloven § 14-5.
"""
    chunker = TableAwareChunker(max_chunk_chars=300)
    chunks = chunker.chunk_document(markdown_doc, source="test_doc.md")

    assert len(chunks) >= 2
    table_chunks = [c for c in chunks if c.is_table]
    assert len(table_chunks) == 1
    assert "| 202 |" in table_chunks[0].content
    assert "| 401 |" in table_chunks[0].content


def test_hybrid_retriever_search():
    retriever = HybridRetriever()
    c1 = Chunk(id="c1", content="Kommuneloven § 14-5 pålegger kommunedirektøren å melde vesentlig budsjettavvik.", source="lov", title="§ 14-5")
    c2 = Chunk(id="c2", content="Regnskapsføring av vikarutgifter på konto art 1020.", source="kontoplan", title="Konto 1020")
    retriever.add_chunks([c1, c2])

    results = retriever.search("Hva sier § 14-5 om avvik?", top_k=1)
    assert len(results) == 1
    assert results[0]["chunk"].id == "c1"


def test_sha256_audit_logging():
    logger = AuditLogger()
    entry = logger.log_action(
        prompt="Testspørsmål om rammer",
        response="Rammen er 12 mrd.",
        actor="Frank Ellingsen",
        action_type="TEST_RUN"
    )
    assert len(entry.sha256_hash) == 64
    assert entry.actor == "Frank Ellingsen"
    assert entry.verified_hitl is True


def test_ground_truth_evals_template_valid():
    eval_path = PILOT_ROOT / "evals" / "01_ground_truth_eval_template.json"
    assert eval_path.exists()
    data = json.loads(eval_path.read_text(encoding="utf-8"))
    assert "project" in data
    assert "target_faithfulness" in data
    assert data["target_faithfulness"] == 1.00
    assert len(data["test_cases"]) > 0


def test_prompt_file_structure():
    prompt_path = PILOT_ROOT / "prompts" / "01_promptsett-m365-copilot-kostra.md"
    assert prompt_path.exists()
    content = prompt_path.read_text(encoding="utf-8")
    assert "Prompt 1.1" in content
    assert "Art 1020" in content
    assert "Kristiansand kommune" in content
