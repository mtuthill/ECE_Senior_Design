import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import RPi.GPIO as GPIO

currValue = 1
outputPin = 18  # BOARD pin 12, BCM pin 18

def blinkLEDSlot():
	global currValue
	global outputPin
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(outputPin, GPIO.OUT)
	if (currValue == 1):
		currValue = 0
		GPIO.output(outputPin, GPIO.LOW)
	else:
		currValue = 1
		GPIO.output(outputPin, GPIO.HIGH)
	

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
	pixmap = QPixmap("/home/radar/Documents/Example Spectrograms/Earthquake/04010005_1582046023_Raw_0.png")
	picture.setPixmap(pixmap)
	picture.show()

	fall = QLabel(widget)
	fall.setText("Fall Detected")
	fall.setAlignment(Qt.AlignCenter)
	font = fall.font()
	font.setPointSize(30)
	fall.setStyleSheet("QLabel { background-color : red; color : black; }")
	fall.setFont(font)
	
	button = QPushButton("Blink LED")
	button.clicked.connect(blinkLEDSlot)

	layout.addWidget(specLabel, 0, Qt.AlignCenter)
	layout.addWidget(picture, 0, Qt.AlignCenter)
	layout.addWidget(fall, 0, Qt.AlignCenter)
	layout.addWidget(button)

	widget.setLayout(layout)

	widget.setWindowTitle("Senior Design")
	widget.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	window()
	
	
