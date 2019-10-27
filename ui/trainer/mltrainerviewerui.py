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
from mlplotmanager          import MLPlotManager

import uuid

class MLTrainerViewerUI(QListWidget):
    mlShowTrainerPlotSignal = pyqtSignal()
    mlShowSelectedTrainerPlotSignal = pyqtSignal()
    mlRemoveManagedNetworkSignal = pyqtSignal(uuid.UUID)

    def __init__(self, manager, parent = None):
        QListWidget.__init__(self, parent)

        self._manager = manager

        self._items = {}
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(30)

        # build the multiple plots widget
        self._allplots = MLPlotManager()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.itemDoubleClicked.connect(self.mlOnItemDoubleClicked)
        self.itemSelectionChanged.connect(self.mlOnItemSelected)

        self._mouseSelection = False

    def mlOnItemSelected(self):
        items = self.selectedItems()

        if len(items) >= 2:
            self._mouseSelection = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._mouseSelection:
            self._mouseSelection = False

            self._allplots.mlToggleAllPlotsVisibility(False)

            items = self.selectedItems()
            N = len(items)
            i = 0

            for item in items:
                widget = self.itemWidget(item)
                if widget is not None:
                    self._allplots.mlSetPlotVisible(widget.mlGetUniqId(), i, N)
                    i = i + 1

            self.mlShowSelectedTrainerPlotSignal.emit()

        QListWidget.mouseReleaseEvent(self, event)

    def mlGetPlotManager(self):
        return self._allplots

    def mlGetItems(self):
        return self._items

    def mlShowPlot(self, id):
        if id in self._items.keys():
            self._allplots.mlToggleAllPlotsVisibility(False)
            self._allplots.mlSetPlotVisible(id, 0, 1)
            self.mlOnGraphUpdated(id)
            self.mlShowSelectedTrainerPlotSignal.emit()

    def mlOnGraphUpdated(self, id):
        item = None

        if id in self._items.keys():
            item = self._items[id]
            graph = item.mlTrainerItemGetGraph()
            self._allplots.mlUpdate(id, graph)

    def mlOnRemoveTrainer(self, id):
        if id is not None and id in self._items.keys():
            item = self._items[id].mlGetItem()

            networkId = self._items[id].mlGetManagedNetworkId()
            self.mlRemoveManagedNetworkSignal.emit(networkId)

            self.takeItem(self.row(item))
            self._items.pop(id)
            self._manager.mlRemoveProcess(id)
            self._allplots.mlRemoveSubPlot(id)

    def mlRemoveAllTrainers(self):
        for id in self._items.keys():
            self._allplots.mlRemoveSubPlot(id)
            self._items[id].mlOnRemoveTrainerClicked()
            self._manager.mlRemoveProcess(id)

    def mlOnNewTrainerAdded(self, trainer, editUI):
        if trainer is not None:
            uid = trainer.mlGetUniqId()

            if uid not in self._items.keys():
                self._items[uid] = MLTrainerViewerItemUI(trainer, editUI)
                item = self._items[uid].mlGetItem()

                self._items[uid].removeTrainer.connect(self.mlOnRemoveTrainer)
                self._items[uid].graphUpdated.connect(lambda:self.mlOnGraphUpdated(uid))
                self._items[uid].trainerLaunched.connect(lambda:self.mlShowPlot(uid))

                self.addItem(item)
                self.setItemWidget(item, self._items[uid])

                self._allplots.mlAddSubPlot(uid, self._items[uid])

    def mlOnItemDoubleClicked(self, obj):
        if obj is not None:
            for id in self._items.keys():
                item = self._items[id]

                if obj == item.mlGetItem():
                    self.mlShowPlot(id)
                    break

    def mlJSONDecoding(self, d):
        for trainer in self._items.values():
            if trainer is not None:
                trainer.mlJSONDecoding(d)

    def mlJSONEncoding(self, d):
        for trainer in self._items.values():
            if trainer is not None:
                trainer.mlJSONEncoding(d)
