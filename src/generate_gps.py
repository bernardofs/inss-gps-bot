import requests
from bs4 import BeautifulSoup


def generate_gps(response, headers, cookies):
  # Request to generate GPS.
  print('[6/8] Requesting to generate GPS')

  GENERATE_GPS_BUTTON_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={'value': 'Gerar GPS'})['name']

  VIEW_STATE = BeautifulSoup(response, features="html.parser").find(
      attrs={'name': 'javax.faces.ViewState'})['value']

  DTPINFRA_TOKEN = BeautifulSoup(response, features="html.parser").find(
      attrs={'name': 'DTPINFRA_TOKEN'})['value']

  data = f'formExibirDiscriminativoCI=formExibirDiscriminativoCI' \
      f'&DTPINFRA_TOKEN={DTPINFRA_TOKEN}' \
      f'&gridListSalariosCalculo:selected=0' \
      f'&{GENERATE_GPS_BUTTON_NAME}=Gerar+GPS' \
      f'&javax.faces.ViewState={VIEW_STATE}'

  response = requests.post('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/exibirDiscriminativoApos.xhtml',
                           headers=headers, cookies=cookies, data=data)

  return response
