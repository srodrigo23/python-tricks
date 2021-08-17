import numpy as np


class Model:

    def __init__(self):
        self.xpoint = 200
        self.ypoint = 200
        self.res = None

    def calculate(self):
        x, y = np.meshgrid(np.linspace(-5, 5, self.xpoint), np.linspace(-5, 5, self.ypoint))
        z = np.cos(x ** 2 * y ** 3)
        self.res = {"x": x, "y": y, "z": z}
