import base64
import sendgrid
import dates
import os
from sendgrid.helpers.mail import *
from constants import *


def encode_html_attachment(html_filename):
  with open(html_filename, 'rb') as f:
    encoded_file = base64.b64encode(f.read()).decode()
    f.close()

  attachedFile = Attachment(
      FileContent(encoded_file),
      FileName(html_filename),
      FileType('text/html'),
      Disposition('attachment')
  )

  return attachedFile


def gen_success_message(payer_name, inss_ceil_value, payment_value, barcode):
  month_to_pay = dates.month_to_pay()

  subject = f'Guia GPS disponível para pagamento {month_to_pay:%m/%Y}'

  body = f'Contribuinte: {payer_name}\n'\
      f'Categoria: {CATEGORY}\n' \
      f'Mês: {month_to_pay:%m/%Y} ({dates.month_and_year_written_out(month_to_pay.month, month_to_pay.year)})\n' \
      f'Teto INSS: R$ {inss_ceil_value}\n' \
      f'Valor: R$ {payment_value}\n' \
      f'Código de barras: {barcode}'

  return subject, body


def send_success_message(payer_name, inss_ceil_value, payment_value, barcode, html_filename):
  print('[8/8] Sending success message')
  sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

  subject, body = gen_success_message(
      payer_name, inss_ceil_value, payment_value, barcode
  )

  mail = Mail(Email(SENDER_EMAIL), To(RECIPIENT_EMAIL), subject, body)
  mail.attachment = encode_html_attachment(html_filename)

  sg.client.mail.send.post(request_body=mail.get())

  os.remove(html_filename)


def send_error_message():
  print('[ERROR] Sending error message')
  sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

  subject = 'Guia GPS não conseguiu ser gerada'

  body = f'Ocorreu algum tipo de erro durante a geração da guia. ' \
      f'Por favor, gere a guia entrando no seguinte endereço: {HEROKU_ADDRESS}.'

  mail = Mail(Email(SENDER_EMAIL), To(RECIPIENT_EMAIL), subject, body)
  sg.client.mail.send.post(request_body=mail.get())
