import sys
import os
import matlab.engine
import sklearn.metrics
import numpy
import joblib
import pandas
import pymrmr
import time

from os import listdir
from os.path import isfile, join
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

import matplotlib.pyplot as plt

#CHANGE THESE AS NEEDED
##################################
numDCTFeatures = 10
dctFeaturesFlag = 0
envFeaturesFlag = 0
physFeaturesFlag = 1
numFeaturesToSelect = 1
mRMRType = "MIQ"			#Has to be "MIQ" or "MID"
testTrainSplit = 0.3		#Default is 0.3
kernel = "linear"			#Default is linear, can be "linear", "poly", "rbf", "sigmoid"
numberOfRuns = 50			#Default it 50
##################################

#get filenames for data
names = ['GraceSpecs', 'MarcSpecs', 'PeteSpecs']
fallSubdirs = ['fallingSitting', 'fallingStanding', 'fallingWalking']
nonFallSubdirs = ['Movement', 'Sitting', 'Walking']

#get filenames for DataFrame
path = "../../../ECE_Senior_Design_Our_Data"
fallFiles = []
nonFallFiles = []
for name in names:
	for fallDir in fallSubdirs:
		fallFiles = fallFiles + [(path + "/"  + name + "/" + fallDir + "/" + f) for f in listdir(join(path, name, fallDir)) if isfile(join(path, name, fallDir, f))]
	for nonFallDir in nonFallSubdirs:
		nonFallFiles = nonFallFiles + [(path + "/"  + name + "/" + nonFallDir + "/" + f) for f in listdir(join(path, name, nonFallDir)) if isfile(join(path, name, nonFallDir, f))]

#get spectrograms and get features from spectrograms
eng = matlab.engine.start_matlab()
fallData = []
nonFallData = []

for file in nonFallFiles:
	nonFallData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
for file in fallFiles:
	fallData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
    

eng.quit()    

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
nonFallData = [item for sublist in nonFallData for item in sublist]
fallData = [item for sublist in fallData for item in sublist]

#combine to form all data
allData = nonFallData + fallData

#make classification list
results = [0] * len(nonFallData) + [1] * len(fallData)

#find total number of features
numFeatures = 0
if dctFeaturesFlag == 1:
	numFeatures = numFeatures + numDCTFeatures
if envFeaturesFlag == 1:
	numFeatures = numFeatures + 7
if physFeaturesFlag == 1:
	numFeatures = numFeatures + 4

#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = []
for i in range(numFeatures):
	colNames.append(str(i))
kernels = ["poly", "rbf", "sigmoid"]
nums = [1,2,3,4]
array2d = []
for j in kernels:
	for k in nums:
		totalF1 = 0
		totalAcc = 0
		df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)
		#improved feature selection using mRMR
		returned = pymrmr.mRMR(df, mRMRType, nums[k-1])
		returnedInts = [int(i) for i in returned]

		df.insert(numFeatures, "Classes", results)
		for i in range(numberOfRuns):
			#get data after feature selected
			dfFeatureSelectedData = df[df.columns[returnedInts]]
			dfFeatureSelectedResults = results
			#Split test and training sets
			allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = testTrainSplit)

			#Train algorithm
			if (kernel == "poly"):
				classifier = SVC(kernel=j, degree=3)
			elif (kernel == "rbf"):
				classifier = SVC(kernel='rbf', gamma=0.7)
			elif (kernel == "sigmoid"):
				classifier = SVC(kernel = 'sigmoid', gamma=2)
			else:
				classifier = SVC(kernel=j)

			classifier.fit(allDataTrain, resultTrain)

			#Make predictions
			predictions = list(classifier.predict(allDataTest))
			resultTest = list(resultTest)

			totalF1 = totalF1 + sklearn.metrics.f1_score(resultTest, predictions, average = 'weighted')
			totalAcc = totalAcc + sklearn.metrics.accuracy_score(resultTest, predictions)
		array = [str(k), str(returnedInts), str(totalF1/numberOfRuns), str(totalAcc/numberOfRuns)]
		print(array)
		array2d.append(array)


print(array2d)
dfArray2d = pandas.DataFrame(array2d)
dfArray2d.to_csv("testBin.csv", index = False, header = False)