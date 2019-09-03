#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import pyqtSignal

from mltrainervieweritemui  import MLTrainerViewerItemUI

import uuid

class MLTrainerViewerUI(QListWidget):

    showPlot = pyqtSignal(uuid.UUID)

    def __init__(self, manager, parent = None):
        QListWidget.__init__(self, parent)

        self._manager = manager

        self._items = {}
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(10)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mlShowPlot(self, id):
        self.showPlot.emit(id)

    def mlGetPlotWidget(self, id):
        widget = None
        if id is not None and id in self._items.keys():
            widget= self._items[id].mlGetPlot()
        return widget

    def mlOnRemoveTrainer(self, id):
        if id is not None and id in self._items.keys():
            item = self._items[id].mlGetItem()
            self.takeItem(self.row(item))
            self._items.pop(id)
            self._manager.mlRemoveProcess(id)

    def mlOnNewTrainerAdded(self, trainer):
        if trainer is not None:
            id = trainer.mlGetUniqId()

            if id not in self._items.keys():
                self._items[id] = MLTrainerViewerItemUI(trainer)
                item = self._items[id].mlGetItem()

                self._items[id].removeTrainer.connect(self.mlOnRemoveTrainer)

                self.addItem(item)
                self.setItemWidget(item, self._items[id])
                self.itemDoubleClicked.connect(lambda:self.mlShowPlot(id))
