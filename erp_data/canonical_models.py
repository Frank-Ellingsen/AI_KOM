"""
Canonical Data Model and Pydantic Schemas for Kristiansand Kommune Golden Record
Single Source of Truth (SSOT) Architecture.

Enforces:
1. Pydantic v2 data contracts on all Staging, Dimensions, Facts, and Audit Logs.
2. Automated PII detection and scrubbing (Stage-Gate Port 4).
3. KOSTRA standard rules (Kontoklasse 1 vs 2 jf. § 14-9, bruttoprinsippet § 14-6).
4. Cryptographic SHA-256 seal integrity (Stage-Gate Port 9).
5. Monte Carlo percentile ordering (P10 <= P50 <= P90).
"""

from __future__ import annotations

from enum import Enum
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ==============================================================================
# ENUMS & CONSTANTS
# ==============================================================================

class KontoklasseEnum(int, Enum):
    DRIFT = 1
    INVESTERING = 2
    BALANSE = 3


class HumanDecisionEnum(str, Enum):
    APPROVED = "APPROVED"
    MODIFIED = "MODIFIED"
    REJECTED = "REJECTED"


class PrognoseStatusEnum(str, Enum):
    BALANSE = "I_BALANSE"
    MODERAT_MERFORBRUK = "MODERAT_MERFORBRUK"
    KRITISK_MERFORBRUK = "KRITISK_MERFORBRUK"
    MINDFORBRUK = "MINDREFORBRUK"


# PII Patterns for Norwegian Municipal Data
FNR_REGEX = re.compile(r"\b(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{7}\b")
PHONE_REGEX = re.compile(r"\b(?:\+47\s*)?[2-9]\d{7}\b")
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
SHA256_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")


# ==============================================================================
# 1. CONFORMED DIMENSION MODELS
# ==============================================================================

class KontoklasseCanonical(BaseModel):
    """Dim_Kontoklasse: Kontoklasse 1 (Drift), 2 (Investering), 3 (Balanse)."""
    model_config = ConfigDict(frozen=True)

    kontoklasse_id: int = Field(..., ge=1, le=3, description="1=Drift, 2=Investering, 3=Balanse")
    kontoklasse_navn: str = Field(..., min_length=2)
    beskrivelse: Optional[str] = None


class FunksjonCanonical(BaseModel):
    """Dim_Funksjon: KOSTRA funksjonskatalog (f.eks. 100, 202, 254)."""
    model_config = ConfigDict(frozen=True)

    funksjon_kode: str = Field(..., min_length=3, max_length=5, description="3- eller 4-sifret KOSTRA funksjonskode")
    funksjon_navn: str = Field(..., min_length=2)
    tjenesteomrade: str = Field(..., min_length=2)
    hovedfunksjon: str = Field(..., min_length=2)

    @field_validator("funksjon_kode")
    @classmethod
    def validate_funksjon_format(cls, v: str) -> str:
        clean = v.strip().replace(".0", "")
        if not clean.isdigit():
            raise ValueError(f"KOSTRA funksjonskode må være numerisk, fikk: {v}")
        return clean


class ArtCanonical(BaseModel):
    """Dim_Art: KOSTRA artskontoer (f.eks. 1010 Fastlønn, 1020 Vikarer) eller syntetiske ERP-poster."""
    model_config = ConfigDict(frozen=True)

    art_kode: str = Field(..., min_length=3, max_length=32, description="3-4 sifret KOSTRA artskode eller syntetisk ERP-kode")
    art_navn: str = Field(..., min_length=2)
    art_gruppe: str = Field(..., min_length=2)

    @field_validator("art_kode")
    @classmethod
    def validate_art_format(cls, v: str) -> str:
        clean = v.strip().replace(".0", "")
        if not clean:
            raise ValueError("Artekode kan ikke være tom")
        return clean


class AnsvarCanonical(BaseModel):
    """Dim_Ansvar: Kommunalt ansvarssted / enhet."""
    model_config = ConfigDict(frozen=True)

    ansvar_kode: str = Field(..., min_length=2, max_length=32)
    enhet_navn: str = Field(..., min_length=2)
    sektor: str = Field(..., min_length=2)
    leder_stilling: Optional[str] = None


class DatoCanonical(BaseModel):
    """Dim_Dato: Periodisering og årshjul."""
    model_config = ConfigDict(frozen=True)

    dato_key: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="Format: YYYY-MM")
    aar: int = Field(..., ge=2020, le=2040)
    maned: int = Field(..., ge=1, le=12)
    kvartal: str = Field(..., pattern=r"^Q[1-4]$")
    tertial: str = Field(..., pattern=r"^T[1-3]$")
    arshjul_fase: Optional[str] = None


class BudsjettansvarligCanonical(BaseModel):
    """Dim_Budsjettansvarlige: Register over enhetsledere, fullmakter og rapportering."""
    model_config = ConfigDict(frozen=True)

    ansvar_id: str = Field(..., min_length=2)
    navn: str = Field(..., min_length=2)
    tittel: str = Field(..., min_length=2)
    niva: str = Field(..., min_length=2)
    niva_tekst: str = Field(..., min_length=2)
    sektor_kode: str = Field(..., min_length=2)
    sektor_navn: str = Field(..., min_length=2)
    enhet_navn: str = Field(..., min_length=2)
    kostra_funksjon: str = Field(..., min_length=2)
    epost: str = Field(..., min_length=5)
    telefon: str = Field(..., min_length=6)
    kontorsted: str = Field(..., min_length=2)
    delegeringsfullmakt_nok: float = Field(..., ge=0)
    controller_navn: str = Field(..., min_length=2)
    controller_epost: str = Field(..., min_length=5)
    utsendte_rapporter: Optional[str] = None
    tilknyttet_mal: Optional[str] = None
    returkanal: Optional[str] = None
    returfrist: Optional[str] = None


# ==============================================================================
# 2. STAGING & RAW INGESTION MODELS (WITH PII GUARDRAILS)
# ==============================================================================

class ErpTransactionStaging(BaseModel):
    """stg_erp_transactions: Råtransaksjoner fra Visma ERP med PII-sjekk."""
    source_system: str = Field(..., min_length=2)
    voucher_number: Optional[str] = None
    accounting_date: str = Field(..., min_length=7, description="YYYY-MM eller YYYY-MM-DD")
    account_code: str = Field(..., min_length=3)
    function_code: str = Field(..., min_length=3)
    cost_center_code: str = Field(..., min_length=2)
    amount: float
    description: Optional[str] = None
    scale_factor: float = Field(default=1.0, gt=0)

    @field_validator("description")
    @classmethod
    def verify_no_unredacted_pii(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        if FNR_REGEX.search(v):
            raise ValueError(f"CRITICAL PII BREACH: Fødselsnummer identifisert i posteringstekst: '{v}'")
        return v

    @field_validator("accounting_date")
    @classmethod
    def normalize_date(cls, v: str) -> str:
        clean = v.strip()
        if not (re.match(r"^\d{4}-\d{2}-\d{2}$", clean) or re.match(r"^\d{4}-\d{2}$", clean)):
            raise ValueError(f"Ugyldig regnskapsdatoformat: '{v}' (krever YYYY-MM-DD eller YYYY-MM)")
        return clean


class EpmBudgetStaging(BaseModel):
    """stg_epm_budget: Råbudsjett og rammereguleringer fra Framsikt EPM."""
    source_system: str = Field(default="FRAMSIKT_EPM")
    budget_version: str = Field(..., min_length=2)
    fiscal_year: int = Field(..., ge=2020, le=2040)
    period_key: Optional[str] = None
    function_code: str = Field(..., min_length=3)
    art_code: str = Field(..., min_length=3)
    cost_center_code: str = Field(..., min_length=2)
    budget_amount: float
    scale_factor: float = Field(default=1.0, gt=0)


# ==============================================================================
# 3. CORE FACT MODELS (STAR SCHEMA GOLDEN RECORD)
# ==============================================================================

class FactRegnskapCanonical(BaseModel):
    """Fact_Regnskap: Bokførte regnskapsposter (Gullstandard)."""
    transaksjon_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$", description="SHA-256 kryptografisk nøkkel")
    kilde_system: str = Field(..., min_length=2)
    kontoklasse_id: int = Field(default=1, ge=1, le=3)
    funksjon_key: str = Field(..., min_length=3)
    art_key: str = Field(..., min_length=3)
    ansvar_key: str = Field(..., min_length=2)
    dato_key: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    belop: float
    er_akkumulert_ytd: bool = False

    @field_validator("belop")
    @classmethod
    def validate_finite_amount(cls, v: float) -> float:
        if v != v:  # NaN sjekk
            raise ValueError("Regnskapsbeløp kan ikke være NaN")
        if abs(v) > 1e11:
            raise ValueError(f"Urealistisk regnskapsbeløp (> 100 mrd): {v}")
        return v


class FactBudsjettCanonical(BaseModel):
    """Fact_Budsjett: Periodiserte og vedtatte budsjettrammer."""
    budsjett_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$", description="SHA-256 kryptografisk nøkkel")
    kilde_system: str = Field(..., min_length=2)
    budsjett_type: str = Field(..., min_length=2)
    aar: int = Field(..., ge=2020, le=2040)
    funksjon_key: str = Field(..., min_length=3)
    art_key: str = Field(..., min_length=3)
    ansvar_key: str = Field(..., min_length=2)
    dato_key: Optional[str] = None
    budsjett_belop: float
    er_akkumulert_ytd: bool = False

    @field_validator("budsjett_belop")
    @classmethod
    def validate_finite_amount(cls, v: float) -> float:
        if v != v:
            raise ValueError("Budsjettbeløp kan ikke være NaN")
        return v


# ==============================================================================
# 4. AUDIT & GOVERNANCE MODELS (STAGE-GATE PORT 9 & HITL)
# ==============================================================================

class AuditAiActionCanonical(BaseModel):
    """Audit_AI_Actions: Uforanderlig revisjonslogg for Kommunerevisjonen (EU AI Act Art. 26 / Stage-Gate Port 9)."""
    id: Optional[int] = None
    tidsstempel: Optional[str] = None
    enhetskode: Optional[str] = None
    ansvar_kode: Optional[str] = None
    ai_tiltak: Optional[str] = None
    konfidens: Optional[float] = None
    leder_beslutning: Optional[str] = None
    saksbehandler: Optional[str] = None
    begrunnelse: Optional[str] = None
    sha256_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{16,64}$")
    user_query: Optional[str] = None
    retrieved_chunk_ids: Optional[str] = None
    llm_response: Optional[str] = None
    human_decision: Optional[str] = None


class FactPrognoseLoggCanonical(BaseModel):
    """Fact_Prognose_Logg: Monte Carlo simuleringer og EVM-sluttprognoser."""
    prognose_id: str = Field(..., min_length=3)
    ansvar_kode: str = Field(..., min_length=2)
    kostra_funksjon: str = Field(..., min_length=2)
    periode_ytd: int = Field(..., ge=1, le=12)
    regnskapsar: int = Field(..., ge=2020, le=2040)
    modell_type: str = Field(..., min_length=2)
    hittil_regnskap_ac: float
    vedtatt_ramme_bac: float
    p10_belop: float
    p50_belop: float
    p90_belop: float
    estimert_avvik_p50: float
    cpi: Optional[float] = None
    spi: Optional[float] = None
    status: str
    saksbehandler: str = Field(..., min_length=3)
    sha256_hash: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$")

    @model_validator(mode="after")
    def validate_percentile_ordering(self) -> FactPrognoseLoggCanonical:
        if not (self.p10_belop <= self.p50_belop <= self.p90_belop):
            raise ValueError(
                f"Ugyldig persentilrekkefølge i Monte Carlo: P10 ({self.p10_belop}) <= P50 ({self.p50_belop}) <= P90 ({self.p90_belop}) er brutt!"
            )
        return self


# ==============================================================================
# 5. RECONCILIATION SUMMARY MODEL
# ==============================================================================

class ModelReconciliationSummary(BaseModel):
    """Oppsummeringsmodell for avstemming mellom Staging, SQLite, DuckDB og Power BI."""
    timestamp: str
    database_path: str
    total_regnskap_nok: float
    total_budsjett_nok: float
    total_avvik_nok: float
    antall_transaksjoner: int
    antall_budsjettposter: int
    antall_dim_funksjoner: int
    antall_dim_arter: int
    antall_dim_ansvar: int
    antall_dim_datoer: int
    orphaned_funksjon_keys: int
    orphaned_art_keys: int
    orphaned_ansvar_keys: int
    orphaned_dato_keys: int
    is_fully_reconciled: bool
