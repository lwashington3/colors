from .color import Color, Colors
from .color_list import ColorList
from .gradient import Gradient
from .palette import Palette
from .tools import convert_color

try:
	from .comparison import *
except ImportError as e:
	print(e)
