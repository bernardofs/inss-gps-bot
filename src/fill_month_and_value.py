from constants import PAYMENT_CODE
import dates
from get_inss_ceil_value import get_inss_ceil_value
import requests
from bs4 import BeautifulSoup

# Payments can't be done on weekends.
PAYMENT_DAY = dates.first_weekday_from_now()

# First month available to pay without taxes if we pay today.
MONTH_TO_PAY = dates.month_to_pay()


def fill_month_and_value(response, headers, cookies):
  # Get INSS ceil value and request the payment of it.

  INSS_CEIL_VALUE = get_inss_ceil_value(
      response, headers, cookies, MONTH_TO_PAY, PAYMENT_DAY
  )

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

  # Request the GPS for a salary equal to the INSS ceil.
  data = f'informarSalariosContribuicaoDomestico=informarSalariosContribuicaoDomestico' \
      f'&DTPINFRA_TOKEN={DTPINFRA_TOKEN}' \
      f'&{MONTH_OF_PAYMENT_FIELD_NAME}={MONTH_TO_PAY:%m/%Y}' \
      f'&{VALUE_TO_PAY_FIELD_NAME}={INSS_CEIL_VALUE}' \
      f'&informarSalariosContribuicaoDomestico:selCodigoPagamento={PAYMENT_CODE}' \
      f'&informarSalariosContribuicaoDomestico:dataPag={PAYMENT_DAY:%d/%m/%Y}'\
      f'&{CONFIRM_BUTTON_NAME}=Confirmar'\
      f'&javax.faces.ViewState={VIEW_STATE}'

  response = requests.post('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/informarSalariosContribuicaoApos.xhtml',
                           headers=headers, cookies=cookies, data=data)

  return response.content, INSS_CEIL_VALUE
