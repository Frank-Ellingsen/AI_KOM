"""
Cryptographic SHA-256 Audit Logger for Stage-Gate Port 9 & Kommunerevisjonen
Kristiansand Kommune — AI Guardrails & M365 Copilot Pilot
"""

import json
import hashlib
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class AuditEntry:
    timestamp: str
    actor: str
    action_type: str
    prompt: str
    response: str
    retrieved_chunk_ids: List[str]
    sha256_hash: str
    verified_hitl: bool = True
    metadata: Optional[Dict[str, Any]] = None


class AuditLogger:
    """
    Loggfører alle AI-genererte responser med kryptografisk SHA-256 forsegling.
    """

    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file
        self.entries: List[AuditEntry] = []

    @staticmethod
    def compute_sha256(timestamp: str, actor: str, prompt: str, response: str) -> str:
        payload = f"{timestamp}|{actor}|{prompt}|{response}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def log_action(
        self,
        prompt: str,
        response: str,
        actor: str = "Frank Ellingsen",
        action_type: str = "COPILOT_RAG_QUERY",
        retrieved_chunk_ids: Optional[List[str]] = None,
        verified_hitl: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEntry:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        sha256 = self.compute_sha256(now, actor, prompt, response)

        entry = AuditEntry(
            timestamp=now,
            actor=actor,
            action_type=action_type,
            prompt=prompt,
            response=response,
            retrieved_chunk_ids=retrieved_chunk_ids or [],
            sha256_hash=sha256,
            verified_hitl=verified_hitl,
            metadata=metadata or {}
        )
        self.entries.append(entry)

        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

        return entry

    def get_latest_hash(self) -> Optional[str]:
        if not self.entries:
            return None
        return self.entries[-1].sha256_hash
