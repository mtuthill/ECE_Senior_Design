<<<<<<< HEAD
import sys
import os
import classify
import matlab.engine

from multiprocessing import Process, Pipe
from os import listdir
from os.path import isfile, join
from time import sleep

def readXbee():
    #readXbee
    for i in range(40):
        sleep(1.6548666)

    #sendXbee to callMatlab

def getFeaturesFromSpectrogram(postFeatureConn):
    #need to pass in data from xbees

    #get filenames for spectrograms
    path = "../../ECE_Senior_Design_Data/nonFallSpectrograms/05_Walking_towards_radar/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    eng = matlab.engine.start_matlab()
    for file in onlyfiles:
        returned = eng.dctFromPng(path + file)
        postFeatureConn.send(returned)
        #print("Sent the message: {}".format(returned))
        sleep(1)

    eng.quit()

def callClassification(postFeatureConn):
    while 1:
        msg = postFeatureConn.recv()
        #print("Recieved the message: {}".format(msg))
        #classify


if __name__ == "__main__":
    matlabSender, classificationReciever = Pipe()

    p1 = Process(target = getFeaturesFromSpectrogram, args = (matlabSender,))
    p2 = Process(target = callClassification, args = (classificationReciever,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
