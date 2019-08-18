#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QLabel

from PyQt5.QtCore    import Qt

from mltrainerviewerui      import MLTrainerViewerUI
from mltrainerloaderbaseui  import MLTrainerLoaderBaseUI
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
        settings = QAction('&Settings', self)
        pluginMenu.addAction(settings)

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
            Populate the new trainer menu
            """

            loadUI = plugin.mlGetTrainerLoaderUI()

            if isinstance(loadUI, MLTrainerLoaderBaseUI):
                self.addDockWidget(Qt.LeftDockWidgetArea, loadUI)

                action = loadUI.toggleViewAction()
                action.triggered.connect(loadUI.show)
                self._newTrainerMenu.addAction(action)

                loadUI.mlValidateTrainerSignal.connect(lambda:self.onLoadTrainerValidateClicked(plugin))
                loadUI.mlValidateTrainerSignal.connect(self._trainerviewer.mlOnNewTrainerAdded)


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
                    trainer = plugin.mlGetTrainer(network_filepath, data_filepath, trainer_name)
                    if trainer is not None:
                        trainer.mlConfigureTrainer(trainer_filepath)
                        self._trainermanager.mlAddTrainer(trainer)

    def mlRegisterAllPlugins(self, loader):
        plugins = loader.mlGetAllPlugins()
        if plugins is not None:
            for name in plugins.keys():
                self.mlAddPlugin(plugins[name])
