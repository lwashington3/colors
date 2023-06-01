from .color import Color
from abc import ABC, abstractmethod


class ColorList(ABC):
	@property
	@abstractmethod
	def color_list(self):
		pass

	def rgba_list(self) -> list[Color]:
		return [i.rgba for i in self]

	def as_mpl_colormap(self) -> ListedColormap:
		"""
		:returns: matplotlib.colors.ListedColormap
		"""
		try:
			from matplotlib.colors import ListedColormap
			return ListedColormap(self.rgba_list())
		except ModuleNotFoundError as e:
			raise ModuleNotFoundError("This function requires the matplotlib library. Please run `pip install matplotlib` and try again.")

	def __iter__(self):
		return iter(self.color_list)

	def __len__(self):
		return len(self.color_list)

	def __getitem__(self, key):
		return self.color_list[key]