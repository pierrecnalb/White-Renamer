#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.
from os.path import dirname, realpath
import sys
from .ui import MainWindow, resource_rc
from urllib.request import urlopen
from PySide.QtGui import QApplication, QIcon
from PySide.QtCore import QTranslator, QLocale

def main():
    app = QApplication(sys.argv)
    translator = QTranslator()
    locale = QLocale.system().name()[:2]
    if getattr(sys, 'frozen', False):
        # frozen
        dir_ = dirname(sys.executable)
    else:
        # unfrozen
        dir_ = dirname(realpath(__file__))
        if locale == "fr":
            translator.load('i18n/tr_fr', dir_)
        app.installTranslator(translator)
        win = MainWindow()
        app.setWindowIcon(QIcon(':/white_renamer48.png'))
        # MainWidget.SizeCalculator(win)
        win.show()
        app.exec_()
