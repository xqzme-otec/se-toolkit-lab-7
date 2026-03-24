from services.lms_client import LMSClient
from typing import Dict, Any

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_labs",
            "description": "Get list of all available labs",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task pass rates for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get all items (labs and tasks)",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

class ToolExecutor:
    def __init__(self, lms_client: LMSClient):
        self.lms_client = lms_client
    
    async def execute(self, tool_name: str, arguments: Dict) -> str:
        if tool_name == "get_labs":
            labs = await self.lms_client.get_labs()
            if not labs:
                return "No labs found."
            result = "Available labs:\n"
            for lab in labs:
                result += f"- {lab['title']}\n"
            return result
        
        elif tool_name == "get_pass_rates":
            lab = arguments.get("lab")
            rates = await self.lms_client.get_pass_rates(lab)
            if not rates:
                return f"No data found for {lab}"
            result = f"Pass rates for {lab}:\n"
            for task in rates:
                result += f"- {task['task']}: {task['avg_score']}% ({task['attempts']} attempts)\n"
            return result
        
        elif tool_name == "get_items":
            items = await self.lms_client.get_items()
            labs = [i['title'] for i in items if i.get('type') == 'lab']
            return f"Total items: {len(items)}. Labs: {', '.join(labs[:5])}"
        
        return f"Tool {tool_name} not implemented"