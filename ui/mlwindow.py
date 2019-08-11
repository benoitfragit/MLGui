#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

class MLWindow(QMainWindow):
    def __init__(self, *argv):
        """
        Building tha mainwindow
        """
        QMainWindow.__init__(self)

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
        newTrainerMenu = trainerMenu.addMenu('&New trainer')
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
