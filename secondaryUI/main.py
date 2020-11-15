from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
import os
import time

class Ui(QtWidgets.QMainWindow):
    def xor(self, lst1, lst2):
        """ returns a tuple of items of item not in either of lists
        """
        x = lst2 if len(lst2) > len(lst1) else lst1
        y = lst1 if len(lst1) < len(lst2) else lst2
        return tuple(item for item in x if item not in y)

    def resetButtonClicked(self):
        self.setStyleSheet("background-color: white;")
        gifResults = QMovie("media/resultsgif.gif")
        self.result.setMovie(gifResults)
        gifResults.start()
        if (os.path.isfile("infoFromBoard.txt")):
            os.remove("infoFromBoard.txt")

    def displayResult(self, fallNonFallClass, type):
        #Display result
        #0 = fallingSitting, 1 = fallingStanding, 2 = fallingWalking, 3 = movement, 4 = sitting, 5 = walking
        #or 0 = nonfall, 1 = fall
        if (type == 0):
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

    def slotDirChanged(self):
        path = "./"
        newContent = ''.join(self.xor(os.listdir(path), self._initialContent))

        self._initialContent = os.listdir(path)
        msg = ""
        if newContent not in self._initialContent:
            msg = "removed: %s" % newContent
            self.resetButtonClicked()
        else:
            msg = "added: %s" %  newContent
            file = open('infoFromBoard.txt', 'r')
            Lines = file.readlines()
            if (int(Lines[0]) == 1):
                self.displayResult(int(Lines[1]), int(Lines[2]))
        print(msg)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('form.ui', self)
        #connect buttons
        self.resetButton.clicked.connect(self.resetButtonClicked)

        # Gif word test #
        gifResults = QMovie("media/resultsgif.gif")
        self.result.setMovie(gifResults)
        gifResults.start()

        self._pathToWatch = "./"
        self._initialContent = os.listdir(self._pathToWatch)
        self._fileSysWatcher = QtCore.QFileSystemWatcher()
        self._fileSysWatcher.addPath(self._pathToWatch)

        self._fileSysWatcher.directoryChanged.connect(self.slotDirChanged)

        self.show()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


