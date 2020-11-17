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
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

#get filenames for data
names = ['GraceSpecsNew', 'MarcSpecsNew', 'PeteSpecsNew', 'CharlesSpecsNew']
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
numDCTFeatures = 10
totalNumFeatures = 21
totalNumFeaturesToSelectSVM = 12
totalNumFeaturesToSelectKNN = 12

for file in fallingSittingFiles:
	fallingSittingData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())

for file in fallingStandingFiles:
	fallingStandingData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())
    
for file in fallingWalkingFiles:
	fallingWalkingData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())

for file in movementFiles:
	movementData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())
    
for file in sittingFiles:
	sittingData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())

for file in walkingFiles:
	walkingData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())
    
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

#prepare data for feature selection
#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = []
for i in range(totalNumFeatures):
	colNames.append(str(i))
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)

#improved feature selection using mRMR
returnedMIQ = pymrmr.mRMR(df, "MIQ", totalNumFeaturesToSelectSVM)
returnedIntsMIQ = [int(i) for i in returnedMIQ]
returnedMID = pymrmr.mRMR(df, "MID", totalNumFeaturesToSelectKNN)
returnedIntsMID = [int(i) for i in returnedMID]

df.insert(totalNumFeatures, "Classes", results)

#get data after feature selected
dfFeatureSelectedDataSVM = df[df.columns[returnedIntsMIQ]]
dfFeatureSelectedResults = df[df.columns[totalNumFeatures]]

dfFeatureSelectedDataKNN = df[df.columns[returnedIntsMID]]

#scale data
scaler = StandardScaler()
scaler.fit(dfFeatureSelectedDataKNN)
KNNdata = scaler.transform(dfFeatureSelectedDataKNN)

classifierKNN = KNeighborsClassifier(5)
classifierKNN.fit(KNNdata, dfFeatureSelectedResults)

classifierSVM = SVC(kernel="linear")
classifierSVM.fit(dfFeatureSelectedDataSVM, dfFeatureSelectedResults)

filenameSVM = "storedTestSVM_allClass.sav"
filenameKNN = "storedTestKNN_allClass.sav"
joblib.dump(classifierSVM, filenameSVM)
joblib.dump(classifierKNN, filenameKNN)