#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

class MLLoader:
    def __init__(self, lib):
        self._libc = ctypes.CDLL(lib)

    def wrap(self, funcname, restype, argtypes):
        func = self._libc.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func
