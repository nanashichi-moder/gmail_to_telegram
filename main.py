import logging
import config
import asyncio
from emoji import emojize

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
        email = gmail_client.get_last_email_formatted_json()
        print("Got email", email)
        if email:
            # {"sender": sender, "subject": subject, "body": body, "attachments": attachments_paths}
            print(email)
            if email and email["id"] != cache["last_email_id"]: # if email was not already sent
                logger.info("New message found -> sending to Telegram")
                msg_body = email["body"]
                if len(msg_body) > 1000:
                    msg_body = msg_body[:600] + f"... (и еще {len(msg_body) - 600} символов)"
                
                text = f"""
:label: <b>{email["subject"].replace('<', "(").replace('>', ")")}</b>

<i>{email["sender"].replace('<', "(").replace('>', ")")}</i>

<blockquote>
{email["body"].replace('<', "(").replace('>', ")")}
</blockquote>
                """
                await send_to_channel(text=text, attachments=email["attachments"])
                cache["last_email_id"] = email["id"] 
                save_cache(cache) # saving mail ID
        logger.warning("No new email found")
        await asyncio.sleep(15*60)

if __name__ == "__main__": #Main function activation
    asyncio.run(main())