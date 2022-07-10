import os
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
from authenticate_gmail import gmail_authenticate
from constants import CATEGORY, HEROKU_ADDRESS, SENDER_EMAIL, RECIPIENT_EMAIL
from fill_month_and_value import MONTH_TO_PAY_FORMATTED

# Follow the tutorial available on:
# https://www.thepythoncode.com/article/use-gmail-api-in-python


def add_attachment(message, filename):
  # Adds the attachment with the given filename to the given message
  content_type, encoding = guess_mime_type(filename)
  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(filename, 'rb')
    msg = MIMEText(fp.read().decode(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(filename, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(filename, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(filename, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(filename)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)


def build_message(subject, body, attachments=[]):
  if not attachments:  # no attachments given
    message = MIMEText(body)
    message['to'] = RECIPIENT_EMAIL
    message['from'] = SENDER_EMAIL
    message['subject'] = subject
  else:
    message = MIMEMultipart()
    message['to'] = RECIPIENT_EMAIL
    message['from'] = SENDER_EMAIL
    message['subject'] = subject
    message.attach(MIMEText(body))
    for filename in attachments:
      add_attachment(message, filename)
  return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(barcode, html_filename):
  print('[8/8] Sending successful message')

  # Get the Gmail API service
  service = gmail_authenticate()

  SUBJECT = 'Guia GPS disponível para pagamento ' + MONTH_TO_PAY_FORMATTED

  BODY = f'Categoria: {CATEGORY}\nBarcode: {barcode}'

  service.users().messages().send(
      userId="me",
      body=build_message(SUBJECT, BODY, [html_filename])
  ).execute()

  os.remove(html_filename)


def send_error_message():
  print('[ERROR] Sending error message')
  # get the Gmail API service
  service = gmail_authenticate()

  SUBJECT = 'Guia GPS não conseguiu ser gerada'

  BODY = f'Ocorreu algum tipo de erro durante a geração da guia. ' \
      f'Por favor, gere a guia entrando no seguinte endereço: {HEROKU_ADDRESS}.'

  service.users().messages().send(
      userId="me",
      body=build_message(SUBJECT, BODY, [])
  ).execute()
