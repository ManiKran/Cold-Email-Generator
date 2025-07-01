import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Optional: Load from token.json or environment (depends on your flow)
def get_gmail_service(user_token_dict):
    creds = Credentials(
        token=user_token_dict["access_token"],
        refresh_token=user_token_dict["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )
    service = build("gmail", "v1", credentials=creds)
    return service

def create_message(to, subject, body_text):
    message = MIMEText(body_text)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email_via_gmail(to_email, subject, body_text, user_token_dict):
    try:
        service = get_gmail_service(user_token_dict)
        message = create_message(to_email, subject, body_text)
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        return f"Email sent! Message ID: {sent_message['id']}"
    except Exception as e:
        return f"Failed to send email: {e}"