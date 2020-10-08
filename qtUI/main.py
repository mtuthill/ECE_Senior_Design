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

def readXbee():
    #readXbee
    for i in range(40):
        sleep(1.6548666)

    #sendXbee to callMatlab

def callMatlab():
    #need to pass in data from xbees

    #get filenames for spectrograms
    path = "../../ECE_Senior_Design_Data/nonFallSpectrograms/05_Walking_towards_radar/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    eng = matlab.engine.start_matlab()
    for file in onlyfiles:
        returned = eng.dctFromPng(path + file)
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
    result1 = pool.apply_async(callMatlab)
    result2 = pool.apply_async(startUI)
    result3 = pool.apply_async(readXbee)
    callMatlab()


