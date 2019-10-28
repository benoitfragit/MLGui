#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import pyqtSignal

from mlnetworkvieweritemui import MLNetworkViewerItemUI

import uuid

class MLNetworkViewerUI(QListWidget):
    mlShowNetworkSignal = pyqtSignal()

    def __init__(self, parent = None):
        QListWidget.__init__(self, parent)

        self._items = {}

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(30)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.itemDoubleClicked.connect(self.mlOnItemDoubleClicked)

    def mlOnNewNetworkAdded(self, network):
        if network is not None:
            uid = network.mlGetUniqId()

            if uid not in self._items.keys():
                self._items[uid] = MLNetworkViewerItemUI(network)
                item = self._items[uid].mlGetItem()

                self._items[uid].removeNetwork.connect(self.mlOnRemoveNetwork)

                self.addItem(item)
                self.setItemWidget(item, self._items[uid])

    def mlOnRemoveManagedNetwork(self, id):
        self.mlOnRemoveNetwork(id)

    def mlOnRemoveNetwork(self, uid):
        if uid is not None and uid in self._items.keys():
            item = self._items[uid].mlGetItem()
            self.takeItem(self.row(item))
            self._items.pop(uid)

    def mlOnItemDoubleClicked(self, widget):
        if widget is not None:
            item = self.itemWidget(widget)
            if item is not None:
                item.mlDisplayNetwork()

    def mlJSONDecoding(self, d):
        pass

    def mlJSONEncoding(self, d):
        pass
