#!/usr/bin/env python
# coding: utf-8

# In[50]:


get_ipython().run_line_magic('matplotlib', 'notebook')
#%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from astropy import units as u
import astropy.coordinates as coord


# In[2]:


import SciServer.CasJobs as CasJobs
from astroquery.sdss import SDSS


# In[3]:


query="""
SELECT TOP 20 specObjID, z, survey, plate, fiberID, mjd, ra, dec
FROM SpecObj
WHERE class = 'STAR' AND survey='sdss'
"""

stars = CasJobs.executeQuery(query, "dr18")
stars


# In[4]:


star1 = SDSS.get_spectra(plate=1198, fiberID=63, mjd=52669)[0]
star2 = SDSS.get_spectra(plate=1188, fiberID=498, mjd=52650)[0]
star3 = SDSS.get_spectra(plate=1198, fiberID=65, mjd=52669)[0]


# In[5]:


star1.info()


# In[6]:


star1[1].columns


# In[7]:


star1[1].header


# In[8]:


line_data = {"Nombre": star1[3].data['LINENAME'], "Longitud": star1[3].data['LINEWAVE']}
df_lines = pd.DataFrame(line_data)
df_lines


# In[22]:


fig, ax = plt.subplots(figsize=(9,5))
ax.plot(10**star1[1].data['loglam'], star1[1].data['flux'], c='k')
ax.plot(10**star2[1].data['loglam'], star2[1].data['flux'])
ax.plot(10**star3[1].data['loglam'], star3[1].data['flux'])
#ax.plot(10**star1[1].data['loglam'], star1[1].data['model'])
ax.set_ylabel('Flujo', fontsize=16)
ax.set_xlabel('$\lambda$ ($\AA$)', fontsize=16)
ax.axvline(x=6562.81, color='red', label=r'H$\alpha$ = 6563 $\AA$')
ax.axvline(x=6564.613894, color='orange', label=r'H$\alpha_{obs}$')
#ax.axvline(x=4861.0, color='green', label=r'H$\beta$ = 4861 $\AA$')
ax.legend(fontsize=16)


# In[10]:


fig, ax = plt.subplots(3,1, figsize=(9,5), sharex=True)
fig.subplots_adjust(hspace=0)
ax[0].plot(10**star1[1].data['loglam'], star1[1].data['flux'], c='k')
ax[1].plot(10**star2[1].data['loglam'], star2[1].data['flux'])
ax[2].plot(10**star3[1].data['loglam'], star3[1].data['flux'])
ax[1].set_ylabel(r'Flujo $\times$10$^{-17}$ (erg cm$^{-2}$ s$^{-1}$ $\AA^{-1}$)', fontsize=16)
ax[2].set_xlabel('$\lambda$ ($\AA$)', fontsize=16)


# In[11]:


star1[0].header['BUNIT']


# ## Usando SQL y  SciServer para obterner datos de las galaxias en SDSS
# 
# El SDSS es una base de datos SQL. SQL es un lenguaje usado pata comunicar base de datos a traves de "queries". Para cada comando de peticion la base de datos regresa una respuesta. Usualmente, esta es una muestra mas pequena dela base de datos original. En este cuadernillo usaremos SQL para reunir los datos necesarios.
# 
# Para un mas informacion de como usar el SDSS DR18 ir a:
# http://cas.sdss.org/dr18
# 
# En corto, los comandos de SQL consisten en tres bloques:
# - **SELECT** : define las cantidades que se quiere solicitar a la base de datos.
# - **FROM** : define cuales tablas se quieren accesar.
# - **WHERE** : define los parametros a imponer en la sellecion de datos.

# In[12]:


# Encontrar los objetos en SDSS DR18
#
# Para mas informacion del DR18 SDSS http://cas.sdss.org/dr18
#
# Esta peticion ("query") encuentra las galaxias con tamano (petror90_r) mas de 10 arco de segundo
# en una region del cielo entre 100 < RA < 250, un corrimiento al rojo (redshift) entre 0.02 - 0.5, y con magnitud de brillo en la banda mayor a 17.
# 
# Se junta todo en una variable llamada "query"
query="""
SELECT p.objId, p.ra,p.dec, p.petror90_r, p.expAB_r,
    p.dered_u as u, p.dered_g as g, p.dered_r as r, p.dered_i as i, 
    s.z, s.plate, s.mjd, s.fiberid, n.sersic_n, p.modelmag_r, p.modelmag_r-5*log10(4.28E+08*s.z) as abs_mag_r
FROM galaxy AS p
   JOIN SpecObj AS s ON s.bestobjid = p.objid
   JOIN nsatlas AS n ON n.mjd = s.mjd and n.fiberID = s.fiberID and n.plate = s.plate
WHERE p.petror90_r > 10
  and p.ra between 100 and 250
  and s.z between 0.01 and 0.5
  and p.g < 17
"""

# Despues se solicitan los datos. El resultado es una tabla en forma de "dataframe" que nombramos "all_gals".
all_gals = CasJobs.executeQuery(query, "dr18")
print("La peticion tiene " + str(len(all_gals))+ " galaxias")


# In[14]:


all_gals[:10]


# ## Mostrar algunas galaxias en los datos solicitados

# In[17]:


# Importando los modulos de Python para trabajar con SciServer
import SciServer.CasJobs as CasJobs # busqueda con CasJobs
#import SciServer.SciDrive as SciDrive   # escribir/leer de/para SciDrive
import SciServer.SkyServer as SkyServer   # mostrar objetos individuales y generar pequenas imagenes con SkyServer
print('Importando modulos del SciServer')


# In[63]:


#Graficando un subconjunto al azar de 16 galaxias
# estableciendo parametros de las "figuritas"
width=200           # ancho de la imagen
height=200          # altura de la imagen
pixelsize=0.396     # escala de la imagen
plt.figure(figsize=(15, 15))   # Mostrar las figuritas en un mosaico de 15 x 15
subPlotNum = 1

#Preseleccionando un subconjunto con especificos parametros
#my_galaxies = np.where( (all_gals['z'] > 0.02) & (all_gals['z'] < 0.03))[0]
#my_galaxies = np.where( (all_gals['z'] > 0.12) & (all_gals['z'] < 0.20))[0]
#my_galaxies = np.where( (all_gals['z'] > 0.12) & (all_gals['z'] < 0.20))[0]
#my_galaxies = np.where( (all_gals['sersic_n'] > 4.0))[0]
#my_galaxies = np.where( (all_gals['sersic_n']  > 5.5))[0]
#my_galaxies = np.where((all_gals['u']-all_gals['r'] > 1.60) & (all_gals['u']-all_gals['r'] < 1.70))[0]
#my_galaxies = np.where((all_gals['u']-all_gals['g'] > 1.15) & (all_gals['u']-all_gals['g'] < 1.35))[0]
my_galaxies = np.where((all_gals['u']-all_gals['g'] > 1.75) & (all_gals['u']-all_gals['g'] < 2.0))[0]


i = 0
nGalaxies = 16 #numero de galaxias a mostrar
ind = np.random.randint(0,len(my_galaxies), nGalaxies) #seleccionar de manera aleatoria las filas
count=0
for i in ind:           # iterando a traves de las filas seleccionadas en la tabla de datos
    count=count+1
    print('Getting image '+str(count)+' of '+str(nGalaxies)+'...')
    if (count == nGalaxies):
        print('Plotting images...')
    scale=2*all_gals.loc[i]['petror90_r']/pixelsize/width
    #img = SkyServer.getJpegImgCutout(ra=all_gals.loc[my_galaxies[i]]['ra'], dec=all_gals.loc[my_galaxies[i]]['dec'], width=width, height=height, scale=scale,dataRelease='DR16')
    img = SkyServer.getJpegImgCutout(ra=all_gals.loc[my_galaxies[i]]['ra'], dec=all_gals.loc[my_galaxies[i]]['dec'], width=width, height=height, scale=scale)

    plt.subplot(4,4,subPlotNum)
    subPlotNum += 1
    plt.imshow(img) # Mostrar la imagen en el mosaico
    plt.axis('off')
    plt.title(all_gals.loc[my_galaxies[i]]['z'])     


# In[35]:


max(all_gals['z'])


# In[36]:


all_gals['z']


# In[58]:


plt.figure(figsize=(10, 10)) 
img = SkyServer.getJpegImgCutout(ra=all_gals.loc[my_galaxies[0]]['ra'], dec=all_gals.loc[my_galaxies[0]]['dec'])
plt.imshow(img)


# # Distribucion bimodal de las galaxias
# 
# - Como se vio en clase las galaxias pueden ser clasificadas en base a su color.
# - Usando la tabla del SDSS solicitada anteriormente podemos hacer un histograma de color 'u-g'
# 
# Para mas referencias de la distribucion bimodal ver: https://ui.adsabs.harvard.edu/abs/2004ApJ...600..681B/abstract
# 

# In[57]:


fig, ax = plt.subplots(figsize=(6,6))
ax.hist(all_gals['u']-all_gals['g'], bins=40, range=(0.5,2.5))
ax.set_xlabel('Indice de color u-g')
ax.set_ylabel('# Galaxias')


# In[68]:


seleccion = (all_gals['z'] > 0.02) & (all_gals['z'] < 0.03)
x = all_gals['abs_mag_r'][seleccion]
y = all_gals['u'][seleccion]-all_gals['r'][seleccion]
fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(x,y, alpha=0.03)
ax.set_xlim(-23,-17)
ax.set_ylim(0.0,3.0)
ax.set_xlabel('$M_{abs}$')
ax.set_ylabel('u-r')


# In[69]:


fig, ax = plt.subplots(figsize=(6,6))
ax.hist2d(x,y, bins=50, range=([[-23,-17],[0.5,3.5]]))
ax.set_xlabel('$M_{abs}$')
ax.set_ylabel('$u-r$')


# # Estructura a gran escala

# In[71]:


fig, ax = plt.subplots(figsize=(10,10))
sele3 = (all_gals['z']>0.02) & (all_gals['z']<0.05) 
ax.plot(all_gals['ra'][sele3], all_gals['dec'][sele3], '.')


# In[72]:


from astropy.cosmology import WMAP5


# In[74]:


from mpl_toolkits import mplot3d
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

sele4 = (all_gals['z']>0.02) & (all_gals['z']<0.05)
dist = coord.Distance(z=all_gals['z'][sele4].values, cosmology=WMAP5)
phi = all_gals['ra'][sele4]*np.pi/180
theta = all_gals['dec'][sele4]*np.pi/180 + np.pi/2

x = dist*np.cos(phi)*np.sin(theta)
y = dist*np.sin(phi)*np.sin(theta)
z = dist*np.cos(theta)
ax.scatter3D(x,y,z, alpha=0.05)
#ax.set_xlim(-125, -75)
#ax.set_ylim(-50,50)
#ax.set_zlim(50,150)
ax.view_init(30, 30)


# In[ ]:




