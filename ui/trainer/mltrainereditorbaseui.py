#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QSizePolicy

from iface.trainer.mltrainereditorbaseiface import MLTrainerEditorBaseIface


class MLTrainerEditorBaseUI(QDockWidget, MLTrainerEditorBaseIface):
    def __init__(self, plugin, parent=None):
        QDockWidget.__init__(self, parent=parent)

        try:
            self.setWindowTitle(plugin.mlGetPluginName() + ' trainer editor')
        except:
            self.setWindowTitle('Plugin trainer editor')
        self._mainWidget = QWidget()
        self._plugin = plugin

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._mainWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.mlBuildTrainerEditorMainWidget()

        self.setWidget(self._mainWidget)
        self.setVisible(False)

        self.visibilityChanged.connect(self.mlOnVisibilityChanged)
        self.setFeatures(QDockWidget.DockWidgetClosable)

        self._exclusiveUI = None

    def setExclusiveUI(self, exclusive):
        self._exclusiveUI = exclusive

    def mlResetUI(self):
        pass

    def mlOnVisibilityChanged(self, visible):
        if visible:
            if self._exclusiveUI is not None:
                self._exclusiveUI.setVisible(not visible)

            self.mlResetUI()
