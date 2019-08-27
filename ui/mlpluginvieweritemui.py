#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore    import pyqtSignal

import uuid

class MLPluginViewerItemUI(QWidget):

    activatePlugin      = pyqtSignal(uuid.UUID)
    deactivatePlugin    = pyqtSignal(uuid.UUID)

    def __init__(self, plugin, item, parent = None):
        QWidget.__init__(self, parent)

        self._item   = item
        self._plugin = plugin

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        vbox = QVBoxLayout()

        self._check = QCheckBox()
        self._check.setChecked(self._plugin.mlIsPluginActivated())
        self._check.toggled.connect(self.mlOnPluginActivationToggled)
        hbox1.addWidget(QLabel('Plugin'))
        hbox1.addWidget(QLabel(self._plugin.mlGetPluginName()))
        hbox1.addStretch(1)
        hbox1.addWidget(self._check)

        hbox2.addWidget(QLabel('Author'))
        hbox2.addStretch(1)
        hbox2.addWidget(QLabel(self._plugin.mlGetPluginAuthor()))

        hbox3.addWidget(QLabel('Version'))
        hbox3.addStretch(1)
        hbox3.addWidget(QLabel(self._plugin.mlGetPluginVersion()))

        hbox4.addWidget(QLabel('Description'))
        hbox4.addStretch(1)
        hbox4.addWidget(QLabel(self._plugin.mlGetPluginDescription()))

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

        self._item.setSizeHint(self.sizeHint())

    def mlOnPluginActivationToggled(self):
        if self._check.isChecked():
            self._plugin.mlSetPluginActivated(True)
            self.activatePlugin.emit(self._plugin.mlGetUniqId())
        else:
            self._plugin.mlSetPluginActivated(False)
            self.deactivatePlugin.emit(self._plugin.mlGetUniqId())
