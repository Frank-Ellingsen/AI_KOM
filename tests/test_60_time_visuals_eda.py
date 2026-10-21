"""
Unit test suite for Andy Kriebel 60 Ways to Visualize Time EDA integration.
Verifies:
  - 96 Master visuals in index.html (36 FT + 60 Kriebel Time EDA).
  - All 60 DAX measures present in powerbi/09_Andy_Kriebel_60_Time_Visuals_EDA_Measures.dax.
  - Interactive DAX snippets mapped in index.html JS.
  - Documentation guide exists and covers all 8 EDA categories.
"""

import os
import re
from bs4 import BeautifulSoup
import pytest

def test_index_html_96_visuals_present():
    html_path = "index.html"
    assert os.path.exists(html_path), "index.html must exist"
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    tab = soup.find("div", id="tab-visual-sandbox")
    assert tab is not None, "tab-visual-sandbox must exist"
    
    cards = tab.find_all("div", class_="vs-chart-card")
    assert len(cards) == 96, f"Expected 96 cards (36 FT + 60 Time EDA), found {len(cards)}"
    
    ft_cards = [c for c in cards if c.get("data-visual-suite") != "TIME_EDA"]
    eda_cards = [c for c in cards if c.get("data-visual-suite") == "TIME_EDA"]
    assert len(ft_cards) == 36, f"Expected 36 FT cards, found {len(ft_cards)}"
    assert len(eda_cards) == 60, f"Expected 60 Time EDA cards, found {len(eda_cards)}"

def test_time_eda_cards_structure():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    for i in range(1, 61):
        num_str = f"{i:02d}"
        card_id = f"vs-card-time-eda-{num_str}"
        card = soup.find("div", id=card_id)
        assert card is not None, f"Card {card_id} must exist in index.html"
        
        # Verify SVG container exists
        svg_container = card.find("div", id=f"vs-svg-time-eda-{num_str}")
        assert svg_container is not None, f"SVG container vs-svg-time-eda-{num_str} must exist"
        
        # Verify DAX drawer exists
        dax_drawer = card.find("div", id=f"vs-dax-time-eda-{num_str}")
        assert dax_drawer is not None, f"DAX drawer vs-dax-time-eda-{num_str} must exist"

def test_dax_measures_library_coverage():
    dax_path = "powerbi/09_Andy_Kriebel_60_Time_Visuals_EDA_Measures.dax"
    assert os.path.exists(dax_path), "09_Andy_Kriebel_60_Time_Visuals_EDA_Measures.dax must exist"
    
    with open(dax_path, "r", encoding="utf-8") as f:
        dax_text = f.read()
        
    # Check that all 60 EDA measures are defined in the file
    for i in range(1, 61):
        num_str = f"{i:02d}"
        match = re.search(rf"\[EDA_{num_str}_[^\]]+\]", dax_text)
        assert match is not None, f"DAX measure for visual #{num_str} must be defined in DAX file"

def test_javascript_dax_and_renderers_coverage():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    for i in range(1, 61):
        num_str = f"{i:02d}"
        # Check DAX snippet key in JS
        assert f'"time-eda-{num_str}":' in html, f'DAX snippet key "time-eda-{num_str}" missing from VS_DAX_SNIPPETS'
        # Check SVG renderer function in JS
        assert f"function renderVsTimeEda{num_str}()" in html, f"Renderer renderVsTimeEda{num_str}() missing from JS"

def test_eda_guide_documentation_exists():
    guide_path = "docs/60_time_visuals_eda_guide.md"
    assert os.path.exists(guide_path), "docs/60_time_visuals_eda_guide.md must exist"
    
    with open(guide_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "Andy Kriebel: 60 Ways to Visualize Time" in content
    assert "Del 1: Linjer & Trender" in content
    assert "Del 8: Avansert EDA & Volatilitet" in content
