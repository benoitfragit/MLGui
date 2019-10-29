#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui     import QPen

from PyQt5.QtCore    import Qt

from iface           import MLNetworkDrawerBaseIface

class MLNetworkDrawerBaseUI(QGraphicsScene, MLNetworkDrawerBaseIface):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self._pen = QPen(Qt.black)
        self._pen.setWidth(5)
