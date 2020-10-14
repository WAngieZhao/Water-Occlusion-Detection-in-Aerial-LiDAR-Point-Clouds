#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import laspy
import matplotlib.pyplot as plt


# In[2]:


inFile = laspy.file.File("/Users/xRai/NYU/CUSP/Dublin/NW-SE/nyu_2451_38671_laz/F_150326_150519 - Cloud.las", mode="r")


# In[3]:


#sorting gpstime
gpstime = inFile.gps_time
gps_sort_ind = np.argsort(gpstime)
gpstime = gpstime[gps_sort_ind]


# In[4]:


#sort inFile.points
FPoints = inFile.points
FPoints = FPoints[gps_sort_ind]


# In[5]:


#calculate gpstime difference
tdiff = np.diff(gpstime)


# In[6]:


#sort flight edge
fle = inFile.edge_flight_line
fle = fle[gps_sort_ind]


# In[7]:


#get index where 'edge' ==1
ind_fle = np.where(fle==1)
ind_fle = np.hstack(ind_fle)


# In[8]:


#remove even index in index_fle & last index
e_ind_fle = ind_fle[1::2]
e_ind_fle = e_ind_fle[:-1]


# In[9]:


#replace gap between scanline by -1
tdiffF = tdiff[:]
for i in e_ind_fle:
    tdiffF[i] = -1


# In[22]:


count_all = len(np.where(tdiffF >= 0)[0])
count_1 = len(np.where(abs(tdiffF-0.00052) <= 0.00048)[0])
count_2 = len(np.where(abs(tdiffF-0.00002) <= 0.00002)[0])
ratio = count_1 / count_all
print(count_all)
print(count_2)
print(ratio)


# In[35]:


#find points greater than 0.00015
#index
tdiffF_masked = np.where(abs(tdiffF-0.00052) <= 0.00048)
tdiffF_masked = np.hstack(tdiffF_masked)
tdiffF_masked_1 = tdiffF_masked + 1


# In[36]:


#merge two lists
tdiffF_merged = np.concatenate((tdiffF_masked,tdiffF_masked_1))
sorted_indF = np.argsort(tdiffF_merged)
tdiffF_merged = tdiffF_merged[sorted_indF]
tdiffF_merged = np.unique(tdiffF_merged)


# In[37]:


#keep points
#ind = tdiffF_merged
#lst = FPoints
outtype = FPoints.dtype
outPoint = np.empty(len(tdiffF_merged),outtype)
for i in range(len(tdiffF_merged)):
    outPoint[i]=FPoints[tdiffF_merged[i]]


# In[38]:


outFile = laspy.file.File("/Users/xRai/NYU/CUSP/Dublin/NW-SE/nyu_2451_38671_laz/19_t4.las", mode = "w",
                header = inFile.header)
outFile.points = outPoint
outFile.close()


# In[1]:





# In[ ]:




