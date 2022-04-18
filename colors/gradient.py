from .color import Color
from .color_list import ColorList


class Gradient(ColorList):  # TODO: Implement gradient through lch
    def __init__(self, color1:Color, color2:Color, steps:int = 7):
        super().__init__()
        self._recalculate = False
        self.color1 = color1
        self.color2 = color2
        self.steps = steps
        self._recalculate = True
        self._calculate_gradient_list()

    @property
    def color1(self) -> Color:
        return self._color1

    @color1.setter
    def color1(self, color1:Color):
        if isinstance(color1, str):
            color1 = Color(rgba=color1)
        elif not isinstance(color1, Color):
            color1 = Color(color1)
        self._color1 = color1
        if self._recalculate:
            self._calculate_gradient_list()

    @property
    def color2(self) -> Color:
        return self._color2

    @color2.setter
    def color2(self, color2: Color):
        if isinstance(color2, str):
            color2 = Color(rgba=color2)
        elif not isinstance(color2, Color):
            color2 = Color(color2)
        self._color2 = color2
        if self._recalculate:
            self._calculate_gradient_list()

    @property
    def steps(self) -> int:
        return self._steps

    @steps.setter
    def steps(self, steps:int):
        if not isinstance(steps, int):
            steps = int(steps)
        self._steps = steps
        if self._recalculate:
            self._calculate_gradient_list()

    @property
    def color_list(self):
        return self._gradient_list

    def _calculate_gradient_list(self):
        self._gradient_list = [self.color1]
        steps = self.steps - 1
        for i in range(1, steps):
            red = self.color1.red + ((i/steps) * (self.color2.red - self.color1.red))
            blue = self.color1.blue + ((i/steps) * (self.color2.blue - self.color1.blue))
            green = self.color1.green + ((i/steps) * (self.color2.green - self.color1.green))
            alpha = self.color1.alpha + ((i/steps) * (self.color2.alpha - self.color1.alpha))
            self._gradient_list.append(Color(red, green, blue, alpha))
        self._gradient_list.append(self.color2)

    def __len__(self):
        return self.steps
