#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGraphicsView

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from ui.trainer.mltrainervieweritemui import MLTrainerViewerItemUI
from ui.trainer.mlplotmanager import MLPlotManager

import uuid


class MLTrainerGraphicsViewUI(QGraphicsView):
    """

    """
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

    def resizeEvent(self, event):
        """

        @param event:
        """
        QGraphicsView.resizeEvent(self, event)
        scene = self.scene()
        if scene is not None:
            self.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)


class MLTrainerOverviewUI(QWidget):
    """

    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self._plot = MLPlotManager()
        self._view = MLTrainerGraphicsViewUI()

        layout = QHBoxLayout()

        layout.addWidget(self._view)
        layout.addWidget(self._plot)

        self.setLayout(layout)

    @property
    def plot(self):
        """

        @return:
        """
        return self._plot

    @property
    def view(self):
        """

        @return:
        """
        return self._view


class MLTrainerViewerUI(QListWidget):
    """

    """
    mlShowTrainerPlotSignal = pyqtSignal()
    mlShowSelectedTrainerPlotSignal = pyqtSignal()
    mlPluginActivationChanged = pyqtSignal(uuid.UUID, bool)

    def __init__(self, manager, parent=None):
        QListWidget.__init__(self, parent)

        self._manager = manager

        self._items = {}
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(30)

        self._overview = MLTrainerOverviewUI()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.itemDoubleClicked.connect(self.mlOnItemDoubleClicked)
        self.itemSelectionChanged.connect(self.mlOnItemSelected)

        self._mouseSelection = False

    def mlOnItemSelected(self):
        """

        """
        items = self.selectedItems()

        if len(items) >= 2:
            self._mouseSelection = True

    def mouseReleaseEvent(self, event):
        """

        @param event:
        """
        if event.button() == Qt.LeftButton and self._mouseSelection:
            self._mouseSelection = False

            self._overview.view.setVisible(False)
            self._overview.plot.setVisible(True)
            self._overview.plot.mlToggleAllPlotsVisibility(False)

            items = self.selectedItems()
            N = len(items)
            i = 0

            for item in items:
                widget = self.itemWidget(item)
                if widget is not None:
                    self._overview.plot.mlSetPlotVisible(widget.mlGetUniqId(), i, N)
                    i = i + 1

            self.mlShowSelectedTrainerPlotSignal.emit()

        QListWidget.mouseReleaseEvent(self, event)

    def mlGetTrainerOverview(self):
        """

        @return:
        """
        return self._overview

    def mlGetItems(self):
        """

        @return:
        """
        return self._items

    def mlShowPlot(self, id):
        """

        @param id:
        """
        if id in self._items.keys():
            self._overview.plot.setVisible(True)
            self._overview.view.setVisible(True)

            self._overview.plot.mlToggleAllPlotsVisibility(False)
            self._overview.plot.mlSetPlotVisible(id, 0, 1)

            self.mlOnGraphUpdated(id)
            self.mlShowSelectedTrainerPlotSignal.emit()

    def mlOnGraphUpdated(self, id):
        """

        @param id:
        """
        item = None

        if id in self._items.keys():
            item = self._items[id]
            graph = item.mlTrainerItemGetGraph()
            self._overview.plot.mlUpdate(id, graph)

    def mlOnRemoveTrainer(self, id):
        """

        @param id:
        """
        if id is not None and id in self._items.keys():
            item = self._items[id].mlGetItem()

            self.takeItem(self.row(item))
            self._items.pop(id)
            self._manager.mlRemoveProcess(id)
            self._overview.plot.mlRemoveSubPlot(id)

    def mlRemoveAllTrainers(self):
        """

        """
        for id in self._items.keys():
            self._overview.plot.mlRemoveSubPlot(id)
            self._items[id].mlKillTrainer()
            self._manager.mlRemoveProcess(id)
        self._items.clear()

    def mlOnNewTrainerAdded(self, trainer, editUI, sceneUI):
        """

        @param trainer:
        @param editUI:
        @param sceneUI:
        """
        if trainer is not None:
            uid = trainer.mlGetUniqId()

            if uid not in self._items.keys():
                self._items[uid] = MLTrainerViewerItemUI(trainer, editUI, sceneUI, self._overview.view)
                item = self._items[uid].mlGetItem()

                self._items[uid].removeTrainer.connect(self.mlOnRemoveTrainer)
                self._items[uid].graphUpdated.connect(lambda: self.mlOnGraphUpdated(uid))
                self._items[uid].trainerLaunched.connect(lambda: self.mlShowPlot(uid))

                self.addItem(item)
                self.setItemWidget(item, self._items[uid])

                self._overview.plot.mlAddSubPlot(uid, self._items[uid])

                self.mlPluginActivationChanged.connect(self._items[uid].mlOnPluginActivationChanged)

    def mlOnItemDoubleClicked(self, item):
        """

        @param item:
        """
        if item is not None:
            widget = self.itemWidget(item)

            if widget is not None:
                id = widget.mlGetUniqId()
                widget.mlOnDisplayTrainer()
                self.mlShowPlot(id)

    def mlJSONDecoding(self, d):
        """

        @param d:
        """
        for trainer in self._items.values():
            if trainer is not None:
                trainer.mlJSONDecoding(d)

    def mlJSONEncoding(self, d):
        """

        @param d:
        """
        for trainer in self._items.values():
            if trainer is not None:
                trainer.mlJSONEncoding(d)

    def mlOnPluginActivationChanged(self, id, activated):
        """

        @param id:
        @param activated:
        """
        self.mlPluginActivationChanged.emit(id, activated)
