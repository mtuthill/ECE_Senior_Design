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
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

import matplotlib.pyplot as plt

#CHANGE THESE AS NEEDED
##################################
numDCTFeatures = 10
dctFeaturesFlag = 1
envFeaturesFlag = 0
physFeaturesFlag = 1
numFeaturesToSelect = 2
mRMRType = "MIQ"			#Has to be "MIQ" or "MID"
testTrainSplit = 0.1		#Default is 0.3
kernel = "linear"			#Default is linear, can be "linear", "poly", "rbf", "sigmoid"
numberOfRuns = 50			#Default it 50
##################################

#get filenames for data
names = ['GraceSpecs', 'MarcSpecs', 'PeteSpecs']
fallSubdirs = ['fallingSitting', 'fallingStanding', 'fallingWalking']
nonFallSubdirs = ['Movement', 'Sitting', 'Walking']

#get filenames for DataFrame
path = "../../../ECE_Senior_Design_Our_Data"
fallFiles = []
nonFallFiles = []
for name in names:
	for fallDir in fallSubdirs:
		fallFiles = fallFiles + [(path + "/"  + name + "/" + fallDir + "/" + f) for f in listdir(join(path, name, fallDir)) if isfile(join(path, name, fallDir, f))]
	for nonFallDir in nonFallSubdirs:
		nonFallFiles = nonFallFiles + [(path + "/"  + name + "/" + nonFallDir + "/" + f) for f in listdir(join(path, name, nonFallDir)) if isfile(join(path, name, nonFallDir, f))]

#get spectrograms and get features from spectrograms
eng = matlab.engine.start_matlab()
fallData = []
nonFallData = []

for file in nonFallFiles:
	nonFallData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
for file in fallFiles:
	fallData.append(numpy.array(eng.spectrogramToFeatures(file, dctFeaturesFlag, envFeaturesFlag, physFeaturesFlag, numDCTFeatures)).tolist())
    

eng.quit()    

#Fixing data. Was [[[list], [list]]] now is [[list], [list]]
nonFallData = [item for sublist in nonFallData for item in sublist]
fallData = [item for sublist in fallData for item in sublist]

#combine to form all data
allData = nonFallData + fallData

#make classification list
results = [0] * len(nonFallData) + [1] * len(fallData)

#find total number of features
numFeatures = 0
if dctFeaturesFlag == 1:
	numFeatures = numFeatures + numDCTFeatures
if envFeaturesFlag == 1:
	numFeatures = numFeatures + 7
if physFeaturesFlag == 1:
	numFeatures = numFeatures + 4

#prepare data for feature selection
numpyArrayofArrays = numpy.array([numpy.array(xi) for xi in allData])
colNames = []
for i in range(numFeatures):
	colNames.append(str(i))
df = pandas.DataFrame(data = numpyArrayofArrays, index = None, columns = colNames)

#improved feature selection using mRMR
returned = pymrmr.mRMR(df, mRMRType, numFeaturesToSelect)
returnedInts = [int(i) for i in returned]

df.insert(numFeatures, "Classes", results)

#get data after feature selected
dfFeatureSelectedData = df[df.columns[returnedInts]]
dfFeatureSelectedResults = df[df.columns[numFeatures]]

h = 0.2

svc = SVC(kernel='linear').fit(dfFeatureSelectedData, dfFeatureSelectedResults)
rbf_svc = SVC(kernel='rbf', gamma=0.7).fit(dfFeatureSelectedData, dfFeatureSelectedResults)
poly_svc = SVC(kernel='poly', degree=3).fit(dfFeatureSelectedData, dfFeatureSelectedResults)
sig_svc = SVC(kernel = 'sigmoid', gamma=2).fit(dfFeatureSelectedData, dfFeatureSelectedResults)

dfFeatureSelectedDataNum0 = pandas.to_numeric(dfFeatureSelectedData["10"])
dfFeatureSelectedDataNum1 = pandas.to_numeric(dfFeatureSelectedData["8"])


x_min, x_max = dfFeatureSelectedDataNum0.min() - 1, dfFeatureSelectedDataNum0.max() + 1
y_min, y_max = dfFeatureSelectedDataNum1.min() - 1, dfFeatureSelectedDataNum1.max() + 1
xx, yy = numpy.meshgrid(numpy.arange(x_min, x_max, h),
                     numpy.arange(y_min, y_max, h))

titles = ['SVM with Linear Kernel',
          'SVM with RBF Kernel',
          'SVM with Polynomial (degree 3) Kernel',
          'SVM with Sigmoid Kernel']

for i, clf in enumerate((svc, rbf_svc, poly_svc, sig_svc)):
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    plt.subplot(2, 2, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(numpy.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot also the training points
    plt.scatter(dfFeatureSelectedDataNum0, dfFeatureSelectedDataNum1, c=results, cmap=plt.cm.coolwarm)
    plt.xlabel('10th DCT Coefficient')
    plt.ylabel('8th DCT Coefficient')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])

plt.show()