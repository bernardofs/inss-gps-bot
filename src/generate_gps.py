from bs4 import BeautifulSoup


def generate_gps(session, response):
  # Request to generate GPS.
  print("[6/8] Requesting to generate GPS")

  GENERATE_GPS_BUTTON_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={"value": "Gerar GPS"}
  )["name"]

  VIEW_STATE = BeautifulSoup(response, features="html.parser").find(
      attrs={"name": "javax.faces.ViewState"}
  )["value"]

  DTPINFRA_TOKEN = BeautifulSoup(response, features="html.parser").find(
      attrs={"name": "DTPINFRA_TOKEN"}
  )["value"]

  data = {
      "formExibirDiscriminativoCI": "formExibirDiscriminativoCI",
      "DTPINFRA_TOKEN": DTPINFRA_TOKEN,
      "gridListSalariosCalculo:selected": 0,
      GENERATE_GPS_BUTTON_NAME: "Gerar+GPS",
      "javax.faces.ViewState": VIEW_STATE,
  }

  response = session.post(
      "https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/exibirDiscriminativoApos.xhtml",
      data=data,
      verify=False,
  )

  return response
