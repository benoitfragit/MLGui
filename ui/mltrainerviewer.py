#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QSizePolicy

class MLTrainerViewer(QDockWidget):
    def __init__(self, manager, title= "Trainer viewer", parent = None):
        QDockWidget.__init__(self, title, parent)

        self._manager = manager

        self._list = QListWidget()

        self.setWidget(self._list)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def mlOnTrainerManagerListChanged(self):
        trainers = self._manager.mlGetAllTrainers()
        for uuid in trainers.keys():
            if uuid is not None:
                trainer = trainers[uuid]
                self._list.addItem(trainer.mlGetUserName())
