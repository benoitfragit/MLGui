#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt

class MLMultiplePlot(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure(frameon=False)
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)

        self._axes = {}
        self._lines= {}
        self._annotations = {}

    def registerNewPlot(self, uid):
        self._axes[uid] = self._figure.add_subplot(111)
        self._axes[uid].set(frame_on=False)
        self._axes[uid].axis('off')

        self.redraw(uid)

    def redraw(self, uid, title=''):
        if uid in self._axes.keys():
            self._axes[uid].cla()
            self._lines[uid], = self._axes[uid].plot([], [], '-')

            self._axes[uid].grid(linestyle='--')
            self._axes[uid].set_title(title + ' training report')
            self._axes[uid].set_xlabel('Progress')
            self._axes[uid].set_ylabel('Error')

            self._annotations[uid] = self._axes[uid].annotate('',
                                                xy=(0.85, 0.84),
                                                xycoords='figure fraction',
                                                horizontalalignment='right',
                                                verticalalignment='top',
                                                clip_on=True,
                                                size=25,
                                                bbox=dict(boxstyle='round', ec=None))

            self._axes[uid].set_xlim(0.0, 100.0)
            self._axes[uid].set_ylim(0.0, 100.0)

            self._axes[uid].yaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))
            self._axes[uid].xaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))

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
