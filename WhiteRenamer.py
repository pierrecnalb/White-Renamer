#author : pierrecnalb
#copyright pierrecnalb
import os
import sys
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
# from PySide.QtSvg  import *
import resource_rc
import MainWindow
import urllib.request

__version__ = '1.0.0'


def main():
    app = QApplication(sys.argv)
    translator = QTranslator()
    locale = QLocale.system().name()[:2]
    if getattr(sys, 'frozen', False):
        # frozen
        dir_ = os.path.dirname(sys.executable)
    else:
        # unfrozen
        dir_ = os.path.dirname(os.path.realpath(__file__))
    if locale == "fr":
        translator.load('i18n/tr_fr', dir_)

    app.installTranslator(translator)
    win = MainWindow.MainWindow()
    # MainWidget.SizeCalculator(win)
    win.show()
    try:
        code_online = urllib.request.urlopen("https://raw.githubusercontent.com/pierrecnalb/White-Renamer/master/WhiteRenamer.py").read().splitlines()
        version_online = code_online[12].decode().split('=')[-1]
        version_online = version_online.split("'")[1]
        if(version_online != __version__):
            win.update_message(__version__, "version_online")
    except:
        pass
    app.exec_()


if __name__ == '__main__':
    main()
