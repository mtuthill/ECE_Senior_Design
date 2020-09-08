import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

def classify(type):
    #Import dataset
    radarData = pd.read_csv("../ml_tests/fall_non_fall_test.csv")

    #Data preprocessing
    X_train = radarData.drop('Class', axis = 1)
    y_train = radarData['Class']

    if (type == "Support Vector Machine"):
        #Train algorithm
        classifier = SVC(kernel='linear')
        classifier.fit(X_train, y_train)

        #Data to classify
        to_classify = [[1.4, 150, 4]]
    elif (type == "K Nearest Neighbor"):
        #scale data
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)

        #training
        classifier = KNeighborsClassifier(n_neighbors=5)
        classifier.fit(X_train, y_train)

        #Data to classify
        to_classify = [[0.5, 100, 1.4]]
        to_classify = scaler.transform(to_classify)

    #Make predictions
    y_pred = classifier.predict(to_classify)
    return y_pred[0]