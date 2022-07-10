from bs4 import BeautifulSoup
import re
import requests

from constants import PAYMENT_CODE


def get_inss_ceil_value(response, headers, cookies, MONTH_TO_PAY_FORMATTED,
                        FIRST_WORKING_DAY_BEFORE_LIMIT_FORMATTED):
  # Get the INSS ceil value by requesting the payment of a very large amount of money.
  # This returns an error in the screen which shows the ceil value for the INSS. We
  # can use the error message of this field to get the value we want.
  print('[3/8] Getting INSS ceil value')

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

  # Request the GPS for a salary of R$ 100.000,00 (beyond the INSS limit).
  data = f'informarSalariosContribuicaoDomestico=informarSalariosContribuicaoDomestico&DTPINFRA_TOKEN={DTPINFRA_TOKEN}&{MONTH_OF_PAYMENT_FIELD_NAME}={MONTH_TO_PAY_FORMATTED}&{VALUE_TO_PAY_FIELD_NAME}=100.000,00&informarSalariosContribuicaoDomestico:selCodigoPagamento={PAYMENT_CODE}&informarSalariosContribuicaoDomestico:dataPag={FIRST_WORKING_DAY_BEFORE_LIMIT_FORMATTED}&{CONFIRM_BUTTON_NAME}=Confirmar&javax.faces.ViewState={VIEW_STATE}'

  response = requests.post('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/informarSalariosContribuicaoApos.xhtml',
                           headers=headers, cookies=cookies, data=data)

  # Scrap the HTML to get the INSS ceil value from the error message.
  error_text_that_contains_ceil_value = BeautifulSoup(response.content, features="html.parser").find(
      "li", attrs={'class': 'erro'}).get_text()

  INSS_CEIL_VALUE = re.search(
      r"R\$ ([\d,.]+)\.$", error_text_that_contains_ceil_value).groups()[0]

  return INSS_CEIL_VALUE
