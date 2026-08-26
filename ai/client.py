import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AIClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("LLM_MODEL", "mistral-large-latest")
        
        # Auto-detect base URL based on which key is provided
        base_url = "https://api.mistral.ai/v1" if os.getenv("MISTRAL_API_KEY") else "https://openrouter.ai/api/v1"

        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Trendly Support Agent",
            }
        )

    async def chat_completion(self, messages: list[dict], tools: list[dict] = None) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else "none"
            )
            return response.choices[0].message
        except Exception as e:
            return {"error": str(e)}
