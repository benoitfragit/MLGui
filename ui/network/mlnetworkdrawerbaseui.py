#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui import QPen

from PyQt5.QtCore import Qt

from iface.network import MLNetworkDrawerBaseIface


class MLNetworkDrawerBaseUI(QGraphicsScene, MLNetworkDrawerBaseIface):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self._pen = QPen(Qt.black)
        self._pen.setWidth(5)

    def mlOnDisplayNetwork(self, *args, **kwargs):
        if len(args) >= 1:
            provider = args[0]

            if provider is not None:
                ncols = len(provider.arrays.keys())

                for i in provider.arrays.keys():
                    title = 'Layer ' + str(i)
                    if i == 0:
                        title = 'in'
                    self.mlAddSignalRepresentation(ncols, i, len(provider.arrays[i]), title)

    def mlOnUpdateNetwork(self, *args, **kwargs):
        if len(args) >= 1:
            provider = args[0]

            if self._items and provider is not None:
                for i in provider.arrays.keys():
                    self.mlOnUpdateSignalRepresentation(i, provider.arrays[i])
