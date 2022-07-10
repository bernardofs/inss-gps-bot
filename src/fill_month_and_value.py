import datetime
from constants import PAYMENT_CODE
import meaningful_dates as md
from get_inss_ceil_value import get_inss_ceil_value
import requests
from bs4 import BeautifulSoup

# Closest non-weekend day before the limit (payments can't be done on weekends).
FIRST_WORKING_DAY_BEFORE_LIMIT = md.first_working_day_before_limit(
    md.last_day_to_pay()
)

FIRST_WORKING_DAY_BEFORE_LIMIT_FORMATTED = FIRST_WORKING_DAY_BEFORE_LIMIT.strftime(
    '%d/%m/%Y'
)

# First month available to pay without taxes if we pay today.
MONTH_TO_PAY = md.month_to_pay(FIRST_WORKING_DAY_BEFORE_LIMIT)

MONTH_TO_PAY_FORMATTED = MONTH_TO_PAY.strftime('%m/%Y')


def fill_month_and_value(response, headers, cookies):
  # Get INSS ceil value and request the payment of it.

  INSS_CEIL_VALUE = get_inss_ceil_value(
      response, headers, cookies, MONTH_TO_PAY_FORMATTED, FIRST_WORKING_DAY_BEFORE_LIMIT_FORMATTED)

  print('[4/8] Writing month and value to pay')
  MONTH_OF_PAYMENT_FIELD_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={'class': 'center competenciaFormat'})['name']

  VALUE_TO_PAY_FIELD_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={'class': 'right moedaFormat'})['name']

  CONFIRM_BUTTON_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={'value': 'Confirmar'})['name']

  VIEW_STATE = BeautifulSoup(response, features="html.parser").find(
      attrs={'name': 'javax.faces.ViewState'})['value']

  DTPINFRA_TOKEN = BeautifulSoup(response, features="html.parser").find(
      attrs={'name': 'DTPINFRA_TOKEN'})['value']

  if datetime.date.today() > FIRST_WORKING_DAY_BEFORE_LIMIT:
    raise Exception("The last day available to pay has passed.")

  # Request the GPS for a salary equal to the INSS ceil.
  data = f'informarSalariosContribuicaoDomestico=informarSalariosContribuicaoDomestico&DTPINFRA_TOKEN={DTPINFRA_TOKEN}&{MONTH_OF_PAYMENT_FIELD_NAME}={MONTH_TO_PAY_FORMATTED}&{VALUE_TO_PAY_FIELD_NAME}={INSS_CEIL_VALUE}&informarSalariosContribuicaoDomestico:selCodigoPagamento={PAYMENT_CODE}&informarSalariosContribuicaoDomestico:dataPag={FIRST_WORKING_DAY_BEFORE_LIMIT_FORMATTED}&{CONFIRM_BUTTON_NAME}=Confirmar&javax.faces.ViewState={VIEW_STATE}'

  response = requests.post('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/informarSalariosContribuicaoApos.xhtml',
                           headers=headers, cookies=cookies, data=data)

  return response.content
