import pandas
import sklearn
import joblib
import time
import matlab.engine
import pymrmr

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

eng = matlab.engine.start_matlab()
features = eng.featuresFromSpec("rainyDay.png", 10)
h = open('featuresSelected.txt', 'r')
numDCTFeatures = 10
listofFeatures = []
content = h.readlines()
for line in content:
	listofFeatures.append(int(line))
selectedFeaturesList = [features[0][i] for i in listofFeatures]
selectedFeatures = [selectedFeaturesList]

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[numFeatures]]

#training
classifierSVM = SVC(kernel='linear')
classifierSVM.fit(dfFeatureSelectedData, dfFeatureSelectedResults)
classifierKNN = KNeighborsClassifier(n_neighbors=5)
classifierKNN.fit(dfFeatureSelectedData, dfFeatureSelectedResults)

#Make predictions
predictionsSVM = list(classifierSVM.predict(selectedFeatures))
predictionsKNN = list(classifierKNN.predict(selectedFeatures))

print(predictionsSVM)
print(predictionsKNN)