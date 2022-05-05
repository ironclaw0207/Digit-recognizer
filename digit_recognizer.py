# -*- coding: utf-8 -*-
"""Digit_recognizer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13JR0Ls27Vzg45_gqx7lLTz_HFF9mKOWb

Import libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers import Convolution2D, MaxPooling2D
from sklearn.model_selection import train_test_split

"""Read the data from train and test CSV file inside your google drive. Divide the data into x and y values. First column is labels and will be copied to y variable. x variable will have the pixel values."""

df = pd.read_csv('/content/drive/MyDrive/digit-recognizer/train.csv')
x_test= pd.read_csv('/content/drive/MyDrive/digit-recognizer/test.csv')

y_train= df.iloc[:,0]
x_train= df.iloc[:,1:df.shape[0]]

"""Convert x into numpy array and reshape it from 1 x 784 to 28 by 28 images. Visualize the images"""

x_train=np.array(x_train)
x_test=np.array(x_test)
x_train=x_train.reshape(df.shape[0],28,28)
x_test=x_test.reshape(x_test.shape[0],28,28)
plt.imshow(x_train[10])

"""Feature scaling with mean and std deviation to make the data have zero mean"""

x_train=x_train/255
x_test=x_test/255

"""Add channel dimension for training images"""

x_train=x_train.reshape(x_train.shape[0],28,28,1)
x_test=x_test.reshape(x_test.shape[0],28,28,1)
print(x_train.shape,x_test.shape)

"""Create a one-hot vector representation of labels for softmax"""

y_train=tf.one_hot(y_train,10)
print(y_train)

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=8,
    width_shift_range=0.08,
    shear_range=0.3,
    height_shift_range=0.08, zoom_range=0.08,
    validation_split=0.1)

"""Build a CNN model with max pooling, softmax layer,batch normalization. Normalization improved the accuracy of the model. Always have norm after CNN and before max pooling."""

model=tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(28,28,1)),
      tf.keras.layers.Conv2D(32,3,activation='relu'),
      tf.keras.layers.BatchNormalization(),
      tf.keras.layers.Conv2D(32,3,activation='relu'),
      tf.keras.layers.BatchNormalization(),
      tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
      tf.keras.layers.Conv2D(64,3,activation='relu'),
      tf.keras.layers.BatchNormalization(),
      tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
      tf.keras.layers.Conv2D(64,3,activation='relu'),
      tf.keras.layers.BatchNormalization(),
      tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
      tf.keras.layers.Dropout(0.25),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(512,activation='relu'),
      tf.keras.layers.Dense(10,activation='softmax')]
)

"""Before making network ready for training we have to make sure to add below things:

    A loss function: to measure how good the network is

    An optimizer: to update network as it sees more data and reduce loss value

    Metrics: to monitor performance of network

Batch size of 64 was helpful in increasing the speed of the training.
"""

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
#model.fit(x_train, y_train, batch_size=2000,validation_split=0.1,epochs=5)
model.fit(datagen.flow(x_train, y_train, batch_size=64,
        subset='training'),
        validation_data=datagen.flow(x_train, y_train,
        batch_size=64, subset='validation'),
         epochs=10)

"""Perform the predictions"""

y_pred=model.predict(x_test)
y_pred= np.argmax(y_pred, axis=1)
d = {'ImageId': range(1,len(y_pred)+1,1), 'Label': y_pred}
print(d)

"""Create a CSV file with the image ID and the prediction. This is the format for submitting the results in Digit recognizer competition in Kaggle"""

submissions=pd.DataFrame({"ImageId": list(range(1,len(y_pred)+1)),
                         "Label": y_pred})
submissions.to_csv("/content/drive/MyDrive/digit-recognizer/submission.csv", index=False, header=True)