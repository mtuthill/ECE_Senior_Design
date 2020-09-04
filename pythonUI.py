import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
	

def window():
	app = QApplication(sys.argv)
	widget = QWidget()
	
	layout = QVBoxLayout(widget)

	specLabel = QLabel(widget)
	specLabel.setText("Spectrogram")
	specLabel.setAlignment(Qt.AlignCenter)
	font = QFont() 
	font = specLabel.font()
	font.setPointSize(30)
	specLabel.setFont(font)

	picture = QLabel(widget)
	pixmap = QPixmap("Five Class ASL/Car/4030013_1582826208_Raw_0.png")
	picture.setPixmap(pixmap)
	picture.show()

	fall = QLabel(widget)
	fall.setText("Fall Detected")
	fall.setAlignment(Qt.AlignCenter)
	font = fall.font()
	font.setPointSize(30)
	fall.setStyleSheet("QLabel { background-color : red; color : black; }")
	fall.setFont(font)

	layout.addWidget(specLabel, 0, Qt.AlignCenter)
	layout.addWidget(picture, 0, Qt.AlignCenter)
	layout.addWidget(fall, 0, Qt.AlignCenter)

	widget.setLayout(layout)
	widget.setStyleSheet("background-color:darkGray;") 

	widget.setWindowTitle("Senior Design")
	widget.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	window()
	
	
