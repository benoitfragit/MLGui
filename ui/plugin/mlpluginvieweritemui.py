#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

import uuid


class MLPluginViewerItemUI(QWidget):
    """

    """
    mlPluginActivationChanged = pyqtSignal(uuid.UUID, bool)

    def __init__(self, plugin, trainerMenu, loadUI, parent=None):
        QWidget.__init__(self, parent)

        self._trainerMenu = trainerMenu
        self._item = QListWidgetItem()
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
        try:
            hbox1.addWidget(QLabel(self._plugin.mlGetPluginName()))
        except:
            hbox1.addWidget(QLabel('Plugin name'))
        hbox1.addStretch(1)
        hbox1.addWidget(self._check)

        hbox2.addWidget(QLabel('Author'))
        hbox2.addStretch(1)
        try:
            hbox2.addWidget(QLabel(self._plugin.mlGetPluginAuthor()))
        except:
            hbox2.addWidget(QLabel('Plugin author'))

        hbox3.addWidget(QLabel('Version'))
        hbox3.addStretch(1)
        try:
            hbox3.addWidget(QLabel(self._plugin.mlGetPluginVersion()))
        except:
            hbox3.addWidget(QLabel('Plugin version'))

        try:
            text = QLabel(self._plugin.mlGetPluginDescription())
        except:
            text = QLabel("Plugin description")
        text.setWordWrap(True)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(QLabel('Description'))
        vbox.addWidget(text)

        self.setLayout(vbox)

        self._item.setSizeHint(self.sizeHint())
        self._item.setFlags(self._item.flags() & ~ Qt.ItemIsSelectable)

        self._trainerAction = loadUI.toggleViewAction()

        if self._plugin.mlIsPluginActivated():
            self._trainerMenu.addAction(self._trainerAction)

    def mlGetItem(self):
        """

        @return:
        """
        return self._item

    def mlJSONEncoding(self, d):
        """

        @param d:
        """
        if self._plugin is not None:
            pluginName = self._plugin.mlGetPluginName()

            d[pluginName] = {}
            d[pluginName]['activated'] = self._plugin.mlIsPluginActivated()
            d[pluginName]['trainers'] = {}
            d[pluginName]['networks'] = {}

    def mlOnPluginActivationToggled(self):
        """

        """
        if self._check.isChecked():
            self._plugin.mlSetPluginActivated(True)
            self._trainerMenu.addAction(self._trainerAction)
            self.mlPluginActivationChanged.emit(self._plugin.mlGetUniqId(), True)
        else:
            self._plugin.mlSetPluginActivated(False)
            self._trainerMenu.removeAction(self._trainerAction)
            self.mlPluginActivationChanged.emit(self._plugin.mlGetUniqId(), False)
