import numpy as np
import pandas as pd
import sklearn
import joblib
import time
import matlab.engine

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

def classify(type, binAllClass, file):
    eng = matlab.engine.start_matlab()
    if (type == "Support Vector Machine"):
        if (binAllClass == "Binary"):
            classifier = joblib.load("storedTestSVM.sav")
        else:
            classifier = joblib.load("storedTestSVM_allClass.sav")

    elif (type == "K Nearest Neighbor"):
        if (binAllClass == "Binary"):
            classifier = joblib.load("storedTestKNN.sav")
        else:
            classifier = joblib.load("storedTestKNN_allClass.sav")

    if (binAllClass == "Binary"):
        h = open('featuresSelected.txt', 'r')
    else:
        h = open('featuresSelectedAllClass.txt', 'r')
    numDCTFeatures = 10
    outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
    features = eng.binToDct(file, outfile, numDCTFeatures)

    #use only the features selected from classifier
    listofFeatures = []
    content = h.readlines()
    for line in content:
        listofFeatures.append(int(line))

    selectedFeaturesList = [features[0][i] for i in listofFeatures]
    selectedFeatures = [selectedFeaturesList]

    #get classification result
    result = classifier.predict(selectedFeatures)
    return result
