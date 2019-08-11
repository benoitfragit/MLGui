#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Queue
from multiprocessing import Manager
from multiprocessing import Process
from multiprocessing import Lock

import sys

def mlRun(p, lock, queue, shared):
    lock.acquire()
    if p is not None:
        if 'running' not in shared.keys():
            shared['running']   = True
            shared['progress']  = p.mlGetTrainerProgress()
            shared['error']     = p.mlGetTrainerError()

        while (shared['running']):
            p.mlTrainerRun()
            shared['running'] = p.mlIsTrainerRunning()
            shared['progress']  = p.mlGetTrainerProgress()
            shared['error']     = p.mlGetTrainerError()

        print >>sys.stdout, 'Progress:%(prog)f, Error:%(err)f' % {'prog':shared['progress'], 'err':shared['error']}

    lock.release()

class MLProcessManager:
    def __init__(self):
        self._processes = {}
        self._manager   = Manager()
        self._shared    = {}
        self._queue     = {}
        self._lock      = {}

    def mlNewProcess(self, p):
        uuid = p.mlGetUniqId()
        if uuid not in self._processes.keys():
            self._queue[uuid]       = Queue()
            self._lock[uuid]        = Lock()
            self._shared[uuid]      = self._manager.dict()

            self._processes[uuid]   = Process(target=mlRun, args=(p, self._lock[uuid], self._queue[uuid], self._shared[uuid]))

            self._processes[uuid].start()
