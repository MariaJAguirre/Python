#!/usr/bin/env python
# coding: utf-8

# In[48]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
import astropy.constants as cons
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy.coordinates import Distance
from astropy.io import fits


# In[4]:


import pyvo as vo


# In[5]:


#pip install pyvo


# In[ ]:


import warnings 
warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")


# In[7]:


#help(vo.regsearch)


# In[37]:


uv_services = vo.regsearch(servicetype='image',waveband='uv')
uv_services.to_table()


# - Para otros tipos de servicios (servicetype):
# 
#     "image": "sia",
#     "spectrum": "ssa",
#     "scs": "conesearch",
#     "line": "slap",
#     "sla": "slap",
#     "table": "tap"

# In[38]:


uv_services.to_table()[0]


# In[39]:


uv_services.to_table()['ivoid','short_name','res_title']


# In[40]:


uv_services.to_table()[16]['ivoid','short_name','res_title']


# In[32]:


coords_m51 = SkyCoord.from_name('m51')
coords_m51


# In[46]:


im_table = uv_services[16].search(pos=coords_m51,size=0.2,format='image/fits')


# In[47]:


im_table.to_table()


# In[49]:


m51_imgf = fits.open(im_table[0].getdataurl())


# In[50]:


m51_imgf.info()


# In[75]:


fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(m51_imgf[0].data, cmap='gray', vmin=0.01, vmax=0.1)


# In[63]:


m51_imgf[0].header


# In[64]:


from astropy.wcs import WCS


# In[67]:


wcs_m51 = WCS(m51_imgf[0])
wcs_m51


# In[70]:


fig, ax = plt.subplots(figsize=(6,6))
plt.subplot(projection=wcs_m51)
plt.imshow(m51_imgf[0].data, cmap='gray', vmax=0.18)
plt.savefig('IMG_m51.png')


# In[ ]:




