import sys
import os
import matlab.engine
import joblib

from time import perf_counter
from os.path import isfile

#start matlab
eng = matlab.engine.start_matlab()

#load classifier that is pretrained
classifierFile = "storedTestSVM.sav"
classifier = joblib.load(classifierFile)

#find data
dataPath = r"./"
filename = r"target_Raw_0.bin"
fileSizeFlag = 0
startedTimerFlag = 0
startTime = perf_counter()

#print("Checking for file")
while ((not(isfile(dataPath + filename))) and fileSizeFlag == 0):
    if (isfile(dataPath + filename)):
    	if (os.stat(filename).st_size > 76799000):
        	fileSizeFlag = 1

print("Time from start to finding binary data file")
print(perf_counter() - startTime)

#read file
f = open(filename, "rb")
rawData = list(f.read())
print("Time from start to reading binary data")
print(perf_counter() - startTime)

#get spectrogram

#get filenames for spectrograms (temporay until actual spectrogram)
path = r"../../ECE_Senior_Design_Data/nonFallSpectrograms/0_Walking_towards_radar/"
dataFile = r"04000000_1574696114_Raw_0.png"

#get features
features = eng.dctFromPng(path + dataFile)
print("Time from start to getting features from spectrogram")
print(perf_counter() - startTime)

#get classification result
result = classifier.predict(features)

#stop timer
endTime = perf_counter()
print("Total time in secs = ")
print(endTime - startTime)

f.close()
eng.quit()
