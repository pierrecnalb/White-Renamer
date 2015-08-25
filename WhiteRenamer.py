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
    app.setStyleSheet("""
QToolButton
{ selection-background-color: #ffaa00; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646); border-style: solid; border: 1px solid #1e1e1e; border-radius: 5; }

""")


    # app.setStyle(QStyleFactory.create("fusion"));

    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(53,53,53));
    # palette.setColor(QPalette.WindowText, Qt.white);
    # palette.setColor(QPalette.Base, QColor(15,15,15));
    # palette.setColor(QPalette.AlternateBase, QColor(53,53,53));
    # palette.setColor(QPalette.ToolTipBase, Qt.white);
    # palette.setColor(QPalette.ToolTipText, Qt.white);
    # palette.setColor(QPalette.Text, Qt.white);
    # palette.setColor(QPalette.Button, QColor(53,53,53));
    # palette.setColor(QPalette.ButtonText, Qt.white);
    # palette.setColor(QPalette.BrightText, Qt.red);
# 
    # palette.setColor(QPalette.Highlight, QColor(142,45,197).lighter());
    # palette.setColor(QPalette.HighlightedText, Qt.black);
    # app.setPalette(palette);

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
    #MainWidget.SizeCalculator(win)
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
