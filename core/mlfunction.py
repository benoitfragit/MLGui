#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class MLFunction:
    def __init__(self, loader, name, restype, argstype, livewrapping = False):
        self._name = name
        self._restype = restype
        self._argstype = argstype
        self._func = None
        self._loaded = None

        if not livewrapping:
            self.load(loader)

        if self._func is not None:
            print >> sys.stderr, 'Method:' + self._name + ' has been loaded'
        else:
            print >> sys.stderr, 'Method:' + self._name + ' hasn t been loaded'

    @property
    def restype(self):
        return self._restype

    @property
    def argstype(self):
        return self._argstype

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
                print >> sys.stderr, 'Method ' + self._name + ': Invalid number of argument'
        else:
            print >> sys.stderr, 'Method:' + self._name + ' hasn t been loaded'

        return ret
