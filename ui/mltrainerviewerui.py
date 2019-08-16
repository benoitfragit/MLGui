#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton


from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt

from mltrainervieweritemui  import MLTrainerViewerItemUI

class MLTrainerViewerUI(QDockWidget):
    def __init__(self, manager, title= "Trainer viewer", parent = None):
        QDockWidget.__init__(self, title, parent)

        self._manager = manager

        self._list = QListWidget()
        self._list.setViewMode(QListWidget.IconMode)

        self.setWidget(self._list)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def mlOnNewTrainerAdded(self):
        trainers = self._manager.mlGetAllTrainers()
        for uuid in trainers.keys():
            if uuid is not None:
                trainer = trainers[uuid]
                item = QListWidgetItem()
                internal = MLTrainerViewerItemUI(self._manager, trainer)
                item.setSizeHint(internal.sizeHint())
                self._list.addItem(item)
                self._list.setItemWidget(item, internal)
