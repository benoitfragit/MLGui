#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLTrainerLoaderBaseIface:
    @abstractmethod
    def mlBuildTrainerLoaderMainWidget(self):
        raise NotImplementedError
