# Dummy audioop module for Python 3.13+
# This is a compatibility shim since audioop was removed from stdlib
# Voice features won't work but text-based bot will function fine

import sys

def mult(fragment, width, factor):
    """Stub implementation"""
    return fragment

def tomono(stereo, width, lfactor, rfactor):
    """Stub implementation"""
    return stereo

def tostereo(mono, width, lfactor, rfactor):
    """Stub implementation"""
    return mono

def findfit(fragment, reference):
    """Stub implementation"""
    return (0, 0)

def findfactor(fragment, reference):
    """Stub implementation"""
    return (0.0, 0.0)

def findmax(fragment, length):
    """Stub implementation"""
    return 0

def avgpp(fragment, length):
    """Stub implementation"""
    return 0

def maxpp(fragment, length):
    """Stub implementation"""
    return 0

def avg(fragment, width):
    """Stub implementation"""
    return 0

def rms(fragment, width):
    """Stub implementation"""
    return 0

def add(fragment1, fragment2, width):
    """Stub implementation"""
    return fragment1

def bias(fragment, width, bias):
    """Stub implementation"""
    return fragment

def reverse(fragment, width):
    """Stub implementation"""
    return fragment

def lin2alaw(fragment, width):
    """Stub implementation"""
    return fragment

def alaw2lin(fragment, width):
    """Stub implementation"""
    return fragment

def lin2ulaw(fragment, width):
    """Stub implementation"""
    return fragment

def ulaw2lin(fragment, width):
    """Stub implementation"""
    return fragment

def lin2adpcm(fragment, width, state):
    """Stub implementation"""
    return (fragment, None)

def adpcm2lin(fragment, width, state):
    """Stub implementation"""
    return (fragment, None)

def ratecv(fragment, width, nchannels, inrate, outrate, state, weightA=1, weightB=2):
    """Stub implementation"""
    return (fragment, None)

__all__ = ['mult', 'tomono', 'tostereo', 'findfit', 'findfactor', 'findmax',
           'avgpp', 'maxpp', 'avg', 'rms', 'add', 'bias', 'reverse',
           'lin2alaw', 'alaw2lin', 'lin2ulaw', 'ulaw2lin',
           'lin2adpcm', 'adpcm2lin', 'ratecv']
