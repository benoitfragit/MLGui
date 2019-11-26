#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class MLFunction:
    def __init__(self, loader, name, restype, argstype):
        self._name = name
        self._restype = restype
        self._argstype = argstype
        self._func = None
        self._loaded = None

        self.load(loader)

    @property
    def loaded(self):
        return self._loaded

    def load(self, loader):
        if loader is not None:
            print >> sys.stderr, 'Method:' + self._name + ' has been loaded'
            self._func = loader.wrap(self._name, self._restype, self._argstype)
        if self._func is None:
            print >> sys.stderr, 'Method:' + self._name + ' hasn t been loaded'

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
