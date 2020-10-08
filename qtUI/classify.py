import numpy as np
import pandas as pd
import sklearn
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

def classify(type):
    if (type == "Support Vector Machine"):
        #load classifier
        classifier = joblib.load("storedTestSVM.sav")

        #Data to classify
        to_classify = [[1.4, 150, 4]]
    elif (type == "K Nearest Neighbor"):
        #load classifier
        classifier = joblib.load("storedTestKNN.sav")
        scaler = joblib.load("storedTestKNNScaler.pkl")

        #Data to classify
        to_classify = [[0.5, 100, 1.4]]
        to_classify = scaler.transform(to_classify)

    #Make predictions
    y_pred = classifier.predict(to_classify)
    return y_pred[0]
