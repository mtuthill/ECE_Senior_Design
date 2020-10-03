import sys
import os
import matlab.engine

from PyQt5 import QtWidgets
from MainWindow import MainWindow
from ui_mainwindow import Ui_MainWindow

if __name__ == "__main__":

    #read in values from Xbee, might need to run in parallel?


    #organize data as needed


    #matlab calls
    eng = matlab.engine.start_matlab()
    for i in range(0, 5):
        returned = eng.generaterandom(20)
        print(returned)

    eng.quit()

    #set up UI
    app = QtWidgets.QApplication([])    #need to pass returned matlab data
    widget = MainWindow()
    widget.ui.show()
    sys.exit(app.exec_())
