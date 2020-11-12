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
numFeaturesToSelect = 1
mRMRType = "MIQ"			#Has to be "MIQ" or "MID"
testTrainSplit = 0.3		#Default is 0.3
kernel = "linear"			#Default is linear, can be "linear", "poly", "rbf", "sigmoid"
numberOfRuns = 50			#Default it 50
##################################

names = ['GraceSpecs', 'MarcSpecs', 'PeteSpecs']
subDirs = ['fallingSitting', 'fallingStanding', 'fallingWalking', 'Movement', 'Sitting', 'Walking']

#get filenames for data
path = "../../ECE_Senior_Design_Our_Data"
fallingSittingFiles = []
fallingStandingFiles = []
fallingWalkingFiles = []
movementFiles = []
sittingFiles = []
walkingFiles = []

for name in names:
	fallingSittingFiles = fallingSittingFiles + [(path + "/"  + name + "/" + subDirs[0] + "/" + f) for f in listdir(join(path, name, subDirs[0])) if isfile(join(path, name, subDirs[0], f))]
	fallingStandingFiles = fallingStandingFiles + [(path + "/"  + name + "/" + subDirs[1] + "/" + f) for f in listdir(join(path, name, subDirs[1])) if isfile(join(path, name, subDirs[1], f))]
	fallingWalkingFiles = fallingWalkingFiles + [(path + "/"  + name + "/" + subDirs[2] + "/" + f) for f in listdir(join(path, name, subDirs[2])) if isfile(join(path, name, subDirs[2], f))]
	movementFiles = movementFiles + [(path + "/"  + name + "/" + subDirs[3] + "/" + f) for f in listdir(join(path, name, subDirs[3])) if isfile(join(path, name, subDirs[3], f))]
	sittingFiles = sittingFiles + [(path + "/"  + name + "/" + subDirs[4] + "/" + f) for f in listdir(join(path, name, subDirs[4])) if isfile(join(path, name, subDirs[4], f))]
	walkingFiles = walkingFiles + [(path + "/"  + name + "/" + subDirs[5] + "/" + f) for f in listdir(join(path, name, subDirs[5])) if isfile(join(path, name, subDirs[5], f))]


#get spectrograms and get features from spectrograms
eng = matlab.engine.start_matlab()
fallingSittingData = []
fallingStandingData = []
fallingWalkingData = []
movementData = []
sittingData = []
walkingData = []

for file in fallingSittingFiles:
	fallingSittingData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())

for file in fallingStandingFiles:
	fallingStandingData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
    
for file in fallingWalkingFiles:
	fallingWalkingData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())

for file in movementFiles:
	movementData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
    
for file in sittingFiles:
	sittingData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())

for file in walkingFiles:
	walkingData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
    
eng.quit()    
  

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
fallingSittingData = [item for sublist in fallingSittingData for item in sublist]
fallingStandingData = [item for sublist in fallingStandingData for item in sublist]
fallingWalkingData = [item for sublist in fallingWalkingData for item in sublist]
movementData = [item for sublist in movementData for item in sublist]
sittingData = [item for sublist in sittingData for item in sublist]
walkingData = [item for sublist in walkingData for item in sublist]

#combine to form all data
allData = fallingSittingData + fallingStandingData + fallingWalkingData + movementData + sittingData + walkingData

#make classification list
results = [0] * len(fallingSittingData) + [1] * len(fallingStandingData) + [2] * len(fallingWalkingData) + [3] * len(movementData) + [4] * len(sittingData) + [5] * len(walkingData)

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
	if (kernel == "poly"):
		classifier = SVC(kernel=kernel, degree=3)
	else:
		classifier = SVC(kernel=kernel)

	classifier.fit(allDataTrain, resultTrain)

	#Make predictions
	predictions = list(classifier.predict(allDataTest))
	resultTest = list(resultTest)

	totalF1 = totalF1 + sklearn.metrics.f1_score(resultTest, predictions, average = 'weighted')
	totalAcc = totalAcc + sklearn.metrics.accuracy_score(resultTest, predictions)
	

#show results
print("\n\n\nFeatures selected are " + str(returnedInts))
print("Average F1 across " + str(numberOfRuns) +" runs is " + str(totalF1/numberOfRuns))
print("Running accuracy across " + str(numberOfRuns) +" runs is " + str(totalAcc/numberOfRuns))
