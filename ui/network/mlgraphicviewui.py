#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsView

from PyQt5.QtCore    import Qt

class MLGraphicsViewUI(QGraphicsView):
    def __init__(self, parent = None):
        QGraphicsView.__init__(self, parent)

    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self, event)
        scene = self.scene()
        if scene is not None:
            self.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
