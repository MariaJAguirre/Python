#!/usr/bin/env python
# coding: utf-8

# In[30]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
import astropy.constants as cons
from astropy.time import Time
from astroquery.jplhorizons import Horizons


# ## Cuerpos menores
# 
# - El JPLH tiene una seccion para cuerpos menores del Sistema Solar ("Small Bodies" https://ssd.jpl.nasa.gov/tools/sbdb_query.html) en la cual podemos hacer consultas discrimando entre diferentes tipos de cuerpo, por ejemplo: Con los datos generados en JPLH graficar la posicion de los asteorides "Amor" y "Apolo"

# In[3]:


df_amor = pd.read_csv('sbdb_amor.csv')
df_apollo = pd.read_csv('sbdb_apollo.csv')


# In[6]:


df_amor.columns


# In[7]:


df_amor['diameter'][0]


# ## Buscando un aniquilador global
# 
# - Los asteroides con mas de ~10 km se denominan asesinos globales. Busquemos los asteorides Amor y Apollo que tengan un diametro mayor a 10 km.

# In[8]:


df_amor[(df_amor['diameter'] >= 10)]


# In[11]:


df_amor['name'][(df_amor['diameter'] >= 10)]


# In[12]:


df_amor['spkid'][(df_amor['diameter'] >= 5) & (df_amor['diameter'] <= 10)]


# In[13]:


df_apollo['name'][(df_apollo['diameter'] >= 10)]


# In[14]:


max(df_apollo['diameter'])


# In[15]:


df_apollo['name'][(df_apollo['diameter'] >= 5) & (df_apollo['diameter'] <= 10)]


# In[17]:


df_apollo[(df_apollo['diameter'] >= 5) & (df_apollo['a'] >= 0.5) & (df_apollo['a'] <= 1.5) ]


# In[23]:


fig, ax = plt.subplots(figsize=(7,7))
ax.hist(df_amor['a'], bins=1000 ,label='Amor', alpha=0.5)
ax.hist(df_apollo['a'], bins=100 , label='Apolo', alpha=0.5)
ax.set_xlabel('Semieje mayor')
ax.set_xlim(0,5)
ax.legend()


# In[24]:


fig, ax = plt.subplots(figsize=(7,7))
ax.plot(df_amor['a'], df_amor['e'], 'o', color='yellow', label='Amor', alpha=0.01)
ax.plot(df_apollo['a'], df_apollo['e'], 'o', color='k', label='Apolo', alpha=0.01)
ax.set_xlabel('Semieje mayor')
ax.set_ylabel('Excentricidad')
ax.set_xlim(0,5)
ax.legend()


# In[25]:


df_amor['pdes']


# In[26]:


df_amor['pdes'][:10]


# In[27]:


for i in df_amor['pdes'][:10]:
    print(i)


# In[28]:


df_amor['pdes'][:10].values


# ## Vamos a graficar donde estan los primeros 100 asteroides Amor y Apolo.
# 
# - Voy a obtener las orbitas del Sol y la Tierra para referencia

# In[31]:


sun = Horizons(id='Sun', location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()
tierra = Horizons(id=3, location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()


# In[33]:


fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.scatter(sun['x'],sun['y'],sun['z'], 'o', c='y')
ax.scatter(tierra['x'],tierra['y'],tierra['z'], 'o')
for i in df_amor['pdes'][:100].values:
    amo = Horizons(id=i, location="@sun", epochs={'2023-10-12'}).vectors()
    ax.scatter(amo['x'],amo['y'], amo['z'], 'o', c='g')

for j in df_apollo['pdes'][:100].values:
    apo = Horizons(id=j, location="@sun", epochs={'2023-10-12'}).vectors()
    ax.scatter(apo['x'],apo['y'], apo['z'], 'o', c='k')

ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_zlim(-2.2, 2.2)


# In[36]:


df_apollo['pdes'][(df_apollo['name'] == 'Phaethon')]


# In[37]:


phaethon = Horizons(id='3200', location="@sun", epochs={'start':"2017-01-01", 'stop':"2019-01-01", 'step':'1d'}).vectors()


# In[38]:


fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.scatter(sun['x'],sun['y'],sun['z'], 'o', c='y')
ax.scatter(tierra['x'],tierra['y'],tierra['z'], 'o')
ax.scatter(phaethon['x'], phaethon['y'], phaethon['z'], 'o', c='orange')
for i in df_amor['pdes'][:10].values:
    amo = Horizons(id=i, location="@sun", epochs={'2023-10-12'}).vectors()
    ax.scatter(amo['x'],amo['y'], amo['z'], 'o', c='g')

for j in df_apollo['pdes'][:10].values:
    apo = Horizons(id=j, location="@sun", epochs={'2023-10-12'}).vectors()
    ax.scatter(apo['x'],apo['y'], apo['z'], 'o', c='k')

ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_zlim(-2.2, 2.2)


# ## Objetos del Cinturon Principal (MBOs)

# In[39]:


df_mba = pd.read_csv('sbdb_MBA.csv')


# In[40]:


df_mba


# In[45]:


fig, ax = plt.subplots(figsize=(7,7))
ax.hist(df_mba['a'], bins=100)
ax.set_xlabel('Semieje Mayor (UA)')


# ## Tercera ley de Kepler
# 
# $$ P^{2} \propto a^{3} $$

# In[46]:


P_J = (4331.0*u.d).to(u.yr)
P_J


# In[48]:


a_J = P_J**(2/3)
(a_J.value * u.AU)


# In[49]:


two_1 = ((1/2)*P_J)**(2/3)
two_1


# In[60]:


three_1 = ((1/3)*P_J)**(2/3)
four_1 = ((1/4)*P_J)**(2/3)
five_2 = ((2/5)*P_J)**(2/3)
seven_3 = ((3/7)*P_J)**(2/3)


# In[61]:


fig, ax = plt.subplots(figsize=(7,7))
ax.hist(df_mba['a'], bins=100)
ax.set_xlabel('Semieje Mayor (UA)')
ax.axvline(x=two_1.value, color='g', label='2:1')
ax.axvline(x=three_1.value, color='orange', label='3:1')
ax.axvline(x=four_1.value, color='r', label='4:1')
ax.axvline(x=five_2.value, color='gray', label='5:2')
ax.axvline(x=seven_3.value, color='k', label='7:3')
ax.legend()


# ## Graficando diferentes parametro

# In[65]:


fig, ax = plt.subplots(figsize=(7,7))
ax.scatter(df_mba['a'], df_mba['i'], alpha=0.05)


# In[77]:


fig, ax = plt.subplots(figsize=(7,7))
ax.hist2d(df_mba['a'], df_mba['i'], bins=(100,100), cmax=100)


# In[ ]:




