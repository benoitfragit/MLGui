#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QActionGroup
from PyQt5.QtWidgets import QLabel

from PyQt5.QtCore    import Qt

from mltrainerviewerui      import MLTrainerViewerUI
from mltrainerloaderbaseui  import MLTrainerLoaderBaseUI
from mlpluginviewerui       import MLPluginViewerUI

from core import MLTrainer

import os

class MLWindow(QMainWindow):
    def __init__(self, trainermanager, pluginloader):
        """
        Building tha mainwindow
        """
        QMainWindow.__init__(self)

        self._trainermanager = trainermanager

        self.setWindowTitle('ML Gui')
        self.resize(500, 300)

        """
        Building the MenuBar
        """
        mainMenu = self.menuBar()

        """
        Building the Manage menu
        """
        manageMenu = mainMenu.addMenu('&Manage')
        trainerMenu = manageMenu.addMenu('&Trainer')
        self._newTrainerMenu = trainerMenu.addMenu('&New trainer')
        networkMenu = manageMenu.addMenu('&Network')
        quit = QAction('Quit', self)
        quit.triggered.connect(self.close)
        manageMenu.addAction(quit)

        """
        Building the DIsplay Menu
        """
        displayMenu = mainMenu.addMenu('&Displays')
        displayTrainers = QAction('&Trainers', self)
        displayTrainers.triggered.connect(self.mlOnDisplayTrainers)
        displayMenu.addAction(displayTrainers)


        """
        Building the Plugin Menu
        """
        pluginMenu = mainMenu.addMenu('&Plugins')

        """
        Build the Help Menu
        """
        helpMenu = mainMenu.addMenu('&Help')
        help = QAction('&Help', self)
        helpMenu.addAction(help)

        """
        Build the trainer viewer
        """
        self._trainerviewer = MLTrainerViewerUI(self._trainermanager, self)
        self._trainerviewer.setVisible(False)

        """
        Build the plugin viewer
        """
        self._pluginviewer = MLPluginViewerUI()
        self._pluginviewer.setVisible(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self._pluginviewer)
        pluginViewerAction = self._pluginviewer.toggleViewAction()
        pluginViewerAction.setCheckable(True)
        pluginMenu.addAction(pluginViewerAction)

        """
        Build the central widget
        """
        self._mainLabel = QLabel()
        self.setCentralWidget(self._mainLabel)

        self.mlRegisterAllPlugins(pluginloader)

    def mlOnDisplayTrainers(self):
        self._trainerviewer.setVisible(True)
        self.setCentralWidget(self._trainerviewer)

    def mlAddPlugin(self, plugin):
        if plugin is not None:
            """
            Populate the plugin viewer ui
            """
            self._pluginviewer.mlOnNewPluginAdded(plugin, self._newTrainerMenu)

            """
            Populate the new trainer menu
            """

            loadUI = plugin.mlGetTrainerLoaderUI()

            if isinstance(loadUI, MLTrainerLoaderBaseUI):
                self.addDockWidget(Qt.LeftDockWidgetArea, loadUI)
                loadUI.mlValidateTrainerSignal.connect(lambda:self.onLoadTrainerValidateClicked(plugin))

    def onLoadTrainerValidateClicked(self, plugin):
        if plugin is not None:
            loadUI = plugin.mlGetTrainerLoaderUI()
            network_filepath = loadUI.mlGetNetworkFilePath()
            data_filepath = loadUI.mlGetDataFilePath()
            trainer_filepath = loadUI.mlGetTrainerFilePath()
            trainer_name = loadUI.mlGetTrainerName()

            if  os.path.exists(network_filepath) and \
                os.path.isfile(network_filepath) and \
                os.path.exists(data_filepath)    and \
                os.path.isfile(data_filepath)    and \
                os.path.exists(trainer_filepath) and \
                os.path.isfile(trainer_filepath):
                    trainer = MLTrainer(self._trainermanager, plugin, network_filepath, data_filepath, trainer_name)
                    trainer.mlConfigureTrainer(trainer_filepath)
                    self._trainermanager.mlAddProcess(trainer)
                    self._trainerviewer.mlOnNewTrainerAdded(trainer)

    def mlRegisterAllPlugins(self, loader):
        plugins = loader.mlGetAllPlugins()
        if plugins is not None:
            for name in plugins.keys():
                self.mlAddPlugin(plugins[name])
