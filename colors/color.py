from colorsys import rgb_to_hsv, hsv_to_rgb
from re import search
from os.path import dirname, realpath, join
from xml.dom import minidom


class Color(object):
	"""
	A base to keep colors standard
	"""
	def __init__(self, red=None, green=None, blue=None, alpha=255, **kwargs):
		self._recalculate = False

		if (red is not None or "r" in kwargs.keys()) and (green is not None or "g" in kwargs.keys()) and (blue is not None or "b" in kwargs.keys()):
			red = kwargs.get("r", red)
			green = kwargs.get("g", green)
			blue = kwargs.get("b", blue)
			alpha = kwargs.get("a", alpha)

			self.red = red
			self.green = green
			self.blue = blue
			self.alpha = alpha
			self._hue, self._saturation, self._visibility = rgb_to_hsv(red, green, blue)

		elif "rgba" in kwargs.keys():
			match = search(r"#?([\da-f]{1,2})([\da-f]{1,2})([\da-f]{1,2})([\da-f]{1,2})?", kwargs["rgba"].lower())
			if match is None:
				raise ValueError(f"The given RGB(A) code is not valid: {kwargs['rgba']}")
			self.red = int(match.group(1), base=16)
			self.green = int(match.group(2), base=16)
			self.blue = int(match.group(3), base=16)
			self.alpha = int(match.group(4), base=16) if match.group(4) is not None else 255

		elif ("hue" in kwargs.keys() or "h" in kwargs.keys()) and ("saturation" in kwargs.keys() or "s" in kwargs.keys()) and ("visibility" in kwargs.keys() or "v" in kwargs.keys()):
			hue = kwargs["hue"] if "hue" in kwargs else kwargs["h"]
			saturation = kwargs["saturation"] if "saturation" in kwargs else kwargs["s"]
			visibility = kwargs["visibility"] if "visibility" in kwargs else kwargs["v"]
			self.red, self.green, self.blue = hsv_to_rgb(hue, saturation, visibility)
			self._hue = hue
			self._saturation = saturation
			self._visibility = visibility
		if not hasattr(self, "_hue"):
			self.hue, self.saturation, self.visibility = rgb_to_hsv(self.red, self.green, self.blue)
		self._recalculate = True
		self.name = kwargs.get("name", None)

	@staticmethod
	def _value_check(value) -> int:
		if isinstance(value, str):
			value = int(value, base=16)
		if not isinstance(value, float | int):
			raise ValueError(f"Color value must be a float or integer, not {type(value)}")
		if 0 > value or value > 255:
			raise ValueError(f"Color value must be between 0 and 255, not {value}")
		return int(value)

	@property
	def is_dark(self):
		return ((self.red * .2126) + (self.green * .7152) + (self.blue * .0722)) < 0.5

	@property
	def red(self):
		return self._red

	@red.setter
	def red(self, value):
		self._red = self._value_check(value)
		if self._recalculate:
			self._hue, self._saturation, self._visibility = rgb_to_hsv(self.red, self.green, self.blue)

	@red.deleter
	def red(self):
		raise ValueError("Cannot delete red channel for Color object")

	@property
	def green(self):
		return self._green

	@green.setter
	def green(self, value):
		self._green = self._value_check(value)
		if self._recalculate:
			self._hue, self._saturation, self._visibility = rgb_to_hsv(self.red, self.green, self.blue)

	@green.deleter
	def green(self):
		raise ValueError("Cannot delete green channel for Color object")

	@property
	def blue(self):
		return self._blue

	@blue.setter
	def blue(self, blue):
		self._blue = self._value_check(blue)
		if self._recalculate:
			self._hue, self._saturation, self._visibility = rgb_to_hsv(self.red, self.green, self.blue)

	@blue.deleter
	def blue(self):
		raise ValueError("Cannot delete blue channel for Color object")

	@property
	def alpha(self):
		return self._alpha

	@alpha.setter
	def alpha(self, alpha):
		self._alpha = self._value_check(alpha)

	@alpha.deleter
	def alpha(self):
		self.alpha = 0

	@property
	def red_hex(self):
		return self.toHex(self._red)

	@red_hex.setter
	def red_hex(self, hexadecimal):
		value = int(hexadecimal, base=16)
		self.red = value

	@property
	def green_hex(self):
		return self.toHex(self._green)

	@green_hex.setter
	def green_hex(self, hexadecimal):
		value = int(hexadecimal, base=16)
		self.green = value

	@property
	def blue_hex(self):
		return self.toHex(self._blue)

	@blue_hex.setter
	def blue_hex(self, hexadecimal):
		value = int(hexadecimal, base=16)
		self.blue = value

	@property
	def alpha_hex(self):
		return self.toHex(self._alpha)

	@alpha_hex.setter
	def alpha_hex(self, hexadecimal):
		value = int(hexadecimal, base=16)
		self.alpha = value

	@property
	def rgb(self):
		return f"#{self.red_hex}{self.green_hex}{self.blue_hex}"

	@property
	def rgba(self):
		return self.rgb + self.alpha_hex

	@property
	def hue(self):
		return self._hue

	@hue.setter
	def hue(self, hue):
		if self._recalculate:
			self.red, self.green, self.blue = hsv_to_rgb(hue, self.saturation, self.visibility)
		self._hue = hue

	@property
	def saturation(self):
		return self._saturation

	@saturation.setter
	def saturation(self, saturation):
		if self._recalculate:
			self.red, self.green, self.blue = hsv_to_rgb(self.hue, saturation, self.visibility)
		self._saturation = saturation

	@property
	def visibility(self):
		return self._visibility

	@visibility.setter
	def visibility(self, visibility):
		if self._recalculate:
			self.red, self.green, self.blue = hsv_to_rgb(self.hue, self.saturation, visibility)
		self._visibility = visibility

	@property
	def name(self) -> str|None:
		return self._name

	@name.setter
	def name(self, name:str|None):
		if name is not None and not isinstance(name, str):
			name = str(name)
		self._name = name

	@staticmethod
	def toHex(color):
		return str(hex(color))[2:].zfill(2)

	def __hex__(self):
		return self.rgba

	def __eq__(self, other):
		if not isinstance(other, Color):
			try:
				other = Color(other)
			except:
				return False
		return self.red == other.red and self.green == other.green and self.blue == other.blue and self.alpha == self.alpha

	def __ne__(self, other):
		return not self == other

	def __add__(self, other):
		if isinstance(other, Color):
			red = (self.red + other.red) // 2
			green = (self.green + other.green) // 2
			blue = (self.blue + other.blue) // 2
			alpha = (self.alpha + other.alpha) // 2
			return Color(red, green, blue, alpha)
		elif isinstance(other, list) or isinstance(other, tuple):
			if len(other) >= 3:
				red = (self.red + other[0]) // 2
				green = (self.green + other[1]) // 2
				blue = (self.blue + other[2]) // 2
				alpha = self.alpha if len(other) == 3 else (self.alpha + other[3])//2
				return Color(red, green, blue, alpha)
		else:
			return TypeError(f"unsupported operand type(s) for +: 'Color' and '{other.__name__}'")

	def __repr__(self):
		return f"\033[38;2;{self.red};{self.green};{self.blue}mColor(red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha})\033[0m"

	def __int__(self):
		return int(self.red_hex + self.green_hex + self.blue_hex, 16)

	def __str__(self):
		return f"Color: {self.rgba} Red: {self.red}\t Green: {self.green}\t Blue: {self.blue}\t Alpha: {self.alpha}"

	def __format__(self, fmt:str) -> str:
		"""
		Formats the given string with information about the class:

		Use %R, %G, %B, %A to fill in the respective hexadecimal values for the object.
		Use %r, %g, %b, %a to fill in the respective integer values (0-255) for the object.
		Use %h, %s, %v to fill in the respective HSV values.
		Use %n to fill in the name of the color object, if it's provided at some point. If there is no name, %n will be replaced with nothing.
		Anything wrapped in %f and %t will have its forecolor as this color. These can be used multiple times, but there must be the same amount.
		"""
		from re import search, sub

		string = fmt.replace("%R", self.red_hex)\
			.replace("%G", self.green_hex)\
			.replace("%B", self.blue_hex)\
			.replace("%A", self.alpha_hex)\
			.replace("%r", f"{self.red}")\
			.replace("%g", f"{self.green}")\
			.replace("%b", f"{self.blue}")\
			.replace("%a", f"{self.alpha}")\
			.replace("%h", f"{self.hue}")\
			.replace("%s", f"{self.saturation}")\
			.replace("%v", f"{self.visibility}")\
			.replace("%n", self.name if self.name else "")

		starts = search(r"%f", string)
		ends = search(r"%t", string)

		if starts is not None and ends is not None:
			if (starts is None) ^ (ends is None):
				raise ValueError(f"There were a different amount of start characters and end characters for color formatting")

			string = sub("%f", self.termstart, string)
			string = sub("%t", self.termend, string)

		return string

	def __hash__(self):
		return hash((self.red, self.green, self.blue, self.alpha))

	def __iter__(self):
		for i in (self.red, self.green, self.blue, self.alpha):
			yield i

	@property
	def termstart(self) -> str:
		"""
		Colors the foreground of the terminal with this color.
		"""
		return f"\033[38;2;{self.red};{self.green};{self.blue}m"

	@property
	def termend(self) -> str:
		"""
		Returns the foreground color of the terminal to normal.
		"""
		return "\033[0m"

	def __enter__(self):
		return self.termstart

	def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
		return self.termend

	def copy(self):
		"""
		Creates a new color object with the same information as this object
		:rtype Color:
		"""
		return Color(self.red, self.green, self.blue, self.alpha)


class Colors(dict):
	def __init__(self, *args):
		super().__init__()
		self.populate_from_xml(list(args))

	def __getattribute__(self, item):
		try:
			return super().__getattribute__(item)
		except KeyError:
			return self[item.lower().replace("_", " ")]

	def populate_from_xml(self, file_paths:list = None):
		default = join(dirname(realpath(__file__)), "colors.xml")
		if file_paths is None:
			file_paths = [default]
		else:
			file_paths.insert(0, default)
		for file in file_paths:
			file = minidom.parse(file)
			colors = file.getElementsByTagName("resources")
			for color in colors[0].childNodes:
				if color.nodeName == "color":
					name = color.attributes["name"].value
					value = Color(rgba=color.firstChild.nodeValue, name=name)
					self[name] = value
					setattr(Colors, name.upper(), value)
				elif color.nodeName == "array":
					lst = []
					name = color.attributes["name"].value
					for index in color.childNodes:
						if index.nodeName == "color":
							value = Color(rgba=index.firstChild.nodeValue, name=name)
							lst.append(value)
					self[name] = lst
					setattr(Colors, name.upper(), lst)
