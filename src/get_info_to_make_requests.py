def get_info_to_make_requests(JSESSIONID):
  headers = {
      "Content-Type": "application/x-www-form-urlencoded",
  }

  cookies = {
      "JSESSIONID": JSESSIONID,
      "WWW2_ROUTEID": ".3",
  }

  return (headers, cookies)
