#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod

class MLTrainerLoaderBaseIface:
    """
    Define all requested methods that a trainer loader should implement
    """
    @abstractmethod
    def mlBuildTrainerLoaderMainWidget(self):
        raise NotImplementedError
