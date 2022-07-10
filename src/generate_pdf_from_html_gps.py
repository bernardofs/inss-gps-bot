from bs4 import BeautifulSoup
import re
from fill_month_and_value import MONTH_TO_PAY_FORMATTED
import pdfkit


def generate_pdf_from_html_gps(response):
  # Generate the PDF file from the GPS gotten in a HTML response.

  # Remove all <img> tags because it generates an error when converting to PDF.
  gps = re.sub("(<img.*?>)", "", response.content.decode('utf-8'), 0,
               re.IGNORECASE | re.DOTALL | re.MULTILINE)

  barcodes = BeautifulSoup(gps, features="html.parser").findAll("input",
                                                                attrs={'size': '13'}, limit=4)

  barcodes = [code['value'].replace('-', '') for code in barcodes]
  barcode = ''.join(barcodes)
  print(barcode)

  MONTH_TO_PAY_FORMATTED_TO_FILE = MONTH_TO_PAY_FORMATTED.replace('/', ':')

  pdfkit.from_string(
      gps, f'guia_de_pagamento_{MONTH_TO_PAY_FORMATTED_TO_FILE}.pdf')
