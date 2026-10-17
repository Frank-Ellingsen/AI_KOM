"""
Top 3 KPI & Cascading Budget Hierarchy Service
for Kristiansand kommune — Control Office Hub (AI_KOM)
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from app.schemas.kpi import (
    Top3KpiItem,
    UnitKpi,
    SectorHierarchyItem,
    Top3KpiDashboardResponse,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_JSON_PATH = ROOT_DIR / "antigravity_top3_kpi_visualisering_pakke" / "Top3_KPI_Gauge_Dashboard_Data.json"


class Top3KpiService:
    def __init__(self, json_path: Optional[Path] = None):
        self.json_path = Path(json_path) if json_path else DEFAULT_JSON_PATH
        self._raw_data: Optional[dict] = None

    def _load_data(self) -> dict:
        if self._raw_data is None:
            if not self.json_path.exists():
                raise FileNotFoundError(f"Fant ikke KPI-datafil: {self.json_path}")
            self._raw_data = json.loads(self.json_path.read_text(encoding="utf-8"))
        return self._raw_data

    def get_dashboard_payload(self) -> Top3KpiDashboardResponse:
        data = self._load_data()
        kommune_info = data.get("kommunenivå", {})
        kommune_name = kommune_info.get("kommune", "Kristiansand kommune")
        periode = kommune_info.get("periode", "2026-M10 (Oktober)")

        kpis_raw = kommune_info.get("top3_kpis", {})
        top3_kpis: Dict[str, Top3KpiItem] = {}
        for k, v in kpis_raw.items():
            top3_kpis[k] = Top3KpiItem(
                navn=v.get("navn", k),
                enhet=v.get("enhet", "%"),
                verdi=float(v.get("verdi", 0.0)),
                mål_tbu=float(v.get("mål_tbu", 0.0)),
                mål_kommune=float(v.get("mål_kommune", 0.0)),
                gauge_skala=v.get("gauge_skala", {}),
                status=v.get("status", "GRØNN"),
            )

        hierarchy_raw = data.get("budsjetthierarki", [])
        hierarchy: List[SectorHierarchyItem] = []
        for sec in hierarchy_raw:
            units: List[UnitKpi] = []
            for u in sec.get("enheter", []):
                units.append(
                    UnitKpi(
                        enhet_id=u.get("enhet_id", ""),
                        enhet_navn=u.get("enhet_navn", ""),
                        leder=u.get("leder", ""),
                        ramme_ytd_nok=float(u.get("ramme_ytd_nok", 0.0)),
                        forbruk_ytd_nok=float(u.get("forbruk_ytd_nok", 0.0)),
                        avvik_ytd_nok=float(u.get("avvik_ytd_nok", 0.0)),
                        avvik_prosent=float(u.get("avvik_prosent", 0.0)),
                        triage_status=u.get("triage_status", "GRØNN"),
                        enhets_kpis=u.get("enhets_kpis", {}),
                    )
                )

            hierarchy.append(
                SectorHierarchyItem(
                    sektor_id=sec.get("sektor_id", ""),
                    sektor_navn=sec.get("sektor_navn", ""),
                    direktør=sec.get("direktør", ""),
                    ramme_ytd_nok=float(sec.get("ramme_ytd_nok", 0.0)),
                    forbruk_ytd_nok=float(sec.get("forbruk_ytd_nok", 0.0)),
                    avvik_ytd_nok=float(sec.get("avvik_ytd_nok", 0.0)),
                    avvik_prosent=float(sec.get("avvik_prosent", 0.0)),
                    triage_status=sec.get("triage_status", "GRØNN"),
                    sektor_spesifikke_kpis=sec.get("sektor_spesifikke_kpis", {}),
                    enheter=units,
                )
            )

        payload_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        seal = hashlib.sha256(payload_bytes).hexdigest()

        return Top3KpiDashboardResponse(
            kommune=kommune_name,
            periode=periode,
            top3_kpis=top3_kpis,
            budsjetthierarki=hierarchy,
            sha256_audit_seal=seal,
        )

    def get_top3_kpis(self) -> Dict[str, Top3KpiItem]:
        return self.get_dashboard_payload().top3_kpis

    def get_hierarchy(self) -> List[SectorHierarchyItem]:
        return self.get_dashboard_payload().budsjetthierarki

    def get_sector(self, sektor_id: str) -> Optional[SectorHierarchyItem]:
        for sec in self.get_hierarchy():
            if sec.sektor_id.lower() == sektor_id.lower():
                return sec
        return None
