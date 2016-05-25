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
# from PyQt5.QtGui import QApplication, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def main():
    app = QApplication(sys.argv)

    #UI Design style
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(250, 250, 250))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(233, 233, 233))
    palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(220, 220, 220))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(52, 140, 228))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    translator = QTranslator()
    locale = QLocale.system().name()[:2]
    if getattr(sys, 'frozen', False):
        # frozen
        dir_ = dirname(sys.executable)
    else:
        # unfrozen
        dir_ = dirname(realpath(__file__))
        if locale == "fr":
            translator.load('ui/i18n/tr_fr', dir_)
        app.installTranslator(translator)
        win = MainWindow()
        app.setWindowIcon(QIcon(':/white_renamer48.png'))
        # MainWidget.SizeCalculator(win)
        win.show()
        app.exec_()
