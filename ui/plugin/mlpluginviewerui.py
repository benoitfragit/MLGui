#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ui.plugin.mlpluginvieweritemui import MLPluginViewerItemUI

import uuid


class MLPluginViewerUI(QDockWidget):
    """

    """
    mlPluginActivationChanged = pyqtSignal(uuid.UUID, bool)

    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent=parent)
        self.setWindowTitle('Available plugins')
        self._items = {}

        self._mainWidget = QListWidget()
        self._mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._mainWidget.setResizeMode(QListWidget.Adjust)

        self.setWidget(self._mainWidget)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setVisible(False)

    def mlOnNewPluginAdded(self, plugin, menu, loadUI):
        """

        @param plugin:
        @param menu:
        @param loadUI:
        """
        if plugin is not None:
            uid = plugin.mlGetUniqId()

            if uid not in self._items.keys():
                self._items[uid] = MLPluginViewerItemUI(plugin, menu, loadUI)
                self._mainWidget.addItem(self._items[uid].mlGetItem())
                self._mainWidget.setItemWidget(self._items[uid].mlGetItem(), self._items[uid])
                self._items[uid].mlPluginActivationChanged.connect(self.mlOnPluginActivationChanged)

    def mlOnPluginActivationChanged(self, id, activated):
        """

        @param id:
        @param activated:
        """
        self.mlPluginActivationChanged(id, activated)

    def mlJSONEncoding(self, d):
        """

        @param d:
        """
        for item in self._items.values():
            if item is not None:
                item.mlJSONEncoding(d)
