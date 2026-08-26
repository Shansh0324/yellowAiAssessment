from typing import List
from pydantic import BaseModel
from datetime import datetime
from domain.enums import ExchangeStatus

class ExchangeItem(BaseModel):
    item_id: str
    quantity: int
    new_size: str
    reason: str

class ExchangeRequest(BaseModel):
    exchange_id: str
    order_id: str
    customer_id: str
    status: ExchangeStatus
    items: List[ExchangeItem]
    created_at: datetime
