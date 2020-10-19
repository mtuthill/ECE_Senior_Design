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

def callMatlab():
    #get binary data
    dataPath = "./"
    onlyfiles = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]
    filename = 'empty_target_Raw_0.bin'
    while (not(filename in onlyfiles)):
        print("file checked for")
        sleep(10)
        onlyfiles = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]

    print("File found")

    f=open(filename, "rb")
    num=list(f.read())
    f.close()

    #get spectrogram

    #get filenames for spectrograms
    path = "../../ECE_Senior_Design_Data/nonFallSpectrograms/05_Walking_towards_radar/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    #get features
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
    callMatlab()


