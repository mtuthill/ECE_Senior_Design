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
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

numFeatures = 1000

#get data from csv
df = pandas.read_csv('dataFrame.csv')

numFeaturesSelect = [7, 8, 9, 10, 11, 12]
for j in numFeaturesSelect:
	totalF1SVMMIQ = 0
	for i in range(100):
		#improved feature selection using mRMR
		returned = pymrmr.mRMR(df, "MIQ", numFeaturesSelect[j-7])
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
		totalF1SVMMIQ = totalF1SVMMIQ + sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')

	f = open("results.txt", "a")
	f.write("SVM - MIQ - " + str(numFeaturesSelect[j-7]) + " - " + str(totalF1SVMMIQ / 100) + '\n')
	f.close()
	totalF1MIDSVM = 0
	for i in range(100):
		#improved feature selection using mRMR
		returned = pymrmr.mRMR(df, "MID", numFeaturesSelect[j-7])
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
		totalF1MIDSVM = totalF1MIDSVM + sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')
	f = open("results.txt", "a")
	f.write("SVM - MID - " + str(numFeaturesSelect[j-7]) + " - " + str(totalF1MIDSVM / 100) + '\n')
	totalF1KNNMIQ = 0
	f.close()
	for i in range(100):
		#improved feature selection using mRMR
		returned = pymrmr.mRMR(df, "MIQ", numFeaturesSelect[j-7])
		returnedInts = [int(i) for i in returned]

		#get data after feature selected
		dfFeatureSelectedData = df[df.columns[returnedInts]]
		dfFeatureSelectedResults = df[df.columns[numFeatures]]

		#Split test and training sets
		allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.3)

		#scale data
		scaler = StandardScaler()
		scaler.fit(allDataTrain)
		allDataTrain = scaler.transform(allDataTrain)
		allDataTest = scaler.transform(allDataTest)

		#training
		classifier = KNeighborsClassifier(n_neighbors=5)
		classifier.fit(allDataTrain, resultTrain)

		#Make predictions
		predictions = list(classifier.predict(allDataTest))
		resultTest = list(resultTest)

		#show results
		totalF1KNNMIQ = totalF1KNNMIQ + sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')
	f = open("results.txt", "a")
	f.write("KNN - MIQ - " + str(numFeaturesSelect[j-7]) + " - " + str(totalF1KNNMIQ / 100) + '\n')
	f.close()
	totalF1KNNMID = 0
	for i in range(100):
		#improved feature selection using mRMR
		returned = pymrmr.mRMR(df, "MID", numFeaturesSelect[j-7])
		returnedInts = [int(i) for i in returned]

		#get data after feature selected
		dfFeatureSelectedData = df[df.columns[returnedInts]]
		dfFeatureSelectedResults = df[df.columns[numFeatures]]

		#Split test and training sets
		allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.3)

		#scale data
		scaler = StandardScaler()
		scaler.fit(allDataTrain)
		allDataTrain = scaler.transform(allDataTrain)
		allDataTest = scaler.transform(allDataTest)

		#training
		classifier = KNeighborsClassifier(n_neighbors=5)
		classifier.fit(allDataTrain, resultTrain)

		#Make predictions
		predictions = list(classifier.predict(allDataTest))
		resultTest = list(resultTest)

		#show results
		totalF1KNNMID = totalF1KNNMID + sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')

	f = open("results.txt", "a")
	f.write("KNN - MID - " + str(numFeaturesSelect[j-7]) + " - " + str(totalF1KNNMID / 100) + '\n')
	f.close()