import logging, config, telegram

logger = logging.getLogger(__name__)
bot_token, channel_id = config.load_config()

async def send_to_channel(text: str) -> bool: # This function activating bot configurating and sending the text to channel
    logger.info("Sending message to channel") # Эта функция активирует самого бота и от его имени отправляет уже сам текст
    
    try:
        async with telegram.Bot(token=bot_token) as bot:
            await bot.send_message(chat_id=channel_id, text=text)
        logger.info(f"message '{text}' successfully sent")
        return True
    except Exception:
        logger.error("message was NOT sent")
        return False