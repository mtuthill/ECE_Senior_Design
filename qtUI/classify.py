import numpy as np
import pandas as pd
import sklearn
import joblib
import time
import matlab.engine
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from keras.models import load_model
from keras.preprocessing import image

import ftpAccess
from ftplib import FTP

def classify(type, binAllClass, file):
    eng = matlab.engine.start_matlab()
    specfile = "out_spectrogram.png"
    eng.microDoppler_AWR1642_bulk_BPM(file, specfile, nargout=0)
    if (type == "Support Vector Machine"):
        if (binAllClass == "Binary"):
            classifier = joblib.load("storedBinarySVM.sav")
        else:
            classifier = joblib.load("storedSVM_allClass.sav")

    elif (type == "K Nearest Neighbor"):
        if (binAllClass == "Binary"):
            classifier = joblib.load("storedKNN.sav")
        else:
            classifier = joblib.load("storedKNN_allClass.sav")

    elif (type == "Convolutional Neural Network"):
        if (binAllClass == "Binary"):
            model = load_model('storedBinaryCNN.h5')
        else:
            model = load_model('storedAllClassCNN.h5')
        print("Model loaded")

        eng.microDoppler_AWR1642_bulk_BPM(file, specfile, nargout=0)
        test_image = image.load_img(specfile, color_mode ='rgb', target_size = (224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = model.predict(test_image)
        res = np.argmax(result)

        dictAllClass = {0 : 'fallingSitting', 1: 'fallingStanding', 2: 'fallingWalking', 3: 'movement', 4: 'sitting', 5 : 'walkingData'}
        dictBinary = {0 : 'nonFall', 1: 'fall'}

        if (binAllClass == "Binary"):
            resultNum = dictBinary[res]
        else:
            resultNum = dictAllClass[res]

        print("The predicted output is : ", resultNum)

        #write file
        filename = "classificationInfo.txt"
        classInfoFile = open(filename, "w")
        classInfoFile.write("1\n")
        classInfoFile.write(str(res) + '\n')
        classInfoFile.write(str(binAllClass))
        classInfoFile.close()

        #Send info to ftp
        ftp = FTP('192.168.10.199')     #192.168.10.199 -wavlink
        ftp.login(user='pi', passwd = 'radar')
        ftpAccess.uploadFileToServer(ftp, filename, "~/ftp/files", filename)
        ftp.quit()

        os.remove(filename)

        return res

    if (type == "Support Vector Machine"):
        h = open('featuresSVM.txt', 'r')
    else:
        h = open('featuresKNN.txt', 'r')
    numDCTFeatures = 10
    features = eng.spectrogramToFeatures(specfile, 1, 1, 1, numDCTFeatures)

    #use only the features selected from classifier
    listofFeatures = []
    content = h.readlines()
    for line in content:
        listofFeatures.append(int(line))

    selectedFeaturesList = [features[0][i] for i in listofFeatures]
    selectedFeatures = [selectedFeaturesList]

    #get classification result
    result = classifier.predict(selectedFeatures)

    #write file
    filename = "classificationInfo.txt"
    classInfoFile = open(filename, "w")
    classInfoFile.write("1\n")
    classInfoFile.write(str(result[0]) + '\n')
    classInfoFile.write(str(binAllClass))
    classInfoFile.close()

    #Send info to ftp
    ftp = FTP('192.168.10.199')
    ftp.login(user='pi', passwd = 'radar')
    ftpAccess.uploadFileToServer(ftp, filename, "~/ftp/files", filename)
    ftp.quit()

    os.remove(filename)

    return result
