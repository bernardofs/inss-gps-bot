import requests
from bs4 import BeautifulSoup


def pass_confirmation(session, response):
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

  data = {
      "DTPINFRA_TOKEN": DTPINFRA_TOKEN,
      "formDadosCadastraisCalcContribuicoesCI": "formDadosCadastraisCalcContribuicoesCI",
      CONFIRM_BUTTON_NAME: "Confirmar",
      "javax.faces.ViewState": VIEW_STATE,
  }

  response = session.post(
      "https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/exibirDadosCadastraisCIApos.xhtml",
      data=data,
      verify=False,
  )

  return response.content
