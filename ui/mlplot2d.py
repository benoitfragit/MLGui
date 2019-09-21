#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FormatStrFormatter

import matplotlib.pyplot as plt

class MLPlot2D(FigureCanvas):
    def __init__(self):
        self._figure = plt.figure()
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        self._ax = self._figure.add_subplot(111)

        self.redraw()

    def redraw(self, title=''):
        self._ax.cla()

        self._ax.grid(linestyle='--')
        self._ax.set_title(title + ' training report')
        self._ax.set_xlabel('Progress')
        self._ax.set_ylabel('Error')

        self._annotation = self._ax.annotate('',
                                            xy=(0.85, 0.84),
                                            xycoords='figure fraction',
                                            horizontalalignment='right',
                                            verticalalignment='top',
                                            clip_on=True,
                                            size=25,
                                            bbox=dict(boxstyle='round', ec=None))

        self._ax.set_xlim(0.0, 100.0)
        self._ax.set_ylim(0.0, 100.0)

        self._line, = self._ax.plot([], [], '-')

        self._ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))
        self._ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))

    def mlUpdate(self, graph, clr='blue'):
        self._line.set_xdata(graph[0])
        self._line.set_ydata(graph[1])
        self._line.set_color(clr)

        if len(graph[1]) > 0 :
            self._annotation.set_text('Error:{0:.2f} %'.format(graph[1][-1]))

        self._ax.relim()
        self._ax.autoscale()

        self._figure.canvas.draw_idle()
