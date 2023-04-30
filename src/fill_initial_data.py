import os
from twocaptcha import TwoCaptcha
from bs4 import BeautifulSoup


# Function that setup the browser parameters and return browser object.
def fill_initial_data(session):
  print("[1/8] Filling initial data")

  response = session.get(
      "https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml",
      verify=False,
  )

  VIEW_STATE = BeautifulSoup(response.text, features="html.parser").find(
      attrs={"name": "javax.faces.ViewState"}
  )["value"]

  DTPINFRA_TOKEN = BeautifulSoup(response.text, features="html.parser").find(
      attrs={"name": "DTPINFRA_TOKEN"}
  )["value"]

  RECAPTCHA_SITE_KEY = BeautifulSoup(response.text, features="html.parser").find(
      attrs={"class": "g-recaptcha"}
  )["data-sitekey"]

  # Solve Captcha using 2Captcha (https://2captcha.com)
  solver = TwoCaptcha(os.getenv("CP_API_KEY"))
  rechaptcha_code = solver.recaptcha(
      sitekey=RECAPTCHA_SITE_KEY,
      url="https://sal.rfb.gov.br/PortalSalInternet/faces/page-s/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml",
  )["code"]

  data = {
      "opcoesCalcContribuicoesCI": "opcoesCalcContribuicoesCI",
      "DTPINFRA_TOKEN": DTPINFRA_TOKEN,
      "opcoesCalcContribuicoesCI:categoria": os.getenv("INSS_CATEGORY"),
      "opcoesCalcContribuicoesCI:nome": os.getenv("NIT"),
      "opcoesCalcContribuicoesCI:botaoConfirmar": "Confirmar",
      "g-recaptcha-response": rechaptcha_code,
      "javax.faces.ViewState": VIEW_STATE,
  }

  response = session.post(
      "https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml",
      data=data,
      verify=False,
  )

  return response.content
