#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import QSize

class MLTrainerViewerItem(QWidget):
    def __init__(self, manager, trainer, parent = None):
        QWidget.__init__(self, parent)

        self._manager = manager
        self._trainer = trainer

        hbox = QHBoxLayout()
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

        hbox.addWidget(self._label)
        hbox.addStretch(1)
        hbox.addWidget(self._run)
        hbox.addWidget(self._pause)
        hbox.addWidget(self._stop)
        hbox.addWidget(configure)
        hbox.addWidget(remove)

        vbox.addWidget(pixLabel)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def mlOnTrainerRunClicked(self):
        if self._manager is not None and self._trainer is not None:
            uuid = self._trainer.mlGetUniqId()
            self._pause.setVisible(True)
            self._stop.setVisible(True)
            self._run.setVisible(False)
            self._manager.mlStartTrainerWithId(uuid)

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
            self._manager.mlResumeTrainerWithId(uuid)

    def mlOnRemoveTrainerClicked(self):
        if self._manager is not None and self._trainer is not None:
            uuid = self._trainer.mlGetUniqId()
            self._pause.setVisible(False)
            self._stop.setVisible(False)
            self._run.setVisible(True)
            self._manager.mlRemoveTrainerWithId(uuid)

class MLTrainerViewerUI(QDockWidget):
    def __init__(self, manager, title= "Trainer viewer", parent = None):
        QDockWidget.__init__(self, title, parent)

        self._manager = manager

        self._list = QListWidget()

        self.setWidget(self._list)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def mlOnNewTrainerAdded(self):
        trainers = self._manager.mlGetAllTrainers()
        for uuid in trainers.keys():
            if uuid is not None:
                trainer = trainers[uuid]
                item = QListWidgetItem()
                internal = MLTrainerViewerItem(self._manager, trainer)
                item.setSizeHint(internal.sizeHint())
                self._list.addItem(item)
                self._list.setItemWidget(item, internal)
