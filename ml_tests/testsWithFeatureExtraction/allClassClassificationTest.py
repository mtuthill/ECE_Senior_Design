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
pathWalkingToward = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/0_Walking_towards_radar/"
filesWalkingToward = [f for f in listdir(pathWalkingToward) if isfile(join(pathWalkingToward, f))]

pathWalkingAway = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/1_walking_away_from_Radar/"
filesWalkingAway = [f for f in listdir(pathWalkingAway) if isfile(join(pathWalkingAway, f))]

pathPickingUp = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/2_picking_up_an_object/"
filesPickingUp = [f for f in listdir(pathPickingUp) if isfile(join(pathPickingUp, f))]

pathBending = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/3_bending/"
filesBending = [f for f in listdir(pathBending) if isfile(join(pathBending, f))]

pathSitting = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/4_sitting/"
filesSitting = [f for f in listdir(pathSitting) if isfile(join(pathSitting, f))]

pathKneeling = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/5_kneeling/"
filesKneeling = [f for f in listdir(pathKneeling) if isfile(join(pathKneeling, f))]

pathCrawling = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/6_crawling/"
filesCrawling = [f for f in listdir(pathCrawling) if isfile(join(pathCrawling, f))]

pathWalkingOnToes = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/7_Walking_on_both_toes/"
filesWalkingOnToes = [f for f in listdir(pathWalkingOnToes) if isfile(join(pathWalkingOnToes, f))]

pathLimping = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/8_limping_with_RL_Stiff/"
filesLimping = [f for f in listdir(pathLimping) if isfile(join(pathLimping, f))]

pathShortSteps = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/9_short_steps/"
filesShortSteps = [f for f in listdir(pathShortSteps) if isfile(join(pathShortSteps, f))]

pathScissorsGait = "../../../ECE_Senior_Design_Data/nonFallSpectrograms/10_scissors_gait/"
filesScissorsGait = [f for f in listdir(pathScissorsGait) if isfile(join(pathScissorsGait, f))]

listOfFileLists = [filesWalkingToward, filesWalkingAway, filesPickingUp, filesBending,
filesSitting, filesKneeling, filesCrawling, filesWalkingOnToes, filesLimping,
filesShortSteps, filesScissorsGait]

listOfFilePaths = [pathWalkingToward, pathWalkingAway, pathPickingUp, pathBending,
pathSitting, pathKneeling, pathCrawling, pathWalkingOnToes, pathLimping,
pathShortSteps, pathScissorsGait]

#get features from spectrograms
eng = matlab.engine.start_matlab()
data = []

#get dct values for all specs
i = 0
for fileList in listOfFileLists:
	for file in fileList:
		data.append(numpy.array(eng.dctFromPngZigzag(listOfFilePaths[i] + file)).tolist())
		print(listOfFilePaths[i] + file)
	i = i + 1

eng.quit()

#clean up
data = [item for sublist in data for item in sublist]

#get results
results = [0] * len(filesWalkingToward) + [1] * len(filesWalkingAway) + \
[2] * len(filesPickingUp) + [3] * len(filesBending) + [4] * len(filesSitting) + \
[5] * len(filesKneeling) + [6] * len(filesCrawling) + [7] * len(filesWalkingOnToes) + \
[8] * len(filesLimping) + [9] * len(filesShortSteps) + [10] * len(filesScissorsGait)

#feature selection (keep 3 of 10 features)
#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in data])
colNames = []
for i in range(500):
	colNames.append(str(i))
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)
df.insert(500, "Classes", results)
print(df)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, "MIQ", 10)
returnedInts = [int(i) for i in returned]
print(returnedInts)

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[500]]
print(dfFeatureSelectedData)
print(dfFeatureSelectedResults)

#Split test and training sets
allDataTrain, allDataTest, resultTrain, resultTest = train_test_split(dfFeatureSelectedData, dfFeatureSelectedResults, test_size = 0.3)

#Train algorithm
classifier = SVC(kernel='linear')
classifier.fit(allDataTrain, resultTrain)

#Make predictions
predictions = list(classifier.predict(allDataTest))
resultTest = list(resultTest)

print(resultTest)
print(predictions)

#show results
print(sklearn.metrics.f1_score(resultTest, predictions, average = 'weighted'))