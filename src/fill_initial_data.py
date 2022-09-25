import time
import os
from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from twocaptcha import TwoCaptcha


def open_browser():
  options = webdriver.ChromeOptions()
  options.binary_location = '/opt/chrome/chrome'
  options.add_argument('--headless')
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument('--no-sandbox')
  options.add_argument("--single-process")

  return webdriver.Chrome("/opt/chromedriver", options=options)


# Function that setup the browser parameters and return browser object.
def fill_initial_data():
  print('[1/8] Filling initial data')
  # Confirm that the NIT number is valid using selenium in Chrome
  driver = open_browser()

  driver.delete_all_cookies()
  driver.set_page_load_timeout(60)

  driver.get('http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml')
  time.sleep(2)

  category_selector = Select(driver.find_element(
      'xpath', '//*[@id="opcoesCalcContribuicoesCI:categoria"]'))
  category_selector.select_by_visible_text(os.getenv('INSS_CATEGORY'))

  NIT_field = driver.find_element(
      'xpath', '//*[@id="opcoesCalcContribuicoesCI:nome"]')
  NIT_field.click()
  NIT_field.send_keys(os.getenv('NIT'))

  # Solve Captcha using 2Captcha (https://2captcha.com)
  solver = TwoCaptcha(os.getenv('CP_API_KEY'))
  captcha_img = driver.find_element('xpath', '//*[@id="captcha_challenge"]')
  captcha_img.screenshot('/tmp/captcha.png')

  # Get result from printed image
  captcha_result = solver.normal('/tmp/captcha.png')

  captcha_field = driver.find_element(
      'xpath', '//*[@id="captcha_campo_resposta"]')
  captcha_field.click()
  captcha_field.send_keys(captcha_result['code'])

  confirm_button = driver.find_element(
      'xpath', '//*[@id="opcoesCalcContribuicoesCI:botaoConfirmar"]')
  confirm_button.click()

  time.sleep(1)

  os.remove('/tmp/captcha.png')

  # Check whether the app has passed the captcha verification or not
  if driver.find_elements('xpath', '/html/body/div[1]/div[3]/ul/li'):
    raise Exception(driver.find_element(
        'xpath', '/html/body/div[1]/div[3]/ul/li').text)

  # Find request to get [JSESSIONID] from cookies
  REQUEST_URL = 'PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml'
  table_request = next((request for request in driver.requests if request.method == 'POST'
                        and REQUEST_URL in request.url), None)

  JSESSIONID = table_request.response.headers['Set-Cookie'].split(
      ';')[0].replace('JSESSIONID=', '')

  driver.close()
  return (table_request.response.body, JSESSIONID)
