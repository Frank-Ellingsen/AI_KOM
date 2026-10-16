"""
PII Scrubber and FinOps Token Rate Limiter for Municipal AI Gateway
Kristiansand Kommune — AI Guardrails & M365 Copilot Pilot
"""

import re
import time
from typing import Tuple, Dict, Any, Optional


FNR_PATTERN = re.compile(r"\b\d{6}\s?\d{5}\b")
PHONE_PATTERN = re.compile(r"(?:\+47[\s-]?)?(?:[49]\d{7}|[23567]\d{7})\b")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def sanitize_pii(text: str) -> str:
    """
    Renser tekst for personidentifiserende opplysninger (PII) jf. GDPR art. 4/35.
    Erstatter:
      - Norske fødselsnumre (11 siffer) -> [SKJERMET_FNR]
      - Telefonnumre (+47 / 8 siffer)    -> [SKJERMET_TLF]
      - E-postadresser                    -> [SKJERMET_EPOST]
    """
    if not text:
        return ""
    
    cleaned = FNR_PATTERN.sub("[SKJERMET_FNR]", text)
    cleaned = PHONE_PATTERN.sub("[SKJERMET_TLF]", cleaned)
    cleaned = EMAIL_PATTERN.sub("[SKJERMET_EPOST]", cleaned)
    return cleaned


class TokenRateLimiter:
    """
    Token-bøtte (Token Bucket) hastighets- og kostnadsbegrenser for FinOps.
    Sikrer at enheter/brukere ikke overskrider tillatt token-forbruk.
    """

    def __init__(self, capacity: int = 100000, refill_rate_per_sec: float = 1000.0):
        self.capacity = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.tokens: Dict[str, float] = {}
        self.last_refill: Dict[str, float] = {}

    def _refill(self, key: str, now: float) -> None:
        if key not in self.tokens:
            self.tokens[key] = self.capacity
            self.last_refill[key] = now
            return

        elapsed = now - self.last_refill[key]
        added = elapsed * self.refill_rate
        self.tokens[key] = min(self.capacity, self.tokens[key] + added)
        self.last_refill[key] = now

    def acquire(self, key: str, estimated_tokens: int = 500) -> Tuple[bool, float]:
        """
        Prøver å reservere tokens for en forespørsel.
        Returnerer (innvilget: bool, gjenstående_tokens: float).
        """
        now = time.time()
        self._refill(key, now)

        if self.tokens[key] >= estimated_tokens:
            self.tokens[key] -= estimated_tokens
            return True, self.tokens[key]
        else:
            return False, self.tokens[key]

    def get_remaining(self, key: str) -> float:
        now = time.time()
        self._refill(key, now)
        return self.tokens.get(key, self.capacity)
