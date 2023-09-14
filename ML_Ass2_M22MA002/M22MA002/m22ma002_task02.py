# -*- coding: utf-8 -*-
"""m22ma002_task02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_0jKMFjrJtzjTaPfo_X41VpSFFWTGOJa
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
import seaborn as sns
import random as rd
# %matplotlib inline
from sklearn.decomposition import PCA

from google.colab import files
uploaded = files.upload()

import io
df = pd.read_csv(io.BytesIO(uploaded['train.csv']))
print(df)
df
df.keys()

df

print(df['tBodyAcc-mean()-X'])

i=1
for i in range(5):
  print(" ")
  i=i+1

#from sklearn.preprocessing import StandardScaler
#replacing the activity with numerical value inorder to normalise the results.
df1=df.replace({'Activity' : { 'STANDING' : 1, 'LAYING' : 2, 'WALKING_DOWNSTAIRS':3,'SITTING':0,'WALKING':4,'WALKING_UPSTAIRS':5}})
df1

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
norm_df = scaler.fit_transform(df1)
norm_df

norm_df.shape

#reducing the pca dimensions into 2 components using sklearn decomposition 
pcacomp = PCA(n_components=2)
xdim1pca = pcacomp.fit_transform(norm_df)
data = xdim1pca
data.shape

norm_df.shape

#plotting2 dimensions taken in the pca dimensionality reduction
plt.figure(figsize=(28,16))
# plt.scatter(xdim1pca[:,0],xdim1pca[:,1],c=df1['tBodyAcc-mad()-X'],cmap='Accent')
plt.scatter(data[:,0],data[:,1],c=df1['tBodyAcc-mad()-X'],cmap='inferno')
plt.xlabel('First Principal Component ')
plt.ylabel('Second Principal Component')
plt.figure(figsize=(7, 6))
plt.pcolormesh(df1)
plt.colorbar()

x= 14
y=6
if(x<y):
 print(" ")
else:
 print(" second part of the question [applying kmeans clustering]")

# df1['angle(X,gravityMean)'].shape

df1['angle(X,gravityMean)'].shape
from sklearn.decomposition import PCA

print("pca array representation:- ")
pcacomp.components_

#df = df.drop("Activity", axis =1)

#plt.show()

# modified hsv in 256 color class
# hsv_modified = cm.get_cmap('hsv', 256)# create new hsv colormaps in range of 0.3 (green) to 0.7 (blue)
# newcmp = ListedColormap(hsv_modified(np.linspace(0.3, 0.7, 256)))# show figure
# plt.figure(figsize=(7, 6))
# plt.pcolormesh(data, cmap = newcmp)
# plt.colorbar()
pcacomp.components_.shape

# def upd_assg(df1,centroid):
#    centr = []
#    for j in data:
#        t=j.reshape((1,2))
#        x=t-centroid
#        y=np.sum(x**2,axis=1)
#        centr.append(np.argmin(y))
#    return centr

def upd_assg(data, cen):
   c = []
   for i in data:
       c.append(np.argmin(np.sum((i.reshape((1, 2)) - cen) ** 2, axis=1)))
   return c

   print(data.shape)
def upd_centr(data, num_clusters, assignments):
   cen = []
   for c in range(len(num_clusters)):
       cen.append(np.mean([data[x] for x in range(len(data)) if assignments[x] == c], axis=0))
   return cen

cen = (np.random.normal(size=(2, 2)) * 0.0001) + np.mean(data, axis=0).reshape((1, 2))
for i in range(100):
   a = upd_assg(data, cen)
   cen = upd_centr(data, cen, a)
   cen = np.array(cen)

# def upd_centr(df, clusterno, assgno):
#    centr = []
#    l=len(data)
#    for i in range(len(clusterno)):
       
#        centr.append(np.mean([data[x] for x in range(l) if assgno[x] == centr], axis=0))
#    return centr

while(i<=6):
  print(" ")
  i=i+1

print(data.shape)

print(data.shape)
e=np.random.normal(size=(2,2))
t=np.mean(data, axis=0)
# centr = (e * 0.0001) + t.reshape((1, 2))
# for i in range(100):
#    k = upd_assg(df, centr)
#    centr = upd_centr(df, centr, k)
#    centr = np.array(centr)

   
cen = (np.random.normal(size=(2, 2)) * 0.0001) + np.mean(data, axis=0).reshape((1, 2))

cen = (np.random.normal(size=(2, 2)) * 0.0001) + np.mean(data, axis=0).reshape((1, 2))
cen

cen = (np.random.normal(size=(2, 2)) * 0.0001) + np.mean(data, axis=0).reshape((1, 2))
for i in range(100):
   a = upd_assg(data, cen)
   cen = upd_centr(data, cen, a)
   cen = np.array(cen)

plt.scatter(data[:, 0], data[:, 1])
plt.scatter(cen[:, 0], cen[:, 1])
plt.show()

