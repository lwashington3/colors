from .color import Color
from .gradient import Gradient
from .color_list import ColorList


def convert_color(color:str | Color | ColorList) -> str:
	if isinstance(color, Color):
		return color.get_rgba()
	elif isinstance(color, ColorList):
		return [c.get_rgba() for c in color]
	elif isinstance(color, str):
		return Color(rgba=color).get_rgba()
	elif hasattr(color, "__iter__"):
		if len(color) >= 3:
			if len(color) >= 4:
				return Color(color[0], color[1], color[2], color[3]).get_rgba()
			return Color(color[0], color[1], color[2]).get_rgba()
	return color
