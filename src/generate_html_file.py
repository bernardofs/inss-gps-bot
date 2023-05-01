from bs4 import BeautifulSoup
import re
from .fill_month_and_value import MONTH_TO_PAY


def generate_html_file(response):
  # Generate the PDF file from the GPS gotten in a HTML response.
  print("[7/8] Generating html file")

  # Remove all <img> tags because it generates an error when converting to PDF.
  gps = re.sub("(<img.*?>)", "", response.content.decode("utf-8"), 0,
               re.IGNORECASE | re.DOTALL | re.MULTILINE)

  soup = BeautifulSoup(gps, features="html.parser")

  # Add tag to support unicode characters
  soup.head.insert(0, soup.new_tag('meta', charset='utf-8'))

  payer_name = str(soup.find(
      "td", attrs={"colspan": "2", "rowspan": "3", "valign": "top"}
  )).split("<br/>")[2].title()
  # Remove HTML comment from the name
  payer_name = re.sub(r"(<!--.*?-->|\n)", "", payer_name)

  payment_value = soup.find(
      lambda tag: tag.name == "font" and " 11 - TOTAL" in tag.text
  ).parent.parent.select("tr > td")[1].text

  barcode = soup.find(
      "input", attrs={"id": "linhaDigitavelCompleta1"}
  )["value"]

  barcode = re.sub(r"[\s-]+", "", barcode)
  print(f"Barcode: {barcode}")

  MONTH_TO_PAY_FORMATTED_TO_FILE = MONTH_TO_PAY.strftime(
      "%m/%Y"
  ).replace("/", "_")

  HTML_FILENAME = f"/tmp/guia_de_pagamento_{MONTH_TO_PAY_FORMATTED_TO_FILE}.html"

  with open(HTML_FILENAME, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

  return payer_name, payment_value, barcode, HTML_FILENAME
