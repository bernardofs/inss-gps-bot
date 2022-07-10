import datetime

ONE_DAY = datetime.timedelta(days=1)


def last_day_to_pay():
  # The last day to pay a month X is always the day 15 of the next month.
  date = datetime.date.today()
  while date.day != 15:
    date += ONE_DAY
  return date


def first_working_day_before_limit(previous_date):
  # The date of payment can't be on weekends.
  while previous_date.weekday() in [6, 7]:
    previous_date -= ONE_DAY
  return previous_date


def month_to_pay(FIRST_WORKING_DAY_BEFORE_LIMIT):
  # Find the first month available to pay without taxes if we pay today.
  ONE_MONTH = datetime.timedelta(days=28)
  month_to_pay = FIRST_WORKING_DAY_BEFORE_LIMIT - ONE_MONTH
  return month_to_pay
