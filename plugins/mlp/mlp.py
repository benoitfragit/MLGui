#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

import sys
import os

from core  import MLPluginBase
from core  import MLNetwork

from exchange import MLPTrainer
from exchange import MLPNetwork
from exchange import MLPMetaData

from ui import MLPTrainerLoaderUI
from ui import MLPTrainerEditorUI

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

class MLPlugin(MLLoader, MLPluginBase):
    def __init__(self):
        """
        If libMLP is installed in a non common path, please
        add it to the LD_LIBRARY_PATH before using
        """
        MLPluginBase.__init__(self)
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
                                  'TRAINER_SAVE_PROGRESSION',
                                  'TRAINER_RESTORE_PROGRESSION',
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
                        ['mlp_trainer_get_progress',        ctypes.c_double,                [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_run',                 None,                           [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_error',               ctypes.c_double,                [ctypes.POINTER(MLPTrainer)]],
                        ['mlp_trainer_save_progression',    None,                           [ctypes.POINTER(MLPTrainer), ctypes.c_char_p]],
                        ['mlp_trainer_restore_progression', None,                           [ctypes.POINTER(MLPTrainer), ctypes.c_char_p, ctypes.c_double, ctypes.c_double]],
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
        self._trainereditorui = MLPTrainerEditorUI(self)

    def mlGetTrainer(self, net, data):
        model = self._funcs[self._funcnames.TRAINER_NEW](net, data)
        return model

    def mlDeleteTrainer(self, trainer):
        if trainer is not None and 'model' in trainer.keys():
            self._funcs[self._funcnames.TRAINER_DELETE](trainer['model'])

    def mlConfigureTrainer(self, trainer, path):
        if trainer is not None :
            if 'model' in trainer.keys():
                self._funcs[self._funcnames.TRAINER_CONFIGURE](trainer['model'], path)
            if 'settings' in trainer.keys():
                trainer['settings'] = path

    def mlIsTrainerRunning(self, trainer):
        ret = False
        if trainer is not None and 'model' in trainer.keys():
            ret = self._funcs[self._funcnames.TRAINER_IS_RUNNING](trainer['model'])
        return ret

    def mlGetTrainerProgress(self, trainer):
        ret = 0.0
        if trainer is not None and 'model' in trainer.keys():
            ret = self._funcs[self._funcnames.TRAINER_GET_PROGRESS](trainer['model'])
        return ret

    def mlTrainerRun(self, trainer):
        if trainer is not None and 'model' in trainer.keys():
            self._funcs[self._funcnames.TRAINER_RUN](trainer['model'])

    def mlGetTrainerError(self, trainer):
        ret = 100.0
        if trainer is not None and 'model' in trainer.keys():
            ret = self._funcs[self._funcnames.TRAINER_ERROR](trainer['model'])
        return ret

    def mlSaveTrainerProgression(self, trainer, path):
        if trainer is not None and 'model' in trainer.keys():
            real_path = path + '.xml'
            self._funcs[self._funcnames.TRAINER_SAVE_PROGRESSION](trainer['model'], real_path)

    def mlRestoreTrainerProgression(self, trainer, path, progress, error):
        if trainer is not None and 'model' in trainer.keys():
            real_path =  path + '.xml'
            self._funcs[self._funcnames.TRAINER_RESTORE_PROGRESSION](trainer['model'], real_path, progress, error)

    def mlGetLoadedTrainer(self):
        ret = None

        if self._trainerloaderui is not None:

            network_filepath    = self._trainerloaderui.mlGetNetworkFilePath()
            data_filepath       = self._trainerloaderui.mlGetDataFilePath()
            trainer_filepath    = self._trainerloaderui.mlGetTrainerFilePath()

            ret = self.mlGetTrainerInternal(network_filepath, data_filepath, trainer_filepath)

        return ret

    def mlTrainerJSONEncoding(self, trainer, d):
        if 'network' in trainer.keys():
            d['network']  = trainer['network']
        if 'data' in trainer.keys():
            d['data']     = trainer['data']
        if 'settings' in trainer.keys():
            d['settings'] = trainer['settings']

    def mlTrainerJSONDecoding(self, buf):
        ret = None
        if buf is not None:
            if  'network'   in buf.keys() and \
                'settings'  in buf.keys() and \
                'data'      in buf.keys():

                network_filepath = buf['network']
                trainer_filepath = buf['settings']
                data_filepath    = buf['data']

                ret = self.mlGetTrainerInternal(network_filepath, data_filepath, trainer_filepath)

        return ret

    def mlGetTrainerInternal(self,\
                             network_filepath, \
                             data_filepath, \
                             trainer_filepath):
        internal = None

        if network_filepath is not None      and \
            os.path.exists(network_filepath) and \
            os.path.isfile(network_filepath) and \
            data_filepath is not None        and \
            os.path.exists(data_filepath)    and \
            os.path.isfile(data_filepath):

            internal = {}

            internal['model']    = self.mlGetTrainer(network_filepath, data_filepath)

            internal['network']  = network_filepath
            internal['data']     = data_filepath
            internal['settings'] = trainer_filepath

            if  trainer_filepath is not None and \
                os.path.exists(trainer_filepath) and \
                os.path.isfile(trainer_filepath):
                self.mlConfigureTrainer(internal, trainer_filepath)

        return internal

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
    l = MLPlugin()
