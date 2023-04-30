import requests
from bs4 import BeautifulSoup


def pass_confirmation(response, headers, cookies):
  # Confirm that the NIT number was typed correctly by looking at the user info linked to it.
  print("[2/8] Confirming data")

  CONFIRM_BUTTON_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={"value": "Confirmar"}
  )["name"]

  VIEW_STATE = BeautifulSoup(response, features="html.parser").find(
      attrs={"name": "javax.faces.ViewState"}
  )["value"]

  DTPINFRA_TOKEN = BeautifulSoup(response, features="html.parser").find(
      attrs={"name": "DTPINFRA_TOKEN"}
  )["value"]

  data = (
      f"DTPINFRA_TOKEN={DTPINFRA_TOKEN}"
      f"&formDadosCadastraisCalcContribuicoesCI=formDadosCadastraisCalcContribuicoesCI"
      f"&{CONFIRM_BUTTON_NAME}=Confirmar"
      f"&javax.faces.ViewState={VIEW_STATE}"
  )

  response = requests.post(
      "https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/exibirDadosCadastraisCIApos.xhtml",
      cookies=cookies,
      headers=headers,
      data=data,
      verify=False,
  )

  return response.content
