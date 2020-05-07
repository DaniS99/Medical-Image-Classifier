# -*- coding: utf-8 -*-
"""Testing

Automatically generated by Colaboratory.
"""

import pandas as pd
import os
import numpy as np
from imageio import imread  
import matplotlib.pyplot as plt 
import glob 
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv ("drive/My Drive/HAM10000_metadata.csv")
df.sort_values ("image_id", inplace=True)
df.head (5)
df ['dx_bool'] = df['dx'].apply (lambda x: 1 if x == 'bkl' else 0)
labels = df['dx_bool'].to_numpy()
labels.shape

for i in glob.glob ('drive/My Drive/hamdata/*.jpg'):
  if "(1)" in i:
    os.remove (i)

for n, i in enumerate (sorted (glob.glob ('drive/My Drive/hamdata/*.jpg'))):
  df_jpg = df ['image_id'].values [n] 
  j = i.split ("/")[-1][:-4]
  if j != df_jpg:
    print (i, df_jpg)

arr = [1, 2, 3, 4, 5]

imageList =[]
n = 5000 #number of files you want

labels_short = labels [:n]

for i in sorted (glob.glob('drive/My Drive/hamdata/*.jpg'))[:n]:  
  image = np.array (imread(i))
  imageList.append (image)

imageList = np.array (imageList)
print (imageList.shape)
#plt.imshow(imageList[4])

X_train, X_test, y_train, y_test = train_test_split (imageList, labels_short, test_size=0.2, random_state=0)

model.train (X_train, y_train)

print(labels)

cancer = 0
for i in labels:
  if i == 0:
    cancer = cancer + 1

print (cancer)

