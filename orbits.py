#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
import astropy.constants as cons
from astropy.time import Time


# In[4]:


# Si necesita instalar "astroquery" des-comente la siguiente linea.
#pip install astroquery


# In[16]:


from astroquery.simbad import Simbad
result_table = Simbad.query_object("M1")
result_table


# In[9]:


result_table['RA'][0]


# In[11]:


result_table['DEC'][0]


# In[13]:


result_table['COO_BIBCODE'][0]


# In[17]:


from astroquery.jplhorizons import Horizons


# In[19]:


today = Time('2023-09-22', format='iso').jd
today


# In[44]:


obj_T = Horizons(id='399', location='@sun', epochs=today)


# In[45]:


obj_T.elements()


# In[46]:


obj_T.vectors()


# In[47]:


print(obj_T.raw_response)


# In[58]:


teg = {'lon': -87.2040052 , 'lat': 14.1057433, 'elevation': 0.93}

start = '2023-09-23 00:00:00'
stop = '2023-09-23 01:00:00'
step = '30m'
times = {'start':start, 'stop':stop, 'step':step}

obj_Me = Horizons(id='499', location=teg, epochs=times)


# In[59]:


obj_Me.ephemerides()


# In[60]:


from mpl_toolkits import mplot3d


# In[61]:


sun = Horizons(id='Sun', location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
tierra = Horizons(id=3, location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
merc = Horizons(id=1, location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
venus = Horizons(id=2, location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
mars = Horizons(id=4, location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()


# In[63]:


fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.scatter(sun['x'],sun['y'],sun['z'], 'o', c='y', label='Sol')
ax.scatter(tierra['x'],tierra['y'],tierra['z'], 'o', label='Tierra')
ax.scatter(merc['x'],merc['y'],merc['z'], 'o', label='Mercurio')
ax.scatter(venus['x'],venus['y'],venus['z'], 'o', label='Venus')
ax.scatter(mars['x'],mars['y'],mars['z'], 'o', label='Marte')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)
ax.legend()


# In[71]:


venus_2 = Horizons(id=2, location="3", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
tierra_2 = Horizons(id=3, location="3", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
mars_2 = Horizons(id=4, location="3", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()


# In[72]:


fig, ax = plt.subplots(figsize=(10,10))
ax.scatter(venus_2['x'],venus_2['y'], label='Venus')
ax.scatter(tierra_2['x'],tierra_2['y'], label='Tierra')
ax.scatter(mars_2['x'],mars_2['y'], label='Marte')
ax.legend()


# In[ ]:




