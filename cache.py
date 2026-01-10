import logging, json

logger = logging.getLogger(__name__)

# This is cache file. It saves cashe to cache.json  .  It is supposed to check email ID and save it simply not to send the same message every 30 minuts
# Файл кеширования. Сохраняет кэш в cache.json  .  Он служит сохранением ID email сообщения чтобы не повторять в чат одно сообщение каждые 30 минут

def load_cache():
    logger.info("Trying to load cache")
    try:
        with open("cache.json", "r") as f:
            data = json.load(f)
        logger.info("Successful load")
        return data
    except Exception:
        logger.error("File loading failed")
        return None, None

def save_cache(data: dict):
    logger.info("Trying to save message to cache")
    try:
        with open("cache.json", "w") as f:
            json.dump(data, f)
        logger.info("Successfully saved")
        return True
    except Exception:
        logger.error("Saving failed!")
        return False