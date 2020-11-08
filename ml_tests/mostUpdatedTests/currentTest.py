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

numFeaturesToSel = [1,2,3,4,5,6,7]

for j in numFeaturesToSel:
	returned = pymrmr.mRMR(df, "MIQ", numFeaturesToSel[j-1])
	returnedInts = [int(i) for i in returned]

	#get data after feature selected
	dfFeatureSelectedData = df[df.columns[returnedInts]]
	dfFeatureSelectedResults = df[df.columns[numFeatures]]

	KNNtot = 0
	SVMtot = 0
	for i in range(100):
		allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.25)

		#training
		classifierSVM = SVC(kernel='linear')
		classifierSVM.fit(allDataTrain, resultTrain)
		classifierKNN = KNeighborsClassifier(n_neighbors=5)
		classifierKNN.fit(allDataTrain, resultTrain)

		#Make predictions
		predictionsSVM = list(classifierSVM.predict(allDataTest))
		predictionsKNN = list(classifierKNN.predict(allDataTest))
		resultTest = list(resultTest)

		SVMtot = SVMtot + sklearn.metrics.f1_score(resultTest, predictionsSVM, average = 'binary')
		KNNtot = KNNtot + sklearn.metrics.f1_score(resultTest, predictionsKNN, average = 'binary')
		f = open("resultsEnv_updated.txt", "a")
	f.write("SVM - Features: " + str(numFeaturesToSel[j-1]) + " - " + str(SVMtot / 100) + '\n')
	f.write("KNN - Features: " + str(numFeaturesToSel[j-1]) + " - " + str(KNNtot / 100) + '\n')
	f.close()
