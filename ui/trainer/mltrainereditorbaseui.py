#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QSizePolicy

from iface import MLTrainerEditorBaseIface

class MLTrainerEditorBaseUI(QDockWidget, MLTrainerEditorBaseIface):
    def __init__(self, plugin, parent = None):
        QDockWidget.__init__(self, parent=parent)

        self.setWindowTitle(plugin.mlGetPluginName() + ' trainer editor')
        self._mainWidget = QWidget()
        self._plugin = plugin

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._mainWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.mlBuildTrainerEditorMainWidget()

        self.setWidget(self._mainWidget)
        self.setVisible(False)

        self.visibilityChanged.connect(self.mlOnVisibilityChanged)
        self.setFeatures(QDockWidget.DockWidgetClosable)


    def mlResetUI(self):
        pass

    def mlOnVisibilityChanged(self, visible):
        if visible:
            loadUI = self._plugin.mlGetTrainerLoaderUI()

            if loadUI is not None:
                loadUI.setVisible(not visible)

            self.mlResetUI()
