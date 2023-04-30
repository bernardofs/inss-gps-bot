import os
import requests
from bs4 import BeautifulSoup
from .dates import *
from .get_inss_ceil_value import get_inss_ceil_value

# Payments can't be done on weekends.
PAYMENT_DAY = first_weekday_from_now()

# First month available to pay without taxes if we pay today.
MONTH_TO_PAY = month_to_pay()


def fill_month_and_value(session, response):
  # Get INSS ceil value and request the payment of it.

  INSS_CEIL_VALUE = get_inss_ceil_value(
      session, response, MONTH_TO_PAY, PAYMENT_DAY
  )

  print("[4/8] Writing month and value to pay")
  MONTH_OF_PAYMENT_FIELD_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={"class": "center competenciaFormat"}
  )["name"]

  VALUE_TO_PAY_FIELD_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={"class": "right moedaFormat"}
  )["name"]

  CONFIRM_BUTTON_NAME = BeautifulSoup(response, features="html.parser").find(
      attrs={"value": "Confirmar"}
  )["name"]

  VIEW_STATE = BeautifulSoup(response, features="html.parser").find(
      attrs={"name": "javax.faces.ViewState"}
  )["value"]

  DTPINFRA_TOKEN = BeautifulSoup(response, features="html.parser").find(
      attrs={"name": "DTPINFRA_TOKEN"}
  )["value"]

  INSS_PAYMENT_CODE = os.getenv("INSS_PAYMENT_CODE")

  # Request the GPS for a salary equal to the INSS ceil.
  data = {
      "informarSalariosContribuicaoDomestico": "informarSalariosContribuicaoDomestico",
      "DTPINFRA_TOKEN": DTPINFRA_TOKEN,
      MONTH_OF_PAYMENT_FIELD_NAME: f"{MONTH_TO_PAY:%m/%Y}",
      VALUE_TO_PAY_FIELD_NAME: INSS_CEIL_VALUE,
      "informarSalariosContribuicaoDomestico:selCodigoPagamento": INSS_PAYMENT_CODE,
      "informarSalariosContribuicaoDomestico:dataPag": f"{PAYMENT_DAY:%d/%m/%Y}",
      CONFIRM_BUTTON_NAME: "Confirmar",
      "javax.faces.ViewState": VIEW_STATE,
  }

  response = requests.post(
      "https://sal.rfb.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/informarSalariosContribuicaoApos.xhtml",
      data=data,
      verify=False,
  )

  return response.content, INSS_CEIL_VALUE
