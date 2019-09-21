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
import json

class MLWindow(QMainWindow):
    def __init__(self, trainermanager, pluginloader):
        # Building tha mainwindow
        QMainWindow.__init__(self)

        self._trainermanager = trainermanager

        self.setWindowTitle('ML Gui')
        self.resize(500, 300)

        self._mlgui_directory = self.mlGetSavingDirectory()

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

        # Register all plugins
        self.mlRegisterAllPlugins(pluginloader)

    def mlGetSavingDirectory(self):
        saving = '.'

        home = os.environ['HOME']
        if os.path.isdir(home):
            local = os.path.join(home, '.local')
            local = os.path.join(local, 'share')
            if os.path.isdir(local):
                saving = local

        mlgui = os.path.join(saving, 'mlgui')

        if not os.path.isdir(mlgui):
            os.mkdir(mlgui)

        return mlgui

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

    def mlAddNewTrainer(self, plugin, trainer_filepath, network_filepath, data_filepath, trainer_name):
        if  plugin is not None:
            if  network_filepath is not None and \
                os.path.exists(network_filepath) and \
                os.path.isfile(network_filepath) and \
                data_filepath is not None and \
                os.path.exists(data_filepath)    and \
                os.path.isfile(data_filepath):
                    trainer = MLTrainer(trainer_name, self._trainermanager, plugin, network_filepath, data_filepath)

                    if  trainer_filepath is not None and \
                        os.path.exists(trainer_filepath) and \
                        os.path.isfile(trainer_filepath):
                        trainer.mlConfigureTrainer(trainer_filepath)

                    self._trainermanager.mlAddProcess(trainer)
                    self._trainerviewer.mlOnNewTrainerAdded(trainer)
                    self.mlOnDisplayTrainers()

    def onLoadTrainerValidateClicked(self, plugin):
        if plugin is not None:
            loadUI = plugin.mlGetTrainerLoaderUI()
            network_filepath = loadUI.mlGetNetworkFilePath()
            data_filepath = loadUI.mlGetDataFilePath()
            trainer_filepath = loadUI.mlGetTrainerFilePath()
            trainer_name = loadUI.mlGetTrainerName()

            self.mlAddNewTrainer(plugin, trainer_filepath, network_filepath, data_filepath, trainer_name)

    def mlRegisterAllPlugins(self, loader):
        json_file = os.path.join(self._mlgui_directory, 'mlgui.json')

        decoded = None
        if os.path.exists(json_file) and os.path.isfile(json_file):
            with open(json_file, 'r') as jf:
                try:
                    decoded  = json.load(jf)
                except ValueError:
                    pass

        plugins = loader.mlGetAllPlugins()
        if plugins is not None:
            for plugin in plugins.values():
                # Restore plugin status
                name = plugin.mlGetPluginName()
                state = None
                if decoded is not None and name in decoded.keys():
                    state = decoded[name]
                    plugin.mlSetPluginActivated(state['activated'])

                # Add the plugin to the GUI
                self.mlAddPlugin(plugin)

                # Restore all trainers associated to this plugins
                if state is not None:
                    trainers = state['trainers']
                    for username in trainers.keys():
                        trainer          = trainers[username]

                        network_filepath = trainer['network']
                        trainer_filepath = trainer['settings']
                        data_filepath    = trainer['data']

                        error            = trainer['error']
                        progress         = trainer['progress']

                        # Add a new trainer
                        self.mlAddNewTrainer(plugin, trainer_filepath, network_filepath, data_filepath, username)

                        # Finally restore its progression
                        self._trainermanager.mlRestoreProgression(self._mlgui_directory, username, progress, error)

        self._trainerviewer.mlJSONDecoding(decoded)

    def mlSave(self):
        json_file = os.path.join(self._mlgui_directory, 'mlgui.json')

        self._trainermanager.mlSaveProgression(self._mlgui_directory)

        # Saving to JSON current architecture
        encoded = {}
        self._pluginviewer.mlJSONEncoding(encoded)
        self._trainerviewer.mlJSONEncoding(encoded)

        with open(json_file, 'w') as jfile:
            json.dump(encoded, jfile, indent=4)

    def mlLeave(self):
        self.mlSave()
        self._trainerviewer.mlRemoveAllTrainers()
