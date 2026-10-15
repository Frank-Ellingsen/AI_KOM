# Edward Tufte Data-Ink Ratio & Visualization Standards
# Applied to Kristiansand Kommune EPM & Project Controlling

## 1. Core Principles
* **Maximize Data-Ink Ratio**: Eliminate all non-essential visual elements (drop shadows, rounded bevels, heavy gradient borders, decorative icons).
* **Gridlines**: Remove all vertical gridlines from tables and Gantt charts. Keep subtle horizontal dividers (`#eeeeee` or `1px solid var(--border-light)`).
* **Typography**: Clean, sans-serif typography (-apple-system, Segoe UI, Roboto) for text; monospace for accounts, hashes, and codes.
* **Alignment**:
  * Left-align text columns, descriptions, and categories.
  * Right-align numeric columns, amounts (NOK), percentages, and indices.
  * Vertically align decimal points.
* **Color Discipline**:
  * Use a muted, monochromatic slate/navy palette for base structure.
  * Bright highlight colors are strictly reserved for active variances and alerts:
    * Red (`#c0392b` / `--alert-red`): Critical unfavorable variance (e.g., merforbruk > threshold, CPI < 0.95).
    * Amber (`#d35400` / `--alert-amber`): Moderate variance / warning (e.g., CPI 0.95 - 0.999).
    * Green (`#27ae60` / `--success-green`): Favorable variance / balance (e.g., CPI >= 1.000).
* **Charts & Visuals**:
  * S-Curves and trendlines must use direct endpoint labeling instead of detached legends.
  * Bar charts must start at zero and avoid 3D perspective.
  * Waterfall charts must clearly show steps from budget to actual with red/green delta blocks.
