#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.ticker import FormatStrFormatter
from matplotlib.gridspec import GridSpec

import matplotlib.pyplot as plt
import math

class MLPlotManager(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure(frameon=False)
        self._figure.patch.set_visible(False)

        FigureCanvas.__init__(self, self._figure)

        self._handle = self._figure.canvas.mpl_connect('button_press_event', self.mlOnAxeClicked)

        self._lines= {}
        self._annotations = {}
        self._axes = {}

    def mlReogarnizePlot(self, N):
        cols = 2
        rows = int(math.ceil(float(N)/float(cols)))
        grid = GridSpec(rows, cols)
        grid.update(wspace=0.5,hspace=0.5)

        for gs, ax in zip(grid, self._axes.values()):
            ax.set_position(gs.get_position(self._figure))

        return grid

    def mlOnAxeClicked(self, event):
        if event.dblclick:
            self.mlToggleAllPlotsVisibility(True)
        else:
            if event.inaxes is not None:
                visible_id = None
                for uid in self._axes.keys():
                    if self._axes[uid].get_visible() and self._axes[uid].in_axes(event):
                        visible_id = uid
                        break

                if visible_id is not None:
                    self.mlToggleAllPlotsVisibility(False)
                    self.mlSetPlotVisible(visible_id, 0, 1)

    def mlRemoveSubPlot(self, uid):
        if uid in self._lines.keys():
            self._lines.pop(uid)
            self._annotations.pop(uid)
            self._figure.delaxes(self._axes[uid])
            self._axes.pop(uid)

            N = len(self._axes.keys())

            self.mlReogarnizePlot(N)

            self._figure.canvas.draw_idle()

    def mlAddSubPlot(self, uid, item):
        if item is not None:
            # new number of axes
            N = len(self._axes.keys()) + 1

            grid = self.mlReogarnizePlot(N)

            # adding new axis
            self._axes[uid] = self._figure.add_subplot(grid[N - 1], frame_on=False)

            self._lines[uid], = self._axes[uid].plot([], [], '-')

            self._axes[uid].grid(linestyle='--')
            self._axes[uid].set_title(item.mlGetUserName() + ' training report', size=9)
            self._axes[uid].set_xlabel('Progress')
            self._axes[uid].set_ylabel('Error')
            self._axes[uid].xaxis.label.set_size(8)
            self._axes[uid].yaxis.label.set_size(8)
            self._axes[uid].xaxis.set_ticks(range(0,150, 50))
            self._axes[uid].yaxis.set_ticks(range(0,150, 50))

            self._annotations[uid] = self._axes[uid].annotate('',
                                                xy=(0.85, 0.84),
                                                xycoords='axes fraction',
                                                horizontalalignment='right',
                                                verticalalignment='top',
                                                clip_on=True,
                                                size=10,
                                                bbox=None)
                                                #dict(boxstyle='round', ec=None)

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

            if len(graph[0]) > 0:
                val = graph[0][-1]
                if val < 95.0:
                    self._axes[uid].set_frame_on(True)
                    self._axes[uid].patch.set_alpha(0.2)
                    self._axes[uid].patch.set_edgecolor('yellow')
                    self._axes[uid].patch.set_facecolor('yellow')
                else:
                    self._axes[uid].set_frame_on(False)

            self._lines[uid].set_color(clr)

            if len(graph[1]) > 0 :
                self._annotations[uid].set_text('Error:{0:.2f} %'.format(graph[1][-1]))

            self._axes[uid].relim()
            self._axes[uid].autoscale()

            self._figure.canvas.draw_idle()

    def mlToggleAllPlotsVisibility(self, visible):
        for uid in self._axes.keys():
            self._axes[uid].set_visible(visible)

        if visible:
            N = len(self._axes.keys())

            self.mlReogarnizePlot(N)

        self._figure.canvas.draw_idle()

    def mlSetPlotVisible(self, uid, i, N):
        if uid in self._axes.keys():
            self._axes[uid].set_visible(True)

            if N > 0 and i >= 0 and i <= N:
                cols = 1
                if N > 1:
                    cols = 2
                rows = int(math.ceil(float(N)/float(cols)))
                grid = GridSpec(rows, cols)
                grid.update(wspace=0.5,hspace=0.5)

                # move old axes to their new position
                self._axes[uid].set_position(grid[i].get_position(self._figure))

            self._figure.canvas.draw_idle()
