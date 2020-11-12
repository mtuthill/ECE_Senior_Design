import sys
import os
import matlab.engine
import sklearn.metrics
import numpy
import joblib
import pandas
import pymrmr
import time

from os import listdir
from os.path import isfile, join
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

#get filenames for data
names = ['Grace', 'Marc', 'Pete']
fallSubdirs = ['fallingSitting', 'fallingStanding', 'fallingWalking']
nonFallSubdirs = ['Movement', 'Sitting', 'Walking']

#get filenames for DataFrame
path = "../../ECE_Senior_Design_Our_Data"
fallFiles = []
nonFallFiles = []
for name in names:
	for fallDir in fallSubdirs:
		fallFiles = fallFiles + [(path + "/"  + name + "/" + fallDir + "/" + f) for f in listdir(join(path, name, fallDir)) if isfile(join(path, name, fallDir, f))]
	for nonFallDir in nonFallSubdirs:
		nonFallFiles = nonFallFiles + [(path + "/"  + name + "/" + nonFallDir + "/" + f) for f in listdir(join(path, name, nonFallDir)) if isfile(join(path, name, nonFallDir, f))]

#get spectrograms and get features from spectrograms
eng = matlab.engine.start_matlab()

for file in nonFallFiles:
	print(file)
	base = os.path.splitext(file)[0]
	if "Grace" in base:
		outfile = base.replace("Grace", "GraceSpecs") + ".png"
	elif "Pete" in base:
		outfile = base.replace("Pete", "PeteSpecs") + ".png"
	elif "Marc" in base:
		outfile = base.replace("Marc", "MarcSpecs") + ".png"
	print(outfile)
	eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
for file in fallFiles:
	print(file)
	base = os.path.splitext(file)[0]
	if "Grace" in base:
		outfile = base.replace("Grace", "GraceSpecs") + ".png"
	elif "Pete" in base:
		outfile = base.replace("Pete", "PeteSpecs") + ".png"
	elif "Marc" in base:
		outfile = base.replace("Marc", "MarcSpecs") + ".png"
	eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
    

eng.quit()    
