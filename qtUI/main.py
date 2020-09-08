import sys
import os
from PyQt5 import QtWidgets
from MainWindow import MainWindow
from ui_mainwindow import Ui_MainWindow

if __name__ == "__main__":
    #set up UI
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.ui.show()
    sys.exit(app.exec_())
