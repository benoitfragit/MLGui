#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui     import QPixmap

from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import QSize
from PyQt5.QtCore    import pyqtSignal

from importlib import resources
from ui import data
import uuid
import os

class MLNetworkViewerItemUI(QWidget):
    removeNetwork = pyqtSignal(uuid.UUID)

    def __init__(self, network, parent = None):
        QWidget.__init__(self, parent)

        self._network = network
        self._scene   = self._network.mlGetScene()

        vbox = QVBoxLayout()

        label   = QLabel(network.username)
        label.setAlignment(Qt.AlignCenter)
        pixLabel    = QLabel()
        with resources.path(data, 'network.png') as p:
            pixmap = QPixmap(str(p))
            pixmap = pixmap.scaledToWidth(120)
            pixLabel.setAlignment(Qt.AlignCenter)
            pixLabel.setPixmap(pixmap)

        vbox.addWidget(label)
        vbox.addWidget(pixLabel)

        self.setLayout(vbox)

        self._item = QListWidgetItem()
        self._item.setSizeHint(self.sizeHint())

    def mlGetUserName(self):
        return self._network.username

    def mlGetItem(self):
        return self._item

    def contextMenuEvent(self, event):
        if not self._network.managed:
            menu = QMenu(self)

            connect     = QAction(QIcon.fromTheme('media-playback-start'), '&Connect', self)
            disconnect  = QAction(QIcon.fromTheme('media-playback-pause'), '&Disconnect', self)
            remove      = QAction(QIcon.fromTheme('user-trash'),'&Remove', self)
            configure   = QAction(QIcon.fromTheme('document-properties'), '&Configure', self)

            connect.triggered.connect(self.mlOnConnectNetworkClicked)
            disconnect.triggered.connect(self.mlOnDisconnectNetworkClicked)
            remove.triggered.connect(self.mlOnRemoveNetworkClicked)
            configure.triggered.connect(self.mlOnConfigureNetworkClicked)

            menu.addAction(connect)
            menu.addAction(disconnect)
            menu.addAction(remove)
            menu.addAction(configure)

            menu.exec_(self.mapToGlobal(event.pos()))

    def mlOnConnectNetworkClicked(self):
        pass

    def mlOnDisconnectNetworkClicked(self):
        pass

    def mlOnConfigureNetworkClicked(self):
        pass

    def mlOnRemoveNetworkClicked(self):
        self.removeNetwork.emit(self._network.mlGetUniqId())

    def mlJSONEncoding(self, d):
        pass

    def mlJSONDecoding(self, d):
        pass

    def mlGetUniqId(self):
        return self._network.mlGetUniqId()

    def mlOnUpdate(self):
        if  self._network is not None:
            self._network.mlUpdateNetworkDrawerUI(self._scene)

    def mlOnDisplayNetwork(self, viewer):
        if viewer is not None:
            # Initially create the scene
            self._network.mlDisplayNetworkDrawerUI(self._scene)
            viewer.setScene(self._scene)
            viewer.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
