import sys
import os
import matlab.engine

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import uic
from PyQt5.Qt import QUrl

import classify

class MainWindow:
    file = "fallExample.bin"

    def __init__(self):
        #Set up
        self.ui = uic.loadUi('form.ui')

        #connect button click to slot for classifyButtonClicked
        self.ui.classifyButton.clicked.connect(self.classifyButtonClicked)

        #Add spectrogram to UI
        #self.ui.spectrogram.setText(QPixmap("media/pete_fallingSitting_toward_1.png"))
        #spectrogramGif = QMovie("media/spectrogramGif.gif")
        #self.ui.spectrogram.setMovie(spectrogramGif)
        #spectrogramGif.start()
        self.ui.spectrogram.setText("Spectrogram awaiting")

        # Gif word test #
        gifResults = QMovie("media/resultsgif.gif")
        self.ui.result.setMovie(gifResults)
        gifResults.start()

    def classifyButtonClicked(self):
        fallNonFallClass = classify.classify(self.ui.algorithmDropDown.currentText(), self.file)

        #Display result
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
