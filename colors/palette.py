from .color import Color
from .color_list import ColorList


class Palette(ColorList):
	def __init__(self, *colors):
		super().__init__()
		self._color_list = colors

	@property
	def color_list(self):
		return self._color_list

