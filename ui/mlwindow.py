#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
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
        displayTrainers = QAction('&Display', self)
        trainerMenu.addAction(displayTrainers)
        networkMenu = manageMenu.addMenu('&Network')
        quit = QAction('Quit', self)
        quit.triggered.connect(self.close)
        manageMenu.addAction(quit)

        """
        Building the Plugin Menu
        """
        pluginMenu = mainMenu.addMenu('&Plugins')
        settings = QAction('&Settings', self)
        pluginMenu.addAction(settings)

        """
        Build the Help Menu
        """
        helpMenu = mainMenu.addMenu('&Help')
        help = QAction('&Help', self)
        helpMenu.addAction(help)

        self.mlRegisterAllPlugins(pluginloader)

    def mlAddPlugin(self, plugin):
        if plugin is not None:
            """
            Populate the new trainer menu
            """

            action = QAction('Create new ' + plugin.mlGetPluginName() + ' trainer', self)
            loadUI = plugin.mlGetTrainerLoaderUI()
            validate = loadUI.mlGetValidateButton()
            validate.clicked.connect(lambda:self.onLoadTrainerValidateClicked(plugin))
            action.triggered.connect(loadUI.show)
            self._newTrainerMenu.addAction(action)

    def onLoadTrainerValidateClicked(self, plugin):
        if plugin is not None:
            loadUI = plugin.mlGetTrainerLoaderUI()
            network_filepath = loadUI.mlGetNetworkFilePath()
            data_filepath = loadUI.mlGetDataFilePath()
            trainer_filepath = loadUI.mlGetTrainerFilePath()

            if  os.path.exists(network_filepath) and \
                os.path.isfile(network_filepath) and \
                os.path.exists(data_filepath)    and \
                os.path.isfile(data_filepath)    and \
                os.path.exists(trainer_filepath) and \
                os.path.isfile(trainer_filepath):
                    trainer = plugin.mlGetTrainer(network_filepath, data_filepath, 'Network')
                    if trainer is not None:
                        trainer.mlConfigureTrainer(trainer_filepath)
                        self._trainermanager.mlAddTrainer(trainer)
                        self._trainermanager.mlStartTrainerWithId(trainer.mlGetUniqId())

    def mlRegisterAllPlugins(self, loader):
        plugins = loader.mlGetAllPlugins()
        if plugins is not None:
            for name in plugins.keys():
                self.mlAddPlugin(plugins[name])
