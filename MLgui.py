#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5    import QtWidgets
from optparse import OptionParser
from core     import MLPluginLoader
from core     import MLProcessManager
from ui       import MLWindow
import os
import sys
import signal

def main():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    window = MLWindow()


    parser = OptionParser()
    parser.add_option('-n','--network',
                      action='store',
                      dest='net',
                      default='',
                      help='Give a valid network filename')
    parser.add_option('-d', '--data',
                      action='store',
                      dest='data',
                      default='',
                      help='Give a valid data fileneme')
    parser.add_option('-s', '--settings',
                      action='store',
                      dest='settings',
                      default='',
                      help='Give a valid settings fileneme')
    (options, args) = parser.parse_args()

    if  os.path.exists(options.net)     and \
        os.path.exists(options.data)    and \
        os.path.exists(options.settings):

        loader  = MLPluginLoader()

        manager = MLProcessManager()
        app.aboutToQuit.connect(manager.mlKillAll)

        plugin  = loader.getPluginByName('mlp')

        trainer = None
        if plugin is not None:
            print >>sys.stdout, "name:%(name)s\n \
                                 author:%(author)s\n \
                                 version:%(version)s\n \
                                 description:%(description)s" \
                                 % {'name'  :plugin.mlGetPluginName(),    \
                                    'author':plugin.mlGetPluginAuthor(),  \
                                    'version':plugin.mlGetPluginVersion(), \
                                    'description':plugin.mlGetPluginDescription()}
            trainer = plugin.mlGetTrainer(options.net, options.data, 'Network')

        if trainer is not None:
            trainer.mlConfigureTrainer(options.settings)

            try:
                manager.mlNewProcess(trainer)
            finally:
                pass

            trainer.mlDeleteTrainer()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
