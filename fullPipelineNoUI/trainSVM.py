import sys
import os
import matlab.engine
import sklearn.metrics
import numpy
import joblib
import pymrmr
import pandas

from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_selection import GenericUnivariateSelect

#get filenames for spectrograms
pathOne = "../../ECE_Senior_Design_Data/nonFallSpectrograms/0_Walking_towards_radar/"
filesOne = [f for f in listdir(pathOne) if isfile(join(pathOne, f))]

pathTwo = "../../ECE_Senior_Design_Data/nonFallSpectrograms/2_picking_up_an_object/"
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

#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = []
for i in range(10):
	colNames.append(str(i + 1))
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)
df.insert(0, "Classes", results)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, "MIQ", 3)
returnedInts = [int(i) for i in returned]

#write ints to file that show what features are being used
with open('featuresSelected.txt', 'w') as f:
    for item in returnedInts:
        f.write("%s\n" % item)

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[0]]

#Train algorithm
classifier = SVC(kernel='linear')
classifier.fit(dfFeatureSelectedData, dfFeatureSelectedResults)

#save classifier
filename = "stored_mRMR_SVM.sav"
joblib.dump(classifier, filename)
