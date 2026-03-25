import httpx
from services.lms_client import LMSClient
from typing import Dict, Any

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get all items (labs and tasks)",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_labs",
            "description": "Get list of all available labs",
            "parameters": {"type": "object", "properties": {}, "required": []}
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
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled students",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution histogram for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top learners by average score for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"},
                    "limit": {"type": "integer", "description": "Number of top learners to return", "default": 10}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab (scored >= 60%)",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-01'"}
                },
                "required": ["lab"]
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
        
        elif tool_name == "get_learners":
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.lms_client.base_url}/learners/",
                    headers=self.lms_client.headers
                )
                resp.raise_for_status()
                learners = resp.json()
                return f"Total learners: {len(learners)}"
        
        elif tool_name == "get_scores":
            lab = arguments.get("lab")
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.lms_client.base_url}/analytics/scores?lab={lab}",
                    headers=self.lms_client.headers
                )
                resp.raise_for_status()
                scores = resp.json()
                return f"Scores for {lab}: {scores}"
        
        elif tool_name == "get_timeline":
            lab = arguments.get("lab")
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.lms_client.base_url}/analytics/timeline?lab={lab}",
                    headers=self.lms_client.headers
                )
                resp.raise_for_status()
                timeline = resp.json()
                return f"Timeline for {lab}: {len(timeline)} days of submissions"
        
        elif tool_name == "get_groups":
            lab = arguments.get("lab")
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.lms_client.base_url}/analytics/groups?lab={lab}",
                    headers=self.lms_client.headers
                )
                resp.raise_for_status()
                groups = resp.json()
                if not groups:
                    return f"No group data for {lab}"
                result = f"Groups for {lab}:\n"
                for g in groups:
                    result += f"- {g.get('group')}: {g.get('avg_score')}% ({g.get('students')} students)\n"
                return result
        
        elif tool_name == "get_top_learners":
            lab = arguments.get("lab")
            limit = arguments.get("limit", 5)
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.lms_client.base_url}/analytics/top-learners?lab={lab}&limit={limit}",
                    headers=self.lms_client.headers
                )
                resp.raise_for_status()
                learners = resp.json()
                result = f"Top {limit} learners for {lab}:\n"
                for i, l in enumerate(learners[:limit], 1):
                    result += f"{i}. {l.get('learner_id')}: {l.get('avg_score')}%\n"
                return result
        
        elif tool_name == "get_completion_rate":
            lab = arguments.get("lab")
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.lms_client.base_url}/analytics/completion-rate?lab={lab}",
                    headers=self.lms_client.headers
                )
                resp.raise_for_status()
                rate = resp.json()
                return f"Completion rate for {lab}: {rate.get('completion_rate', 0)}%"
        
        return f"Tool {tool_name} not implemented"
