#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets    import QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui        import QIcon

class MLPTrainerLoaderUI(QWidget):
    def __init__(self, plugin):
        QWidget.__init__(self)

        self._plugin = plugin

        self._network_filepath = None
        self._trainer_filepath = None
        self._data_filepath    = None

        self.resize(350, 200)
        self.setWindowTitle(plugin.mlGetPluginName() + ' trainer builder')

        label0 = QLabel('Choose the trainer name')
        label1 = QLabel('Open a network settings file')
        label2 = QLabel('Open a trainer settings file')
        label3 = QLabel('Open a data file')

        self._entry = QLineEdit()
        button1 = QPushButton('Find')
        button1.setIcon(QIcon.fromTheme('system-search'))
        button2 = QPushButton('Find')
        button2.setIcon(QIcon.fromTheme('system-search'))
        button3 = QPushButton('Find')
        button3.setIcon(QIcon.fromTheme('system-search'))
        cancel  = QPushButton('Cancel')
        cancel.setIcon(QIcon.fromTheme('edit-undo'))
        validate= QPushButton('Apply')
        validate.setIcon(QIcon.fromTheme('system-run'))

        button1.clicked.connect(self.mlOpenNetworkFile)
        button2.clicked.connect(self.mlOpenTrainerFile)
        button3.clicked.connect(self.mlOpenDataFile)
        cancel.clicked.connect(self.mlCancel)
        validate.clicked.connect(self.mlValidate)

        hbox0   = QHBoxLayout()
        hbox1   = QHBoxLayout()
        hbox2   = QHBoxLayout()
        hbox3   = QHBoxLayout()
        hbox4   = QHBoxLayout()
        vbox    = QVBoxLayout()

        hbox0.addWidget(label0)
        hbox0.addStretch(1)
        hbox0.addWidget(self._entry)
        hbox1.addWidget(label1)
        hbox1.addStretch(1)
        hbox1.addWidget(button1)
        hbox2.addWidget(label2)
        hbox2.addStretch(1)
        hbox2.addWidget(button2)
        hbox3.addWidget(label3)
        hbox3.addStretch(1)
        hbox3.addWidget(button3)
        hbox4.addStretch(1)
        hbox4.addWidget(cancel)
        hbox4.addWidget(validate)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

    def mlOpenNetworkFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self._network_filepath, _ = QFileDialog.getOpenFileName(self, "Select a network file", "", "All files (*);;Xml files (*.xml)", options=options)

    def mlOpenTrainerFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self._trainer_filepath, _ = QFileDialog.getOpenFileName(self, "Select a network file", "", "All files (*);;Xml files (*.xml)", options=options)

    def mlOpenDataFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self._data_filepath, _ = QFileDialog.getOpenFileName(self, "Select a network file", "", "All files (*);;Xml files (*.xml)", options=options)

    def mlCancel(self):
        self._entry.setText('')
        self.close()

    def mlValidate(self):
        if self._entry != '' and \
            self._network_filepath is not None and \
            self._trainer_filepath is not None and \
            self._data_filepath is not None:
            trainer = self._plugin.mlGetTrainer(self._network_filepath, \
                                                self._data_filepath,\
                                                self._entry.text())
            if trainer is not None:
                trainer.mlConfigureTrainer(self._trainer_filepath)

        self.close()
