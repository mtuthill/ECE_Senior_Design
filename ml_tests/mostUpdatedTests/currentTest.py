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

numFeatures = 17

df = pandas.read_csv('dataFrameWithEnvFeat.csv')
returned = pymrmr.mRMR(df, "MIQ", 7)
returnedInts = [int(i) for i in returned]

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[numFeatures]]

#Split test and training sets
allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.2)

#scale data
#scaler = StandardScaler()
#scaler.fit(allDataTrain)
#allDataTrain = scaler.transform(allDataTrain)
#allDataTest = scaler.transform(allDataTest)

#training
classifierSVM = SVC(kernel='linear')
classifierSVM.fit(allDataTrain, resultTrain)
classifierKNN = KNeighborsClassifier(n_neighbors=5)
classifierKNN.fit(allDataTrain, resultTrain)

#Make predictions
predictionsSVM = list(classifierSVM.predict(allDataTest))
predictionsKNN = list(classifierKNN.predict(allDataTest))
resultTest = list(resultTest)

print(resultTest)
print(predictionsSVM)
print(predictionsKNN)

#show results
print("\n\nSVM=")
print(sklearn.metrics.f1_score(resultTest, predictionsSVM, average = 'binary'))
print("\n\nKNN=")
print(sklearn.metrics.f1_score(resultTest, predictionsKNN, average = 'binary'))
