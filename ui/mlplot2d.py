#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

class MLPlot2D(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure()
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        self._ax = self._figure.add_subplot(111)

        self.redraw()

    def redraw(self):
        self._ax.cla()

        self._ax.grid(linestyle='--')
        self._ax.set_title('Training error evolution')
        self._ax.set_xlabel('Progress')
        self._ax.set_ylabel('Error')
        self._ax.set_xlim(0.0, 100.0)
        self._ax.set_ylim(0.0, 100.0)

        self._line, = self._ax.plot([], [], '-')

    def mlUpdate(self, graph, lbl='', clr='blue'):
        self._line.set_xdata(graph[0])
        self._line.set_ydata(graph[1])
        self._line.set_color(clr)

        self._ax.relim()
        self._ax.autoscale()

        self._figure.canvas.draw_idle()
