from bs4 import BeautifulSoup
import re
from fill_month_and_value import MONTH_TO_PAY_FORMATTED


def generate_html_file(response):
  # Generate the PDF file from the GPS gotten in a HTML response.
  print('[7/8] Generating html file')

  # Remove all <img> tags because it generates an error when converting to PDF.
  gps = re.sub("(<img.*?>)", "", response.content.decode('ISO-8859-1'), 0,
               re.IGNORECASE | re.DOTALL | re.MULTILINE)

  barcodes = BeautifulSoup(gps, features="html.parser").findAll("input",
                                                                attrs={'size': '13'}, limit=4)

  barcodes = [code['value'].replace('-', '') for code in barcodes]
  barcode = ''.join(barcodes)
  print(f'Barcode: {barcode}')

  MONTH_TO_PAY_FORMATTED_TO_FILE = MONTH_TO_PAY_FORMATTED.replace('/', '_')

  HTML_FILENAME = f'guia_de_pagamento_{MONTH_TO_PAY_FORMATTED_TO_FILE}.html'

  file = open(HTML_FILENAME, 'w')
  file.write(gps)
  file.close()

  return barcode, HTML_FILENAME
