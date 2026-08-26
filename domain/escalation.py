from pydantic import BaseModel
from datetime import datetime

class Escalation(BaseModel):
    escalation_id: str
    session_id: str
    customer_id: str
    order_id: str | None = None
    reason: str
    summary: str
    actions_taken: list[str]
    created_at: datetime
    status: str = "open"
