# Project Controlling & Earned Value Management (EVM) Rules
# Applied to Municipal Operations & Capex Portfolios

## 1. Professional Context
* The user is **Frank Ellingsen**, Senior Project Controller and Business Intelligence specialist for Kristiansand Kommune.
* All controlling explanations, variance models, and forecast calculations must strictly map to Norwegian municipal finance (Kommuneloven, KOSTRA, FAST modeling standard).

## 2. EVM Formulas & Metric Definitions
* **Planned Value (PV)**: Periodized budget to date ($PV = \text{Akkumulert periodisert ramme fra Framsikt EPM}$).
* **Actual Cost (AC)**: Actual recorded accounting expenditure from Visma Enterprise ERP ($AC = \text{Bokført forbruk}$).
* **Earned Value (EV)**: Value of work performed ($EV = \text{Fysisk fremdrift \%} \times BAC$).
* **Cost Variance (CV)**: $CV = EV - AC$ (in investment projects) or $CV = PV - AC$ (in operational budget controlling).
  * $CV < 0$: Merforbruk (unfavorable variance).
  * $CV > 0$: Mindreforbruk (favorable variance).
* **Cost Performance Index (CPI)**: $CPI = \frac{EV}{AC}$ (or $\frac{PV}{AC}$). Target is $1.000$.
  * $CPI < 0.95$: Red alert, immediate corrective action and administrative freeze.
  * $0.95 \le CPI < 1.00$: Amber alert, monthly surveillance and internal reallocation.
  * $CPI \ge 1.00$: Green, on or under budget.
* **Estimate at Completion (EAC)**:
  * Formula: $EAC = \frac{BAC}{CPI}$ or $EAC = AC + \frac{BAC - EV}{CPI \times SPI}$.
* **Estimate to Complete (ETC)**: $ETC = EAC - AC$.
* **Variance at Completion (VAC)**: $VAC = BAC - EAC$.

## 3. Statutory Compliance Thresholds
* **Kommuneloven § 14-5 (Balansekrav & Handleplikt)**: If rolling forecast indicates year-end deficit ($VAC < 0$), Kommunedirektøren is legally obligated to submit a formal supplementary budget case to Bystyret / Formannskapet.
* **Kommuneloven § 14-6 (Bruttoprinsippet)**: Revenues (e.g. NAV refunds, art 1600/1690) and expenses (e.g. salaries, art 1010/1020/1090) must be recorded gross; netting is illegal.
* **Selvkostforskriften § 8**: VAR utilities (water, wastewater, waste) operate under 5-year rolling balance. Annual variances do not affect general fund balance but must adjust the utility reserve fund.
* **Hovedtariffavtalen (HTA) § 4**: Significant changes to work schedule, overtime, or staffing pools require formal consultation protocols with employee unions (NSF, Fagforbundet, Utdanningsforbundet).
