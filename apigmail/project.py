from flask import Flask,redirect, url_for, request
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from bs4 import BeautifulSoup
from playsound import playsound
import pyttsx3
import os
import speech_recognition as sr

CLIENT_SECRET_FILE = 'abc.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly']

"""def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

authenticate()"""
app = Flask(__name__)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen_and_execute():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Recognizing...")

            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)

        
    except sr.WaitTimeoutError:
        print("Timeout. No speech detected.")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))




def read_emails():
    """
    Retrieve emails from Gmail inbox
    """
    speak("reading mails")
    listen_and_execute()
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Call the Gmail API to retrieve emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        return 'No messages found.'
    else:
        print("Messages:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            message_data = msg['payload']['headers']
            for values in message_data:
                name = values['name']
               
                if name == 'From':
                    from_name = values['value']
                    speak(from_name)
                if name == 'Subject':
                    subject = values['value']
            if 'parts' in msg['payload']:        
                msg_str = base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data'].encode('ASCII')).decode('utf-8')
                soup = BeautifulSoup(msg_str, 'html.parser')
                body = soup.get_text()
                print(f"From: {from_name}")
                print(f"Subject: {subject}")
            else:
                print("noooooo") 


def delete_last_message_from_sender(sender_name):
    """
    Retrieve emails from Gmail inbox and delete the last message from a specific sender
    """
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Call the Gmail API to retrieve emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        return 'No messages found.'

    last_message_id = None
    flag=1
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        message_data = msg['payload']['headers']
        for values in message_data:
            name = values['name']
          
            if name == 'From':
                from_name = values['value']
                print(from_name)
                # Check if the sender matches the specified sender name
                if sender_name in from_name:

                    last_message_id = message['id']
                    flag=0
                    break
        if(flag==0):
            break        
    if last_message_id:
        # Delete the last message from the sender
        service.users().messages().delete(userId='me', id=last_message_id).execute()
        return f"Last message from {sender_name} deleted successfully!"
    else:
        return f"No messages found from {sender_name}."



def search_email(sender_name):
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Call the Gmail API to retrieve emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        return 'No messages found.'
    flag=1
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        message_data = msg['payload']['headers']
        for values in message_data:
            name = values['name']
          
            if name == 'From':
                from_name = values['value']
              
                if sender_name in from_name:

                    
                    flag=0
                    break
        if(flag==0):
            break    
    if(flag==0):
        speak("yes there is") 
    else:
        speak("no message")     

def create_draft_email():
    """
    Create a draft email using Gmail API
    """
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = 'This is a draft email.'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'aanittantony@gmail.com'
    mimeMessage['subject'] = 'Draft Email'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    draft = {
        'message': {
            'raw': raw_string
        }
    }

    draft = service.users().drafts().create(userId='me', body=draft).execute()
    return 'Draft email created successfully!' 







@app.route('/send')
def send_email():
    """
    Send email using Gmail API
    """
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = 'You won kkjhjkh'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'vmail456345@gmail.com'
    mimeMessage['subject'] = 'You weree'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    return 'Email sent successfully!'

@app.route('/read')

def read():
    read_emails()


@app.route('/')

def hw():
   return "helloworld"
  

@app.route('/delete') 
      
def delete():
    sender_name = "vmail456345@gmail.com"
    result = delete_last_message_from_sender(sender_name)
    return result

@app.route('/search') 
      
def search():
    sender_name = "noreply@jobalertshub.com"
    search_email(sender_name)

@app.route('/draft')
def draftemail():
    result = create_draft_email()
    return result
    


if __name__ == '__main__':
    app.run()
