from bs4 import BeautifulSoup
import re
from .fill_month_and_value import MONTH_TO_PAY


def generate_html_file(response):
  # Generate the PDF file from the GPS gotten in a HTML response.
  print('[7/8] Generating html file')

  # Remove all <img> tags because it generates an error when converting to PDF.
  gps = re.sub("(<img.*?>)", "", response.content.decode('ISO-8859-1'), 0,
               re.IGNORECASE | re.DOTALL | re.MULTILINE)

  payer_name = str(BeautifulSoup(gps, features="html.parser").find(
      'td', attrs={"colspan": "2", "rowspan": "3", "valign": "top"}
  )).split('<br/>')[2].title()

  payment_value = BeautifulSoup(gps, features="html.parser").find(
      lambda tag: tag.name == "font" and " 11 - TOTAL" in tag.text).parent.parent.select('tr > td')[1].text

  barcodes = BeautifulSoup(gps, features="html.parser").findAll("input",
                                                                attrs={'size': '13'}, limit=4)

  barcodes = [code['value'].replace('-', '') for code in barcodes]
  barcode = ''.join(barcodes)
  print(f'Barcode: {barcode}')

  MONTH_TO_PAY_FORMATTED_TO_FILE = MONTH_TO_PAY.strftime(
      '%m/%Y'
  ).replace('/', '_')

  HTML_FILENAME = f'/tmp/guia_de_pagamento_{MONTH_TO_PAY_FORMATTED_TO_FILE}.html'

  file = open(HTML_FILENAME, 'w')
  file.write(gps)
  file.close()

  return payer_name, payment_value, barcode, HTML_FILENAME
