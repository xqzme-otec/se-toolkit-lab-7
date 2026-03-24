import httpx
import json
from typing import List, Dict, Any

class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat(self, messages: List[Dict[str, Any]], tools: List[Dict] = None) -> Dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            resp.raise_for_status()
            return resp.json()