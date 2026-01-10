from dotenv import load_dotenv
import os, logging

load_dotenv() # <- needs to load API and keys correctly / нужно чтобы загрузить все ключи корректно
logger = logging.getLogger(__name__)

FILES_DIR = "files/"

def load_config():
    logger.info("Loading telegram config")
    if os.path.exists(".env"):
        logger.info("File found: loading...")
        return os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHANNEL_ID")
    else:
        logger.error("File '.env' did NOT found")
        return None, None
    
# Main function for loading API and ID of telegram bot or telegram channel keys from .env file
# Функция загружает ключи телеграмма (бота и чата) из файла .env