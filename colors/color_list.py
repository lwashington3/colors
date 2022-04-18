from .color import Color
from abc import ABC, abstractmethod
from matplotlib.colors import ListedColormap


class ColorList(ABC):
	@property
	@abstractmethod
	def color_list(self):
		pass

	def rgba_list(self) -> list[Color]:
		return [i.get_rgba() for i in self]

	def as_colormap(self) -> ListedColormap:
		return ListedColormap(self.rgba_list())

	def __iter__(self):
		return iter(self.color_list)

	def __len__(self):
		return len(self.color_list)

	def __getitem__(self, key):
		return self.color_list[key]