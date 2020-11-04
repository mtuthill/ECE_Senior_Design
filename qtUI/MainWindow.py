import sys
import os

from PyQt5.QtGui import *
#from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import uic
#from PyQt5 import QtMultimedia, uic, QtCore
from PyQt5.Qt import QUrl

import classify

class MainWindow:
    def __init__(self):
        #Set up
        self.ui = uic.loadUi('form.ui')

        #connect button click to slot for classifyButtonClicked
        self.ui.classifyButton.clicked.connect(self.classifyButtonClicked)

        #Add spectrogram to UI
        self.ui.spectrogram.setPixmap(QPixmap("media/pete_fallingSitting_toward_1.png"))

<<<<<<< Updated upstream
=======
        #Add test gif to UI
        #gifTest = QMovie("media/person_Falling.gif")
        #self.ui.result.setMovie(gifTest)
        #gifTest.start()

        # Gif word test #
        gifResults = QMovie("media/resultsgif.gif")
        self.ui.result.setMovie(gifResults)
        gifResults.start()

        #Set up MP4
        #self.player = QMediaPlayer()
        #self.player.setVideoOutput(self.ui.wgt_player)
        #self.player.setMedia(QMediaContent(QUrl.fromLocalFile("media/testMP4.mp4")))
        #self.player.play()
        #self.ui.openVideoButton.clicked.connect(self.openVideoFile)
        #self.ui.playButton.clicked.connect(self.play)
        self.ui.pauseButton.clicked.connect(self.pause)
        self.ui.stopButton.clicked.connect(self.stop)

    def openVideoFile(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
        self.player.play()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

>>>>>>> Stashed changes
    def classifyButtonClicked(self):
        fallNonFallClass = classify.classify(self.ui.algorithmDropDown.currentText())

        #Display result
        if(fallNonFallClass == 0):
            gifFall = QMovie("media/Non-fall.gif")
            self.ui.result.setMovie(gifFall)
            gifFall.start()

        else:
            gifNonFall = QMovie("media/Fall_gif.gif")
            self.ui.result.setMovie(gifNonFall)
            gifNonFall.start()
