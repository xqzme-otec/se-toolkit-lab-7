import os
from dotenv import load_dotenv

# Загружаем .env.bot.secret если есть, иначе .env
load_dotenv(".env.bot.secret", override=True)
load_dotenv(".env", override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:8000")
LMS_API_KEY = os.getenv("LMS_API_KEY", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# Для тестового режима проверяем только LMS, Telegram не нужен
def validate_lms_config() -> bool:
    return bool(LMS_API_BASE_URL and LMS_API_KEY)