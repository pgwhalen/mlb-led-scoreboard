import re

import requests

import debug


class UntappdStandings:
  __USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'

  def __init__(self, config):
    self._untappd_user_to_name = config.untappd_user_to_name
    self.name_to_uniques = {}

  def fetch(self):
    debug.log("Fetching from Untappd")
    for user, name in self._untappd_user_to_name.items():
      self.name_to_uniques[name] = self.get_user_data(user)
    debug.log("Names to uniques: " + str(self.name_to_uniques))

  def get_user_data(self, untappd_user):
    # Parsing user information
    url = 'https://untappd.com/user/{}'.format(untappd_user)
    # Setting up and Making the Web Call
    try:
      headers = {'User-Agent': UntappdStandings.__USER_AGENT}
      # Make web request for that URL and don't verify SSL/TLS certs
      response = requests.get(url, headers=headers)
      next_line_is_uniques = False
      for line in str(response.content).splitlines():
        if next_line_is_uniques:
          uniques_str = re.sub('[^0-9]', '', line)
          return int(uniques_str)
        if 'stats/beerhistory' in line:
          next_line_is_uniques = True
        else:
          next_line_is_uniques = False
      return None
    except Exception as e:
      debug.error(e)
      return None


