#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.ticker import FormatStrFormatter

import matplotlib.pyplot as plt
import math

class MLMultiplePlot(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure(frameon=False)
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)

        self._lines= {}
        self._annotations = {}
        self._axes = []
        self._map = {}

    def redraw(self, items):
        if items is not None:
            self._figure.clf()

            self._axes = []
            self._lines.clear()
            self._annotations.clear()
            self._map.clear()

            n = math.ceil(math.sqrt(len(items.keys())))

            for i in range(len(items.keys())):
                keys = items.keys()
                uid = keys[i]
                self._map[uid] = i

                if i == 0:
                    self._axes.append(self._figure.add_subplot(n, n, i + 1, frame_on=False))
                else:
                    self._axes.append(self._figure.add_subplot(n, n, i + 1, frame_on=False, sharex=self._axes[0], sharey=self._axes[0]))

                self._lines[i], = self._axes[i].plot([], [], '-')

                self._axes[i].grid(linestyle='--')
                self._axes[i].set_title(' training report')
                #self._axes[i].set_xlabel('Progress')
                #self._axes[i].set_ylabel('Error')

                self._annotations[i] = self._axes[i].annotate('',
                                                    xy=(0.85, 0.84),
                                                    xycoords='figure fraction',
                                                    horizontalalignment='right',
                                                    verticalalignment='top',
                                                    clip_on=True,
                                                    size=25,
                                                    bbox=dict(boxstyle='round', ec=None))

                self._axes[i].set_xlim(0.0, 100.0)
                self._axes[i].set_ylim(0.0, 100.0)

                self._axes[i].yaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))
                self._axes[i].xaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))

    def mlUpdateMore(self, uid, graph):
        pass

    def mlUpdate(self, uid, graph, clr='blue'):
        if uid in self._lines.keys():
            self._lines[uid].set_xdata(graph[0])
            self._lines[uid].set_ydata(graph[1])
            self._lines[uid].set_color(clr)

            self.mlUpdateMore(uid, graph)

            self._axes[uid].relim()
            self._axes[uid].autoscale()

            self._figure.canvas.draw_idle()
