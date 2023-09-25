#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord

import pyvo as vo 


import warnings 
warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")


# In[8]:


coords_xray = SkyCoord.from_name('Cyg X-1')


# In[9]:


print('La AR: ', coords_xray.ra.hms)
print('La Dec: ', coords_xray.dec)


# In[10]:


xray_services = vo.regsearch(servicetype='spectrum',waveband='x-ray')
xray_services.to_table()['ivoid','short_name','res_title']


# In[11]:


xray_table = xray_services[0].search(pos=coords_xray,size=0.2,format='fits')
xray_table.to_table()


# In[12]:


xray_table.to_table()[xray_table.to_table()['pi']=='Canizares']


# In[13]:


lista = [4,5,7,8]
lista.index(7)


# In[14]:


np.where(xray_table.to_table()['pi'] == 'Canizares')


# In[15]:


fits_xray = fits.open(xray_table[14].getdataurl())
fits_xray.info()


# In[16]:


fits_xray[0].header


# In[17]:


fits_xray[1].header


# In[18]:


fits_xray[1].columns


# In[19]:


xray_spec = fits_xray[1].data


# In[20]:


xray_spec['SPEC_NUM']


# In[22]:


xray_spec['COUNTS']


# In[27]:


fig, ax = plt.subplots(figsize=(8,5))
ax.plot(xray_spec[3]['CHANNEL'], xray_spec[3]['COUNTS'])


# In[31]:


xray_services2 = vo.regsearch(servicetype='image',waveband='x-ray', keywords=['Swift'])
xray_services2.to_table()['ivoid','short_name','res_title']


# In[40]:


img_xray = xray_services2[0].search(pos=coords_xray, format='image/fits')
img_xray.to_table()


# In[42]:


xray_img = fits.open(img_xray[0].getdataurl())
xray_img.info()


# In[44]:


fig, ax = plt.subplots(figsize=(6,6))
plt.imshow(xray_img[0].data, cmap='gray')

