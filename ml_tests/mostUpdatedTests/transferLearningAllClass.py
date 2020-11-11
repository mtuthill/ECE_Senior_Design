import os
import matlab.engine
import numpy as np
import time
from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split

import keras 
from keras.datasets import mnist
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Flatten
from keras import optimizers
from keras.models import Sequential
from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import keras.backend as K
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

def f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

#get filenames for data
names = ['Grace', 'Marc', 'Pete']
subDirs = ['fallingSitting', 'fallingStanding', 'fallingWalking', 'Movement', 'Sitting', 'Walking']

#get filenames for data
path = "../../../ECE_Senior_Design_Our_Data"
fallingSittingFiles = []
fallingStandingFiles = []
fallingWalkingFiles = []
movementFiles = []
sittingFiles = []
walkingFiles = []

for name in names:
  fallingSittingFiles = fallingSittingFiles + [(path + "/"  + name + "/" + subDirs[0] + "/" + f) for f in listdir(join(path, name, subDirs[0])) if isfile(join(path, name, subDirs[0], f))]
  fallingStandingFiles = fallingStandingFiles + [(path + "/"  + name + "/" + subDirs[1] + "/" + f) for f in listdir(join(path, name, subDirs[1])) if isfile(join(path, name, subDirs[1], f))]
  fallingWalkingFiles = fallingWalkingFiles + [(path + "/"  + name + "/" + subDirs[2] + "/" + f) for f in listdir(join(path, name, subDirs[2])) if isfile(join(path, name, subDirs[2], f))]
  movementFiles = movementFiles + [(path + "/"  + name + "/" + subDirs[3] + "/" + f) for f in listdir(join(path, name, subDirs[3])) if isfile(join(path, name, subDirs[3], f))]
  sittingFiles = sittingFiles + [(path + "/"  + name + "/" + subDirs[4] + "/" + f) for f in listdir(join(path, name, subDirs[4])) if isfile(join(path, name, subDirs[4], f))]
  walkingFiles = walkingFiles + [(path + "/"  + name + "/" + subDirs[5] + "/" + f) for f in listdir(join(path, name, subDirs[5])) if isfile(join(path, name, subDirs[5], f))]


#get spectrograms and get features from spectrograms
eng = matlab.engine.start_matlab()
fallingSittingData = []
fallingStandingData = []
fallingWalkingData = []
movementData = []
sittingData = []
walkingData = []

for file in fallingSittingFiles:
	print(file)
	outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
	eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
	fallingSittingData[:0] = [outfile]

for file in fallingStandingFiles:
	print(file)
	outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
	eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
	fallingStandingData[:0] = [outfile]

for file in fallingWalkingFiles:
  print(file)
  outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
  eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
  fallingWalkingData[:0] = [outfile]

for file in movementFiles:
  print(file)
  outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
  eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
  movementData[:0] = [outfile]

for file in sittingFiles:
  print(file)
  outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
  eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
  sittingData[:0] = [outfile]

for file in walkingFiles:
  print(file)
  outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
  eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
  walkingData[:0] = [outfile]

eng.quit()

#make classification list
resultsFallingSitting = [0] * len(fallingSittingData)
resultsFallingStanding = [1] * len(fallingStandingData)
resultsFallingWalking = [2] * len(fallingWalkingData)

resultsMovement = [3] * len(movementData)
resultsSitting = [4] * len(sittingData)
resultsWalking = [5] * len(walkingData)

#prepare data for feature selection
fallingSittingData = np.array(fallingSittingData)
fallingStandingData = np.array(fallingStandingData)
fallingWalkingData = np.array(fallingWalkingData)

movementData = np.array(movementData)
sittingData = np.array(sittingData)
walkingData = np.array(walkingData)

fallingSittingData_Train, fallingSittingData_Test, fallingSittingData_TrainResults, fallingSittingData_TestResults = train_test_split(fallingSittingData, resultsFallingSitting, test_size = 0.3)
fallingStandingData_Train, fallingStandingData_Test, fallingStandingData_TrainResults, fallingStandingData_TestResults = train_test_split(fallingStandingData, resultsFallingStanding, test_size = 0.3)
fallingWalkingData_Train, fallingWalkingData_Test, fallingWalkingData_TrainResults, fallingWalkingData_TestResults = train_test_split(fallingWalkingData, resultsFallingWalking, test_size = 0.3)

movementData_Train, movementData_Test, movementData_TrainResults, movementData_TestResults = train_test_split(movementData, resultsMovement, test_size = 0.3)
sittingData_Train, sittingData_Test, sittingData_TrainResults, sittingData_TestResults = train_test_split(sittingData, resultsSitting, test_size = 0.3)
walkingData_Train, walkingData_Test, walkingData_TrainResults, walkingData_TestResults = train_test_split(walkingData, resultsWalking, test_size = 0.3)

os.mkdir("allClassSpecs")
os.mkdir("allClassSpecs/train")
os.mkdir("allClassSpecs/test")

os.mkdir("allClassSpecs/train/fallingSittingFiles")
os.mkdir("allClassSpecs/test/fallingSittingFiles")

os.mkdir("allClassSpecs/train/fallingStandingFiles")
os.mkdir("allClassSpecs/test/fallingStandingFiles")

os.mkdir("allClassSpecs/train/fallingWalkingFiles")
os.mkdir("allClassSpecs/test/fallingWalkingFiles")

os.mkdir("allClassSpecs/train/movementFiles")
os.mkdir("allClassSpecs/test/movementFiles")

os.mkdir("allClassSpecs/train/sittingFiles")
os.mkdir("allClassSpecs/test/sittingFiles")

os.mkdir("allClassSpecs/train/walkingFiles")
os.mkdir("allClassSpecs/test/walkingFiles")

for spec in fallingSittingData_Train:
	os.rename(spec, "allClassSpecs/train/fallingSittingFiles/"+spec)
for spec in fallingSittingData_Test:
	os.rename(spec, "allClassSpecs/test/fallingSittingFiles/"+spec)

for spec in fallingStandingData_Train:
	os.rename(spec, "allClassSpecs/train/fallingStandingFiles/"+spec)
for spec in fallingStandingData_Test:
	os.rename(spec, "allClassSpecs/test/fallingStandingFiles/"+spec)

for spec in fallingWalkingData_Train:
  os.rename(spec, "allClassSpecs/train/fallingWalkingFiles/"+spec)
for spec in fallingWalkingData_Test:
  os.rename(spec, "allClassSpecs/test/fallingWalkingFiles/"+spec)

for spec in movementData_Train:
  os.rename(spec, "allClassSpecs/train/movementFiles/"+spec)
for spec in movementData_Test:
  os.rename(spec, "allClassSpecs/test/movementFiles/"+spec)

for spec in sittingData_Train:
  os.rename(spec, "allClassSpecs/train/sittingFiles/"+spec)
for spec in sittingData_Test:
  os.rename(spec, "allClassSpecs/test/sittingFiles/"+spec)

for spec in walkingData_Train:
  os.rename(spec, "allClassSpecs/train/walkingFiles/"+spec)
for spec in walkingData_Test:
  os.rename(spec, "allClassSpecs/test/walkingFiles/"+spec)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory("../../../ECE_Senior_Design_Our_Data/allClassSpecs/train",
                                                 target_size = (224, 224),
                                                 batch_size = 8,
                                                 subset="training",
                                                 class_mode = 'categorical')

test_set = train_datagen.flow_from_directory("../../../ECE_Senior_Design_Our_Data/allClassSpecs/test",
                                                 target_size = (224, 224),
                                                 batch_size = 8,
                                                 class_mode = 'categorical')

STEP_SIZE_TRAIN=training_set.n//training_set.batch_size
STEP_SIZE_TEST=test_set.n//test_set.batch_size

IMAGE_SIZE = [224, 224]
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
#here [3] denotes for RGB images(3 channels)

#don't train existing weights
for layer in vgg.layers:
 layer.trainable = False
 
x = Flatten()(vgg.output)
prediction = Dense(6, activation='softmax')(x)
model = Model(inputs=vgg.input, outputs=prediction)
model.compile(loss='categorical_crossentropy',
                    optimizer=optimizers.Adam(),
                    metrics=['accuracy', f1])
model.summary()

from datetime import datetime
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras.callbacks import ReduceLROnPlateau
lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1),
                               cooldown=0,
                               patience=5,
                               min_lr=0.5e-6)
checkpoint = ModelCheckpoint(filepath='mymodel.h5', 
                               verbose=1, save_best_only=True)
callbacks = [checkpoint, lr_reducer]
start = datetime.now()
history = model.fit_generator(training_set, 
                    steps_per_epoch=STEP_SIZE_TRAIN, 
                    epochs = 18, verbose=5)
duration = datetime.now() - start
print("Training completed in time: ", duration)

score = model.evaluate(test_set)
print('Test Loss:', score[0])
print('Test accuracy:', score[1])

print(history.history["f1"])

import matplotlib.pyplot as plt
plt.plot(history.history["accuracy"])
plt.plot(history.history["loss"])
plt.plot(history.history["f1"])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy", "loss", "F1"])
plt.show()