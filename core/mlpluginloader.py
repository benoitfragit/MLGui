#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import importlib

class MLPluginLoader:
    def __init__(self):
        self._modules = {}

        plugin_directories = os.getenv('MLGUI_PLUGIN_DIRS')
        for directory in plugin_directories.split(':'):
            if os.path.exists(directory) and os.path.isdir(directory):
                module_dirs = glob.glob(directory + os.path.sep + '*' + os.path.sep)
                dir         = os.path.basename(directory)
                base        = os.path.dirname(directory)

                for module_dir in module_dirs:
                    dirname = os.path.dirname(module_dir).split('/')[-1]
                    dir = dir + '.' + dirname

                    module  = importlib.import_module(dir, package=base)

                    if dirname not in self._modules.keys():
                        self._modules[dirname] = module

    def getPluginByName(self, name):
        ret = None
        if name in self._modules.keys():
            ret = self._modules[name].Plugin()
        return ret

    def getAllModules(self):
        return self._modules

if __name__ == '__main__':
    d = MLPluginLoader()
