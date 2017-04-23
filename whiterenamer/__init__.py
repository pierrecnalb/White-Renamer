#!/usr/bin/python3

from . import model

from file_system_tree_model import DataModel
from file_system_visitor import FilenameActionCollection, ExtensionActionCollection, FolderActionCollection




def start():
    run.main()

version = Version(1, 0, 0)
__version__=str(version)
print(__version__)

