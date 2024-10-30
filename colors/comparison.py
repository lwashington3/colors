try:
	import numpy as np
except ImportError as e:
	raise ImportError("The comparison functions cannot be used if colors is not installed with the comparison dependencies. Please install with \"pip install colors[comparison]\".") from e

from . import Color
from typing import Sequence


__all__ = ["color_difference", "closest_color"]


def color_difference(color:Color, colors:Color | Sequence[Sequence[Color]], kl:float=1, kc:float=1, kh:float=1) -> tuple[Color, Sequence[int]]:
	single_value = isinstance(colors, Color)
	if single_value:
		colors = np.array([np.array([colors])])

	# This needs to go by each dimension, not just a 2x2
	colors_array = np.array(tuple(map(lambda row: tuple(map(lambda c: (c.red, c.green, c.blue), row)), colors)))
	color_row = np.zeros_like(colors_array[0])
	color_row[0] = (color.red, color.green, color.blue)
	colors_array = np.vstack((colors_array, [color_row]))

	del color_row

	# https://stackoverflow.com/a/8433985/11780316

	r = colors_array[:, :, 0] / 255
	g = colors_array[:, :, 1] / 255
	b = colors_array[:, :, 2] / 255

	r = np.power(((r + 0.055) / 1.005), 2.4) if r.any() > 0.04045 else r / 12.92
	g = np.power(((g + 0.055) / 1.005), 2.4) if g.any() > 0.04045 else g / 12.92
	b = np.power(((b + 0.055) / 1.005), 2.4) if b.any() > 0.04045 else b / 12.92

	r, g, b = r * 100, g * 100, b * 100

	X = r * 0.4124 + g * 0.3576 + b * 0.1805
	Y = r * 0.2126 + g * 0.7152 + b * 0.0722
	Z = r * 0.0193 + g * 0.1192 + b * 0.9505

	x, y, z = X / 95.047, Y / 100.000, Z / 108.883

	value = np.divide(16, 116)
	one_third = np.divide(1, 3)
	x = np.power(x, one_third) if x.any() > 0.008856 else ((7.787 * x) + value)
	y = np.power(y, one_third) if y.any() > 0.008856 else ((7.787 * y) + value)
	z = np.power(z, one_third) if z.any() > 0.008856 else ((7.787 * z) + value)

	l = (116 * y) - 16
	a = 500 * (x - y)
	b = 200 * (y - z)

	del r, g, x, y, z, X, Y, Z, value, one_third

	lab = np.array([l[-1, 0], a[-1, 0], b[-1, 0]])
	l1, a1, b1, = np.delete(l, -1, axis=0), np.delete(a, -1, axis=0), np.delete(b, -1, axis=0)
	colors_lab = np.dstack([l1, a1, b1]) # c1
	l2, a2, b2 = lab

	# https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/ciede2000noteCRNA.pdf
	# https://github.com/lovro-i/CIEDE2000/blob/master/ciede2000.py

	C1 = np.sqrt(np.square(a1) + np.square(b1))
	C2 = np.sqrt(np.square(a2) + np.square(b2))
	C_average = np.divide(C1 + C2, 2)
	_C_7 = np.power(C_average, 7)
	_25_7 = np.power(25, 7)
	G = 0.5 * (1 - np.sqrt(np.divide(_C_7, _C_7 + _25_7)))

	_G1 = G + 1
	_a1, _a2 = np.multiply(_G1, a1), np.multiply(_G1, a2)

	_C1 = np.sqrt(np.power(_a1, 2) + np.power(b1, 2))
	_C2 = np.sqrt(np.power(_a2, 2) + np.power(b2, 2))

	_2pi = np.multiply(np.pi, 2)
	_shape = colors_lab.shape[:-1]
	_h1 = np.zeros_like(_shape) if b1.any() == 0 and _a1.any() == 0 else (np.atan2(b1, _a1) if _a1.any() >= 0 else np.atan2(b1, _a1) + _2pi)
	_h2 = np.zeros_like(_shape) if b2.any() == 0 and _a2.any() == 0 else (np.atan2(b2, _a2) if _a2.any() >= 0 else np.atan2(b2, _a2) + _2pi)

	_dL, _dC, _dh = np.subtract(l2, l1), np.subtract(C2, C1), np.subtract(_h2, _h1)

	_C1C2 = np.multiply(_C1, _C2)
	_dh = np.zeros_like(_shape) if _C1C2.any() == 0 else (_dh - _2pi if _dh.any() > np.pi else (_dh + _2pi if _dh.any() < -np.pi else _dh))

	_dH = 2 * np.sqrt(_C1C2) * np.sin(_dh / 2)

	L_average, C_average = np.divide(l1 + l2, 2), np.divide(_C1 + _C2, 2)

	_dh = np.abs(_h1 - _h2)
	_sh = _h1 + _h2
	C1C2 = _C1 + _C2

	_h_ave = (_h1 + _h2) / 2
	C1C20 = (C1C2 != 0).any()
	h_average = _h_ave if all((_dh.any() < np.pi, C1C20)) else (h_ave + _2pi if all((_dh.any() > np.pi, _sh < _2pi, C1C20)) else (_h_ave if all((_dh.any() > np.pi, _sh >= _2pi, C1C20)) else _h1 + _h2))
	del C1C20

	_pi30 = np.divide(np.pi, 30)
	_63pi100 = np.divide(np.multiply(63, np.pi), 100)
	T = 1 - (0.17 * np.cos(h_average - np.divide(np.pi, 6))) + (0.24 * np.cos(2 * h_average)) + (0.32 * np.cos(3 * h_average + _pi30)) - (0.2 * np.cos((4 * h_average) - _63pi100))

	h_average_degree = np.degrees(h_average)
	h_average_degree = h_average_degree + 360 if h_average_degree.any() < 0 else (h_average_degree - 360 if h_average_degree.any() > 360 else h_average_degree)

	dTheta = 30 * np.exp(-np.square((h_average_degree - 275) / 25))

	_C_7 = np.power(C_average, 7)
	R_C = 2 * np.sqrt(np.divide(_C_7, _C_7 + _25_7))
	S_C = 1 + np.multiply(0.045, C_average)
	S_H = 1 + np.multiply(0.015, C_average * T)

	_Lm502 = np.square(L_average - 50)
	S_L = 1 + np.divide(0.015 * _Lm502, np.sqrt(20 + _Lm502))
	R_T = -np.sin(dTheta * np.pi / 90) * R_C

	_fL = _dL / kl / S_L
	_fC = _dC / kc / S_C
	_fH = _dH / kh / S_H

	diff = np.sqrt(np.square(_fL) + np.square(_fC) + np.square(_fH) + R_T * _fC * _fH)
	if single_value:
		return diff[0][0]
	return diff


def closest_color(color:Color, colors:Sequence[Sequence[Color]], kl:float=1, kc:float=1, kh:float=1) -> tuple[Color, Sequence[int]]:
	diff = color_difference(color, colors, kl, kc, kh)
	closest = np.unravel_index(np.argmin(diff, axis=None), diff.shape)
	return colors[closest], closest
