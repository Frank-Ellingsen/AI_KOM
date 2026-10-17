# app/services/cash_engine.py
import polars as pl
from datetime import date
from pydantic import BaseModel

class CashManagementEngine:
    def __init__(self, credit_limit_nok: float = 150_000_000.0):
        self.credit_limit_nok = credit_limit_nok

    def process_forecast(self, df_flows: pl.DataFrame, initial_balance: float) -> pl.DataFrame:
        """
        Runs liquidity projection and checks compliance with financial regulations.
        """
        balance = initial_balance
        results = []

        for row in df_flows.iter_rows(named=True):
            inflow = row['Skatteinntekter_NOK'] + row['Rammetilskudd_NOK'] + row['Andre_Innbetalinger_NOK']
            outflow = row['Lønnsutbetaling_NOK'] + row['Leverandørbetalinger_NOK'] + row['Renter_Avdrag_NOK']
            net = inflow - outflow
            balance += net

            credit_draw = abs(balance) if balance < 0 else 0.0
            overdraft_hazard = credit_draw > self.credit_limit_nok

            results.append({
                "Dato": row["Dato"],
                "Netto_Endring": net,
                "Beregnet_Saldo": balance,
                "Kassakreditt_Trekk": credit_draw,
                "Status": "CRITICAL_LIMIT" if overdraft_hazard else ("UTILIZING_CREDIT" if credit_draw > 0 else "OK")
            })

        return pl.DataFrame(results)
