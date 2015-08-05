#author : pierrecnalb
#copyright pierrecnalb
import os
import sys
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtSvg  import *
import resource_rc
import MainWindow

__version__ = '1.0.0'

def main():
    app = QApplication(sys.argv)
    translator = QTranslator()
    locale = QLocale.system().name()[:2]
    if locale == "fr":
        translator.load('i18n/tr_fr', os.path.dirname(__file__))
    app.installTranslator(translator)
    win = MainWindow.MainWindow()
    #MainWidget.SizeCalculator(win)
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
