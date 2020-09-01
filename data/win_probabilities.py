import csv
import datetime

import requests

import debug


class WinProbabilities:
  """
  Fetches 538 MLB game predictions.  The are apparently updated after every game,
  but pulling them on startup each day is probably good enough.
  """
  __URL = 'https://projects.fivethirtyeight.com/mlb-api/mlb_elo_latest.csv'
  __TEAM_ABBREV_TO_538_NAME = {
    'ARI': 'ARI',
    'ATL': 'ATL',
    'BAL': 'BAL',
    'BOS': 'BOS',
    'CHC': 'CHC',
    'CHW': 'CHW',
    'CWS': 'CHW',
    'CIN': 'CIN',
    'CLE': 'CLE',
    'COL': 'COL',
    'DET': 'DET',
    'FLA': 'FLA',
    'HOU': 'HOU',
    'KAN': 'KCR',
    'KC': 'KCR',
    'LAA': 'ANA',
    'LAD': 'LAD',
    'MIA': 'MIA',
    'MIL': 'MIL',
    'MIN': 'MIN',
    'NYM': 'NYM',
    'NYY': 'NYY',
    'OAK': 'OAK',
    'PHI': 'PHI',
    'PIT': 'PIT',
    'SD': 'SDP',
    'SF': 'SFG',
    'SEA': 'SEA',
    'STL': 'STL',
    'TB': 'TBD',
    'TEX': 'TEX',
    'TOR': 'TOR',
    'WAS': 'WSN',
    'WSH': 'WSN'
  }

  def __init__(self, year, month, day):
    date_str = datetime.datetime(year=year, month=month, day=day).strftime('%Y-%m-%d')
    self.team_abbrev_to_win_percentage = {}
    debug.log("Fetching 538 win probabilities from {url}".format(url=WinProbabilities.__URL))
    resp = requests.get(WinProbabilities.__URL)
    if resp.status_code == 200:
      for game_row in csv.reader(resp.text.splitlines(), delimiter=','):
        game_date, team_1, team_2 = game_row[0], game_row[4], game_row[5]
        team_1_prob, team_2_prob = game_row[20], game_row[21]
        if game_date == date_str:
          self.team_abbrev_to_win_percentage[team_1] = self.str_to_win_percentage(team_1_prob)
          self.team_abbrev_to_win_percentage[team_2] = self.str_to_win_percentage(team_2_prob)
      debug.log("Done fetching 538 win probabilities")
    else:
      raise Exception("Could not download 538 win probabilities")

  def str_to_win_percentage(self, win_pct_str):
    return int(round(float(win_pct_str) * 100))

  def pct_for_team(self, team_abbrev):
    pct_num = self.team_abbrev_to_win_percentage.get(WinProbabilities.__TEAM_ABBREV_TO_538_NAME[team_abbrev])
    if pct_num:
      return str(pct_num) + "%"
    else:
      return ""
