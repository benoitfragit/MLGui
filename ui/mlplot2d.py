#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class MLPlot2D(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure()
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        self._ax = self._figure.add_subplot(111)
        self._ax.axis('off')

    def plot(self, graph):
        self._ax.cla()
        self._ax.grid()
        self._ax.set_title('Training error evolution')
        self._ax.set_xlabel('Progress')
        self._ax.set_ylabel('Error')
        self._ax.plot(graph[0], graph[1], '-', color='blue')

        self.draw()
