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

#CHANGE THESE AS NEEDED
##################################
numDCTFeatures = 10
dctFeaturesFlag = 1
envFeaturesFlag = 1
physFeaturesFlag = 1
numFeaturesToSelect = 10
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
path = "../../ECE_Senior_Design_Our_Data"
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
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, mRMRType, numFeaturesToSelect)
returnedInts = [int(i) for i in returned]

df.insert(numFeatures, "Classes", results)

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[numFeatures]]

totalF1 = 0
totalAcc = 0

for i in range(numberOfRuns):
	#Split test and training sets
	allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = testTrainSplit)

	#Train algorithm
	classifier = SVC(kernel=kernel)
	classifier.fit(allDataTrain, resultTrain)

	#Make predictions
	predictions = list(classifier.predict(allDataTest))
	resultTest = list(resultTest)

	totalF1 = totalF1 + sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')
	totalAcc = totalAcc + sklearn.metrics.accuracy_score(resultTest, predictions)
	

#show results
print("\n\n\nFeatures selected are " + str(returnedInts))
print("Average F1 across " + str(numberOfRuns) +" runs is " + str(totalF1/numberOfRuns))
print("Running accuracy across " + str(numberOfRuns) +" runs is " + str(totalAcc/numberOfRuns))
