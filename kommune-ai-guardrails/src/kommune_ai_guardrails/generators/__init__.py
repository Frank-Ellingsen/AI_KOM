"""
Automatiske generatorer for kommunale standarddokumenter:
- PowerPoint (Bystyret & Formannskapet 16:9 dekk)
- Excel (FAST-standard FP&A finansiell modell)
- Word (Politiske saksfremlegg & HØP-notat)
- Power BI (PBIP Developer Mode med 7 rapporteringssider & TMDL)
"""

from .excel_fast_generator import generate_fast_excel_model
from .excel_evm_generator import generate_project_controller_evm_model
from .excel_cfo_generator import generate_cfo_executive_konsern_model
from .excel_hr_generator import generate_hr_lonn_vikar_monitor_model
from .powerpoint_generator import generate_bystyret_deck
from .word_saksfremlegg_generator import (
    generate_saksfremlegg_docx,
    generate_hop_notat_docx,
    generate_raadmann_notat_docx,
    generate_sektornotat_oppvekst_docx,
    generate_prosjektkontroll_capex_docx,
    generate_avviksnotat_enhetsleder_docx,
)
from .powerbi_pbip_generator import build_pbip_project

# Aliases for convenience
generate_fast_model = generate_fast_excel_model
generate_bystyret_presentation = generate_bystyret_deck
generate_politisk_saksfremlegg = generate_saksfremlegg_docx
generate_hop_notat = generate_hop_notat_docx

__all__ = [
    "generate_fast_excel_model",
    "generate_fast_model",
    "generate_project_controller_evm_model",
    "generate_cfo_executive_konsern_model",
    "generate_hr_lonn_vikar_monitor_model",
    "generate_bystyret_deck",
    "generate_bystyret_presentation",
    "generate_saksfremlegg_docx",
    "generate_politisk_saksfremlegg",
    "generate_hop_notat_docx",
    "generate_hop_notat",
    "generate_raadmann_notat_docx",
    "generate_sektornotat_oppvekst_docx",
    "generate_prosjektkontroll_capex_docx",
    "generate_avviksnotat_enhetsleder_docx",
    "build_pbip_project",
]

