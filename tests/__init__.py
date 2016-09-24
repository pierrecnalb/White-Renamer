import unittest
import os, sys
from . import TestCases
from . import TestCasesModel


def whiterenamer_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(TestCases)
    return suite

