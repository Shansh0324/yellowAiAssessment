from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    customer_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    message: str
    status: str = "completed"
