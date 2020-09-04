import sys
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        #Set up
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #connect button click to slot for classifyButtonClicked
        self.ui.classifyButton.clicked.connect(self.classifyButtonClicked)

        #Add spectrogram to UI
        self.ui.spectrogram.setPixmap(QPixmap("../Five Class ASL/Breath/04020036_1582825283_Raw_0.png"))

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
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
