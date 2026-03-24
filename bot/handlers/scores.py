import httpx
from services.lms_client import LMSClient
from config import LMS_API_BASE_URL, LMS_API_KEY

async def handle_scores(lab: str = None) -> str:
    if not lab:
        return "Usage: /scores <lab-name>\nExample: /scores lab-01"
    
    client = LMSClient(LMS_API_BASE_URL, LMS_API_KEY)
    try:
        rates = await client.get_pass_rates(lab)
        if not rates:
            return f"No data found for {lab}"
        
        result = f"📊 Pass rates for {lab}:\n"
        for task in rates:
            result += f"• {task.get('task')}: {task.get('avg_score')}% ({task.get('attempts')} attempts)\n"
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 422:
            return f"Lab '{lab}' not found. Check available labs with /labs"
        return f"❌ Failed to fetch scores: HTTP {e.response.status_code}"
    except Exception as e:
        return f"❌ Failed to fetch scores: {str(e)}"
