#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt

class MLPlot2D(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure(frameon=False)
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        self._ax = self._figure.add_subplot(111)
        self._ax.set(frame_on=False)
        self._ax.axis('off')

        self.redraw()

    def redraw(self, title=''):
        self._ax.cla()
        self._line, = self._ax.plot([], [], '-')

    def mlUpdateMore(self, graph):
        pass

    def mlUpdate(self, graph, clr='blue'):
        self._line.set_xdata(graph[0])
        self._line.set_ydata(graph[1])
        self._line.set_color(clr)

        self.mlUpdateMore(graph)

        self._ax.relim()
        self._ax.autoscale()

        self._figure.canvas.draw_idle()
