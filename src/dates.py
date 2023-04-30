import datetime


def first_weekday_from_now():
  # The date of payment can't be on weekends.
  date = datetime.date.today()
  while date.weekday() in [5, 6]:
    date += datetime.timedelta(days=1)
  return date


def month_to_pay():
  # First month available to pay if we pay today.
  # From 16 of the current month to 15 of the next month.
  date = datetime.date.today()
  if date.day <= 15:
    date -= datetime.timedelta(days=20)
  return date


def month_and_year_written_out(month, year):
  month_name = {
      "1": "Janeiro",
      "2": "Fevereiro",
      "3": "Março",
      "4": "Abril",
      "5": "Maio",
      "6": "Junho",
      "7": "Julho",
      "8": "Agosto",
      "9": "Setembro",
      "10": "Outubro",
      "11": "Novembro",
      "12": "Dezembro"
  }
  return f"{month_name[str(month)]} de {str(year)}"
