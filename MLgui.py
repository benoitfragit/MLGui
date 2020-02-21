#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5    import QtWidgets

from core.mlpluginloader import MLPluginLoader
from core.mltrainermanager import MLTrainerManager

from ui.mlwindow   import MLWindow

import os
import sys
import signal

def main():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    manager = MLTrainerManager()
    loader  = MLPluginLoader()

    window = MLWindow(manager, loader)

    app.aboutToQuit.connect(window.mlLeave)

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
