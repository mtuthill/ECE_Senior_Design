import sys
import os
import matlab.engine
import joblib
import multiprocessing

from time import perf_counter
from os.path import isfile, getsize

def findResult(startBit, lengthToRead, f, eng, procNum):
	#read data starting at specified bit for a certain length
	f.seek(startBit)
	rawData = list(f.read(lengthToRead))

	#get spectrogram
	#get filenames for spectrograms (temporay until actual spectrogram)
	path = r"../../ECE_Senior_Design_Data/nonFallSpectrograms/0_Walking_towards_radar/"
	dataFile = r"04000000_1574696114_Raw_0.png"

	#get features
	features = eng.dctFromPng(path + dataFile)

	#get classification result
	result = classifier.predict(features)
	
	print("Result {} = {}".format(procNum, result1))


	return result


if __name__ == "__main__":
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

	#find file
	while ((not(isfile(dataPath + filename))) and fileSizeFlag == 0):
	    if (isfile(dataPath + filename)):
	    	if (os.stat(filename).st_size > 76799000):
	        	fileSizeFlag = 1

	#open file
	f = open(filename, "rb")
	fileSize = getsize(filename)

	#find results
	pool = multiprocessing.Pool()
	result1 = pool.apply_async(findResult, args = (0, fileSize * 0.5, f, eng, 0))
	result2 = pool.apply_async(findResult, args = (fileSize * 0.25, fileSize * 0.5, f, eng, 1))
	result3 = pool.apply_async(findResult, args = (fileSize * 0.5, fileSize * 0.5, f, eng, 2))
	pool.close()
	pool.join()

	#stop timer
	endTime = perf_counter()
	print("Total time in secs = ")
	print(endTime - startTime)

	f.close()
	eng.quit()
