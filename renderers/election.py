from rgbmatrix import graphics

import debug
from renderers.scrollingtext import ScrollingText
from utils import get_font, get_file, center_text_position
import json


class ElectionRenderer:
  __WHITE = graphics.Color(255, 255, 255)
  __YELLOW = graphics.Color(255, 235, 59)

  """
  Renders the candidates in the race, the percentage likelihood of the candidates winning,
  and the name of the race."""

  def __init__(self, canvas, race, data, scroll_text, scroll_pos):
    self.canvas = canvas
    self.name = race.name
    self.bottom_candidate = race.bottom_candidate
    self.top_candidate = race.top_candidate
    self.layout = data.config.layout
    self.data = data
    self.scroll_text = scroll_text
    self.scroll_pos = scroll_pos
    self.bg_color = self.data.config.scoreboard_colors.color("default.background")

  def render(self):
    self.canvas.Fill(self.bg_color["r"], self.bg_color["g"], self.bg_color["b"])

    bg_coords = {
      "top": self.layout.coords("election.candidates.background.top"),
      "bottom": self.layout.coords("election.candidates.background.bottom")
    }
    accent_coords = {
      "top": self.layout.coords("election.candidates.accent.top"),
      "bottom": self.layout.coords("election.candidates.accent.bottom")
    }

    top_name_coords = self.layout.coords("election.candidates.name.top")
    bottom_name_coords = self.layout.coords("election.candidates.name.bottom")

    top_percent_coords = self.layout.coords("election.candidates.percent.top")
    bottom_percent_coords = self.layout.coords("election.candidates.percent.bottom")

    for loc in ["top", "bottom"]:
      for x in range(bg_coords[loc]["width"]):
        for y in range(bg_coords[loc]["height"]):
          color = self.top_candidate.main_color if loc == "top" else self.bottom_candidate.main_color
          x_offset = bg_coords[loc]["x"]
          y_offset = bg_coords[loc]["y"]
          self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])

    for loc in ["top", "bottom"]:
      for x in range(accent_coords[loc]["width"]):
        for y in range(accent_coords[loc]["height"]):
          color = self.top_candidate.accent_color if loc == "top" else self.bottom_candidate.accent_color
          x_offset = accent_coords[loc]["x"]
          y_offset = accent_coords[loc]["y"]
          self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])

    self.__render_candidate_text(self.top_candidate, "top", top_name_coords["x"], top_name_coords["y"])
    self.__render_candidate_text(self.bottom_candidate, "bottom", bottom_name_coords["x"], bottom_name_coords["y"])

    self.__render_candidate_percent(self.top_candidate.percent, "top", top_percent_coords["x"], top_percent_coords["y"])
    self.__render_candidate_percent(self.bottom_candidate.percent, "bottom", bottom_percent_coords["x"], bottom_percent_coords["y"])

    self.__render_race_name()

    return self.__render_scroll_text()

  def __render_candidate_text(self, candidate, loc, x, y):
    font = self.layout.font("election.candidates.name.{}".format(loc))
    team_text = '{:3s}'.format(candidate.name)
    if self.canvas.width > 32:
      team_text = '{:13s}'.format(candidate.name)
    graphics.DrawText(self.canvas, font["font"], x, y, ElectionRenderer.__WHITE, team_text)

  def __render_candidate_percent(self, percent, loc, x, y):
    coords = self.layout.coords("election.candidates.percent.{}".format(loc))
    font = self.layout.font("election.candidates.percent.{}".format(loc))
    percent_str = "%.1f" % (percent * 100,) + "%"
    candidate_percent_x = coords["x"] - (len(percent_str) * font["size"]["width"])
    graphics.DrawText(self.canvas, font["font"], candidate_percent_x, y, ElectionRenderer.__WHITE, percent_str)

  def __render_race_name(self):
    race_name_text = self.name
    coords = self.layout.coords("election.name")
    font = self.layout.font("election.name")
    race_name_x = center_text_position(race_name_text, coords["x"], font["size"]["width"])
    graphics.DrawText(self.canvas, font["font"], race_name_x, coords["y"], ElectionRenderer.__YELLOW, race_name_text)

  def __render_scroll_text(self):
    coords = self.layout.coords("election.scrolling_text")
    font = self.layout.font("election.scrolling_text")
    return ScrollingText(self.canvas, coords["x"], coords["y"], coords["width"], font, ElectionRenderer.__YELLOW, self.bg_color,
                         self.scroll_text).render(self.scroll_pos)