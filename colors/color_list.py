from .color import Color
from abc import ABC, abstractmethod


class ColorList(ABC):
	@property
	@abstractmethod
	def color_list(self):
		pass

	def __iter__(self):
		return iter(self.color_list)

	def __len__(self):
		return len(self.color_list)

	def __getitem__(self, key):
		return self.color_list[key]