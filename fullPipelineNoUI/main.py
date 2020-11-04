import sys
import os
import matlab.engine
import joblib
import time

from multiprocessing import Pool
from time import perf_counter
from os.path import isfile, getsize

classifierOption = "SVM"

def findResult(num):
	#annoyingly, matlab engine api does not like to pass an engine object to a different process
	eng = matlab.engine.start_matlab()

	#load classifier that is pretrained
	if (classifierOption == "KNN"):
		classifierFile = "stored_mRMR_KNN.sav"
		h = open('featuresSelectedKNN.txt', 'r')
	elif (classifierOption == "SVM"):
		classifierFile = "stored_mRMR_SVM.sav"
		h = open('featuresSelectedSVM.txt', 'r')
	else:
		classifierFile = "stored_mRMR_SVM.sav"
		h = open('featuresSelectedSVM.txt', 'r')

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

	#get file size
	#fileSize = getsize(filename)

	#openfile
	#f = open(filename, "rb")

	#find what bits to read
	#if (num == 1):
	#	startBit = 0
	#elif (num == 2):
	#	startBit = int(fileSize * 0.25)
	#else:
	#	startBit = int(fileSize * 0.5)
	#lengthToRead = int(fileSize * 0.5)

	#read data starting at specified bit for a certain length
	#f.seek(startBit)
	#rawData = list(f.read(lengthToRead))

	#get features
	numFeatures = 500
	outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
	features = eng.binToDct(dataPath + filename, outfile, numFeatures)

	#use only the features selected from classifier
	listofFeatures = []
	content = h.readlines() 
	for line in content:
		listofFeatures.append(int(line))

	selectedFeaturesList = [features[0][i] for i in listofFeatures]
	selectedFeatures = [selectedFeaturesList]

	#get classification result
	result = classifier.predict(selectedFeatures)

	#f.close()

	endTime = perf_counter()
	print("Total time in secs for fragment {} = {}".format(num, endTime - startTime))
	
	return result


if __name__ == "__main__":
	with Pool(3) as pool:
		results = pool.map(findResult, [1, 2, 3])

	print(results)