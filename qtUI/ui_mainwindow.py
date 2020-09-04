from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.spectrogram = QGraphicsView(self.centralwidget)
        self.spectrogram.setObjectName(u"spectrogram")
        self.spectrogram.setGeometry(QRect(90, 10, 611, 341))
        self.algorithmDropDown = QComboBox(self.centralwidget)
        self.algorithmDropDown.addItem("")
        self.algorithmDropDown.addItem("")
        self.algorithmDropDown.setObjectName(u"algorithmDropDown")
        self.algorithmDropDown.setGeometry(QRect(190, 410, 171, 31))
        self.algorithmLabel = QLabel(self.centralwidget)
        self.algorithmLabel.setObjectName(u"algorithmLabel")
        self.algorithmLabel.setGeometry(QRect(200, 390, 141, 16))
        self.resultGraphic = QGraphicsView(self.centralwidget)
        self.resultGraphic.setObjectName(u"resultGraphic")
        self.resultGraphic.setGeometry(QRect(160, 470, 441, 101))
        self.classifyButton = QPushButton(self.centralwidget)
        self.classifyButton.setObjectName(u"classifyButton")
        self.classifyButton.setGeometry(QRect(420, 410, 171, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.algorithmDropDown.setItemText(0, QCoreApplication.translate("MainWindow", u"Support Vector Machine", None))
        self.algorithmDropDown.setItemText(1, QCoreApplication.translate("MainWindow", u"K Nearest Neighbor", None))

        self.algorithmLabel.setText(QCoreApplication.translate("MainWindow", u"Classification Algorithm", None))
        self.classifyButton.setText(QCoreApplication.translate("MainWindow", u"Classify", None))
    # retranslateUi

