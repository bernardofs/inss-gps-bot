import requests
from bs4 import BeautifulSoup


def check_all_checkboxes(response, headers, cookies):
  # Check all checkboxes which indicates which filled months should be included on the GPS.
  print('[5/8] Checking checkbox')

  CHECK_ALL_CHECKBOX_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={'value': 'Marcar Todos'})['name']

  VIEW_STATE = BeautifulSoup(response, features="html.parser").find(
      attrs={'name': 'javax.faces.ViewState'})['value']

  DTPINFRA_TOKEN = BeautifulSoup(response, features="html.parser").find(
      attrs={'name': 'DTPINFRA_TOKEN'})['value']

  data = f'formExibirDiscriminativoCI=formExibirDiscriminativoCI&DTPINFRA_TOKEN={DTPINFRA_TOKEN}&{CHECK_ALL_CHECKBOX_NAME}=Marcar+Todos&javax.faces.ViewState={VIEW_STATE}'

  response = requests.post('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/exibirDiscriminativoApos.xhtml',
                           headers=headers, cookies=cookies, data=data)

  return response.content
