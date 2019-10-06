#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.ticker import FormatStrFormatter
from matplotlib.gridspec import GridSpec

import matplotlib.pyplot as plt
import math

class MLMultiplePlot(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure(frameon=False)
        self._figure.patch.set_visible(False)

        FigureCanvas.__init__(self, self._figure)

        self._lines= {}
        self._annotations = {}
        self._axes = {}

    def mlRemoveSubPlot(self, uid):
        if uid in self._lines.keys():
            self._lines.pop(uid)
            self._annotations.pop(uid)
            self._figure.delaxes(self._axes[uid])
            self._axes.pop(uid)

            N = len(self._axes.keys())

            # new gridspec
            cols = 2
            rows = int(math.ceil(float(N)/float(cols)))
            grid = GridSpec(rows, cols)
            grid.update(wspace=0.5,hspace=0.5)

            # move old axes to their new position
            for gs, ax in zip(grid, self._axes.values()):
                ax.set_position(gs.get_position(self._figure))

            self._figure.canvas.draw_idle()

    def mlAddSubPlot(self, uid, item):
        if item is not None:
            # new number of axes
            N = len(self._axes.keys()) + 1

            # new gridspec
            cols = 2
            rows = int(math.ceil(float(N)/float(cols)))
            grid = GridSpec(rows, cols)
            grid.update(wspace=0.5,hspace=0.5)

            # move old axes to their new position
            for gs, ax in zip(grid, self._axes.values()):
                ax.set_position(gs.get_position(self._figure))

            # adding new axis
            self._axes[uid] = self._figure.add_subplot(grid[N - 1], frame_on=False)

            self._lines[uid], = self._axes[uid].plot([], [], '-')

            self._axes[uid].grid(linestyle='--')
            self._axes[uid].set_title(item.mlGetUserName() + ' training report', size=9)
            self._axes[uid].set_xlabel('Progress')
            self._axes[uid].set_ylabel('Error')
            self._axes[uid].xaxis.label.set_size(8)
            self._axes[uid].yaxis.label.set_size(8)

            self._annotations[uid] = self._axes[uid].annotate('',
                                                xy=(0.85, 0.84),
                                                xycoords='axes fraction',
                                                horizontalalignment='right',
                                                verticalalignment='top',
                                                clip_on=True,
                                                size=10,
                                                bbox=dict(boxstyle='round', ec=None, fc=(0.0, 0.0, 0.9)))

            self._axes[uid].set_xlim(0.0, 100.0)
            self._axes[uid].set_ylim(0.0, 100.0)

            self._axes[uid].yaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))
            self._axes[uid].xaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))

            graph = item.mlTrainerItemGetGraph()

            self.mlUpdate(uid, graph)

            self._figure.canvas.draw_idle()

    def mlUpdate(self, uid, graph, clr='blue'):
        if uid in self._axes.keys():
            self._lines[uid].set_xdata(graph[0])
            self._lines[uid].set_ydata(graph[1])
            self._lines[uid].set_color(clr)

            if len(graph[1]) > 0 :
                self._annotations[uid].set_text('Error:{0:.2f} %'.format(graph[1][-1]))

            self._axes[uid].relim()
            self._axes[uid].autoscale()

            self._figure.canvas.draw_idle()
