#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import laspy
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import chart_studio.plotly as py
import plotly.graph_objects as go


# In[2]:


#inFile = output from TimeDiff_Segregation
inFile = laspy.file.File("/Users/xRai/NYU/CUSP/Dublin/NW-SE/nyu_2451_38647_laz_121253/0.00001_0.001.las", mode="r")


# In[3]:


#sorting gpstime
gpstime = inFile.gps_time
gps_sort_ind = np.argsort(gpstime)
gpstime = gpstime[gps_sort_ind]


# In[4]:


#sort inFile.points
FPoints = inFile.points
FPoints = FPoints[gps_sort_ind]


# In[262]:


coord = np.vstack((inFile.X, inFile.Y, inFile.Z)).transpose()
coord = coord[gps_sort_ind]


# In[461]:


db = DBSCAN(eps=500,min_samples=3).fit(coord)


# In[462]:


#same length list with all zero
label = db.labels_
# Number of clusters in label, ignoring noise if present.
n_clusters_ = len(set(label)) - (1 if -1 in label else 0)
n_noise_ = list(label).count(-1)
print(n_clusters_)
print(n_noise_)


# In[463]:


FPointst = FPoints[:]
i = np.argsort(label)
label, FPointst = label[i], FPointst[i]
FPointst
len(label)#110757
len(FPoints)


# In[464]:


coords = coord[:]
i = np.argsort(label)
label, coords = label[i], coords[i]


# In[465]:


#group coord
coord_c = np.split(coords, np.flatnonzero(label[1:] != label[:-1])+1)
FPointst_c = np.split(FPointst, np.flatnonzero(label[1:] != label[:-1])+1)
len(FPointst_c)
label


# In[466]:


#remove -1 (noises)
FPointst_c = FPointst_c[1:]
len(FPointst_c)


# In[467]:


#check length of each lst (should be >5)
for i in range(len(FPointst_c)):
    print(str(i)+" "+ str(len(FPointst_c[i])))


# In[468]:


coord_c = coord_c[1:]
len(coord_c)


# In[469]:


coordt=np.array([])

for lst in coord_c:
    if (len(lst)<60):
        #remove
        coordt = np.append(coordt,None)
        coordt[-1] = lst
    else:
        #recluster
        db = DBSCAN(eps=500,min_samples=3).fit(lst)
        label = db.labels_
        lst_c = lst[:]
        i = np.argsort(label)
        label, lst_c = label[i], lst_c[i]
        lst_tc = np.split(lst_c, np.flatnonzero(label[1:] != label[:-1])+1)
        lst_tc = lst_tc[1:]
        #reclustered, append to list
        for i in range(len(lst_tc)):
            coordt = np.append(coordt,None)
            coordt[-1] = lst_tc[i]
            
len(coordt)


# In[472]:


#Fpoints version
#FPointst_c = coord_c
#cooordt = FP2
FP2=np.array([])

for i in range(len(FPointst_c)):
    if (len(FPointst_c[i])<60):
        #remove
        FP2 = np.append(FP2,None)
        FP2[-1] = FPointst_c[i]
    else:
        #recluster
        db = DBSCAN(eps=500,min_samples=3).fit(coord_c[i])
        label = db.labels_
        lst_c = FPointst_c[i][:]
        i = np.argsort(label)
        label, lst_c = label[i], lst_c[i]
        lst_tc = np.split(lst_c, np.flatnonzero(label[1:] != label[:-1])+1)
        lst_tc = lst_tc[1:]
        #reclustered, append to list
        for i in range(len(lst_tc)):
            FP2 = np.append(FP2,None)
            FP2[-1] = lst_tc[i]
            
len(FP2)


# In[483]:


#std, get z axis
#for 1 cluster
z0_data = FP2[0]
z0_lst = [val for sublist in z0_data for val in sublist]
z0 = [row[2] for row in z0_lst]
np.std(z0)


# In[488]:


##calculate z sigma for all
z_std = np.array([])
z_std2 = np.array([])
for i in range(len(FP2)):
    z_data = FP2[i]
    z_lst = [val for sublist in z_data for val in sublist]
    z_val = [row[2] for row in z_lst]
    z_std = np.append(z_std,np.std(z_val))
    
len(z_std)


# In[489]:


plt.plot(z_std)


# In[613]:


#if z_std > 300
#find index
#remove from FP2
z_std_masked = np.where(z_std<300,0,1)
z_std_masked_c = np.count_nonzero(z_std_masked == 1)
z_std_masked_c


# In[631]:


#keep all clusteres less then the acceptable standard deviation
outputlst = np.transpose((z_std<40).nonzero()).flatten()


# In[632]:


outer  = np.array([])
for i in outputlst:
    outer = np.append(outer,None)
    outer[-1] = FP2[i]
    
outPoint = np.concatenate(outer).ravel()


# In[633]:


outFile = laspy.file.File("/Users/xRai/NYU/CUSP/Dublin/NW-SE/nyu_2451_38647_laz_121253/coor500.3_FP2_std40.las", mode = "w",
                header = inFile.header)
outFile.points = outPoint
outFile.close()


# In[ ]:




