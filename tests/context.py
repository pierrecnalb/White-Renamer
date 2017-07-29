#!/usr/bin/python3

"""This module gives the ability to import whiterenamer package without
having to run setup.py everytime."""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import whiterenamer
