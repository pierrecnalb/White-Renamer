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
    app.setStyle(QStyleFactory.create("fusion"))
    palette = QPalette()
    #palette.setColor(QPalette.Window, QColor(210,210,210));
    #palette.setColor(QPalette.WindowText, Qt.white);
    #palette.setColor(QPalette.Base, Qt.white);
    #palette.setColor(QPalette.AlternateBase, QColor(53,53,53));
    #palette.setColor(QPalette.ToolTipBase, Qt.white);
    #palette.setColor(QPalette.ToolTipText, Qt.white);
    #palette.setColor(QPalette.Text, Qt.red);
    #palette.setColor(QPalette.Button, QColor(53,53,53));
    #palette.setColor(QPalette.ButtonText, Qt.red);
    #palette.setColor(QPalette.BrightText, Qt.red);
    #palette.setColor(QPalette.Highlight, QColor(142,45,197).lighter());
    palette.setColor(QPalette.HighlightedText, Qt.green);
    app.setPalette(palette);
    translator = QTranslator()
    translator.load('i18n/tr_fr', os.path.dirname(__file__))
    app.installTranslator(translator)
    win = MainWindow.MainWindow()
    #MainWidget.SizeCalculator(win)
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
