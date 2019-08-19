#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt

from mltrainervieweritemui  import MLTrainerViewerItemUI

class MLTrainerViewerUI(QListWidget):
    def __init__(self, manager, parent = None):
        QListWidget.__init__(self, parent)

        self._manager = manager

        self._items = {}
        self.setViewMode(QListWidget.IconMode)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mlOnRemoveTrainer(self, uuid):
        if uuid is not None and uuid in self._items.keys():
            self.takeItem(self.row(self._items[uuid][0]))
            self._items.pop(uuid)

    def mlOnNewTrainerAdded(self, trainer):
        if trainer is not None:
            uuid = trainer.mlGetUniqId()

            if uuid not in self._items.keys():
                item = QListWidgetItem()
                internal = MLTrainerViewerItemUI(self._manager, trainer)
                internal.removeTrainer.connect(self.mlOnRemoveTrainer)
                self._items[uuid] = [item, internal]
                item.setSizeHint(self._items[uuid][1].sizeHint())
                self.addItem(self._items[uuid][0])
                self.setItemWidget(self._items[uuid][0], self._items[uuid][1])
