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

numFeatures = 500

#get data from csv
df = pandas.read_csv('dataFrameAllClass.csv')
totalF1 = 0

for i in range(100):
	#improved feature selection using mRMR
	returned = pymrmr.mRMR(df, "MIQ", 4)
	returnedInts = [int(i) for i in returned]
	
	#get data after feature selected
	dfFeatureSelectedData = df[df.columns[returnedInts]]
	dfFeatureSelectedResults = df[df.columns[numFeatures]]

	#Split test and training sets
	allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.3)

	#Train algorithm
	classifier = SVC(kernel='linear')
	classifier.fit(allDataTrain, resultTrain)

	#Make predictions
	predictions = list(classifier.predict(allDataTest))
	resultTest = list(resultTest)

	#show results
	totalF1 = totalF1 + sklearn.metrics.f1_score(resultTest, predictions, average = 'weighted')

print("SVM - MIQ - " + str(totalF1 / 100))