#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore    import pyqtSignal

from iface import MLTrainerLoaderBaseIface

class MLTrainerLoaderBaseUI(QDockWidget, MLTrainerLoaderBaseIface):

    mlValidateTrainerSignal = pyqtSignal()

    def __init__(self, plugin, parent = None):
        QDockWidget.__init__(self, parent=parent)

        self.setWindowTitle(plugin.mlGetPluginName() + ' trainer loader')
        self._mainWidget = QWidget()
        self._plugin = plugin

        self._network_filepath = None
        self._trainer_filepath = None
        self._data_filepath    = None
        self._trainer_name     = None

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._mainWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.mlBuildTrainerLoaderMainWidget()

        self.setWidget(self._mainWidget)
        self.setVisible(False)

        self.visibilityChanged.connect(self.mlOnVisibilityChanged)
        self.setFeatures(QDockWidget.DockWidgetClosable)

    def mlResetUI(self):
        self._network_filepath = None
        self._trainer_filepath = None
        self._data_filepath    = None
        self._trainer_name     = None

    def mlOnVisibilityChanged(self, visible):
        if visible:
            editUI = self._plugin.mlGetTrainerEditorUI()

            if editUI is not None:
                editUI.setVisible(not visible)

            self.mlResetUI()

    def mlGetNetworkFilePath(self):
        return self._network_filepath

    def mlGetDataFilePath(self):
        return self._data_filepath

    def mlGetTrainerFilePath(self):
        return self._trainer_filepath

    def mlGetTrainerName(self):
        return self._trainer_name
