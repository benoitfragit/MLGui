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

    def clear(self):
        self._ax.cla()

    def plot(self, graph, lbl='', clr='blue'):
        self._ax.grid(linestyle='--')
        self._ax.set_title('Training error evolution')
        self._ax.set_xlabel('Progress')
        self._ax.set_ylabel('Error')
        self._ax.plot(graph[0], graph[1], '-', color=clr, label=lbl)
        if self._ax.get_legend() == None:
            self._ax.legend()
        self._figure.canvas.draw_idle()
