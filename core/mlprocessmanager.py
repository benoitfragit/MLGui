#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Queue
from multiprocessing import Manager
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import Event

import sys

def mlRun(p, lock, shared, pause, resume, quit):
    lock.acquire()
    if p is not None:
        if 'running' not in shared.keys():
            shared['running']   = True
            shared['progress']  = p.mlGetTrainerProgress()
            shared['error']     = p.mlGetTrainerError()
            shared['pause']     = False
            shared['stopped']   = False

        while (shared['running']):
            if pause.set():
                shared['pause'] = True
            elif resume.set():
                shared['pause'] = False

            if quit.set():
                shared['stopped'] = True
                shared['running'] = False
            elif shared['pause'] is not True:
                p.mlTrainerRun()
                shared['running']   = p.mlIsTrainerRunning()
                shared['progress']  = p.mlGetTrainerProgress()
                shared['error']     = p.mlGetTrainerError()

        print >>sys.stdout, 'Progress:%(prog)f, Error:%(err)f' % {'prog':shared['progress'], 'err':shared['error']}

    lock.release()

class MLProcessManager:
    def __init__(self):
        self._processes = {}
        self._manager   = Manager()
        self._shared    = {}
        self._lock      = {}
        self._pause     = {}
        self._resume    = {}
        self._quit      = {}

    def mlKillWithId(self, uuid):
        if uuid in self._processes.keys():
            self._quit[uuid].set()
            self._processes[uuid].terminate()
            self._processes[uuid].join()

    def mlKillAll(self):
        for uuid in self._processes.keys():
            self.mlKillWithId(uuid)

    def mlPauseProcess(self, uuid):
        if uuid in self._processes.keys():
            self._lock[uuid].acquire()
            self._pause[uuid].set()
            self._lock[uuid].release()

    def mlResumeProcess(self, uuid):
        if uuid in self._processes.keys():
            self._lock[uuid].acquire()
            self._resume[uuid].set()
            self._lock[uuid].release()

    def mlNewProcess(self, p):
        uuid = p.mlGetUniqId()
        if uuid not in self._processes.keys():
            self._lock[uuid]        = Lock()
            self._shared[uuid]      = self._manager.dict()
            self._pause[uuid]       = Event()
            self._resume[uuid]      = Event()
            self._quit[uuid]        = Event()

            self._processes[uuid]   = Process(target=mlRun, args=(p, self._lock[uuid], \
                                                                     self._shared[uuid],\
                                                                     self._pause[uuid],\
                                                                     self._resume[uuid],\
                                                                     self._quit[uuid]))

            self._processes[uuid].start()
