import datetime
from calendar import monthrange

ONE_DAY = datetime.timedelta(days=1)


def last_day_to_pay():
  # The last day to pay a month X is always the day 15 of the next month.
  # The due date should be on the same month/year of the date the GPS is generated.
  date = datetime.date.today()
  if date.day <= 15:
    date = date.replace(day=15)
  else:
    date = date.replace(day=monthrange(date.year, date.month)[1])
  return date


def first_working_day_before_limit(date):
  # The date of payment can't be on weekends.
  while date.weekday() in [5, 6]:
    date -= ONE_DAY
  return date


def month_to_pay(FIRST_WORKING_DAY_BEFORE_LIMIT):
  # Find the first month available to pay without taxes if we pay today.
  ONE_MONTH = datetime.timedelta(days=28)
  month_to_pay = FIRST_WORKING_DAY_BEFORE_LIMIT - ONE_MONTH
  return month_to_pay
