#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui import MLTrainerEditorBaseUI

class MLPTrainerEditorUI(MLTrainerEditorBaseUI):
    def __init__(self, plugin, parent = None):
        MLTrainerEditorBaseUI.__init__(self, plugin, parent)

    def mlBuildTrainerEditorMainWidget(self):
        pass

    def mlResetUI(self):
        pass

    def fromTrainer(self, *args, **kwargs):
        pass
