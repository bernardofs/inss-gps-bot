import time
import os
from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from twocaptcha import TwoCaptcha
from constants import API_KEY, CATEGORY, NIT


def fill_initial_data():
  print('[1/8] Filling initial data')
  # Confirm that the NIT number is valid using selenium in Chrome
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  driver = webdriver.Chrome(chrome_options=chrome_options)
#   The code below is necessary to be deployed on Heroku
  driver = webdriver.Chrome(executable_path=os.environ.get(
      "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  driver.get('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml')
  time.sleep(2)

  category_selector = Select(driver.find_element(
      'xpath', '//*[@id="opcoesCalcContribuicoesCI:categoria"]'))
  category_selector.select_by_visible_text(CATEGORY)

  NIT_field = driver.find_element(
      'xpath', '//*[@id="opcoesCalcContribuicoesCI:nome"]')
  NIT_field.click()
  NIT_field.send_keys(NIT)

  # Solve Captcha using 2Captcha (https://2captcha.com)
  solver = TwoCaptcha(API_KEY)
  captcha_img = driver.find_element('xpath', '//*[@id="captcha_challenge"]')
  captcha_img.screenshot('captcha.png')

  # Get result from printed image
  captcha_result = solver.normal('captcha.png')

  captcha_field = driver.find_element(
      'xpath', '//*[@id="captcha_campo_resposta"]')
  captcha_field.click()
  captcha_field.send_keys(captcha_result['code'])

  confirm_button = driver.find_element(
      'xpath', '//*[@id="opcoesCalcContribuicoesCI:botaoConfirmar"]')
  confirm_button.click()

  time.sleep(1)

  # Find request to get [JSESSIONID] from cookies
  REQUEST_URL = 'PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml'
  table_request = next((request for request in driver.requests if request.method == 'POST'
                        and REQUEST_URL in request.url), None)

  JSESSIONID = table_request.response.headers['Set-Cookie'].split(
      ';')[0].replace('JSESSIONID=', '')

  os.remove('captcha.png')
  driver.close()
  return (table_request.response.body, JSESSIONID)
