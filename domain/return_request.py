from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from domain.enums import ReturnStatus

class ReturnItem(BaseModel):
    item_id: str
    quantity: int
    reason: str

class ReturnRequest(BaseModel):
    return_id: str
    order_id: str
    customer_id: str
    status: ReturnStatus
    items: List[ReturnItem]
    created_at: datetime
    refund_amount: Optional[float] = None
