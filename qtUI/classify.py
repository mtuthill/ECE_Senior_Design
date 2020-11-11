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
from keras.models import load_model
from keras.preprocessing import image

def f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

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

    elif (type == "Convolutional Neural Network"):
        if (binAllClass == "Binary"):
            model = load_model('binaryModel.h5')
        else:
            model = load_model('allClassModel.h5')

        specfile = "out_spectrogram.png"
        eng.microDoppler_AWR1642_bulk_BPM(file, specfile, nargout=0)
        test_image = image.load_img(specfile, color_mode ='rgb', target_size = (224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = model.predict(test_image)
        training_set.class_indices
        print(result)
        res = np.argmax(result)

        dictAllClass = {0 : 'fallingSitting', 1: 'fallingStanding', 2: 'fallingWalking', 3: 'movement', 4: 'sitting', 5 : 'walkingData'}
        dictBinary = {0 : 'nonFall', 1: 'fall'}

        if (binAllClass == "Binary"):
            result = dictBinary[res]
        else:
            result = dictAllClass[res]

        print("The predicted output is : ", result)
        return result

    if (binAllClass == "Binary"):
        h = open('featuresSelected.txt', 'r')
    elif (type == "K Nearest Neighbor"):
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
