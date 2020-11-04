import sys
import os
import matlab.engine

from PyQt5 import QtWidgets
from MainWindow import MainWindow
from ui_mainwindow import Ui_MainWindow
from multiprocessing import Process, Pool, Queue
from time import sleep
from os import listdir
from os.path import isfile, join

def startUI():
    #set up UI
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    startUI()


