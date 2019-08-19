#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLPluginActivableIFace:
    def mlSetPluginActivated(self, activated):
        raise NotImplementedError

    def mlIsPluginActivated(self):
        raise NotImplementedError
