from fastapi import APIRouter, HTTPException
from apps.api.routes.models import ChatRequest, ChatResponse
from ai.orchestrator import AgentOrchestrator
from services.conversation.service import ConversationService

router = APIRouter()
conversation_service = ConversationService()
orchestrator = AgentOrchestrator(conversation_service)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    response_text = await orchestrator.handle_message(
        session_id=request.session_id,
        customer_id=request.customer_id,
        user_message=request.message
    )
    
    return ChatResponse(
        session_id=request.session_id,
        message=response_text
    )

@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    session_doc = await conversation_service.get_session(session_id)
    if not session_doc:
        return {"error": "Session not found"}
    # Convert ObjectId to string to avoid serialization issues
    if "_id" in session_doc:
        session_doc["_id"] = str(session_doc["_id"])
    return session_doc

@router.get("/sessions/customer/{customer_id}")
async def get_customer_sessions(customer_id: str):
    sessions = await conversation_service.get_sessions_by_customer(customer_id)
    return {"sessions": sessions}

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    success = await conversation_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "success", "message": "Session deleted"}
