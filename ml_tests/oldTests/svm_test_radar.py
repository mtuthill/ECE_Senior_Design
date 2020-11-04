from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import sklearn.metrics

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

f1_total = 0
num_passes = 500

for x in range(num_passes):

    #Import dataset
    radarData = pd.read_csv("fall_non_fall_test.csv")
    #radarData = pd.read_csv("bill_authentication.csv")

    #Data preprocessing
    # Class = 1 signifies fall event
    X = radarData.drop('Class', axis = 1)
    y = radarData['Class']

    #Divide into test and training sets. 80% to train, 20% to test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

    #Train algorithm
    svclassifier = SVC(kernel='linear')
    svclassifier.fit(X_train, y_train)

    #Make predictions
    y_pred = svclassifier.predict(X_test)

    #Evaluate algorithm
    #print(sklearn.metrics.confusion_matrix(y_test, y_pred))
    #print(sklearn.metrics.classification_report(y_test, y_pred))
    #print("f1 = ", sklearn.metrics.f1_score(y_test, y_pred, average = 'binary'))
    f1_total += sklearn.metrics.f1_score(y_test, y_pred, average = 'binary')

print("average f1 score in " + repr(num_passes) + " passes = ", f1_total / num_passes)
