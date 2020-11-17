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
    if (type == "Support Vector Machine"):
        if (binAllClass == "Binary"):
            print("Bin SVM")
            classifier = joblib.load("storedTestSVM.sav")
        else:
            print("Multi SVM")
            classifier = joblib.load("storedTestSVM_allClass.sav")

    elif (type == "K Nearest Neighbor"):
        if (binAllClass == "Binary"):
            print("Bin KNN")
            classifier = joblib.load("storedTestKNN.sav")
        else:
            print("Multi KNN")
            classifier = joblib.load("storedTestKNN_allClass.sav")

    elif (type == "Convolutional Neural Network"):
        if (binAllClass == "Binary"):
            print("Binary CNN")
            model = load_model('binaryModel.h5')
        else:
            print("Multi CNN")
            model = load_model('allClassModel.h5')
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
        ftp = FTP('172.20.10.5')     #172.20.10.5 -wavlink
        ftp.login(user='pi', passwd = 'radar')
        ftpAccess.uploadFileToServer(ftp, filename, "~/ftp/files", filename)
        ftp.quit()

        os.remove(filename)

        return res

    if (binAllClass == "Binary"):
        h = open('featuresSelected.txt', 'r')
    else:
        h = open('featuresSelectedAllClass.txt', 'r')
    numDCTFeatures = 10
    features = eng.binToDct(file, specfile, numDCTFeatures)

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
    ftp = FTP('172.20.10.5')
    ftp.login(user='pi', passwd = 'radar')
    ftpAccess.uploadFileToServer(ftp, filename, "~/ftp/files", filename)
    ftp.quit()

    os.remove(filename)

    return result
