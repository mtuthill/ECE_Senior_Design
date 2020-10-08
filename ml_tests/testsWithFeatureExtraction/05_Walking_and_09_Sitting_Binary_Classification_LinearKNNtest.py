import sys
import os
import matlab.engine
import sklearn.metrics
import numpy as np

from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

#get filenames for spectrograms
pathWalking = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/05_Walking_towards_radar/"
onlyfilesWalking = [f for f in listdir(pathWalking) if isfile(join(pathWalking, f))]

pathSitting = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/09_Sitting/"
onlyfilesSitting = [f for f in listdir(pathSitting) if isfile(join(pathSitting, f))]

#get features from spectrograms
eng = matlab.engine.start_matlab()
walkingData = []
sittingData = []
for file in onlyfilesWalking:
    walkingData.append(np.array(eng.dctFromPng(pathWalking + file)).tolist())

for file in onlyfilesSitting:
    sittingData.append(np.array(eng.dctFromPng(pathSitting + file)).tolist())

eng.quit()    

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
sittingData = [item for sublist in sittingData for item in sublist]
walkingData = [item for sublist in walkingData for item in sublist]

#combine to form all data
allData = sittingData + walkingData

#make classification list
results = [0] * len(sittingData) + [1] * len(walkingData)

f1_total = 0

for x in range(500):
	#Split test and training sets
	allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(allData, results, test_size = 0.25)

	#feature scaling
	scaler = StandardScaler()
	scaler.fit(allDataTrain)

	allDataTrain = scaler.transform(allDataTrain)
	allDataTest = scaler.transform(allDataTest)

	#Train algorithm
	classifier = KNeighborsClassifier(n_neighbors=5)
	classifier.fit(allDataTrain, resultTrain)

	#Make predictions
	predictions = classifier.predict(allDataTest)

	f1_total += sklearn.metrics.f1_score(resultTest, predictions, average = 'binary')

print("average f1 score in " + repr(500) + " passes = ", f1_total / 500)

#print results
#print(sklearn.metrics.confusion_matrix(resultTest, predictions))
#print(sklearn.metrics.classification_report(resultTest, predictions))
#print("f1 = ", sklearn.metrics.f1_score(resultTest, predictions, average = 'binary'))