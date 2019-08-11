#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

import sys
import os

sys.path.append('..' + os.path.sep +  '..')

from core  import MLPluginBase
from core  import MLTrainer
from core  import MLNetwork

from exchange import MLPTrainer
from exchange import MLPNetwork
from exchange import MLPMetaData

from ui import MLPTrainerLoaderUI

def enum(*args):
    values = dict(zip(args, range(len(args))))
    return type('Enum', (), values)

class MLLoader:
    def __init__(self, lib):
        self._libc = ctypes.CDLL(lib)

    def wrap(self, funcname, restype, argtypes):
        func = self._libc.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func

    def load(self):
        raise NotImplementedError

class Plugin(MLLoader, MLPluginBase):
    def __init__(self, args):
        """
        If libMLP is installed in a non common path, please
        add it to the LD_LIBRARY_PATH before using
        """
        MLPluginBase.__init__(self, args)
        MLLoader.__init__(self, 'libMLP.so')

        self._funcnames = enum(   'INIT',
                                  'METADATA',
                                  'TRAINER_NEW',
                                  'TRAINER_DELETE',
                                  'TRAINER_CONFIGURE',
                                  'TRAINER_IS_RUNNING',
                                  'TRAINER_GET_PROGRESS',
                                  'TRAINER_RUN',
                                  'TRAINER_ERROR',
                                  'NETWORK_NEW',
                                  'NETWORK_DELETE',
                                  'NETWORK_SERIALIZE',
                                  'NETWORK_DESERIALIZE',
                                  'NETWORK_PREDICT',
                                  'NETWORK_GET_OUTPUT',
                                  'NETWORK_GET_OUTPUT_LENGTH')

        self._number_of_functions = (self._funcnames.NETWORK_GET_OUTPUT_LENGTH - self._funcnames.INIT + 1)

        self._api = [   ['mlp_plugin_init',                 None,                           []],
                        ['mlp_plugin_metadata',             ctypes.POINTER(MLPMetaData),    []],
                        ['mlp_trainer_new',                 ctypes.POINTER(MLPTrainer),     [ctypes.c_char_p, ctypes.c_char_p]],
                        ['mlp_trainer_delete',              None,                           [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_configure',           None,                           [ctypes.POINTER(MLPTrainer), ctypes.c_char_p]],
                        ['mlp_trainer_is_running',          ctypes.c_ubyte,                 [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_get_progress',        ctypes.c_float,                 [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_run',                 None,                           [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_error',               ctypes.c_float,                 [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_network_new',                 ctypes.POINTER(MLPNetwork),     [ctypes.c_char_p]],
                        ['mlp_network_delete',              None,                           [ctypes.POINTER(MLPNetwork)]],
                        ['mlp_network_serialize',           None,                           [ctypes.POINTER(MLPNetwork), ctypes.c_char_p]],
                        ['mlp_network_deserialize',         None,                           [ctypes.POINTER(MLPNetwork), ctypes.c_char_p]],
                        ['mlp_network_predict',             None,                           [ctypes.POINTER(MLPNetwork), ctypes.c_uint, ctypes.c_void_p]],
                        ['mlp_network_get_output',          ctypes.c_void_p,                [ctypes.POINTER(MLPNetwork)]],
                        ['mlp_network_get_output_length',   ctypes.c_uint,                  [ctypes.POINTER(MLPNetwork)]]]

        self._funcs = {}

        self.load()

    def load(self):
        for i in range(self._number_of_functions):
            self._funcs[i] = self.wrap(self._api[i][0],
                                        self._api[i][1],
                                        self._api[i][2])
            if self._funcs[i] is not None:
                print >> sys.stdout, 'Method:' + self._api[i][0] + ' has been loaded'
            else:
                print >> sys.stderr, 'Method:' + self._api[i][0] + ' hasn t been loaded'

        # Call plugin init method
        if self._funcs[self._funcnames.INIT] is not None:
           self._funcs[self._funcnames.INIT]()
           self._activated = True

        # Get all metadata
        if  self._funcs[self._funcnames.METADATA] is not None:
            metadata = self._funcs[self._funcnames.METADATA]().contents
            self._name      = metadata.name
            self._version   = metadata.version
            self._author    = metadata.author
            self._description = metadata.description

        self._trainerloaderui = MLPTrainerLoaderUI(self)

    def mlGetTrainer(self, net, data, username):
        internal = self._funcs[self._funcnames.TRAINER_NEW](net, data)
        trainer = MLTrainer(self, internal, username)
        return trainer

    def mlDeleteTrainer(self, trainer):
        self._funcs[self._funcnames.TRAINER_DELETE](trainer)

    def mlConfigureTrainer(self, trainer, path):
        self._funcs[self._funcnames.TRAINER_CONFIGURE](trainer, path)

    def mlIsTrainerRunning(self, trainer):
        return self._funcs[self._funcnames.TRAINER_IS_RUNNING](trainer)

    def mlGetTrainerProgress(self, trainer):
        return self._funcs[self._funcnames.TRAINER_GET_PROGRESS](trainer)

    def mlTrainerRun(self, trainer):
        self._funcs[self._funcnames.TRAINER_RUN](trainer)

    def mlGetTrainerError(self, trainer):
        return self._funcs[self._funcnames.TRAINER_ERROR](trainer)

    def mlGetNetwork(self, path):
        internal = self._funcs[self._funcnames.NETWORK_NEW](path)
        network = MLNetwork(self, internal)
        return network

    def mlDeleteNetwork(self, net):
        self._funcs[self._funcnames.NETWORK_DELETE](net)

    def mlSaveNetwork(self, net, path):
        self._funcs[self._funcnames.NETWORK_SERIALIZE](net, path)

    def mlLoadNetwork(self, net, path):
        self._funcs[self._funcnames.NETWORK_DESERIALIZE](net, path)

    def mlPredict(self, net, num, sig):
        self._funcs[self._funcnames.NETWORK_PREDICT](net, num, sig)

    def mlGetNetworkOutputLength(self, net):
        return self._funcs[self._funcnames.NETWORK_GET_OUTPUT_LENGTH](net)

    def mlGetNetworkPrediction(self, net):
        return self._funcs[self._funcnames.NETWORK_GET_OUTPUT](net)

if __name__ == '__main__':
    l = Plugin()
