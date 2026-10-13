# 🛠️ Tool Skill: Python Sandbox & Code Execution Driver

> **Isolert og sikker utførelsesdriver for Python-skripter, dataanalyse, ETL-kjøringer og rapportgenerering.**

---

## 1. Oversikt og Formål

Denne verktøy-skillen lar AI-agenten skrive, validere, kjøre og feilsøke Python-skripter i et isolert miljø. Den brukes til dataomforming, beregninger, databasemigrering og automatisk filgenerering.

---

## 2. Kjerneprinsipper & Sikkerhet

1. **Skjermet Miljø:** Kjører uten ekstern nettverkstilgang (air-gapped).
2. **Klargjøring av Stier:**
   * Arbeidsfiler, kladd og skripter lagres i `scratch/` (relativt eller under appDataDir).
   * Ferdige leveranser (PDF, XLSX, MD, CSV, Parquet) eksporteres til `out/` for publisering.
3. **Feilhåndtering og Iterasjon:**
   * Fanger opp `stdout` og `stderr`.
   * Ved feil (f.eks. `KeyError`, `SyntaxError`) leses feilmeldingen automatisk for korrigering og ny kjøring.

---

## 3. Eksempel på Kjørebehandling i Skript

```python
import subprocess
import sys

def run_python_script(script_path: str):
    """Kjører et Python-skript isolert og returnerer resultat eller feilmelding."""
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=120,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"STDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Feil: Skriptet overskred tidsavbruddet på 120 sekunder."
```

---

## 4. Standard Bibliotekstakk
* **Analytics & OLAP:** `duckdb`, `pandas`, `numpy`, `scipy`, `pyarrow`
* **Database & Vektorer:** `sqlite3`, `sqlite-vec`
* **Visualisering (Tufte-kompatibel):** `matplotlib`, `seaborn`
* **Dokumenter & Rapporter:** `openpyxl`, `pypdf`, `python-docx`
