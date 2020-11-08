import sys
import os
import matlab.engine
import sklearn.metrics
import numpy
import joblib
import pandas
import pymrmr
import time

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

numFeatures = 17

df = pandas.read_csv('dataFrameWithEnvFeat_updatedSpec.csv')
returned = pymrmr.mRMR(df, "MIQ", 7)
returnedInts = [int(i) for i in returned]

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[numFeatures]]

#training
classifierSVM = SVC(kernel='linear')
classifierSVM.fit(dfFeatureSelectedData, dfFeatureSelectedResults)
classifierKNN = KNeighborsClassifier(n_neighbors=5)
classifierKNN.fit(dfFeatureSelectedData, dfFeatureSelectedResults)

filenameSVM = "storedTestSVM.sav"
filenameKNN = "storedTestKNN.sav"
joblib.dump(classifierSVM, filenameSVM)
joblib.dump(classifierKNN, filenameKNN)