import base64
import sendgrid
import os
from sendgrid.helpers.mail import *
from .dates import *


def encode_html_attachment(html_filename):
  with open(html_filename, "rb") as f:
    encoded_file = base64.b64encode(f.read()).decode()
    f.close()

  attachedFile = Attachment(
      FileContent(encoded_file),
      FileName(html_filename.split("/")[-1]),
      FileType("text/html"),
      Disposition("attachment"),
  )

  return attachedFile


def gen_success_message(payer_name, inss_ceil_value, payment_value, barcode):
  month = month_to_pay()

  subject = f"Guia GPS disponível para pagamento {month:%m/%Y}"
  CATEGORY = os.getenv("INSS_CATEGORY")

  body = (
      f"Contribuinte: {payer_name}\n"
      f"Categoria: {CATEGORY}\n"
      f"Mês: {month:%m/%Y} ({month_and_year_written_out(month.month, month.year)})\n"
      f"Teto INSS: R$ {inss_ceil_value}\n"
      f"Valor: R$ {payment_value}\n"
      f"Código de barras: {barcode}"
  )

  return subject, body


def send_success_message(
    payer_name, inss_ceil_value, payment_value, barcode, html_filename
):
  print("[8/8] Sending success message")
  sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))

  subject, body = gen_success_message(
      payer_name, inss_ceil_value, payment_value, barcode
  )

  mail = Mail(
      Email(os.getenv("SENDER_EMAIL")),
      To(os.getenv("RECIPIENT_EMAIL")),
      subject,
      body,
  )
  mail.attachment = encode_html_attachment(html_filename)

  sg.client.mail.send.post(request_body=mail.get())

  os.remove(html_filename)


def send_error_message():
  print("[ERROR] Sending error message")
  sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))

  subject = "Guia GPS não conseguiu ser gerada"

  API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")

  body = (
      f"Ocorreu algum tipo de erro durante a geração da guia.\n"
      f"Caso esteja tentando gerar a guia num fim de semana no fim do mês, não será possível devido a limitações do site.\n"
      f"Caso deseje, tente requisitar para o bot tentar gerar a guia manualmente entrando no seguinte endereço: {API_GATEWAY_URL}."
  )

  mail = Mail(
      Email(os.getenv("SENDER_EMAIL")),
      To(os.getenv("RECIPIENT_EMAIL")),
      subject,
      body,
  )
  sg.client.mail.send.post(request_body=mail.get())
