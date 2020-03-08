#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from core.mlprocess import MLProcess
from core.mlnetworkprovider import MLNetworkProvider
from core.mlpluginloader import MLPluginLoader

import multiprocessing
import threading
import logging


class MLTrainer(MLProcess, MLNetworkProvider):
    """

    """
    def __init__(self, username, manager, plugin, network_filepath, data_filepath, trainer_filepath):
        MLProcess.__init__(self, manager)
        # Get the structure of this network without keeping the reference because it will leave in an other process
        network = plugin.mlGetNetwork(network_filepath)
        MLNetworkProvider.__init__(self, plugin, manager, network, username, True)
        plugin.mlDeleteNetwork(network)

        # Adding some queues to send files into the MainLoop
        self._configure_queue = manager.Queue()
        self._restore_queue = manager.Queue()
        self._save_queue = manager.Queue()

        # Initialize everything for the main Loop
        self._shared['running'] = False
        self._shared['finished'] = False
        self._shared['exit'] = False
        self._shared['paused'] = False

        self._shared['progress'] = 0.0
        self._shared['error'] = 1.0
        self._shared['network_filepath'] = network_filepath
        self._shared['data_filepath'] = data_filepath
        self._shared['trainer_filepath'] = trainer_filepath
        self._shared['package'] = plugin.package
        self._shared['module'] = plugin.module
        self._shared['plugin_name'] = plugin.mlGetPluginName()
        self._shared['plugin_id'] = plugin.mlGetUniqId()

        # Launching the process
        self.start()

    def mlGetPluginId(self):
        """

        @return:
        """
        return self._shared['plugin_id']

    def mlGetPluginName(self):
        """

        @return:
        """
        return self._shared['plugin_name']

    def mlConfigureTrainer(self, path):
        """

        @param path:
        """
        self._configure_queue.put(path)

    def mlIsTrainerRunning(self):
        """

        @return:
        """
        return self._shared['running']

    def mlIsTrainerExited(self):
        """

        @return:
        """
        return self._shared['exit']

    def mlGetTrainerProgress(self):
        """

        @return:
        """
        return self._shared['progress']

    def mlTrainerRun(self):
        """

        """
        if not self._shared['exit']:
            self._shared['running'] = True

    def mlGetTrainerError(self):
        """

        @return:
        """
        return self._shared['error']

    def mlSetTrainerExited(self, exited):
        """

        @param exited:
        """
        self._shared['exit'] = exited

    def run(self):
        """

        """
        # Load the given plugin in order to load correctly the trainer
        plugin = MLPluginLoader.mlLoadPlugin(self._shared['module'], self._shared['package'])

        if plugin is not None:
            # Initialize the trainer with the associated plugin
            network_filepath = self._shared['network_filepath']
            data_filepath = self._shared['data_filepath']
            trainer_filepath = self._shared['trainer_filepath']

            trainer = plugin.mlGetLoadedTrainer(network_filepath, data_filepath, trainer_filepath)
            
            # Store pointer to the input and output signals
            pointers = {}
            for i in self._arrays.keys():
                sizeOfSignal = len(self._arrays[i])
                if i == 0:
                    pointers[i] = plugin.mlGetTrainerInputSignal(trainer, sizeOfSignal)
                else:
                    pointers[i] = plugin.mlGetTrainerLayerOutputSignal(trainer, i - 1, sizeOfSignal)

            # effectively start th process lifecycle
            while not self._shared['exit']:
                # Get configure file from configure queue
                if not self._configure_queue.empty():
                    trainer_filepath = self._configure_queue.get(block=False)
                    if trainer_filepath is not None:
                        self._shared['trainer_filepath'] = trainer_filepath
                        plugin.mlConfigureTrainer(trainer, trainer_filepath)

                # Get restore file from restore queue
                if not self._restore_queue.empty():
                    restore_filepath = self._restore_queue.get(block=False)
                    if restore_filepath is not None:
                        plugin.mlRestoreTrainerProgression(trainer, restore_filepath, self._shared['progress'],
                                                           self._shared['error'])

                if not self._save_queue.empty():
                    save_filepath = self._save_queue.get(block=False)
                    if save_filepath is not None:
                        plugin.mlSaveTrainerProgression(trainer, save_filepath)

                # Start the training process if needed
                if self._shared['running'] and not self._shared['finished']:
                    
                    # Starting the input and output drawing update
                    thread = threading.Thread(target=self.mlUpdateTrainerProvider, args=(pointers,))
                    thread.start()

                    # Starting the main loop
                    while self._shared['running']:
                        if self._shared['exit'] or self._shared['finished'] or self._shared['paused']:
                            # Stop everything if we stop this process
                            self._shared['running'] = False
                        else:
                            self._lock.acquire()
                            plugin.mlTrainerRun(trainer)

                            self._shared['finished'] = not plugin.mlIsTrainerRunning(trainer)
                            self._shared['progress'] = plugin.mlGetTrainerProgress(trainer)
                            self._shared['error'] = plugin.mlGetTrainerError(trainer)

                            self._lock.release()

            # try to save the trainer if needed before leaving
            if not self._save_queue.empty():
                save_filepath = self._save_queue.get()
                if save_filepath is not None:
                    plugin.mlSaveTrainerProgression(trainer, save_filepath)

            # Wait for thread stopping
            if thread.is_alive:
                thread.join()

            # Delete the trainer memory
            plugin.mlDeleteTrainer(trainer)

    def mlSaveTrainerProgression(self, directory):
        """

        @param directory:
        """
        path = os.path.join(directory, self._username)
        self._save_queue.put(path)

    def mlRestoreTrainerProgression(self, directory, progress, error, exit, running, finished):
        """

        @param directory:
        @param progress:
        @param error:
        """
        path = os.path.join(directory, self._username)
        self._shared['progress'] = progress
        self._shared['error'] = error
        self._shared['exit'] = exit
        self._shared['running'] = running
        self._shared['finished'] = finished
        self._restore_queue.put(path)

    def mlJSONEncoding(self, d):
        """

        @param d:
        """
        username = self._username
        running = self.mlIsTrainerRunning() > 0
        exited = self.mlIsTrainerExited() > 0
        error = self.mlGetTrainerError()
        progress = self.mlGetTrainerProgress()

        d[username] = {}

        d[username]['network_filepath'] = self._shared['network_filepath']
        d[username]['data_filepath'] = self._shared['data_filepath']
        d[username]['trainer_filepath'] = self._shared['trainer_filepath']
        d[username]['running'] = running
        d[username]['finished'] = self._shared['finished']
        d[username]['exit'] = exited
        d[username]['error'] = error
        d[username]['progress'] = progress

    def mlGetSettingsFilePath(self):
        """

        @return:
        """
        return self._shared['trainer_filepath']

    def mlUpdateTrainerProvider(self, pointers):
        """

        @param pointers:
        """
        while self._shared['running'] and not self._shared['exit'] and not self._shared['finished']:
            for i in self._arrays.keys():
                self._arrays[i] = (pointers[i].contents)[:]
                