import unittest
import os, sys
sys.path.append('/home/pierre/Documents/Programs/white-renamer/whiterenamer')
from . import TestCases
from . import TestCasesModel


def whiterenamer_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(TestCases)
    return suite

