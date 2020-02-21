#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import importlib
import sys

from core.mlpluginbase import MLPluginBase

class MLPluginLoader:
    def __init__(self):
        self._plugins = {}

        plugin_directories = os.getenv('MLGUI_PLUGIN_DIRS')
        for directory in plugin_directories.split(';'):
            if os.path.exists(directory) and os.path.isdir(directory):
                module_dirs = glob.glob(directory + os.path.sep + '*' + os.path.sep)
                dir         = os.path.basename(directory)
                base        = os.path.dirname(directory)

                for module_dir in module_dirs:
                    dirname = os.path.dirname(module_dir).split(os.path.sep)[-1]
                    dir = dir + '.' + dirname

                    print(dir, base)
                    module  = importlib.import_module(dir, package=base)
                    print(module)

                    if dirname not in self._plugins.keys():
                        try:
                            plugin = module.MLPlugin()
                            if isinstance(plugin, MLPluginBase):
                                self._plugins[dirname] = plugin
                            else:
                                sys.stderr.write( 'MLPlugin class is not  a valid MLPluginBase class')
                        except:
                            continue

    def mlGetPluginByName(self, name):
        ret = None
        if name in self._plugins.keys():
            ret = self._plugins[name]
        else:
            sys.stderr.write( "No plugin with name: "+ name)
        return ret

    def mlGetAllPlugins(self):
        return self._plugins

if __name__ == '__main__':
    d = MLPluginLoader()
