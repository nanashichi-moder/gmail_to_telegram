import logging, config, telegram

from emoji import emojize

logger = logging.getLogger(__name__)
bot_token, channel_id = config.load_config()

async def send_to_channel(text: str, attachments: list | None) -> bool: # This function activating bot configurating and sending the text to channel
    logger.info("Sending message to channel") # Эта функция активирует самого бота и от его имени отправляет уже сам текст
    
    # try:
    async with telegram.Bot(token=bot_token) as bot:
        if attachments:
            if len(attachments) == 1:
                file = open(attachments[0], "rb")
                await bot.send_document(chat_id=channel_id, document=file, caption=emojize(text), parse_mode="HTML")
            else:
                await bot.send_message(chat_id=channel_id, text=emojize(text), parse_mode="HTML")
                for attachment in attachments:
                    file = open(attachment, "rb")
                    await bot.send_document(chat_id=channel_id, document=file)
        else:
            await bot.send_message(chat_id=channel_id, text=emojize(text), parse_mode="HTML")
        
    logger.info(f"message '{text}' successfully sent")
    return True
    # except Exception as e:
    #     logger.error("message was NOT sent")
    #     return False