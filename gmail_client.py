import os
import logging
import base64
import traceback

from bs4 import BeautifulSoup

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

    def get_last_email(self, load_attachments=True):    
        """
        Запрос последнего письма
        returns: last_message: dict - письмо, paths_to_file: list - список путей к файлам
        """
        # TODO: return json, not tuple with message and paths
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
            
            attachments_paths = []
            if load_attachments:
                attachments_paths = self.get_attachments("me", message_id)
                print(f"Got attachment: {attachments_paths}")
                
            logger.info("Successful message returning")
            return last_message, attachments_paths
        except HttpError:
            logger.error("Message was NOT returned correctly: HTTP error")
            return None, []
        except Exception as e:
            logger.error(f"Message was NOT returned correctly: {e} \n {traceback.format_exc()}")
            return None, []
    
    def get_email_body(self, msg_payload):
        """Recursively extracts the plain text body from a message payload."""
        if 'parts' in msg_payload:
            for part in msg_payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    # Can also extract HTML and use BeautifulSoup to get text
                    data = part['body']['data']
                    html_body = base64.urlsafe_b64decode(data).decode('utf-8')
                    return BeautifulSoup(html_body, 'html.parser').get_text()
                elif part['mimeType'].startswith('multipart/'):
                    # Recurse into nested parts
                    result = self.get_email_body(part)
                    if result:
                        return result
        else:
            # Fallback for simple messages or 'snippet' if full body not present
            if msg_payload.get('body', {}).get('data'):
                data = msg_payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
        return ""
        
    def get_last_email_formatted_json(self, 
                                      load_attachments=True, 
                                      return_additional_info=False):
        """Функция возвращает текст письма"""
        logger.info("Trying to get message text")
        msg, attachments_paths = self.get_last_email(load_attachments=load_attachments)
        if not msg:
            logger.error("Message was NOT returned correctly")
            return None
        logger.info("Successfully got message text")
        subject = self.get_header(msg["payload"]["headers"], "Subject")
        sender = self.get_header(msg["payload"]["headers"], "From")
        body = self.get_email_body(msg["payload"])
        # print(f"Got message: {subject} \n {sender} \n {body}")
        result = {"id": msg["id"], "sender": sender, "subject": subject, 
                  "body": body, "attachments": attachments_paths}
        if return_additional_info:
            result["full_message"] = msg
        return result
        
    def get_header(self, msg_headers, name): 
        """Эта функция возвращает отправителя"""
        for h in msg_headers:
            if h["name"].lower() == name.lower():
                logger.info(f"Successfully got message header {name}")
                return h["value"]
        logger.error("Message header NOT FOUND. Something went wrong")
        return None
    

gmail_client = GmailClient()
