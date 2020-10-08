import sys
import os
import matlab.engine
import sklearn.metrics
import numpy as np

from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_selection import GenericUnivariateSelect


#get filenames for spectrograms
pathOne = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/05_Walking_towards_radar/"
filesOne = [f for f in listdir(pathOne) if isfile(join(pathOne, f))]

pathTwo = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/09_Sitting/"
filesTwo = [f for f in listdir(pathTwo) if isfile(join(pathTwo, f))]

#get features from spectrograms
eng = matlab.engine.start_matlab()
dataOne = []
dataTwo = []
for file in filesOne:
    dataOne.append(np.array(eng.dctFromPng(pathOne + file)).tolist())

for file in filesTwo:
    dataTwo.append(np.array(eng.dctFromPng(pathTwo + file)).tolist())

eng.quit()    

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
dataTwo = [item for sublist in dataTwo for item in sublist]
dataOne = [item for sublist in dataOne for item in sublist]

#combine to form all data
allData = dataTwo + dataOne

#make classification list
results = [0] * len(dataTwo) + [1] * len(dataOne)

#feature selection (keep 30% of features)
trans = GenericUnivariateSelect(score_func=lambda X, y: X.mean(axis=0), mode='percentile', param=30)
allDataTrans = trans.fit_transform(allData, results)


f1_total = 0

for x in range(500):

	#Split test and training sets
	allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(allDataTrans, results, test_size = 0.25)


	#Train algorithm
	classifier = SVC(kernel='linear')
	classifier.fit(allDataTrain, resultTrain)


	#Make predictions
	predictions = classifier.predict(allDataTest)

	f1_total += sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')

print("average f1 score in " + repr(500) + " passes = ", f1_total / 500)

#print results
#print(sklearn.metrics.confusion_matrix(resultTest, predictions))
#print(sklearn.metrics.classification_report(resultTest, predictions))
#print("f1 = ", sklearn.metrics.f1_score(resultTest, predictions, average = 'binary'))