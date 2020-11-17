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
numDCTFeatures = 10
totalNumFeatures = 21
totalNumFeaturesToSelectSVM = 12
totalNumFeaturesToSelectKNN = 12

for file in nonFallFiles:
	print(file)
	nonFallData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())
for file in fallFiles:
	print(file)
	fallData.append(numpy.array(eng.spectrogramToFeatures(file, 1, 1, 1, numDCTFeatures)).tolist())
    

eng.quit()    

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
nonFallData = [item for sublist in nonFallData for item in sublist]
fallData = [item for sublist in fallData for item in sublist]

#combine to form all data
allData = nonFallData + fallData

#make classification list
results = [0] * len(nonFallData) + [1] * len(fallData)

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

classifierKNN = KNeighborsClassifier(17)
classifierKNN.fit(KNNdata, dfFeatureSelectedResults)

classifierSVM = SVC(kernel="linear")
classifierSVM.fit(dfFeatureSelectedDataSVM, dfFeatureSelectedResults)

filenameSVM = "storedTestSVM.sav"
filenameKNN = "storedTestKNN.sav"
joblib.dump(classifierSVM, filenameSVM)
joblib.dump(classifierKNN, filenameKNN)