#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt

from mlpluginvieweritemui import MLPluginViewerItemUI

class MLPluginViewerUI(QDockWidget):
    def __init__(self, parent = None):
        QDockWidget.__init__(self, parent=parent)
        self.setWindowTitle('Available plugins')
        self._items = {}

        self._mainWidget = QListWidget()
        self._mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._mainWidget.setResizeMode(QListWidget.Adjust)

        self.setWidget(self._mainWidget)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setVisible(False)

    def mlOnNewPluginAdded(self, plugin, menu):
        if plugin is not None:
            uuid = plugin.mlGetUniqId()

            if uuid not in self._items.keys():
                self._items[uuid] = MLPluginViewerItemUI(plugin, menu)
                self._mainWidget.addItem(self._items[uuid].mlGetItem())
                self._mainWidget.setItemWidget(self._items[uuid].mlGetItem(), self._items[uuid])

    def mlJSONEncoding(self, d):
        for item in self._items.values():
            if item is not None:
                item.mlJSONEncoding(d)