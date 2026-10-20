from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

class UserContext(BaseModel):
    user_id: str = Field(..., description="Unik bruker-ID")
    role: Literal["enhetsleder", "kommunalsjef", "okonomidirektor", "revisor"] = Field(..., description="Brukerens organisatoriske rolle")
    ansvar_code: Optional[str] = Field(None, description="Ansvarsnummer for enhetsleder (f.eks. '2530')")
    kommunalsjef_område: Optional[str] = Field(None, description="Områdenavn for kommunalsjef")

class AuditLogEntry(BaseModel):
    timestamp: str
    user_id: str
    role: str
    action_type: str
    query_or_input: str
    execution_result_summary: str
    status: str

class ERPSQLQueryInput(BaseModel):
    sql_query: str = Field(..., description="Parameterisert SQL-spørring mot stg_erp_transactions")
    user_context: UserContext

class MonthlyUnitReportInput(BaseModel):
    ansvar_code: str = Field(..., description="Ansvarsnummer for enheten (f.eks. '2530')")
    period_month: int = Field(..., ge=1, le=12, description="Rapporteringsmåned (1-12)")
    user_context: UserContext

class BudgetReallocationInput(BaseModel):
    fra_ansvar: str = Field(..., description="Ansvarsnummer penger overføres fra")
    til_ansvar: str = Field(..., description="Ansvarsnummer penger overføres til")
    belop: float = Field(..., gt=0, description="Beløp i NOK")
    begrunnelse: str = Field(..., description="Begrunnelse for omdisponeringen")
    user_context: UserContext

class EOYForecastInput(BaseModel):
    ansvar_code: str
    current_month: int
    user_context: UserContext
