#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLNetworkDrawerBaseIface:
    @abstractmethod
    def mlAddSignalRepresentation(self, ncols, j, M, title=''):
        raise NotImplementedError

    @abstractmethod
    def mlOnUpdateSignalRepresentation(self, j, s):
        raise NotImplementedError
