import sys
import os
import matlab.engine
import sklearn.metrics
import numpy
import joblib
import pandas
import pymrmr

from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

#get filenames for spectrograms
pathOne = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/0_Walking_towards_radar/"
filesOne = [f for f in listdir(pathOne) if isfile(join(pathOne, f))]

pathTwo = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/2_picking_up_an_object/"
filesTwo = [f for f in listdir(pathTwo) if isfile(join(pathTwo, f))]

#get features from spectrograms
eng = matlab.engine.start_matlab()
dataOne = []
dataTwo = []
for file in filesOne:
    dataOne.append(numpy.array(eng.dctFromPng(pathOne + file)).tolist())

for file in filesTwo:
    dataTwo.append(numpy.array(eng.dctFromPng(pathTwo + file)).tolist())

eng.quit()    

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
dataTwo = [item for sublist in dataTwo for item in sublist]
dataOne = [item for sublist in dataOne for item in sublist]

#combine to form all data
allData = dataTwo + dataOne

#make classification list
results = [0] * len(dataTwo) + [1] * len(dataOne)

#feature selection (keep 3 of 10 features)
#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = []
for i in range(500):
	colNames.append(str(i))
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)
df.insert(0, "Classes", results)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, "MID", 3)
returnedInts = [int(i) for i in returned]

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[0]]

#Split test and training sets
allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.3, random_state=42)

#Train algorithm
classifier = SVC(kernel='linear')
classifier.fit(allDataTrain, resultTrain)

#Make predictions
predictions = list(classifier.predict(allDataTest))
resultTest = list(resultTest)

#show results
print(sklearn.metrics.f1_score(resultTest, predictions, average = 'binary'))