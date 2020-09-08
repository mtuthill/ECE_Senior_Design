import sys
import os
import PySide2

from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia, uic, QtCore
from PyQt5.Qt import QUrl
#from PyQt5.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow

class MainWindow:
    def __init__(self):
        #Set up
        self.ui = uic.loadUi('form.ui')

        #connect button click to slot for classifyButtonClicked
        self.ui.classifyButton.clicked.connect(self.classifyButtonClicked)

        #Add spectrogram to UI
        self.ui.spectrogram.setPixmap(QPixmap("../Five Class ASL/Breath/04020036_1582825283_Raw_0.png"))

        #Add test gif to UI
        gifTest = QMovie("media/person_Falling.gif")
        self.ui.result.setMovie(gifTest)
        gifTest.start()

        #Set up MP4
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.ui.wgt_player)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("media/testMP4.mp4")))
        self.player.play()
        self.ui.btn_select.clicked.connect(self.openVideoFile)

    def openVideoFile(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
        self.player.play()


    def classifyButtonClicked(self):
        #Classify based on selected algorithm, call function from other file
        #fallNonFallClass = classify()
        fallNonFallClass = 0

        #Display result
        if(fallNonFallClass == 0):
            self.ui.result.setText("Non Fall")
        else:
            self.ui.result.setText("Fall")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.ui.show()
    sys.exit(app.exec_())
