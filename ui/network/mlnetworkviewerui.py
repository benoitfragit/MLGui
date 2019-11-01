#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGraphicsView

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import QTimer
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import pyqtSignal

from mlnetworkvieweritemui import MLNetworkViewerItemUI

import uuid

class MLGraphicsView(QGraphicsView):
    def __init__(self, parent = None):
        QGraphicsView.__init__(self, parent)

    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self, event)
        scene = self.scene()
        if scene is not None:
            self.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

class MLNetworkViewerUI(QListWidget):
    mlShowNetworkSignal = pyqtSignal()

    def __init__(self, parent = None):
        QListWidget.__init__(self, parent)

        self._items = {}

        self._timer = QTimer()
        self._timer.timeout.connect(self.mlOnUpdateGraphicsView)
        self._displayed = None;

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(30)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.itemDoubleClicked.connect(self.mlOnItemDoubleClicked)

        self._viewer = MLGraphicsView()

    def mlOnUpdateGraphicsView(self):
        if self._displayed is not None:
            self._displayed.mlOnUpdate()

    def mlOnNetworkProviderAdded(self, network):
        if network is not None:
            uid = network.mlGetUniqId()

            if uid not in self._items.keys():
                self._items[uid] = MLNetworkViewerItemUI(network)
                item = self._items[uid].mlGetItem()

                self._items[uid].removeNetwork.connect(self.mlOnRemoveNetwork)

                self.addItem(item)
                self.setItemWidget(item, self._items[uid])

    def mlOnRemoveProvider(self, id):
        self.mlOnRemoveNetwork(id)

    def mlOnRemoveNetwork(self, uid):
        if uid is not None and uid in self._items.keys():
            if self._items[uid] == self._displayed:
                self._timer.stop()
                self._displayed = None
            item = self._items[uid].mlGetItem()
            self.takeItem(self.row(item))
            self._items.pop(uid)

    def mlOnItemDoubleClicked(self, widget):
        if widget is not None:
            item = self.itemWidget(widget)
            if item is not None:
                self._timer.stop()
                self._timer.start(100)
                self._displayed = item
                item.mlOnDisplayNetwork(self._viewer)
                self.mlShowNetworkSignal.emit()

    def mlGetNetworkViewer(self):
        return self._viewer;

    def mlJSONDecoding(self, d):
        pass

    def mlJSONEncoding(self, d):
        pass
