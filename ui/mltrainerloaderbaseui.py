#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

class MLTrainerLoaderBaseUI(QWidget):
    def __init__(self, plugin):
        QWidget.__init__(self)

        self._plugin = plugin

        self._network_filepath = None
        self._trainer_filepath = None
        self._data_filepath    = None
        self._trainer_name     = None

        self.resize(350, 200)
        self.setWindowTitle(plugin.mlGetPluginName() + ' trainer builder')

    def mlGetValidateButton(self):
        return self._validate

    def mlGetNetworkFilePath(self):
        return self._network_filepath

    def mlGetDataFilePath(self):
        return self._data_filepath

    def mlGetTrainerFilePath(self):
        return self._trainer_filepath

    def mlGetTrainerName(self):
        return self._trainer_name
