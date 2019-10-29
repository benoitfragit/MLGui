#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLNetworkDrawerBaseIface:
    @abstractmethod
    def mlAddSignalRepresentation   (self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def mlOnDisplayNetwork          (self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def mlUpdateSignalRepresentation(self, *args, **kwargs):
        raise NotImplementedError
