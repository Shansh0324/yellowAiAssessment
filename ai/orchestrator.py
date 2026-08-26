import json
from ai.client import AIClient
from ai.tool_schemas import AGENT_TOOLS
from services.conversation.service import ConversationService
from tools.order_tools import get_order, get_customer_orders
from tools.policy_tools import search_policy
from tools.return_tools import check_return_eligibility, create_return
from tools.escalation_tools import escalate_to_human
import os

class AgentOrchestrator:
    def __init__(self, conversation_service: ConversationService):
        self.client = AIClient()
        self.conversation_service = conversation_service
        self.max_tool_calls = 8
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system.md")
        try:
            with open(prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful customer support agent for Trendly."

    async def handle_message(self, session_id: str, customer_id: str, user_message: str) -> str:
        # Load or create session
        session = await self.conversation_service.get_or_create_session(session_id, customer_id)
        
        # Add user message
        await self.conversation_service.add_message(session_id, "user", user_message)

        # Build messages for LLM
        system_content = self.system_prompt + f"\n\nCURRENT CONTEXT:\n- Customer ID: {customer_id}\n- Session ID: {session_id}"
        messages = [{"role": "system", "content": system_content}]
        for msg in session.messages:
            messages.append({"role": msg.role, "content": msg.content})
            
        # Append the new user message to the LLM context!
        messages.append({"role": "user", "content": user_message})

        tool_call_count = 0

        while tool_call_count < self.max_tool_calls:
            # Call LLM
            response_msg = await self.client.chat_completion(messages, tools=AGENT_TOOLS)
            
            if isinstance(response_msg, dict) and "error" in response_msg:
                return f"I'm sorry, I'm experiencing technical difficulties: {response_msg['error']}"
            
            # If the model didn't call any tools, it's a final response
            if not getattr(response_msg, "tool_calls", None):
                final_content = response_msg.content or ""
                # Strip markdown asterisks and other formatting elements to enforce plain text
                final_content = final_content.replace("**", "").replace("--", "").replace("###", "")
                
                await self.conversation_service.add_message(session_id, "assistant", final_content)
                return final_content
            
            # Handle tool calls
            messages.append({"role": "assistant", "tool_calls": [t.model_dump() for t in response_msg.tool_calls]})
            
            for tool_call in response_msg.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                await self.conversation_service.add_tool_call(session_id, tool_name, arguments)
                
                # Execute tool (Simple dispatch for demo)
                result_str = ""
                try:
                    if tool_name == "get_order":
                        result_str = get_order(arguments["order_id"], arguments["customer_id"])
                    elif tool_name == "get_customer_orders":
                        result_str = get_customer_orders(arguments["customer_id"])
                    elif tool_name == "search_policy":
                        result_str = search_policy(arguments["query"])
                    elif tool_name == "check_return_eligibility":
                        result_str = check_return_eligibility(arguments["order_id"], arguments["customer_id"], arguments["item_id"])
                    elif tool_name == "create_return":
                        result_str = create_return(arguments["order_id"], arguments["customer_id"], arguments["items_to_return"])
                    elif tool_name == "escalate_to_human":
                        result_str = escalate_to_human(
                            arguments["session_id"], arguments["customer_id"], 
                            arguments["reason"], arguments["summary"], 
                            arguments.get("actions_taken", [])
                        )
                    else:
                        result_str = json.dumps({"error": f"Tool {tool_name} not implemented."})
                except Exception as e:
                    result_str = json.dumps({"error": str(e)})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result_str
                })
            
            tool_call_count += 1
            
        return "I'm sorry, but it seems I'm stuck trying to resolve your request. I will escalate this to a human agent."
