import os
from pathlib import Path
from dotenv import load_dotenv

# Путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / ".env.bot.secret"

load_dotenv(env_file)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")
LMS_API_KEY = os.getenv("LMS_API_KEY", "my-secret-api-key")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "")
LLM_API_MODEL = os.getenv("LLM_API_MODEL", "")

def validate_lms_config() -> bool:
    return bool(LMS_API_BASE_URL and LMS_API_KEY)
