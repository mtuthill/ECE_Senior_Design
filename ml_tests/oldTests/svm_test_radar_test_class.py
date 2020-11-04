from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import sklearn.metrics

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Import dataset
radarData = pd.read_csv("fall_non_fall_test.csv")

#Data preprocessing
X_train = radarData.drop('Class', axis = 1)
y_train = radarData['Class']

#Train algorithm
svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

#Data to classify
to_classify = [[0.5, 100, 1.4], [1.4, 150, 4]]

#Make predictions
y_pred = svclassifier.predict(to_classify)
print("predictions are ", y_pred)