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
from PyQt5.QtGui     import QPixmap

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import QSize
from PyQt5.QtCore    import pyqtSignal
from PyQt5.QtCore    import QTimer

import pkgutil
import uuid
import os

class MLTrainerViewerItemUI(QWidget):
    removeTrainer = pyqtSignal(uuid.UUID)
    graphUpdated = pyqtSignal()
    trainerLaunched = pyqtSignal()

    def __init__(self, trainer, parent = None):
        QWidget.__init__(self, parent)

        self._graph = ([], [])

        self._trainer = trainer
        self._timer   = QTimer()
        self._timer.timeout.connect(self.mlUpdateTrainerItemOnTimeout)
        self._clearTimer = QTimer()
        self._clearTimer.timeout.connect(self.mlOnClearTrainerItemOnTimeout)

        vbox = QVBoxLayout()

        label   = QLabel(trainer.mlGetUserName())
        label.setAlignment(Qt.AlignCenter)
        dirname = os.path.split(__file__)[0]
        dirname = os.path.join(dirname, 'resources')
        filename = os.path.join(dirname, 'neural.png')
        res = pkgutil.get_loader('ui.resources')
        pixmap = QPixmap(res.filename + os.path.sep + 'neural.png')
        pixmap = pixmap.scaledToWidth(120)
        pixLabel    = QLabel()
        pixLabel.setAlignment(Qt.AlignCenter)
        pixLabel.setPixmap(pixmap)

        vbox.addWidget(label)
        vbox.addWidget(pixLabel)

        self.setLayout(vbox)

        self._item = QListWidgetItem()
        self._item.setSizeHint(self.sizeHint())

        self._clearTimer.start(100)

    def mlGetUserName(self):
        return self._trainer.mlGetUserName()

    def mlGetItem(self):
        return self._item

    def mlTrainerItemGetGraph(self):
        return self._graph

    def mlOnClearTrainerItemOnTimeout(self):
        if self._clearTimer.isActive():
            if not self._trainer.mlIsPluginActivated():
                self._clearTimer.stop()
                self.mlOnRemoveTrainerClicked()

    def mlUpdateTrainerItemOnTimeout(self):
        if self._timer.isActive():
            error       = 100.0 * self._trainer.mlGetTrainerError()
            progress    = 100.0 * self._trainer.mlGetTrainerProgress()

            self.setToolTip('Progress:' + str(progress) + ' Error:' +str(error))

            self._graph[0].append(progress)
            self._graph[1].append(error)

            if not self._trainer.mlIsProcessRunning():
                self._timer.stop()
            else:
                self.graphUpdated.emit()

    def mlOnTrainerRunClicked(self):
        if self._trainer is not None:
            if self._trainer.mlIsProcessPaused():
                self._trainer.mlResumeProcess()
            elif not self._trainer.mlIsProcessRunning() :
                self._trainer.start()
                self._item.setSizeHint(self.sizeHint())
                self._timer.start(250)
                self.trainerLaunched.emit()

    def mlOnTrainerPauseClicked(self):
        if self._trainer is not None:
            self._trainer.mlPauseProcess()

    def mlOnTrainerStopClicked(self):
        if self._trainer is not None:
            if self._trainer.mlIsProcessRunning():
                self._trainer.mlKillProcess()
                self._timer.stop()

    def mlOnRemoveTrainerClicked(self):
        if self._trainer is not None:
            id = self._trainer.mlGetUniqId()
            self._trainer.mlKillProcess()
            self.removeTrainer.emit(id)
            self._timer.stop()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        run    = QAction(QIcon.fromTheme('media-playback-start'), 'Run', self)
        pause  = QAction(QIcon.fromTheme('media-playback-pause'), 'Pause', self)
        stop   = QAction(QIcon.fromTheme('media-playback-stop'), '&Stop', self)
        remove = QAction(QIcon.fromTheme('user-trash'),'&Remove', self)
        configure = QAction(QIcon.fromTheme('document-properties'), '&Configure', self)

        run.triggered.connect(self.mlOnTrainerRunClicked)
        pause.triggered.connect(self.mlOnTrainerPauseClicked)
        stop.triggered.connect(self.mlOnTrainerStopClicked)
        remove.triggered.connect(self.mlOnRemoveTrainerClicked)

        if self._trainer.mlIsProcessRunning():
            is_paused = self._trainer.mlIsProcessPaused()

            stop.setVisible(True)
            configure.setVisible(False)
            run.setVisible(is_paused)
            pause.setVisible(not is_paused)
        else:
            is_not_finished = not self._trainer.mlIsProcessFinish()
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
