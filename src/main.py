import traceback
from datetime import date
from constants import DAYS_TO_WORK
from generate_gps import generate_gps
from pass_confirmation import pass_confirmation
from fill_initial_data import fill_initial_data
from fill_month_and_value import fill_month_and_value
from check_all_checkboxes import check_all_checkboxes
from generate_html_file import generate_html_file
from get_info_to_make_requests import get_info_to_make_requests
from send_email import send_error_message, send_message


def execute():

  # The bot is going to work on days present in the array below.
  if date.today().day in DAYS_TO_WORK:
    TRIES = 1

    for tries in range(1, TRIES + 1):
      print(f'Attempt {tries}')

      try:
        response, JSESSIONID = fill_initial_data()

        headers, cookies = get_info_to_make_requests(JSESSIONID)

        response = pass_confirmation(response, headers, cookies)

        response = fill_month_and_value(response, headers, cookies)

        response = check_all_checkboxes(response, headers, cookies)

        response = generate_gps(response, headers, cookies)

        barcode, html_filename = generate_html_file(response)

        send_message(barcode, html_filename)

      except Exception:
        print('An error has occurred')
        traceback.print_exc()

      else:
        return '<h1>Success</h1>The program was successfully executed!<br>Please check your email.', 200

    send_error_message()
    return '<h1>Error</h1>', 500
