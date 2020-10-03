import sys
import os
import matlab.engine

from PyQt5 import QtWidgets
from MainWindow import MainWindow
from ui_mainwindow import Ui_MainWindow
from multiprocessing import Pool
from time import sleep

def readXbee():
    #readXbee
    for i in range(40):
        print("read")
        sleep(1.6548666)

    #sendXbee to callMatlab

def callMatlab(num):
    #need to pass in data from xbees

    print("here")
    eng = matlab.engine.start_matlab()
    for i in range(0, 60):
        returned = eng.generaterandom(20)
        print(returned)
        sleep(1)

    eng.quit()

def startUI():
    #set up UI
    app = QtWidgets.QApplication([])    #need to pass returned matlab data
    widget = MainWindow()
    widget.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    #sync calls
    pool = Pool()
    result1 = pool.apply_async(callMatlab, 20)
    result2 = pool.apply_async(startUI)
    result3 = pool.apply_async(readXbee)
    callMatlab(10)


