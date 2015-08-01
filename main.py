#author : pierrecnalb
#copyright pierrecnalb
#v.1.0.11
import os
import sys
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import resource_rc
import MainWindow


def main():
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load('i18n/tr_fr', os.path.dirname(__file__))
    app.installTranslator(translator)
    win = MainWindow.MainWindow()
    #MainWidget.SizeCalculator(win)
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
