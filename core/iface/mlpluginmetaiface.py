#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MLPluginMetaDataIFace:
    def mlGetPluginName(self):
        raise NotImplementedError

    def mlGetPluginAuthor(self):
        raise NotImplementedError

    def mlGetPluginVersion(self):
        raise NotImplementedError

    def mlGetPluginDescription(self):
        raise NotImplementedError
