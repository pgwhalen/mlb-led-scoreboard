import operator

from rgbmatrix import graphics
from utils import get_font, get_file, center_text_position
from renderers.network import NetworkErrorRenderer
import time

class FermentationStatsRenderer:
  def __init__(self, matrix, canvas, data):
    self.matrix = matrix
    self.canvas = canvas
    self.data = data
    self.colors = data.config.scoreboard_colors
    self.bg_color = self.colors.graphics_color("fermentation.background")
    self.divider_color = self.colors.graphics_color("fermentation.divider")
    self.stat_name_color = self.colors.graphics_color("fermentation.stat.name")
    self.stat_value_color = self.colors.graphics_color("fermentation.stat.value")

  def render(self):
    self.__fill_bg()
    self.__render_fermentation_stats()
    NetworkErrorRenderer(self.canvas, self.data).render()

  def __fill_bg(self):
    coords = self.data.config.layout.coords("fermentation")
    for y in range(0, coords["height"]):
      graphics.DrawLine(self.canvas, 0, y, coords["width"], y, self.bg_color)

  def __render_fermentation_stats(self):
    coords = self.data.config.layout.coords("fermentation")
    offset = coords["offset"]

    # probably don't need this
    # graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)

    stats = self.data.tilt_hydrometer
    self._draw_stat('SG', stats.current_specific_gravity, offset)
    offset += coords["offset"]
    self._draw_stat('Temp', stats.current_temp, offset)
    offset += coords["offset"]
    self._draw_stat('Attn', stats.apparent_attenuation, offset)
    offset += coords["offset"]
    self._draw_stat('Days', stats.days, offset)
    offset += coords["offset"]
    self._draw_stat('%Comp', stats.percent_completed, offset)

    self.__fill_standings_footer()

    self.matrix.SwapOnVSync(self.canvas)

  def _draw_stat(self, name, value, offset):
    coords = self.data.config.layout.coords("fermentation")
    font = self.data.config.layout.font("fermentation")

    val_text = "{:>6s}".format(value)
    val_text_x = coords["stat"]["value"]["x"] - (len(val_text) * font["size"]["width"])

    graphics.DrawLine(self.canvas, 0, offset, coords["width"], offset, self.divider_color)
    graphics.DrawText(self.canvas, font["font"], coords["stat"]["name"]["x"], offset, self.stat_value_color, name)
    graphics.DrawText(self.canvas, font["font"], val_text_x, offset, self.stat_name_color, val_text)


  def __fill_standings_footer(self):
    coords = self.data.config.layout.coords("fermentation")
    graphics.DrawLine(self.canvas, 0, coords["height"], coords["width"], coords["height"], self.bg_color)
    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"], self.divider_color)
    graphics.DrawLine(self.canvas, 0, coords["height"]+1, coords["width"], coords["height"]+1, self.bg_color)
    graphics.DrawLine(self.canvas, coords["divider"]["x"], 0, coords["divider"]["x"], coords["height"]+1, self.divider_color)
