import numpy as np
import pandas as pd
import sklearn
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

def trainTestSVM():
    print("SVM")
    #Import dataset
    radarData = pd.read_csv("../ml_tests/fall_non_fall_test.csv")

    #Data preprocessing
    X_train = radarData.drop('Class', axis = 1)
    y_train = radarData['Class']

    #Train algorithm
    classifier = SVC(kernel='linear')
    classifier.fit(X_train, y_train)

    #store
    filename = "storedTestSVM.sav"
    joblib.dump(classifier, filename)


def trainTestKNN():
    print("KNN")
    #Import dataset
    radarData = pd.read_csv("../ml_tests/fall_non_fall_test.csv")

    #Data preprocessing
    X_train = radarData.drop('Class', axis = 1)
    y_train = radarData['Class']

    #scale data
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)

    #training
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, y_train)

    filename = "storedTestKNN.sav"
    joblib.dump(classifier, filename)
    scalarFilename = "storedTestKNNScaler.pkl"
    joblib.dump(scaler, scalarFilename)


trainTestSVM()
trainTestKNN()

