import operator

from rgbmatrix import graphics
from utils import get_font, get_file, center_text_position
from renderers.network import NetworkErrorRenderer
import time

class UntappdStandingsRenderer:
  def __init__(self, matrix, canvas, data):
    self.matrix = matrix
    self.canvas = canvas
    self.data = data
    self.colors = data.config.scoreboard_colors
    self.bg_color = self.colors.graphics_color("untappd.background")
    self.divider_color = self.colors.graphics_color("untappd.divider")
    self.stat_color = self.colors.graphics_color("untappd.stat")
    self.guy_stat_color = self.colors.graphics_color("untappd.guy.stat")
    self.guy_name_color = self.colors.graphics_color("untappd.guy.name")

  def render(self):
    self.__fill_bg()
    self.__render_static_wide_standings()
    NetworkErrorRenderer(self.canvas, self.data).render()

  def __fill_bg(self):
    coords = self.data.config.layout.coords("untappd")
    for y in range(0, coords["height"]):
      graphics.DrawLine(self.canvas, 0, y, coords["width"], y, self.bg_color)

  def __render_static_wide_standings(self):
    coords = self.data.config.layout.coords("untappd")
    font = self.data.config.layout.font("untappd")
    offset = coords["offset"]
    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)

    max_uniques = max(self.data.untappd_standings.name_to_uniques.values())
    for e in sorted(self.data.untappd_standings.name_to_uniques.items(), reverse=True):
      name, uniques = e[0], e[1]
      graphics.DrawLine(self.canvas, 0, offset, coords["width"], offset, self.divider_color)

      graphics.DrawText(self.canvas, font["font"], coords["guy"]["name"]["x"], offset, self.guy_name_color, name)

      record_text = str(uniques)
      record_text_x = center_text_position(record_text, coords["guy"]["uniques"]["x"], font["size"]["width"])

      if uniques == max_uniques:
        bb_text = " - "
      else:
        bb_text = "{:>4s}".format(str(max_uniques - uniques))
      gb_text_x = coords["guy"]["beers_back"]["x"] - (len(bb_text) * font["size"]["width"])

      graphics.DrawText(self.canvas, font["font"], record_text_x, offset, self.guy_stat_color, record_text)
      graphics.DrawText(self.canvas, font["font"], gb_text_x, offset, self.guy_stat_color, bb_text)

      offset += coords["offset"]

    self.__fill_standings_footer()

    self.matrix.SwapOnVSync(self.canvas)

  def __fill_standings_footer(self):
    coords = self.data.config.layout.coords("untappd")
    graphics.DrawLine(self.canvas, 0, coords["height"], coords["width"], coords["height"], self.bg_color)
    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)
    graphics.DrawLine(self.canvas, 0, coords["height"]+1, coords["width"], coords["height"]+1, self.bg_color)
    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"]+1, self.divider_color)