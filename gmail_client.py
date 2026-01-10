import os
import logging
import base64
import traceback

from config import FILES_DIR, logger

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#logger = logging.getLogger(__name__)


#This file is main for comunication with Google service
#Этот файл сделан для связывания с сервисами Google

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailClient:
    
    def __init__(self) -> None:
        self.gmail_service = self.create_gmail_service()
    
    def create_gmail_service(self):
        """
        Функция загружает токен авторизации Google из файла token.json
        и если нет такового - создаёт его, запрашивая у Google необходимые ключи
        """
        logger.info("Initializing Gmail service")

        try:
            creds = None
            if os.path.exists("token.json"): # <- takes cache from token.json
                logger.info("File found. Loading authorisation")
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)

            if not creds or not creds.valid: # <- if there's no token.json - asks google for token
                if creds and creds.expired and creds.refresh_token:
                    logger.warning("Authorisation token expired. Refreshing...")
                    creds.refresh(Request())
                else:
                    logger.warning("Token not cached. Getting token")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                logger.info("Saving new token")
                with open("token.json", "w") as token: #<- creating file token.json
                    token.write(creds.to_json())

            service = build("gmail", "v1", credentials=creds)
            logger.info("Token is valid. Loaded successfully")
            return service
        except Exception:
            logger.error("Something went wrong!")
            return None

    def get_attachments(self, user_id, msg_id):
        """Get and store attachment from Message with given id.

        :param service: Authorized Gmail API service instance.
        :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
        :param msg_id: ID of Message containing attachment.
        """
        try:
            message = self.gmail_service.users().messages().get(userId=user_id, id=msg_id).execute()
            paths = []
            for part in message['payload']['parts']:
                if part['filename']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = self.gmail_service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                        data = att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = part['filename']
                    paths.append(FILES_DIR+path)
                    try:
                        with open(FILES_DIR+path, 'wb') as f:
                            f.write(file_data)
                    except TypeError as e:
                        with open(FILES_DIR+path, 'w') as f:
                            f.write(file_data)
                    except Exception as e:
                        logger.error(f"Something went wrong with attachment: {e} \n {traceback.format_exc()}")

            return paths

        except HttpError as error:
            print(f'An error occurred: {error}')
            logger.error(f'An error occurred: {error}')
        return []

    def get_last_email(self):
        """
        Запрос последнего письма
        returns: last_message: dict - письмо, paths_to_file: list - список путей к файлам
        """
        logger.info("Trying to get last message")

        try:
            message_list = self.gmail_service.users().messages().list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=1,
                q=None
            ).execute() # request list of message
            logger.info("Successfully got list of emails")

            messages = message_list.get("messages", [])
            if not messages: 
                logger.warning("Message NOT found")
                return None, []

            message_id = messages[0]["id"]

            last_message = self.gmail_service.users().messages().get(
                userId="me",
                id=message_id,
                format="full"
            ).execute() # no last message

            paths_to_file = self.get_attachments("me", message_id)
            print(f"Got attachment: {paths_to_file}")
            
            logger.info("Successful message returning")
            return last_message, paths_to_file
        except HttpError:
            logger.error("Message was NOT returned correctly: HTTP error")
            return None, []
        except Exception as e:
            logger.error(f"Message was NOT returned correctly: {e} \n {traceback.format_exc()}")
            return None, []
    
    def get_header(self, headers, name): 
        """Эта функция возвращает отправителя"""
        for h in headers:
            if h["name"].lower() == name.lower():
                logger.info("Successfully got message sender")
                return h["value"]
        logger.error("Message sender was NOT returned. Something went wrong")
        return None
    

gmail_client = GmailClient()
