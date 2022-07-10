import pickle
import os
import sys
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']


def gmail_authenticate():
  creds = None
  PREFIX_PATH = 'auth/'
  if './src' in sys.path:
    PREFIX_PATH = './src/' + PREFIX_PATH
  # the file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time
  if os.path.exists(PREFIX_PATH + "token.pickle"):
    with open(PREFIX_PATH + "token.pickle", "rb") as token:
      creds = pickle.load(token)
  # if there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          PREFIX_PATH + "credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # save the credentials for the next run
    with open(PREFIX_PATH + "token.pickle", "wb") as token:
      pickle.dump(creds, token)
  return build('gmail', 'v1', credentials=creds)
