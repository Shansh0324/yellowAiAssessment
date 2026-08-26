import os
from motor.motor_asyncio import AsyncIOMotorClient
from domain.conversation import Session, Message, ToolCall
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

class ConversationService:
    def __init__(self):
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongodb_uri)
        self.db = self.client.buildhub
        self.sessions = self.db.sessions

    async def get_or_create_session(self, session_id: str, customer_id: str) -> Session:
        doc = await self.sessions.find_one({"session_id": session_id})
        if not doc:
            session = Session(
                session_id=session_id,
                customer_id=customer_id,
                messages=[],
                tool_calls=[],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            await self.sessions.insert_one(session.model_dump())
            return session
        return Session(**doc)

    async def add_message(self, session_id: str, role: str, content: str):
        msg = Message(role=role, content=content, timestamp=datetime.now(timezone.utc))
        await self.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": msg.model_dump()},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )

    async def add_tool_call(self, session_id: str, tool_name: str, arguments: dict):
        tc = ToolCall(
            tool_name=tool_name, 
            arguments=arguments,
            timestamp=datetime.now(timezone.utc)
        )
        await self.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"tool_calls": tc.model_dump()},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )
            
    async def set_active_order(self, session_id: str, order_id: str):
        await self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "active_order_id": order_id,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

    async def get_session(self, session_id: str) -> dict:
        doc = await self.sessions.find_one({"session_id": session_id})
        return doc

    async def get_sessions_by_customer(self, customer_id: str) -> list[dict]:
        cursor = self.sessions.find({"customer_id": customer_id}).sort("updated_at", -1)
        sessions = await cursor.to_list(length=100)
        
        # Format the response to summarize the first message
        result = []
        for s in sessions:
            first_msg = "New Conversation"
            if "messages" in s and len(s["messages"]) > 0:
                # Find the first user message
                for msg in s["messages"]:
                    if msg.get("role") == "user":
                        first_msg = msg.get("content", "New Conversation")
                        break
            
            result.append({
                "session_id": s["session_id"],
                "created_at": s.get("created_at"),
                "updated_at": s.get("updated_at"),
                "summary": first_msg[:50] + "..." if len(first_msg) > 50 else first_msg
            })
        return result

    async def delete_session(self, session_id: str) -> bool:
        result = await self.sessions.delete_one({"session_id": session_id})
        return result.deleted_count > 0
