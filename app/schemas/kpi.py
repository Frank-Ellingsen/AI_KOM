"""
Pydantic schemas for Top 3 KPIs and Cascading Budget Hierarchy
jf. TBU-anbefalinger, Kommuneloven §§ 14-1, 14-13 og KOSTRA-retningslinjer.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field


class GaugeScale(BaseModel):
    rød: Optional[List[float]] = None
    gul: Optional[List[float]] = None
    grønn: Optional[List[float]] = None
    mørk_grønn: Optional[List[float]] = None


class Top3KpiItem(BaseModel):
    navn: str
    enhet: str
    verdi: float
    mål_tbu: float
    mål_kommune: float
    gauge_skala: Dict[str, List[float]]
    status: str = Field("GRØNN", description="Triage status (GRØNN, GUL, RØD)")


class UnitKpi(BaseModel):
    enhet_id: str
    enhet_navn: str
    leder: str
    ramme_ytd_nok: float
    forbruk_ytd_nok: float
    avvik_ytd_nok: float
    avvik_prosent: float
    triage_status: str
    enhets_kpis: Dict[str, Any] = Field(default_factory=dict)


class SectorHierarchyItem(BaseModel):
    sektor_id: str
    sektor_navn: str
    direktør: str
    ramme_ytd_nok: float
    forbruk_ytd_nok: float
    avvik_ytd_nok: float
    avvik_prosent: float
    triage_status: str
    sektor_spesifikke_kpis: Dict[str, Any] = Field(default_factory=dict)
    enheter: List[UnitKpi] = Field(default_factory=list)


class Top3KpiDashboardResponse(BaseModel):
    kommune: str
    periode: str
    top3_kpis: Dict[str, Top3KpiItem]
    budsjetthierarki: List[SectorHierarchyItem]
    sha256_audit_seal: str
