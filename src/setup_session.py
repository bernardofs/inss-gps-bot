import requests


def setup_session():
  headers = {
      "Content-Type": "application/x-www-form-urlencoded",
  }

  session = requests.Session()

  session.headers.update(headers)

  return session
