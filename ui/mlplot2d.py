#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class MLPlot2D(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure()
        FigureCanvas.__init__(self, self._figure)

        self._x = []
        self._y = []

    def append(self, x, y):
        self._x.append(x)
        self._y.append(y)

    def plot(self):
        self._figure.clear()
        ax = self._figure.add_subplot(111)
        ax.plot(self._x, self.y, '*-')
        self.draw()
