# -*- coding: utf-8 -*-
"""HAM10000 Classifier - MASTER

Automatically generated by Colaboratory.

**Problem**

How do we identify cancerous vs noncancerous skin lesions based purely off appearance?
<img style="height: 50px; margin-left: 0" src="https://www.apriorit.com/images/articles/applying-deep_learning-to-classify-skin-cancer-types/fig_8.png">

**Mounting Drive and Importing Packages**
"""

#connecting google drive data to the notebook
from google.colab import drive
drive.mount('/content/drive')

import numpy as np
from imageio import imread  
import matplotlib.pyplot as plt 
import glob 
import pandas as pd
from sklearn import model_selection
import tensorflow as tf
from tqdm.auto import tqdm

"""**Importing the Data**

Importing features (images)
"""

#creating an array data type to store image data
imageList =[]

#how many images we want to import (10015 for full dataset, <10015 for testing)
n = 10015

#for loop running through each jpg file in the drive location
for i in tqdm(sorted (glob.glob('drive/My Drive/hamdata/*.jpg'))[:n]):
  #getting image info, converting to a numpy array, and storing the value in a list
  image = np.array (imread(i))
  imageList.append (image)

##imageList = np.array (imageList)
##print (imageList.shape) 

plt.imshow(imageList[1])

"""Importing the labels (diagnoses data)"""

metadata = pd.read_csv('drive/My Drive/HAM10000_metadata.csv')
metadata.sample(5)

"""**Processing the Data**"""

#sorting both the pictures and diagnoses data ensures that the right labels match up with the right features
metadata.sort_values(by='image_id', inplace=True)

#after sorting, re=indexing the dataframe by the new order makes it easier to manipulate for further processing
index = range(0, 10015)
metadata["ID"]= index #creating a new column that's just counting from 0-10014

metadata.set_index("ID", inplace=True) #setting the column as the new index
metadata.head(5)

#creating a new vector "int_dx" in the data frame
metadata["int_dx"]=metadata["dx"]

#creating a dictionary data type using {}, a dictionary is a list of associations
mappingTemplate = {"bkl": 0, "akiec": 1, "bcc": 2, "df": 3, "mel": 4, "nv": 5, "vasc": 6}

#using the dictionary to replace specific diagnoses with their corresponding integer code
metadata["int_dx"].replace(mappingTemplate, inplace=True)
metadata.head(5)

#the following code deletes 4467 melanocytic nevi images and labels. This balances out the diagnoses so there is aprox. an even number of each

count = 0

#using a reverse for loop so that deleting an item doesn't affect the index of the images we have left to delete
for i in reversed(range(10015)):
  if metadata.int_dx[i] == 5: #5 is the code for the "nv" diagnosis
    metadata.drop([i], inplace= True) #deleting the label
    del imageList[i] #deleting the feature
    count = count + 1
    print(count, i)
  if count == 4467:
    break
    
metadata.head(5)

#converting the image data from a list to a numpy array that we need for splitting
imageList = np.array (imageList)

#converting dataframe 'int_dx' to a numpy array
label = metadata["int_dx"].to_numpy()

print(label)

"""Splitting the data into training and testing sets"""

#using a function to randomly split our data into training and testing sets 
 x_train, x_test, y_train, y_test = model_selection.train_test_split(imageList, label, test_size=0.20, random_state=42)

 print (y_test)

"""**Building the Model**"""

#we are using a variation of the vgg16 model architecture, a structure that has proven to work well for image classification

model = tf.keras.models.Sequential([

  #convolutional and pooling layers
  tf.keras.layers.Conv2D(64, (3, 3), activation = 'relu', padding = 'same', input_shape = (450, 600, 3)),
  tf.keras.layers.Conv2D(64, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.MaxPooling2D(2, 2),

  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.MaxPooling2D(2, 2),

  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.MaxPooling2D(2, 2),

  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(128, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.MaxPooling2D(2, 2),

  tf.keras.layers.Conv2D(256, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(256, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.Conv2D(256, (3, 3), activation = 'relu', padding = 'same'),
  tf.keras.layers.MaxPooling2D(2, 2),

  #fully connected layers
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dropout(0.5),
  tf.keras.layers.Dense(128, activation=tf.nn.relu),
  tf.keras.layers.Dense(128, activation=tf.nn.relu),
  tf.keras.layers.Dense(7, activation=tf.nn.softmax)

])

model.summary()

#setting all the initial parameters and math for our model
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

#training the model on the training sets
model.fit(x_train, y_train, epochs=150

#testing the model on the testing sets 
model.evaluate(x_test, y_test)

model.save('drive/My Drive/Model Files/working_model')

model = tf.keras.models.load_model('drive/My Drive/Model Files/working_model')

"""**Visualizing our model**"""

!pip install keract

from keract import get_activations, display_activations
img = imageList [1]x
img = np.expand_dims (img, axis=0)
activations = get_activations (model, img)

display_activations (activations, save=False)

#image that the filters are working on
plt.imshow(imageList[1])