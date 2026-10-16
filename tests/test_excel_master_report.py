"""
Unit and integration tests for Excel_Master_Report.xlsx.
Validates implementation of:
excel/excel_best_practice_finance_dashboard_powerpivot_dax_rag.md
"""
from pathlib import Path
import openpyxl
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = ROOT_DIR / "excel" / "Excel_Master_Report.xlsx"

EXPECTED_SHEETS = [
    "00_README",
    "01_CONTROL",
    "02_DASHBOARD_EXEC",
    "03_DASHBOARD_OPPVEKST",
    "04_DASHBOARD_HELSE",
    "05_LONN_VIKAR",
    "06_PROGNOSE_SCENARIO",
    "07_EVM",
    "08_ROOT_CAUSE",
    "09_AUDIT",
    "10_DETAIL",
    "90_PIVOTS",
    "91_HELPER",
    "99_QA",
]


@pytest.fixture(scope="module")
def wb():
    assert EXCEL_PATH.exists(), f"Excel file does not exist at {EXCEL_PATH}"
    workbook = openpyxl.load_workbook(str(EXCEL_PATH), data_only=False)
    yield workbook
    workbook.close()


def test_excel_file_exists_and_size():
    assert EXCEL_PATH.exists()
    assert EXCEL_PATH.stat().st_size > 20_000, "Workbook file size is unexpectedly small"


def test_exact_14_sheets_present(wb):
    assert len(wb.sheetnames) == 14, f"Expected 14 sheets, found {len(wb.sheetnames)}: {wb.sheetnames}"
    for expected in EXPECTED_SHEETS:
        assert expected in wb.sheetnames, f"Missing sheet: {expected}"


def test_readme_sheet(wb):
    ws = wb["00_README"]
    assert "KRISTIANSAND KOMMUNE" in str(ws["B2"].value)
    # Check DAX measures catalog
    found_dax = False
    for r in range(1, 60):
        val = str(ws.cell(row=r, column=3).value or "")
        if "Sum Regnskap YTD" in val or "Avvik YTD" in val or "CPI" in val:
            found_dax = True
            break
    assert found_dax, "DAX measure catalog missing from 00_README"


def test_control_sheet_parameters(wb):
    ws = wb["01_CONTROL"]
    params = {}
    for r in range(5, 16):
        k = ws.cell(row=r, column=2).value
        v = ws.cell(row=r, column=3).value
        if k:
            params[str(k).strip()] = v

    assert "Frank Ellingsen" in str(params.get("Default_Controller", ""))
    assert "T2" in str(params.get("Active_Reporting_Period", ""))
    assert params.get("Materiality_Limit_NOK") == 100000


def test_dashboard_exec_kpis_and_rag(wb):
    ws = wb["02_DASHBOARD_EXEC"]
    # Check KPI labels
    assert "REGNSKAP YTD" in str(ws["B5"].value).upper()
    assert "BUDSJETT YTD" in str(ws["E5"].value).upper()
    assert "AVVIK YTD" in str(ws["H5"].value).upper()
    assert "EOY AVVIK" in str(ws["K5"].value).upper()

    # Inverted RAG rule verification:
    # Avvik YTD (-0.42M kr) is favorable, so it must be green
    fill_h = str(ws["H5"].fill.start_color.rgb)
    assert fill_h.endswith("D4EDDA"), f"Expected green fill for favorable cost variance, got {fill_h}"

    # EOY Avvik (+32.3M kr) is adverse overrun, so it must be red
    fill_k = str(ws["K5"].fill.start_color.rgb)
    assert fill_k.endswith("F8D7DA"), f"Expected red fill for adverse cost overrun, got {fill_k}"


def test_dashboard_oppvekst_and_helse(wb):
    ws_opp = wb["03_DASHBOARD_OPPVEKST"]
    assert "Oppvekst" in str(ws_opp["B2"].value) or "OPPVEKST" in str(ws_opp["B2"].value)
    assert ws_opp["B6"].value is not None

    ws_helse = wb["04_DASHBOARD_HELSE"]
    assert "Helse" in str(ws_helse["B2"].value) or "HELSE" in str(ws_helse["B2"].value)
    assert ws_helse["B6"].value is not None


def test_lonn_vikar_monitor(wb):
    ws = wb["05_LONN_VIKAR"]
    assert "PERSONALKONTROLL" in str(ws["B2"].value).upper() or "VIKARBRUK" in str(ws["B2"].value).upper()
    art_codes = [str(ws.cell(row=r, column=2).value) for r in range(10, 15)]
    assert any("1010" in c for c in art_codes)
    assert any("1020" in c for c in art_codes)
    assert any("1270" in c for c in art_codes)
    assert any("1690" in c for c in art_codes)


def test_prognose_scenario_fast_formatting(wb):
    ws = wb["06_PROGNOSE_SCENARIO"]
    assert "SCENARIOMODELL" in str(ws["B2"].value)

    # Check FAST input formatting: Blue font, blue light fill for inputs in column C
    for r in range(6, 11):
        cell = ws[f"C{r}"]
        font_c = str(cell.font.color.rgb)
        fill_c = str(cell.fill.start_color.rgb)
        assert font_c.endswith("000080"), f"Expected dark blue font for FAST inputs, got {font_c}"
        assert fill_c.endswith("E8F0FE"), f"Expected blue input fill, got {fill_c}"


def test_evm_project_controlling(wb):
    ws = wb["07_EVM"]
    assert "EVM" in str(ws["B2"].value) or "PROJECT CONTROLLING" in str(ws["B2"].value)
    # Check table columns: Headers on row 9
    headers = [str(ws.cell(row=9, column=c).value) for c in range(2, 13)]
    assert any("BAC" in h for h in headers)
    assert any("CPI" in h for h in headers)
    assert any("EAC" in h for h in headers)
    assert any("VAC" in h for h in headers)


def test_audit_log_and_sha256(wb):
    ws = wb["09_AUDIT"]
    assert "PORT 9" in str(ws["B2"].value).upper() or "REVISJONSSPOR" in str(ws["B2"].value).upper()

    # Check that SHA-256 hashes are genuine 64 hex characters (column J = col 10) and signed by Frank Ellingsen (col H = col 8)
    found_hash = False
    for r in range(5, 12):
        saksb = ws.cell(row=r, column=8).value
        sha = ws.cell(row=r, column=10).value
        if sha:
            assert len(str(sha)) == 64, f"Invalid SHA-256 length: {sha}"
            assert "Frank" in str(saksb) or "Ellingsen" in str(saksb)
            found_hash = True
    assert found_hash, "No audit entries with SHA-256 found in 09_AUDIT"


def test_qa_checklist_all_pass(wb):
    ws = wb["99_QA"]
    assert "DATAKVALITETSKONTROLL" in str(ws["B2"].value) or "QA" in str(ws["B2"].value)

    # Check QA-01 to QA-09 all have 'PASS'
    qa_results = []
    for r in range(5, 14):
        res = ws.cell(row=r, column=7).value
        if res:
            qa_results.append(str(res))

    assert len(qa_results) >= 9, f"Expected at least 9 QA checks, found {len(qa_results)}"
    for res in qa_results:
        assert "PASS" in res, f"QA check failed: {res}"
        assert "PASS" in res, f"QA check failed: {res}"
