#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mlplot2d import MLPlot2D
from matplotlib.ticker import FormatStrFormatter

class MLErrorPlot(MLPlot2D):
    def __init__(self):
        MLPlot2D.__init__(self)

    def redraw(self, title=''):
        MLPlot2D.redraw(self, title)

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

        self._ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))
        self._ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f %%'))

    def mlUpdateMore(self, graph):
        MLPlot2D.mlUpdateMore(self, graph)

        if len(graph[1]) > 0 :
            self._annotation.set_text('Error:{0:.2f} %'.format(graph[1][-1]))
