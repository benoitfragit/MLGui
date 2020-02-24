#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from core.mlprocess import MLProcess
from core.mlnetworkprovider import MLNetworkProvider

class MLTrainer(MLProcess, MLNetworkProvider):
    def __init__(self, username, manager, plugin, network_filepath, data_filepath, trainer_filepath):
        MLProcess.__init__(self, manager)
        # Get the structure of this network without keeping the reference because it will leave in an other process
        network = plugin.mlGetNetwork(network_filepath)
        MLNetworkProvider.__init__(self, plugin, manager, network ,username, True)
        plugin.mlDeleteNetwork(network)

        # Adding some queues to send files into the MainLoop
        self._configure_queue = manager.Queue()
        self._restore_queue = manager.Queue()
        self._save_queue = manager.Queue()

        # Initialize everything for the main Loop
        self._shared['running']          = False
        self._shared['finished']         = False
        self._shared['exit']             = False
        self._shared['progress']         = 0.0;
        self._shared['error']            = 1.0;
        self._shared['network_filepath'] = network_filepath
        self._shared['data_filepath']    = data_filepath
        self._shared['trainer_filepath'] = trainer_filepath

        # Launching the process
        self.start()

    def mlGetPluginName(self):
        return self._plugin.mlGetPluginName()

    def mlIsPluginActivated(self):
        return self._plugin.mlIsPluginActivated()

    def mlConfigureTrainer(self, path):
        self._configure_queue.put(path)

    def mlIsTrainerRunning(self):
        return self._shared['running']

    def mlIsTrainerExited(self):
        return self._shared['exit']

    def mlGetTrainerProgress(self):
        return self._shared['progress']

    def mlTrainerRun(self):
        if not self._shared['exit']:
            self._shared['running'] = True

    def mlGetTrainerError(self):
        return self._shared['error']

    def mlSetTrainerExited(self, exited):
        self._shared['exit'] = exited

    def mlKillProcess(self):
        self._configure_queue.close()
        self._configure_queue.join_thread()
        self._restore_queue.close()
        self._restore_queue.join_thread()
        self._save_queue.close()
        self._save_queue.join_thread()

        MLProcess.mlKillProcess(self)

    def run(self):
        # Load the given plugin in order to load correctly the trainer

        # Initialize the trainer with the associated plugin
        network_filepath = self._shared['network_filepath']
        data_filepath = self._shared['data_filepath']
        trainer_filepath = self._shared['trainer_filepath']

        trainer = self._plugin.mlGetLoadedTrainer(network_filepath, data_filepath, trainer_filepath)

        # effectively start th process lifecycle
        while (not self._shared['exit']):
            # Get configure file from configure queue
            trainer_filepath = self._configure_queue.get()
            if trainer_filepath is not None:
                self._shared['trainer_filepath'] = trainer_filepath
                self._plugin.mlConfigureTrainer(trainer, trainer_filepath)

            # Get restore file from restore queue
            restore_filepath = self._restore_queue.get()
            if restore_filepath is not None:
                self._plugin.mlRestoreTrainerProgression(trainer, restore_filepath, self._shared['progress'], self._shared['error'])

            save_filepath = self._save_queue.get()
            if save_filepath is not None:
                self._plugin.mlSaveTrainerProgression(trainer, save_filepath)

            # Start the training process if needed
            if self._shared['running'] and not self._shared['finished']: 
                while (self._shared['running']):
                    if self._shared['exit'] or self._shared['finished']:
                        # Stop everything if we stop this process
                        self._shared['running'] = False
                    else:
                        self._lock.acquire()
                        self._plugin.mlTrainerRun(self._internal)

                        self._shared['finished']  = self._plugin.mlIsTrainerRunning(trainer)
                        self._shared['progress']  = self._plugin.mlGetTrainerProgress(trainer)
                        self._shared['error']     = self._plugin.mlGetTrainerError(trainer)

                        self.mlUpdateTrainerProvider()

                        self._lock.release()
        
        # try to save the trainer if needed before leaving
        save_filepath = self._save_queue.get()
        if save_filepath is not None:
            self._plugin.mlSaveTrainerProgression(trainer, save_filepath)

        self._plugin.mlDeleteTrainer(traier)

    def mlSaveTrainerProgression(self, directory):
        path = os.path.join(directory, self._username)
        self._save_queue.put(path)

    def mlRestoreTrainerProgression(self, directory, progress, error):
        path = os.path.join(directory, self._username)
        self._restore_queue.put(path)
        self._shared['progress'] = progress
        self._shared['error']    = error

    def mlJSONEncoding(self, d):
        username    = self._username
        running     = self.mlIsTrainerRunning() > 0
        exited      = self.mlIsTrainerExited() > 0
        error       = self.mlGetTrainerError()
        progress    = self.mlGetTrainerProgress()

        d[username] = {}

        d[username]['network_filepath']  = self._shared['network_filepath']
        d[username]['data_filepath']     = self._shared['data_filepath']
        d[username]['trainer_filepath'] = self._shared['trainer_filepath']
        d[username]['running']  = running
        d[username]['exit']     = exited
        d[username]['error']    = error
        d[username]['progress'] = progress

    def mlGetSettingsFilePath(self):
        return self._shared['trainer_filepath']

    def mlUpdateTrainerProvider(self):
        for i in self.arrays.keys():
            signal = None
            sizeOfSignal = len(self._arrays[i])
            if i == 0:
                signal = self._plugin.mlGetTrainerInputSignal(self._internal, sizeOfSignal)
            else:
                signal = self._plugin.mlGetTrainerLayerOutputSignal(self._internal, i - 1, sizeOfSignal)
            if signal is not None:
                self._arrays[i] = signal[:]
                print (i, self._arrays[i])

