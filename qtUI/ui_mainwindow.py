# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spectrogramLayout = QGridLayout()
        self.spectrogramLayout.setObjectName(u"spectrogramLayout")
        self.horizontalSpacer_2 = QSpacerItem(88, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.spectrogramLayout.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.spectrogramLayout.addItem(self.verticalSpacer_4, 0, 1, 1, 1)

        self.spectrogram = QLabel(self.centralwidget)
        self.spectrogram.setObjectName(u"spectrogram")

        self.spectrogramLayout.addWidget(self.spectrogram, 1, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.spectrogramLayout.addItem(self.horizontalSpacer_7, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.spectrogramLayout.addItem(self.verticalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(88, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.spectrogramLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.btn_select = QPushButton(self.centralwidget)
        self.btn_select.setObjectName(u"btn_select")

        self.spectrogramLayout.addWidget(self.btn_select, 0, 0, 1, 1)

        self.videoGifLabel = QLabel(self.centralwidget)
        self.videoGifLabel.setObjectName(u"videoGifLabel")

        self.spectrogramLayout.addWidget(self.videoGifLabel, 1, 1, 1, 1)

        self.spectrogramLayout.setRowStretch(0, 1)
        self.spectrogramLayout.setRowStretch(1, 6)
        self.spectrogramLayout.setColumnStretch(0, 1)
        self.spectrogramLayout.setColumnStretch(1, 6)
        self.spectrogramLayout.setColumnStretch(2, 1)
        self.spectrogramLayout.setColumnStretch(3, 6)
        self.spectrogramLayout.setColumnStretch(4, 1)

        self.verticalLayout.addLayout(self.spectrogramLayout)

        self.buttonAlgLayout = QGridLayout()
        self.buttonAlgLayout.setObjectName(u"buttonAlgLayout")
        self.horizontalSpacer_3 = QSpacerItem(188, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttonAlgLayout.addItem(self.horizontalSpacer_3, 1, 4, 2, 1)

        self.algorithmLabel = QLabel(self.centralwidget)
        self.algorithmLabel.setObjectName(u"algorithmLabel")

        self.buttonAlgLayout.addWidget(self.algorithmLabel, 1, 1, 1, 1, Qt.AlignBottom)

        self.algorithmDropDown = QComboBox(self.centralwidget)
        self.algorithmDropDown.addItem("")
        self.algorithmDropDown.addItem("")
        self.algorithmDropDown.setObjectName(u"algorithmDropDown")

        self.buttonAlgLayout.addWidget(self.algorithmDropDown, 2, 1, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(168, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttonAlgLayout.addItem(self.horizontalSpacer_4, 1, 0, 2, 1)

        self.classifyButton = QPushButton(self.centralwidget)
        self.classifyButton.setObjectName(u"classifyButton")

        self.buttonAlgLayout.addWidget(self.classifyButton, 2, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 28, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.buttonAlgLayout.addItem(self.verticalSpacer_2, 0, 2, 1, 1)

        self.buttonAlgLayout.setRowStretch(0, 1)
        self.buttonAlgLayout.setColumnStretch(0, 1)

        self.verticalLayout.addLayout(self.buttonAlgLayout)

        self.resultLayout = QGridLayout()
        self.resultLayout.setObjectName(u"resultLayout")
        self.horizontalSpacer_6 = QSpacerItem(178, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.resultLayout.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.resultLayout.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(178, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.resultLayout.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.result = QLabel(self.centralwidget)
        self.result.setObjectName(u"result")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result.sizePolicy().hasHeightForWidth())
        self.result.setSizePolicy(sizePolicy)

        self.resultLayout.addWidget(self.result, 1, 1, 1, 1)

        self.resultLayout.setRowStretch(0, 1)
        self.resultLayout.setRowStretch(1, 6)
        self.resultLayout.setColumnStretch(0, 1)
        self.resultLayout.setColumnStretch(1, 2)
        self.resultLayout.setColumnStretch(2, 1)

        self.verticalLayout.addLayout(self.resultLayout)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.spectrogram.setText("")
        self.btn_select.setText(QCoreApplication.translate("MainWindow", u"Change Event", None))
        self.videoGifLabel.setText("")
        self.algorithmLabel.setText(QCoreApplication.translate("MainWindow", u"Classification Algorithm", None))
        self.algorithmDropDown.setItemText(0, QCoreApplication.translate("MainWindow", u"Support Vector Machine", None))
        self.algorithmDropDown.setItemText(1, QCoreApplication.translate("MainWindow", u"K Nearest Neighbor", None))

        self.classifyButton.setText(QCoreApplication.translate("MainWindow", u"Classify", None))
        self.result.setText("")
    # retranslateUi

