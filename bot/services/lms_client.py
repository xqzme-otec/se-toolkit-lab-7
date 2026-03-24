import httpx
from typing import List, Dict, Any

class LMSClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def get_items(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/items/", headers=self.headers)
            resp.raise_for_status()
            return resp.json()
    
    async def get_labs(self) -> List[Dict[str, Any]]:
        items = await self.get_items()
        return [item for item in items if item.get("type") == "lab"]
    
    async def get_pass_rates(self, lab: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/analytics/pass-rates?lab={lab}",
                headers=self.headers
            )
            resp.raise_for_status()
            return resp.json()