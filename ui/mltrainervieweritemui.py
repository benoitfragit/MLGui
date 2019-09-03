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

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import QSize
from PyQt5.QtCore    import pyqtSignal
from PyQt5.QtCore    import QTimer

from mlplot2d import MLPlot2D

import pkgutil
import uuid
import os

class MLTrainerViewerItemUI(QWidget):
    removeTrainer = pyqtSignal(uuid.UUID)

    def __init__(self, trainer, parent = None):
        QWidget.__init__(self, parent)

        self._plot = MLPlot2D()

        self._trainer = trainer
        self._timer   = QTimer()
        self._timer.timeout.connect(self.mlUpdateTrainerItemOnTimeout)
        self._clearTimer = QTimer()
        self._clearTimer.timeout.connect(self.mlOnClearTrainerItemOnTimeout)

        vbox = QVBoxLayout()

        self._progress = QProgressBar()
        self._progress.setMaximum(100.0)
        self._progress.setMinimum(0.0)
        self._progress.setValue(0.0)
        self._progress.setTextVisible(True)
        self._progress.setVisible(False)
        self._progress.setMaximumHeight(15)

        self._error = QProgressBar()
        self._error.setMaximum(100.0)
        self._error.setMinimum(0.0)
        self._error.setValue(100.0)
        self._error.setTextVisible(True)
        self._error.setVisible(False)
        self._error.setMaximumHeight(15)

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
        vbox.addWidget(self._progress)
        vbox.addWidget(self._error)

        self.setLayout(vbox)

        self._item = QListWidgetItem()
        self._item.setSizeHint(self.sizeHint())

        self._clearTimer.start(100)

    def mlGetItem(self):
        return self._item

    def mlGetPlot(self):
        return self._plot

    def mlOnClearTrainerItemOnTimeout(self):
        if self._clearTimer.isActive():
            if not self._trainer.mlIsPluginActivated():
                self._clearTimer.stop()
                self.mlOnRemoveTrainerClicked()

    def mlUpdateTrainerItemOnTimeout(self):
        if self._timer.isActive():
            error       = 100.0 * self._trainer.mlGetTrainerError()
            progress    = 100.0 * self._trainer.mlGetTrainerProgress()

            self._error.setValue(error)
            self._error.setFormat('Error ' + str(int(error)) + '%')
            self._progress.setValue(progress)
            self._progress.setFormat('Progress ' + str(int(progress)) + '%' )

            self._plot.append(progress, error)
            self._plot.plot()

            if not self._trainer.mlIsProcessRunning():
                self._timer.stop()

    def mlOnTrainerRunClicked(self):
        if self._trainer is not None:
            if self._trainer.mlIsProcessPaused():
                self._trainer.mlResumeProcess()
            elif not self._trainer.mlIsProcessRunning() :
                self._trainer.start()
                self._error.setVisible(True)
                self._progress.setVisible(True)
                self._item.setSizeHint(self.sizeHint())
                self._timer.start(100)

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
