from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
import os
import time

from ftplib import FTP
import ftpAccess

class Ui(QtWidgets.QMainWindow):
    def resetButtonClicked(self):
        self.setStyleSheet("background-color: white;")
        gifResults = QMovie("media/resultsgif.gif")
        self.result.setMovie(gifResults)
        gifResults.start()

    def displayResult(self, fallNonFallClass, type):
        #Display result
        #0 = fallingSitting, 1 = fallingStanding, 2 = fallingWalking, 3 = movement, 4 = sitting, 5 = walking
        #or 0 = nonfall, 1 = fall
        print(type)
        if ("y" in type):
            if(fallNonFallClass == 0):
                gifFall = QMovie("media/Non-fall.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: green;")
            else:
                gifNonFall = QMovie("media/Fall_gif.gif")
                self.result.setMovie(gifNonFall)
                gifNonFall.start()
                self.setStyleSheet("background-color: red;")
        else:
            if(fallNonFallClass == 0):
                gifFall = QMovie("media/FallFromSitting.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: red;")

            elif(fallNonFallClass == 1):
                gifFall = QMovie("media/FallFromStand.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: red;")

            elif(fallNonFallClass == 2):
                gifFall = QMovie("media/FallFromWalk.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: red;")

            elif(fallNonFallClass == 3):
                gifFall = QMovie("media/GenericMovement.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: green;")

            elif(fallNonFallClass == 4):
                gifFall = QMovie("media/Sitting.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: green;")

            elif(fallNonFallClass == 5):
                gifFall = QMovie("media/Walking.gif")
                self.result.setMovie(gifFall)
                gifFall.start()
                self.setStyleSheet("background-color: green;")

            else:
                gifNonFall = QMovie("media/EventUnknown.gif")
                self.result.setMovie(gifNonFall)
                gifNonFall.start()
                self.setStyleSheet("background-color: red;")
        #delete file
        ftp = FTP('172.20.10.5')
        ftp.login(user='pi', passwd = 'radar')
        ftpAccess.deleteFileFromServer(ftp, "classificationInfo.txt", "~/ftp/files")


    def slotCheckForFile(self):
        #delete from local
        if (os.path.exists('classificationInfo.txt')):
            os.remove("classificationInfo.txt")

        #Open ftp
        ftp = FTP('172.20.10.5')
        ftp.login(user='pi', passwd = 'radar')
        ftpAccess.downloadFileFromServer(ftp, "classificationInfo.txt", "~/ftp/files", "classificationInfo.txt")

        #If exists, process
        if (os.path.exists('classificationInfo.txt')):
            file = open('classificationInfo.txt')
            lines = file.readlines()
            file.close()
            if (len(lines) > 1):
                self.displayResult(int(lines[1]), str(lines[2]))

        if (os.path.exists('classificationInfo.txt')):
            os.remove('classificationInfo.txt')

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('form.ui', self)
        #connect buttons
        self.resetButton.clicked.connect(self.resetButtonClicked)

        # Gif word test #
        gifResults = QMovie("media/resultsgif.gif")
        self.result.setMovie(gifResults)
        gifResults.start()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.slotCheckForFile)
        self.timer.start(3000)   #3 seconds

        self.show()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


