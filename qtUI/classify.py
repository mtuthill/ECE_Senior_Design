import numpy as np
import pandas as pd
import sklearn
import joblib
import time
#import matlab.engine

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

def classify(type, file):
    eng = matlab.engine.start_matlab()
    if (type == "Support Vector Machine"):
        #load classifier
        classifier = joblib.load("storedTestSVM.sav")

        #Data to classify
        file = "fallExample.bin"

    elif (type == "K Nearest Neighbor"):
        #load classifier
        classifier = joblib.load("storedTestKNN.sav")

        #Data to classify
        file = "nonFallExample.bin"

    h = open('featuresSelected.txt', 'r')
    numDCTFeatures = 10
    outfile = 'out_spectrogram.png'
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
