import os
import matlab.engine
import numpy as np
import time
import shutil
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
names = ['GraceSpecs', 'MarcSpecs', 'PeteSpecs']
subDirs = ['fallingSitting', 'fallingStanding', 'fallingWalking', 'Movement', 'Sitting', 'Walking']

#get filenames for data
path = "../../ECE_Senior_Design_Our_Data"
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

#make classification list
resultsFallingSitting = [0] * len(fallingSittingFiles)
resultsFallingStanding = [1] * len(fallingStandingFiles)
resultsFallingWalking = [2] * len(fallingWalkingFiles)

resultsMovement = [3] * len(movementFiles)
resultsSitting = [4] * len(sittingFiles)
resultsWalking = [5] * len(walkingFiles)

#prepare data for feature selection
fallingSittingFiles = np.array(fallingSittingFiles)
fallingStandingFiles = np.array(fallingStandingFiles)
fallingWalkingFiles = np.array(fallingWalkingFiles)

movementFiles = np.array(movementFiles)
sittingFiles = np.array(sittingFiles)
walkingFiles = np.array(walkingFiles)

nums = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

for num in nums:
  fallingSittingData_Train, fallingSittingData_Test, fallingSittingData_TrainResults, fallingSittingData_TestResults = train_test_split(fallingSittingFiles, resultsFallingSitting, test_size = 0.3)
  fallingStandingData_Train, fallingStandingData_Test, fallingStandingData_TrainResults, fallingStandingData_TestResults = train_test_split(fallingStandingFiles, resultsFallingStanding, test_size = 0.3)
  fallingWalkingData_Train, fallingWalkingData_Test, fallingWalkingData_TrainResults, fallingWalkingData_TestResults = train_test_split(fallingWalkingFiles, resultsFallingWalking, test_size = 0.3)

  movementData_Train, movementData_Test, movementData_TrainResults, movementData_TestResults = train_test_split(movementFiles, resultsMovement, test_size = 0.3)
  sittingData_Train, sittingData_Test, sittingData_TrainResults, sittingData_TestResults = train_test_split(sittingFiles, resultsSitting, test_size = 0.3)
  walkingData_Train, walkingData_Test, walkingData_TrainResults, walkingData_TestResults = train_test_split(walkingFiles, resultsWalking, test_size = 0.3)

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test")

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/fallingSittingFiles")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/fallingSittingFiles")

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/fallingStandingFiles")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/fallingStandingFiles")

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/fallingWalkingFiles")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/fallingWalkingFiles")

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/movementFiles")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/movementFiles")

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/sittingFiles")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/sittingFiles")

  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/walkingFiles")
  os.mkdir("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/walkingFiles")

  for spec in fallingSittingData_Train:
  	shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/fallingSittingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])
  for spec in fallingSittingData_Test:
  	shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/fallingSittingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])

  for spec in fallingStandingData_Train:
  	shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/fallingStandingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])
  for spec in fallingStandingData_Test:
  	shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/fallingStandingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])

  for spec in fallingWalkingData_Train:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/fallingWalkingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])
  for spec in fallingWalkingData_Test:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/fallingWalkingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])

  for spec in movementData_Train:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/movementFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])
  for spec in movementData_Test:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/movementFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])

  for spec in sittingData_Train:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/sittingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])
  for spec in sittingData_Test:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/sittingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])

  for spec in walkingData_Train:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train/walkingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])
  for spec in walkingData_Test:
    shutil.copy(spec, "../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test/walkingFiles/"+ "_" + spec.rsplit('/', 5)[-2] + "_" + spec.rsplit('/', 5)[-3] + spec.rsplit('/', 5)[-1])

  from keras.preprocessing.image import ImageDataGenerator

  train_datagen = ImageDataGenerator(rescale = 1./255,
                                     shear_range = 0.2,
                                     zoom_range = 0.2,
                                     horizontal_flip = True)

  test_datagen = ImageDataGenerator(rescale = 1./255)

  training_set = train_datagen.flow_from_directory("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/train",
                                                   target_size = (224, 224),
                                                   batch_size = 8,
                                                   subset="training",
                                                   class_mode = 'categorical')

  test_set = train_datagen.flow_from_directory("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN/test",
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
                      epochs = num, verbose=5)
  duration = datetime.now() - start
  print("Training completed in time: ", duration)

  score = model.evaluate(test_set)
  print('Test Loss:', score[0])
  print('Test accuracy:', score[1])

  print(history.history["f1"])

  # import matplotlib.pyplot as plt
  # plt.plot(history.history["accuracy"])
  # plt.plot(history.history["loss"])
  # plt.plot(history.history["f1"])
  # plt.title("model accuracy")
  # plt.ylabel("Accuracy")
  # plt.xlabel("Epoch")
  # plt.legend(["Accuracy", "loss", "F1"])
  # plt.show()

  shutil.rmtree("../../ECE_Senior_Design_Our_Data/specsForMulticlassCNN")