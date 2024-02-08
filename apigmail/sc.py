from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from bs4 import BeautifulSoup

CLIENT_SECRET_FILE = 'abc.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    """
    Authenticate with Gmail API using OAuth 2.0
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def send_email():
    """
    Send email using Gmail API
    """
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = 'You won kkjhjkh'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'vmail456345@gmail.com'
    mimeMessage['subject'] = 'You won'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print("Email sent successfully!")

def read_emails():
    """
    Retrieve emails from Gmail inbox
    """
   
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Call the Gmail API to retrieve emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        print("Messages:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            message_data = msg['payload']['headers']
            for values in message_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value']
                if name == 'Subject':
                    subject = values['value']
            msg_str = base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data'].encode('ASCII')).decode('utf-8')
            soup = BeautifulSoup(msg_str, 'html.parser')
            body = soup.get_text()
            print(f"From: {from_name}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")

if __name__ == '__main__':
    send_email()
    read_emails()
