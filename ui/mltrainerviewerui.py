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
from mlplot2d        import MLPlot2D

import uuid

class MLTrainerViewerUI(QListWidget):
    mlShowTrainerPlotSignal = pyqtSignal()

    def __init__(self, manager, parent = None):
        QListWidget.__init__(self, parent)

        self._manager = manager

        self._items = {}
        self._displayed = None
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(10)

        # build the plot widget
        self._plot = MLPlot2D()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mlGetPlot(self):
        return self._plot

    def mlShowPlot(self, id):
        if id in self._items.keys():
            self._displayed = id
            self._plot.clear()
            self.mlShowTrainerPlotSignal.emit()

    def mlOnGraphUpdated(self, id):
        item = None
        if self._displayed == id and id in self._items.keys():
            item = self._items[id]
            graph = item.mlTrainerItemGetGraph()
            self._plot.plot(graph, item.mlGetUserName(), 'blue')

    def mlOnRemoveTrainer(self, id):
        if id is not None and id in self._items.keys():
            item = self._items[id].mlGetItem()
            self.takeItem(self.row(item))
            self._items.pop(id)
            self._manager.mlRemoveProcess(id)

            if id == self._displayed :
                self._displayed = None

    def mlRemoveAllTrainers(self):
        for id in self._items.keys():
            self._items[id].mlOnRemoveTrainerClicked()
            self._manager.mlRemoveProcess(id)

    def mlOnNewTrainerAdded(self, trainer):
        if trainer is not None:
            id = trainer.mlGetUniqId()

            if id not in self._items.keys():
                self._items[id] = MLTrainerViewerItemUI(trainer)
                item = self._items[id].mlGetItem()

                self._items[id].removeTrainer.connect(self.mlOnRemoveTrainer)
                self._items[id].graphUpdated.connect(lambda:self.mlOnGraphUpdated(id))
                self._items[id].trainerLaunched.connect(lambda:self.mlShowPlot(id))

                self.addItem(item)
                self.setItemWidget(item, self._items[id])
                self.itemDoubleClicked.connect(lambda:self.mlShowPlot(id))

    def mlJSONEncoding(self, d):
        for trainer in self._items.values():
            if trainer is not None:
                trainer.mlJSONEncoding(d)
