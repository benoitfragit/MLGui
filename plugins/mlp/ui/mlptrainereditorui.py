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
        MLTrainerEditorBaseUI.__init__(self, plugin, parent)

    def mlBuildTrainerEditorMainWidget(self):
        label1       = QLabel('Cost-Function')
        costfunction = QComboBox()
        hbox1        = QHBoxLayout()

        label2       = QLabel('Error')
        error        = QDoubleSpinBox()
        error.setRange(0.0, 100.0)
        hbox2        = QHBoxLayout()

        label3       = QLabel('Max-iterations')
        iterations   = QSpinBox()
        iterations.setRange(0, 1000000)
        hbox3        = QHBoxLayout()

        label4       = QLabel('Mini-Batch-Size')
        minibatch    = QSpinBox()
        minibatch.setRange(1, 1000)
        hbox4        = QHBoxLayout()

        label5       = QLabel('Learning-Rate')
        learning     = QDoubleSpinBox()
        learning.setRange(0.0, 5.0)
        hbox5        = QHBoxLayout()

        label6       = QLabel('Momemtum')
        momemtum     = QDoubleSpinBox()
        momemtum.setRange(0.0, 5.0)
        hbox6        = QHBoxLayout()

        cancel  = QPushButton('Cancel')
        cancel.setIcon(QIcon.fromTheme('edit-undo'))
        cancel.setFlat(True)
        validate= QPushButton('Apply')
        validate.setIcon(QIcon.fromTheme('system-run'))
        validate.setFlat(True)
        hbox7        = QHBoxLayout()

        hbox1.addWidget(label1)
        hbox1.addStretch(1)
        hbox1.addWidget(costfunction)

        hbox2.addWidget(label2)
        hbox2.addStretch(1)
        hbox2.addWidget(error)

        hbox3.addWidget(label3)
        hbox3.addStretch(1)
        hbox3.addWidget(iterations)

        hbox4.addWidget(label4)
        hbox4.addStretch(1)
        hbox4.addWidget(minibatch)

        hbox5.addWidget(label5)
        hbox5.addStretch(1)
        hbox5.addWidget(learning)

        hbox6.addWidget(label6)
        hbox6.addStretch(1)
        hbox6.addWidget(momemtum)

        hbox7.addStretch(1)
        hbox7.addWidget(cancel)
        hbox7.addWidget(validate)

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

    def mlResetUI(self):
        pass

    def fromTrainer(self, *args, **kwargs):
        pass
