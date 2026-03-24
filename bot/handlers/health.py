import httpx
from services.lms_client import LMSClient
from config import LMS_API_BASE_URL, LMS_API_KEY

async def handle_health() -> str:
    client = LMSClient(LMS_API_BASE_URL, LMS_API_KEY)
    try:
        items = await client.get_items()
        return f"✅ Backend is healthy. {len(items)} items available."
    except httpx.ConnectError:
        return f"❌ Backend error: connection refused ({LMS_API_BASE_URL}). Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"❌ Backend error: HTTP {e.response.status_code}. The backend service may be down."
    except Exception as e:
        return f"❌ Backend error: {str(e)}"