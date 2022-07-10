import pickle
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']


def gmail_authenticate():
  creds = None
  # the file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time
  if os.path.exists("./src/auth/token.pickle"):
    with open("./src/auth/token.pickle", "rb") as token:
      creds = pickle.load(token)
  # if there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./src/auth/credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # save the credentials for the next run
    with open("./src/auth/token.pickle", "wb") as token:
      pickle.dump(creds, token)
  return build('gmail', 'v1', credentials=creds)
