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

#split into test/train
allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(allData, results, test_size = 0.25)

#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = ["Cos1", "Cos2", "Cos3", "Cos4", "Cos5", "Cos6", "Cos7", "Cos8", "Cos9", "Cos10"]
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)
df.insert(0, "Classes", results)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, "MIQ", 3)
print(returned)

#feature selection (keep 30% of features)
#trans = GenericUnivariateSelect(score_func=lambda X, y: X.mean(axis=0), mode='percentile', param=30)
#allDataTrans = trans.fit_transform(allData, results)

#Train algorithm
classifier = SVC(kernel='linear')
classifier.fit(allDataTrain, resultTrain)

#Make predictions
#predictions = classifier.predict(allDataTest)

#write classifier
#filename = "storedTestSVM.sav"
#joblib.dump(classifier, filename)
