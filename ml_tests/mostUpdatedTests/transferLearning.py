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
fallSubdirs = ['fallingSitting', 'fallingStanding', 'fallingWalking']
nonFallSubdirs = ['Movement', 'Sitting', 'Walking']


#get filenames for DataFrame
path = "../../../ECE_Senior_Design_Our_Data"
fallFiles = []
nonFallFiles = []
for name in names:
	for fallDir in fallSubdirs:
		fallFiles = fallFiles + [(path + "/"  + name + "/" + fallDir + "/" + f) for f in listdir(join(path, name, fallDir)) if isfile(join(path, name, fallDir, f))]
	for nonFallDir in nonFallSubdirs:
		nonFallFiles = nonFallFiles + [(path + "/"  + name + "/" + nonFallDir + "/" + f) for f in listdir(join(path, name, nonFallDir)) if isfile(join(path, name, nonFallDir, f))]

eng = matlab.engine.start_matlab()
fallData = []
nonFallData = []

for file in nonFallFiles:
	print(file)
	outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
	eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
	nonFallData[:0] = [outfile]
for file in fallFiles:
	print(file)
	outfile = 'out_' + str(int(round(time.time() * 1000))) + '.png'
	eng.microDoppler_AWR1642_bulk_BPM(file, outfile, nargout=0)
	fallData[:0] = [outfile]

eng.quit()

#make classification list
resultsFall = [1] * len(fallData)
resultsNonFall = [0] * len(nonFallData)

#prepare data for feature selection
numpyArrayFall = np.array(fallData)
numpyArrayNonFall = np.array(nonFallData)

nonFallTrain, nonFallTest, nonFallTrainRes, nonFallTestRes = train_test_split(numpyArrayNonFall, resultsNonFall, test_size = 0.3)
fallTrain, fallTest, fallTrainRes, fallTestRes = train_test_split(numpyArrayFall, resultsFall, test_size = 0.3)

os.mkdir("specs")
os.mkdir("specs/train")
os.mkdir("specs/test")
os.mkdir("specs/train/nonFall")
os.mkdir("specs/train/fall")
os.mkdir("specs/test/nonFall")
os.mkdir("specs/test/fall")
for spec in nonFallTrain:
	os.rename(spec, "specs/train/nonFall/"+spec)
for spec in nonFallTest:
	os.rename(spec, "specs/test/nonFall/"+spec)
for spec in fallTrain:
	os.rename(spec, "specs/train/fall/"+spec)
for spec in fallTest:
	os.rename(spec, "specs/test/fall/"+spec)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory("../../../ECE_Senior_Design_Our_Data/specs/train",
                                                 target_size = (224, 224),
                                                 batch_size = 8,
                                                 subset="training",
                                                 class_mode = 'categorical')

test_set = train_datagen.flow_from_directory("../../../ECE_Senior_Design_Our_Data/specs/test",
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
prediction = Dense(2, activation='softmax')(x)
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

print(history.history)

import matplotlib.pyplot as plt
plt.plot(history.history["accuracy"])
plt.plot(history.history["loss"])
plt.plot(history.history["f1"])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy", "loss", "f1"])
plt.show()