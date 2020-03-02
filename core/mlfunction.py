#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class MLFunction:
    def __init__(self, loader, name, restype, argstype, livewrapping=False):
        self._name = name
        self._restype = restype
        self._argstype = argstype
        self._func = None
        self._loaded = None

        if not livewrapping:
            self.load(loader)

        if self._func is not None:
            sys.stdout.write('Method:' + self._name + ' has been loaded')
        else:
            sys.stderr.write('Method:' + self._name + ' hasn t been loaded')

    def setResType(self, value):
        self._restype = value

    @property
    def restype(self):
        return self._restype

    @restype.setter
    def restype(self, value):
        self._restype = value

    @property
    def argstype(self):
        return self._argstype

    @argstype.setter
    def argstype(self, value):
        self._argstype = value

    @property
    def loaded(self):
        return self._loaded

    def load(self, loader):
        if loader is not None:
            self._func = loader.wrap(self._name, self._restype, self._argstype)

    def __call__(self, *args):
        ret = None

        if self._func is not None:
            if len(args) == len(self._argstype):
                if len(args) > 0:
                    ret = self._func(*args)
                else:
                    ret = self._func()
            else:
                sys.stderr.write('Method ' + self._name + ': Invalid number of argument')
        else:
            sys.stderr.write('Method:' + self._name + ' hasn t been loaded')

        return ret
