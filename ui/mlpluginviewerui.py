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
                item = QListWidgetItem()
                internal = MLPluginViewerItemUI(plugin, menu, item)
                self._items[uuid] = [item, internal]
                self._mainWidget.addItem(self._items[uuid][0])
                self._mainWidget.setItemWidget(self._items[uuid][0], self._items[uuid][1])
