#!/usr/bin/python3
#WhiteRenamer.py
#copyright pierrecnalb
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
    try:
        code_online = urlopen("https://raw.githubusercontent.com/pierrecnalb/White-Renamer/master/WhiteRenamer.py").read().splitlines()
        version_online = code_online[13].decode().split('=')[-1]
        version_online = version_online.split("'")[1]
        if(version_online != __version__):
            win.update_message(__version__, version_online)
    except:
        pass
    app.exec_()


if __name__ == '__main__':
    main()
