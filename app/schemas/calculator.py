"""
Pydantic schemas for Municipal Advisor Decision Calculators
Kristiansand Kommune — Økonomi og Virksomhetsstyring

Støtter 4 kritiske beregningsdomener jf. Kommuneloven, Selvkostforskriften og Momskompensasjonsloven:
1. NAV Sykepengerefusjonsgap (Bruttoprinsippet jf. Kommuneloven § 14-6 fjerde ledd)
2. KRS 4 Drift vs. Investering Beslutningsmatrise jf. Kommuneloven § 14-9
3. Selvkost VAR 5-års Trajektorie & Swaprente jf. Selvkostforskriften §§ 5 og 7
4. MVA 10-års Justeringsavtale Fast Eiendom jf. Momskompensasjonsloven § 7
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# 1. NAV SYKEPENGEREFUSJON & VIKARGAP
# -----------------------------------------------------------------------------
class NavGapRequest(BaseModel):
    enhet_id: str = Field(..., description="Ansvar / Enhets-ID (f.eks. '2020' eller 'Ternevig')")
    vikar_utgifter_nok: float = Field(..., ge=0, description="Faktiske vikarutgifter i perioden (art 1020)")
    sykedager_totalt: int = Field(..., ge=0, description="Totalt antall registrerte sykefraværsdager")
    sykedager_egenmeldt: int = Field(0, ge=0, description="Dager egenmelding / under 16 dager (dekkes av arbeidsgiver)")
    dagsats_refusjon_nok: float = Field(2200.0, ge=0, description="Gjennomsnittlig dagsats for NAV-refusjon (art 1700/1710)")
    forventet_etterslep_uker: int = Field(8, ge=0, le=26, description="Forventet saksbehandlingstid / etterslep i Altinn/NAV")


class NavGapResponse(BaseModel):
    ok: bool = True
    enhet_id: str
    vikar_utgifter_nok: float
    arbeidsgiverperiode_dager: int
    refusjonsberettigede_dager: int
    forventet_nav_refusjon_nok: float
    reelt_netto_avvik_nok: float
    tilsynelatende_merforbruk_nok: float
    forklaring_til_enhetsleder: str
    lovhjemmel: str = "Kommuneloven § 14-6 fjerde ledd (Bruttoprinsippet)"
    sha256_audit_seal: str


# -----------------------------------------------------------------------------
# 2. KRS 4 DRIFT VS. INVESTERING BESLUTNINGSMATRISE
# -----------------------------------------------------------------------------
class Krs4Request(BaseModel):
    prosjekt_navn: str = Field(..., description="Prosjekt / tiltaksnavn (f.eks. 'Taktekking Wilds Minne skole')")
    kostnad_ekskl_mva_nok: float = Field(..., ge=0, description="Totalkostnad ekskl. mva")
    forventet_levetid_aar: int = Field(..., ge=1, description="Forventet levetid for det ferdige tiltaket i år")
    standardheving_eller_kapasitet: bool = Field(False, description="Medfører tiltaket standardheving eller kapasitetsøkning?")
    er_separat_funksjonell_enhet: bool = Field(False, description="Kan komponenten skilles ut og avskrives separat?")


class Krs4Response(BaseModel):
    ok: bool = True
    prosjekt_navn: str
    kostnad_ekskl_mva_nok: float
    forventet_levetid_aar: int
    klassifisering: str = Field(..., description="'INVESTERING' eller 'DRIFT'")
    anbefalt_kontoklasse: int = Field(..., description="1 (Drift) eller 2 (Investering)")
    anbefalt_art: str = Field(..., description="F.eks. 'Art 2300 Bygg og anlegg' eller 'Art 1230 Vedlikehold'")
    lovlig_laaneopptak: bool = Field(..., description="Kan prosjektet lånefinansieres jf. § 14-15?")
    begrunnelse_og_kriterier: List[str]
    lovhjemler: List[str]
    sha256_audit_seal: str


# -----------------------------------------------------------------------------
# 3. SELVKOST VAR 5-ÅRS TRAJEKTORIE & KALKYLERENTE
# -----------------------------------------------------------------------------
class SelvkostVarRequest(BaseModel):
    sektor_navn: str = Field(..., description="'Vann' (funksjon 340) eller 'Avløp' (funksjon 345)")
    inngaaende_fondssaldo_nok: float = Field(..., description="Saldo på selvkostfond 2560 ved årets start")
    aarsbudsjett_driftskostnader_nok: float = Field(..., ge=0, description="Årlige direkte og indirekte driftskostnader")
    gebyrinntekter_prognose_nok: float = Field(..., ge=0, description="Forventede gebyrinntekter i år (art 1640)")
    swap_rente_5y_pct: float = Field(3.85, ge=0, le=20, description="5-årig swaprente i prosent (f.eks. 3.85)")
    tillegg_margin_pct: float = Field(0.50, description="Fast margin jf. Selvkostforskriften § 5 (0.50 %)")


class SelvkostVarResponse(BaseModel):
    ok: bool = True
    sektor_navn: str
    effektiv_kalkylerente_pct: float
    aarets_renteinntekt_kostnad_nok: float
    aarets_selvkostresultat_nok: float
    utgaaende_fondssaldo_nok: float
    aar_i_fondssyklus: int
    fremfoering_status: str
    anbefalt_gebyrendring_pct: float
    lovhjemmel: str = "Selvkostforskriften §§ 5 og 7"
    sha256_audit_seal: str


# -----------------------------------------------------------------------------
# 4. MVA 10-ÅRS JUSTERINGSAVTALE FAST EIENDOM
# -----------------------------------------------------------------------------
class Mva10yRequest(BaseModel):
    eiendom_navn: str = Field(..., description="Eiendom / Formålsbygg (f.eks. 'Aquarama Gymsal' eller 'Kulturhus')")
    opprinnelig_anleggskost_ekskl_mva_nok: float = Field(..., ge=100000, description="Opprinnelig byggekostnad ekskl. mva")
    fullfoerings_aar: int = Field(..., ge=2015, le=2026, description="Året bygget ble tatt i bruk / ferdigattest")
    endrings_aar: int = Field(2026, ge=2020, description="Året bruksendring / utleie starter")
    andel_avgiftspliktig_utleie_pct: float = Field(..., ge=0, le=100, description="Prosentandel av arealet som leies ut til avgiftspliktig virksomhet")


class Mva10yResponse(BaseModel):
    ok: bool = True
    eiendom_navn: str
    opprinnelig_mva_kompensert_nok: float
    aarlig_justeringsramme_nok: float
    gjenstaaende_justeringsaar: int
    samlet_tilbakebetalingskrav_nok: float
    kontering_balansekonto: str = "Debet art 1429 / Kredit Balansekonto 2130"
    lovhjemmel: str = "Momskompensasjonsloven § 7 og Finansdepartementets forskrift"
    sha256_audit_seal: str
