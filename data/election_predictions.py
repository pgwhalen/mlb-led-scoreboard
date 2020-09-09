import csv
import datetime
import random

import requests
import debug
import time

PREDICTION_UPDATE_RATE = 10 * 60 # 10 minutes between prediction updates

class ElectionPredictions:

  def __init__(self):
    self.races = {}
    self.scenarios = {}
    self.last_update_time = None
    self.race_idx = 0

  def update(self):
    if self._should_update():
      self._fetch_all()
      self.last_update_time = time.time()

  def next_race(self):
    self.race_idx += 1
    return self.races.values()[self.race_idx % len(self.races)]

  def next_scenario(self):
    return self.scenarios.values()[random.randint(0, len(self.scenarios.values())-1)]

  def days_remaining_text(self):
    today = datetime.datetime.now()
    election_day = datetime.datetime(year=2020, month=11, day=3)
    return str((election_day - today).days) + " days until the election."

  def _should_update(self):
    if not self.last_update_time:
      return True
    now = time.time()
    time_since_last_update = now - self.last_update_time
    return time_since_last_update >= PREDICTION_UPDATE_RATE

  def _fetch_all(self):
    self._fetch_presidential_national_toplines()
    self._fetch_presidential_state_toplines()
    self._fetch_presidential_ev_probabilities()
    # self._fetch_presidential_scenario_analysis()

  def _fetch_presidential_national_toplines(self):
    rows = self._fetch_as_dict_list(
      'https://projects.fivethirtyeight.com/2020-general-data/presidential_national_toplines_2020.csv')
    today_row = rows[0] # assume they're in descending order by date
    electoral = Race(
      "Electoral",
      Candidate.trump_pct(float(today_row['ecwin_inc'])),
      Candidate.biden_pct(float(today_row['ecwin_chal']))
    )
    self.races[electoral.name] = electoral
    popular = Race(
      "Popular",
      Candidate.trump_pct(float(today_row['popwin_inc'])),
      Candidate.biden_pct(float(today_row['popwin_chal']))
    )
    self.races[popular.name] = popular


  def _fetch_presidential_state_toplines(self):
    rows = self._fetch_as_dict_list(
      'https://projects.fivethirtyeight.com/2020-general-data/presidential_state_toplines_2020.csv')
    max_date = max([self._row_date(r) for r in rows])
    todays_rows = [r for r in rows if self._row_date(r) == max_date]
    tipping_point_threshold = 0.02 # if a state is this likely to be a tipping point state we'll show it
    for row in [r for r in todays_rows if float(r['tipping']) > tipping_point_threshold]:
      state_race = Race(
        row['state'],
        Candidate.trump_pct(float(row['winstate_inc'])),
        Candidate.biden_pct(float(row['winstate_chal']))
      )
      self.races[state_race.name] = state_race

  def _fetch_presidential_ev_probabilities(self):
    pass
    # rows = self._fetch_as_dict_list(
    #   'https://projects.fivethirtyeight.com/2020-general-data/presidential_ev_probabilities_2020.csv')

  def _fetch_presidential_scenario_analysis(self):
    rows = self._fetch_as_dict_list(
      'https://projects.fivethirtyeight.com/2020-general-data/presidential_scenario_analysis_2020.csv')
    max_date = max([self._row_date(r) for r in rows])
    todays_rows = [r for r in rows if self._row_date(r) == max_date]
    # TODO: dumb csv.DictReader bug causes this to blow up, figure out a workaround
    for row in todays_rows:
      s = Scenario(int(row['scenario_id']), row['description'], float(row['probability']))
      self.scenarios[s.id] = s

  def _fetch_as_dict_list(self, url):
    debug.log("Fetching " + url)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    if resp.status_code == 200:
      return [{k: v for k, v in row.items()}
           for row in csv.DictReader(resp.text.splitlines())]
    else:
      raise Exception("Could not download 538 election prediction from " + url)

  def _row_date(self, row):
    return datetime.datetime.strptime(row['modeldate'],'%m/%d/%Y')

class Candidate:
  __RED = {
    'r': 220,
    'g': 0,
    'b': 0,
  }
  __BLUE = {
    'r': 0,
    'g': 0,
    'b': 220,
  }

  @staticmethod
  def trump_pct(pct):
    return Candidate("Trump", Candidate.__RED, Candidate.__BLUE, pct)

  @staticmethod
  def biden_pct(pct):
    return Candidate("Biden", Candidate.__BLUE, Candidate.__RED, pct)

  def __init__(self, name, main_color, accent_color, pct):
    self.name = name
    self.main_color = main_color
    self.accent_color = accent_color
    self.percent = pct


class Race:

  def __init__(self, name, candidate_one, candidate_two):
    self.name = name
    if candidate_one.percent > candidate_two.percent:
      self.top_candidate, self.bottom_candidate = candidate_one, candidate_two
    else:
      self.top_candidate, self.bottom_candidate = candidate_two, candidate_one

class Scenario:

  def __init__(self, id, description, prob):
    self.id = id
    self.description = description
    self.prob = prob

  def text(self):
    return "{description} ({pct})".format(description=self.description, pct="%.1f" % (self.prob * 100,) + "%")