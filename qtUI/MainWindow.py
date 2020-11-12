import sys
import os
#import matlab.engine

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import uic
from PyQt5.Qt import QUrl

#import classify

file = "default.bin"
class MainWindow:
    global file
    def __init__(self):
        #Set up
        self.ui = uic.loadUi('form.ui')

        #connect buttons
        self.ui.classifyButton.clicked.connect(self.classifyButtonClicked)
        self.ui.changeEventButton.clicked.connect(self.changeEventButtonClicked)

        self.ui.changeVideoButton.clicked.connect(self.changeVideoButtonClicked)

        # Gif word test #
        gifResults = QMovie("media/resultsgif.gif")
        self.ui.result.setMovie(gifResults)
        gifResults.start()

        #spectogram and video gif #
        spect_gif = QMovie("media/spect_gif.gif")
        self.ui.spectrogram.setMovie(spect_gif)
        spect_gif.start()

        video_gif = QMovie("media/vid_gif.gif")
        self.ui.videoGifLabel.setMovie(video_gif)
        video_gif.start()

        self.ui.algorithmLabel.setStyleSheet('border: 2px solid black; border-radius: 10px; background: rgb(203,190,181);')
        self.ui.binaryAllClassLabel.setStyleSheet('border: 2px solid black; border-radius: 10px; background: rgb(203,190,181);')

    def classifyButtonClicked(self):
        print(file)
        fallNonFallClass = classify.classify(self.ui.algorithmDropDown.currentText(), self.ui.numClassCBox.currentText(), file)
        outfile = 'out_spectrogram.png'
        self.ui.spectrogram.setPixmap(QPixmap("out_spectrogram.png"))
        print(fallNonFallClass)

        #Display result
        #0 = fallingSitting, 1 = fallingStanding, 2 = fallingWalking, 3 = movement, 4 = sitting, 5 = walking
        #or 0 = nonfall, 1 = fall
        if (self.ui.numClassCBox.currentText() == "Binary"):
            #print("Binary")
            if(fallNonFallClass == 0):
                gifFall = QMovie("media/Non-fall.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: green;")

            else:
                gifNonFall = QMovie("media/Fall_gif.gif")
                self.ui.result.setMovie(gifNonFall)
                gifNonFall.start()
                self.ui.setStyleSheet("background-color: red;")
        else:
            #print("All class")
            if(fallNonFallClass == 0):
                gifFall = QMovie("media/FallFromSitting.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: red;")

            if(fallNonFallClass == 1):
                gifFall = QMovie("media/FallFromStand.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: red;")

            if(fallNonFallClass == 2):
                gifFall = QMovie("media/FallFromWalk.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: red;")

            if(fallNonFallClass == 3):
                gifFall = QMovie("media/GenericMovement.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: green;")

            if(fallNonFallClass == 4):
                gifFall = QMovie("media/Sitting.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: green;")

            if(fallNonFallClass == 5):
                gifFall = QMovie("media/Walking.gif")
                self.ui.result.setMovie(gifFall)
                gifFall.start()
                self.ui.setStyleSheet("background-color: green;")

            else:
                gifNonFall = QMovie("media/EventUnknown.gif")
                self.ui.result.setMovie(gifNonFall)
                gifNonFall.start()
                self.ui.setStyleSheet("background-color: red;")

    def changeEventButtonClicked(self):
        #open finder and change file. Must be in same directory
        inputFile = QFileDialog.getOpenFileUrl()[0]
        global file
        file = inputFile.fileName()

    def changeVideoButtonClicked(self):
        #open finder and change file. Must be in same directory
        inputFile = QFileDialog.getOpenFileUrl()[0]
        vidfile = inputFile.fileName()
        vidResults = QMovie(vidfile)
        self.ui.videoGifLabel.setMovie(vidResults)
        vidResults.start()






