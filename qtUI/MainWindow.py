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

        # Gif word test #
        gifResults = QMovie("media/resultsgif.gif")
        self.ui.result.setMovie(gifResults)
        gifResults.start()

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
