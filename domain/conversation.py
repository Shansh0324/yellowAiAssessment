from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime

class ToolCall(BaseModel):
    tool_name: str
    arguments: dict
    result: Optional[dict] = None
    timestamp: datetime

class Session(BaseModel):
    session_id: str
    customer_id: str
    messages: List[Message]
    tool_calls: List[ToolCall]
    active_order_id: Optional[str] = None
    escalation_status: bool = False
    created_at: datetime
    updated_at: datetime
