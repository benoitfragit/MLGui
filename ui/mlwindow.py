#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QActionGroup
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStackedWidget

from PyQt5.QtCore           import Qt

from mltrainerviewerui      import MLTrainerViewerUI
from mltrainerloaderbaseui  import MLTrainerLoaderBaseUI
from mlpluginviewerui       import MLPluginViewerUI

from core import MLTrainer

import os

class MLWindow(QMainWindow):
    def __init__(self, trainermanager, pluginloader):
        # Building tha mainwindow
        QMainWindow.__init__(self)

        self._trainermanager = trainermanager

        self.setWindowTitle('ML Gui')
        self.resize(500, 300)

        # Building the MenuBar
        mainMenu = self.menuBar()

        # Building the Manage menu
        manageMenu = mainMenu.addMenu('&Manage')
        trainerMenu = manageMenu.addMenu('&Trainer')
        self._newTrainerMenu = trainerMenu.addMenu('&New trainer')
        networkMenu = manageMenu.addMenu('&Network')
        quit = QAction('Quit', self)
        quit.triggered.connect(self.close)
        manageMenu.addAction(quit)

        # Building the DIsplay Menu
        displayMenu = mainMenu.addMenu('&Displays')
        displayTrainers = QAction('&Trainers', self)
        displayTrainers.triggered.connect(self.mlOnDisplayTrainers)
        displayMenu.addAction(displayTrainers)

        # Building the Plugin Menu
        pluginMenu = mainMenu.addMenu('&Plugins')

        # Build the Help Menu
        helpMenu = mainMenu.addMenu('&Help')
        help = QAction('&Help', self)
        helpMenu.addAction(help)

        # Build the trainer viewer
        self._trainerviewer = MLTrainerViewerUI(self._trainermanager)
        self._trainerviewer.mlShowTrainerPlotSignal.connect(self.mlOnShowTrainerPlot)

        # Build the plugin viewer
        self._pluginviewer = MLPluginViewerUI()
        self._pluginviewer.setVisible(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self._pluginviewer)
        pluginViewerAction = self._pluginviewer.toggleViewAction()
        pluginViewerAction.setCheckable(True)
        pluginMenu.addAction(pluginViewerAction)

        # Build the default label
        self._mainLabel = QLabel()

        # build the statckwidget
        stackwidget = QStackedWidget()
        stackwidget.addWidget(self._mainLabel)
        stackwidget.addWidget(self._trainerviewer)
        stackwidget.addWidget(self._trainerviewer.mlGetPlot())

        # Build the central widget
        self.setCentralWidget(stackwidget)

        self.mlRegisterAllPlugins(pluginloader)

    def mlOnShowTrainerPlot(self):
        self.centralWidget().setCurrentIndex(2)

    def mlOnDisplayTrainers(self):
        self.centralWidget().setCurrentIndex(1)

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
                    self.mlOnDisplayTrainers()

    def mlRegisterAllPlugins(self, loader):
        plugins = loader.mlGetAllPlugins()
        if plugins is not None:
            for name in plugins.keys():
                self.mlAddPlugin(plugins[name])

    def mlSave(self):
        saving = '.'

        home = os.environ['HOME']
        if os.path.isdir(home):
            local = os.path.join(home, '.local')
            if os.path.isdir(local):
                saving = local

        mlgui = os.path.join(saving, 'mlgui')

        if not os.path.isdir(mlgui):
            os.mkdir(mlgui)

    def mlLeave(self):
        self.mlSave()
        self._trainerviewer.mlRemoveAllTrainers()
