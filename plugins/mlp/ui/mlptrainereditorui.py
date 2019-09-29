#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui import MLTrainerEditorBaseUI

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui     import QIcon


class MLPTrainerEditorUI(MLTrainerEditorBaseUI):
    def __init__(self, plugin, parent = None):
        self._costfunction  = QComboBox()
        self._costfunction.addItems(["CrossEntropy", "Quadratic"])

        self._error         = QDoubleSpinBox()
        self._error.setRange(0.0, 100.0)

        self._iterations    = QSpinBox()
        self._iterations.setRange(0, 1000000)

        self._minibatch     = QSpinBox()
        self._minibatch.setRange(1, 1000)

        self._learning      = QDoubleSpinBox()
        self._learning.setRange(0.0, 5.0)

        self._momemtum      = QDoubleSpinBox()
        self._momemtum.setRange(0.0, 5.0)

        self._cancel  = QPushButton('Cancel')
        self._cancel.setIcon(QIcon.fromTheme('edit-undo'))
        self._cancel.setFlat(True)

        self._validate= QPushButton('Apply')
        self._validate.setIcon(QIcon.fromTheme('system-run'))
        self._validate.setFlat(True)

        MLTrainerEditorBaseUI.__init__(self, plugin, parent)

    def mlBuildTrainerEditorMainWidget(self):
        label1       = QLabel('Cost-Function')
        label2       = QLabel('Error')
        label3       = QLabel('Max-iterations')
        label4       = QLabel('Mini-Batch-Size')
        label5       = QLabel('Learning-Rate')
        label6       = QLabel('Momemtum')

        hbox1        = QHBoxLayout()
        hbox2        = QHBoxLayout()
        hbox3        = QHBoxLayout()
        hbox4        = QHBoxLayout()
        hbox5        = QHBoxLayout()
        hbox6        = QHBoxLayout()
        hbox7        = QHBoxLayout()

        hbox1.addWidget(label1)
        hbox1.addStretch(1)
        hbox1.addWidget(self._costfunction)

        hbox2.addWidget(label2)
        hbox2.addStretch(1)
        hbox2.addWidget(self._error)

        hbox3.addWidget(label3)
        hbox3.addStretch(1)
        hbox3.addWidget(self._iterations)

        hbox4.addWidget(label4)
        hbox4.addStretch(1)
        hbox4.addWidget(self._minibatch)

        hbox5.addWidget(label5)
        hbox5.addStretch(1)
        hbox5.addWidget(self._learning)

        hbox6.addWidget(label6)
        hbox6.addStretch(1)
        hbox6.addWidget(self._momemtum)

        hbox7.addStretch(1)
        hbox7.addWidget(self._cancel)
        hbox7.addWidget(self._validate)

        vbox = QVBoxLayout()

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addStretch(1)
        vbox.addLayout(hbox7)

        self._mainWidget.setLayout(vbox)

    def fromTrainer(self, *args, **kwargs):
        trainer = args[0]

        if trainer is not None:
            self.setVisible(True)
