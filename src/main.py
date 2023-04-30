import time
import traceback
from .generate_gps import generate_gps
from .pass_confirmation import pass_confirmation
from .fill_initial_data import fill_initial_data
from .fill_month_and_value import fill_month_and_value
from .check_all_checkboxes import check_all_checkboxes
from .generate_html_file import generate_html_file
from .get_info_to_make_requests import get_info_to_make_requests
from .send_email_sendgrid import send_error_message, send_success_message


def execute():
  TRIES = 5

  for tries in range(1, TRIES + 1):
    print(f"Attempt {tries}")

    try:
      response, JSESSIONID = fill_initial_data()

      headers, cookies = get_info_to_make_requests(JSESSIONID)

      response = pass_confirmation(response, headers, cookies)

      response, inss_ceil_value = fill_month_and_value(
          response, headers, cookies
      )

      response = check_all_checkboxes(response, headers, cookies)

      response = generate_gps(response, headers, cookies)

      payer_name, payment_value, barcode, html_filename = generate_html_file(
          response
      )

      send_success_message(
          payer_name, inss_ceil_value, payment_value, barcode, html_filename
      )

    except Exception:
      print("An error has occurred")
      traceback.print_exc()
      if tries != TRIES:
        # Wait a little bit until execute the scrapping again.
        time.sleep(60)

    else:
      return (
          "O programa foi executado com sucesso!"
          " Por favor, verifique o email cadastrado para baixar a guia."
      )

  send_error_message()
  return "Algum erro ocorreu durante a execução do programa."
