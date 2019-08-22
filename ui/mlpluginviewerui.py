#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt

from mlpluginvieweritemui  import MLPluginViewerItemUI

class MLPluginViewerUI(QListWidget):
    def __init__(self, manager, parent = None):
        QListWidget.__init__(self, parent)

        self._manager = manager
        self._items = {}

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def mlOnNewPluginAdded(self, plugin):
        if plugin is not None:
            uuid = plugin.mlGetUniqId()

            if uuid not in self._items.keys():
                item = QListWidgetItem()
                internal = MLPluginViewerItemUI(self._manager, plugin)
                #internal.removeTrainer.connect(self.mlOnRemoveTrainer)
                self._items[uuid] = [item, internal]
                item.setSizeHint(self._items[uuid][1].sizeHint())
                self.addItem(self._items[uuid][0])
                self.setItemWidget(self._items[uuid][0], self._items[uuid][1])
