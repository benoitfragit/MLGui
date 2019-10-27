#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui     import QPen
from PyQt5.QtGui     import QBrush

LAYER_WIDTH     = 75.0
LAYER_SPACE     = 25.0
SIGNAL_SPACE    = 8.0
SIGNAL_HEIGHT   = 30.0

class MLNetworkVisualizationUI(QGraphicsView):
    def __init__(self, parent = None):
        self._scene = QGraphicsScene()
        QGraphicsView.__init__(self, self._scene, parent)
        self._pen = QPen(Qt.black)

    def mlAddSignalRepresentation(self, label, signal, length, position):
        if length > 0 and position > 0:
            # find where tho put the signal
            x = LAYER_SPACE * (position + 1.0) + LAYER_WIDTH * position + LAYER_WIDTH / 2.0

            # The signal is drawn symmitricaly around 0
            # TODO
