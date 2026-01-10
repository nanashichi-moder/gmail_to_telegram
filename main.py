import logging
import config
import asyncio

from logging_config import setup_logging

setup_logging() #For logs to work correctly / Чтобы логи работали так как мы хотим

from telegram_client import send_to_channel
from gmail_client import gmail_client
from cache import load_cache, save_cache


logger = logging.getLogger(__name__)
token, channel_id = config.load_config()  # <- from file config.py getting keys for function / Берём с помощью файла config.py ключи телеграмма
# logger.warning(f"TOKEN = *****{token[5:]}, CHANNEL = *****{channel_id[5:]}")  # <<---- There's no need to enable this. Just to check if tokens are working well

async def main():
    while True:
        # Main programm function. It is getting cache and email. / Главная функция. Берёт весь кеш и само сообщение, также отправителя
        cache = load_cache()
        email, attachments_paths = gmail_client.get_last_email()
        print("Got email", email, attachments_paths)
        if email:
            from_header = gmail_client.get_header(email["payload"]["headers"], "From")
            # print(email)
            # for k in email["payload"]:
            #     print(k, email["payload"][k], '\n\n')
            # print("PAYLOAD:", email["payload"]["headers"])
            # print("SUBJECT:", get_header(email["payload"]["headers"], "Subject"))
            # if email and email["id"] != cache["last_email_id"]: # if email was not already sent
            #     logger.info("New message found -> sending to Telegram")
            #     await send_to_channel(from_header) # sending the sender
            #     await send_to_channel(email["snippet"]) # sending the message (different message)
            #     cache["last_email_id"] = email["id"] 
            #     save_cache(cache) # saving mail ID
            # else:
        logger.warning("No new email found")
        await asyncio.sleep(5)

if __name__ == "__main__": #Main function activation

    asyncio.run(main())