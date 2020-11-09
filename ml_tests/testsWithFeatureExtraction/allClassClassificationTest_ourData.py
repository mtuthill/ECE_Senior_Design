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
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

#get filenames for data
names = ['Grace', 'Marc', 'Pete']
subDirs = ['fallingSitting', 'fallingStanding', 'fallingWalking', 'Movement', 'Sitting', 'Walking']

#get filenames for data
path = "../../../ECE_Senior_Design_Our_Data"
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
numFeatures = 10
totalFeatures = numFeatures + 7

for file in fallingSittingFiles:
	print(file)
	fallingSittingData.append(numpy.array(eng.binToDct(file, "outfile.png", numFeatures)).tolist())

for file in fallingStandingFiles:
	print(file)
	fallingStandingData.append(numpy.array(eng.binToDct(file, "outfile.png", numFeatures)).tolist())
    
for file in fallingWalkingFiles:
	print(file)
	fallingWalkingData.append(numpy.array(eng.binToDct(file, "outfile.png", numFeatures)).tolist())

for file in movementFiles:
	print(file)
	movementData.append(numpy.array(eng.binToDct(file, "outfile.png", numFeatures)).tolist())
    
for file in sittingFiles:
	print(file)
	sittingData.append(numpy.array(eng.binToDct(file, "outfile.png", numFeatures)).tolist())

for file in walkingFiles:
	print(file)
	walkingData.append(numpy.array(eng.binToDct(file, "outfile.png", numFeatures)).tolist())
    
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

#feature selection (keep 3 of 10 features)
#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = []
for i in range(totalFeatures):
	colNames.append(str(i))
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, "MIQ", 7)
returnedInts = [int(i) for i in returned]
print(returnedInts)
df.insert(totalFeatures, "Classes", results)
print(df)
df.to_csv(r'dataFrameAllClass.csv', index = False, header = True)

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[totalFeatures]]
print(dfFeatureSelectedData)
print(dfFeatureSelectedResults)

#Split test and training sets
allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.2)

#Train algorithm
classifier = SVC(kernel='linear')
classifier.fit(allDataTrain, resultTrain)

#Make predictions
predictions = list(classifier.predict(allDataTest))
resultTest = list(resultTest)

print(resultTest)
print(predictions)

#show results
print(sklearn.metrics.f1_score(resultTest, predictions, average = 'weighted'))