from services.lms_client import LMSClient
from config import LMS_API_BASE_URL, LMS_API_KEY

async def handle_labs() -> str:
    client = LMSClient(LMS_API_BASE_URL, LMS_API_KEY)
    try:
        labs = await client.get_labs()
        if not labs:
            return "No labs found."
        result = "📚 Available labs:\n"
        for lab in labs:
            result += f"• {lab['title']}\n"
        return result
    except Exception as e:
        return f"❌ Failed to fetch labs: {str(e)}"