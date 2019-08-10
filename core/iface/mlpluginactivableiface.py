#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLPluginActivableIFace:
    def mlActivatePlugin(self):
        raise NotImplementedError

    def mlDeactivatePlugin(self):
        raise NotImplementedError

    def mlIsPluginActivated(self):
        raise NotImplementedError
