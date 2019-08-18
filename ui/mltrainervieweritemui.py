#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import QSize
from PyQt5.QtCore    import pyqtSignal

import uuid

class MLTrainerViewerItemUI(QWidget):
    removeTrainer = pyqtSignal(uuid.UUID)

    def __init__(self, manager, trainer, parent = None):
        QWidget.__init__(self, parent)

        self._manager = manager
        self._trainer = trainer

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox = QVBoxLayout()

        self._label = QLabel(trainer.mlGetUserName())
        pixmap      = QIcon.fromTheme('drive-harddisk').pixmap(QSize(90, 90))
        pixLabel    = QLabel()
        pixLabel.setAlignment(Qt.AlignCenter)
        pixLabel.setPixmap(pixmap)

        self._run   = QPushButton()
        self._pause = QPushButton()
        self._stop  = QPushButton()
        configure   = QPushButton()
        remove      = QPushButton()

        self._run.setIcon(QIcon.fromTheme('media-playback-start'))
        self._pause.setIcon(QIcon.fromTheme('media-playback-pause'))
        self._pause.setVisible(False)
        self._stop.setIcon(QIcon.fromTheme('media-playback-stop'))
        self._stop.setVisible(False)
        configure.setIcon(QIcon.fromTheme('document-properties'))
        remove.setIcon(QIcon.fromTheme('user-trash'))

        self._run.clicked.connect(self.mlOnTrainerRunClicked)
        self._pause.clicked.connect(self.mlOnTrainerPauseClicked)
        self._stop.clicked.connect(self.mlOnTrainerStopClicked)
        remove.clicked.connect(self.mlOnRemoveTrainerClicked)

        hbox1.addWidget(configure)
        hbox1.addStretch(1)
        hbox1.addWidget(remove)

        hbox2.addWidget(self._run)
        hbox2.addWidget(self._pause)
        hbox2.addStretch(1)
        hbox2.addWidget(self._label)
        hbox2.addStretch(1)
        hbox2.addWidget(self._stop)

        vbox.addLayout(hbox1)
        vbox.addWidget(pixLabel)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def mlOnTrainerRunClicked(self):
        if self._manager is not None and self._trainer is not None:
            uuid = self._trainer.mlGetUniqId()
            if self._manager.mlIsTrainerWithIdRunning(uuid) is not True:
                self._pause.setVisible(True)
                self._stop.setVisible(True)
                self._run.setVisible(False)
                self._manager.mlStartTrainerWithId(uuid)
            elif self._manager.mlIsTrainerWithIdPaused(uuid):
                self._pause.setVisible(True)
                self._stop.setVisible(True)
                self._run.setVisible(False)
                self._manager.mlResumeTrainerWithId(uuid)

    def mlOnTrainerPauseClicked(self):
        if self._manager is not None and self._trainer is not None:
            uuid = self._trainer.mlGetUniqId()
            self._pause.setVisible(False)
            self._stop.setVisible(False)
            self._run.setVisible(True)
            self._manager.mlPauseTrainerWithId(uuid)

    def mlOnTrainerStopClicked(self):
        if self._manager is not None and self._trainer is not None:
            uuid = self._trainer.mlGetUniqId()
            self._pause.setVisible(False)
            self._stop.setVisible(False)
            self._run.setVisible(True)
            self._manager.mlStopTrainerWithId(uuid)

    def mlOnRemoveTrainerClicked(self):
        if self._manager is not None and self._trainer is not None:
            uuid = self._trainer.mlGetUniqId()
            self._pause.setVisible(False)
            self._stop.setVisible(False)
            self._run.setVisible(True)
            self._manager.mlRemoveTrainerWithId(uuid)
            self.removeTrainer.emit(uuid)
