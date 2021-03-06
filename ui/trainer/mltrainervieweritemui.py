#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer

from importlib import resources
from ui import data

import random
import uuid
import os


class MLTrainerViewerItemUI(QWidget):
    """

    """
    removeTrainer = pyqtSignal(uuid.UUID)
    graphUpdated = pyqtSignal()
    trainerLaunched = pyqtSignal()

    def __init__(self, trainer, editui, sceneui, view, parent=None):
        QWidget.__init__(self, parent)

        self._graph = [[], []]

        self._trainer = trainer
        self._editui = editui
        self._view = view
        self._timer = QTimer()
        self._timer.timeout.connect(self.mlUpdateTrainerItemOnTimeout)

        self._scene = sceneui

        vbox = QVBoxLayout()

        label = QLabel(trainer.username)
        label.setAlignment(Qt.AlignCenter)
        pixLabel = QLabel()
        with resources.path(data, 'trainer.png') as p:
            pixmap = QPixmap(str(p))
            pixmap = pixmap.scaledToWidth(120)
            pixLabel.setAlignment(Qt.AlignCenter)
            pixLabel.setPixmap(pixmap)

        vbox.addWidget(label)
        vbox.addWidget(pixLabel)

        self.setLayout(vbox)

        self._item = QListWidgetItem()
        self._item.setSizeHint(self.sizeHint())

    def mlGetUserName(self):
        """

        @return:
        """
        return self._trainer.username

    def mlGetItem(self):
        """

        @return:
        """
        return self._item

    def mlTrainerItemGetData(self):
        """

        @return:
        """
        error   = 100.0 * self._trainer.mlGetTrainerError()
        progress= 100.0 * self._trainer.mlGetTrainerProgress()
        fps     = self._trainer.mlGetUpdateRate()
        return self._graph, error, progress, fps

    def mlUpdateTrainerItemOnTimeout(self):
        """

        """
        if self._timer.isActive():
            error = 100.0 * self._trainer.mlGetTrainerError()
            progress = 100.0 * self._trainer.mlGetTrainerProgress()

            self.setToolTip('Progress:' + str(progress) + ' Error:' + str(error))

            val = -1.0
            if len(self._graph[0]) > 0:
                val = self._graph[0][-1]

            if val < progress:
                self._graph[0].append(progress)
                self._graph[1].append(error)
                self.graphUpdated.emit()

            self._trainer.mlUpdateNetworkDrawerUI(self._scene)

            if not self._trainer.mlIsProcessRunning():
                self._timer.stop()

    def mlOnTrainerRunClicked(self):
        """

        """
        if self._trainer is not None:
            if self._trainer.mlIsProcessPaused():
                self._trainer.mlResumeProcess()
            elif not self._trainer.mlIsProcessRunning():
                self._trainer.mlTrainerRun()
                self._item.setSizeHint(self.sizeHint())
                self._timer.start(1)
                self.mlOnDisplayTrainer()
                self.trainerLaunched.emit()

    def mlOnTrainerPauseClicked(self):
        """

        """
        if self._trainer is not None:
            self._trainer.mlPauseProcess()

    def mlOnTrainerStopClicked(self):
        """

        """
        if self._trainer is not None:
            if self._trainer.mlIsProcessRunning():
                self._trainer.mlKillProcess()
                self._timer.stop()

    def mlKillTrainer(self):
        """

        """
        self._trainer.mlKillProcess()

    def mlOnRemoveTrainerClicked(self):
        """

        """
        if self._trainer is not None:
            id = self._trainer.mlGetUniqId()
            self.mlKillTrainer()
            self.removeTrainer.emit(id)
            self._timer.stop()

    def mlOnConfigureTrainedClicked(self):
        """

        """
        if self._trainer is not None:
            self._editui.fromTrainer(self._trainer)

    def contextMenuEvent(self, event):
        """

        @param event:
        """
        menu = QMenu(self)
        run = QAction(QIcon.fromTheme('media-playback-start'), 'Run', self)
        pause = QAction(QIcon.fromTheme('media-playback-pause'), 'Pause', self)
        stop = QAction(QIcon.fromTheme('media-playback-stop'), '&Stop', self)
        remove = QAction(QIcon.fromTheme('user-trash'), '&Remove', self)
        configure = QAction(QIcon.fromTheme('document-properties'), '&Configure', self)

        run.triggered.connect(self.mlOnTrainerRunClicked)
        pause.triggered.connect(self.mlOnTrainerPauseClicked)
        stop.triggered.connect(self.mlOnTrainerStopClicked)
        remove.triggered.connect(self.mlOnRemoveTrainerClicked)
        configure.triggered.connect(self.mlOnConfigureTrainedClicked)

        if self._trainer.mlIsProcessRunning():
            is_paused = self._trainer.mlIsProcessPaused()

            stop.setVisible(True)
            configure.setVisible(False)
            run.setVisible(is_paused)
            pause.setVisible(not is_paused)
        else:
            is_not_finished = not self._trainer.mlIsProcessFinished()
            run.setVisible(is_not_finished)
            configure.setVisible(is_not_finished)
            stop.setVisible(False)
            pause.setVisible(False)

        menu.addAction(run)
        menu.addAction(pause)
        menu.addAction(stop)
        menu.addAction(configure)
        menu.addAction(remove)
        menu.exec_(self.mapToGlobal(event.pos()))

    def mlJSONEncoding(self, d):
        """

        @param d:
        """
        pluginName = self._trainer.mlGetPluginName()
        if pluginName in d.keys() and 'trainers' in d[pluginName].keys():
            username = self.mlGetUserName()

            self._trainer.mlJSONEncoding(d[pluginName]['trainers'])

            d[pluginName]['trainers'][username]['graph_x'] = []
            d[pluginName]['trainers'][username]['graph_x'] = self._graph[0][:]
            d[pluginName]['trainers'][username]['graph_y'] = []
            d[pluginName]['trainers'][username]['graph_y'] = self._graph[1][:]

    def mlJSONDecoding(self, d):
        """

        @param d:
        """
        pluginname = self._trainer.mlGetPluginName()
        username = self._trainer.username

        if pluginname in d.keys():
            if username in d[pluginname]['trainers'].keys():
                if 'graph_x' in d[pluginname]['trainers'][username].keys():
                    self._graph[0] = d[pluginname]['trainers'][username]['graph_x'][:]
                if 'graph_y' in d[pluginname]['trainers'][username].keys():
                    self._graph[1] = d[pluginname]['trainers'][username]['graph_y'][:]
                if 'exit' in d[pluginname]['trainers'][username].keys():
                    self._trainer.mlSetTrainerExited(d[pluginname]['trainers'][username]['exit'] > 0)

                self.graphUpdated.emit()

    def mlGetUniqId(self):
        """

        @return:
        """
        return self._trainer.mlGetUniqId()

    def mlOnDisplayTrainer(self):
        """

        """
        if self._view is not None:
            # Initially create the scene
            self._trainer.mlDisplayNetworkDrawerUI(self._scene)
            self._view.setScene(self._scene)
            self._view.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def mlOnPluginActivationChanged(self, id, activated):
        """

        @param id:
        @param activated:
        """
        if self._trainer is not None and not activated and id == self._trainer.mlGetPluginId():
            self.mlOnRemoveTrainerClicked()
