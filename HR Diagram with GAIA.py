#!/usr/bin/env python
# coding: utf-8

# In[10]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
import astropy.constants as cons
from astropy.time import Time
from astroquery.jplhorizons import Horizons
import astropy.coordinates as coord


# ## Accesando base de datos de GAIA.
# 
# - GAIA es una misión espacial con la tarea de catalogar y hacer un mapa en 3 dimensiones de la Vía Láctea.
# - En el camino GAIA busca revelar la composición, formación y evolución de nuestra galaxia.
# - Para mas información visitar: https://www.cosmos.esa.int/web/gaia .
# 
# En este cuadernillo de Jupyter se tiene como objetivos:
# * Poder acceder la base de datos de GAIA "Data Realese 3" (DR3) que contiene 1000 millones de estrellas, con mediciones de las paralajes, movimientos propios, y fotometría.
# * Aprender la manipulación de los datos usando el modulo de Python "<code>astropy</code>".
# * Construir diagramas Hertzsprung-Russell (HR) con las observaciones e identificar los diferentes subgrupos de estrellas dentro del mismo.
# 
# Para mas informacion sobre <code>astroquery.gaia</code> ir a: 
# https://astroquery.readthedocs.io/en/latest/gaia/gaia.html.

# In[2]:


# Si el comando da error porque no esta instalado el paquete astroquery instalar usando pip
#pip install astroquery
from astroquery.gaia import Gaia


# ## Buscando datos en GAIA usando <code>Astroquery</code>
# 

# In[5]:


query_text = '''SELECT TOP 4096 ra, dec, parallax, pmra, pmdec, radial_velocity,
phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag
FROM gaiadr3.gaia_source
WHERE parallax_over_error > 10 AND
    parallax > 4 AND
    radial_velocity IS NOT null
ORDER BY random_index
'''


# In[8]:


job = Gaia.launch_job(query_text)
gaia_data = job.get_results()

# Si desea guardar los datos en un archivo descomente la siguiente linea.
#gaia_data.write('gaia_data.fits')

# Si desea leer la tabla desde un archivo descomente la siguiente linea.
# gaia_data = QTable.read('gaia_data.fits')


# In[9]:


gaia_data


# In[37]:


dist0 = coord.Distance(parallax=u.Quantity(gaia_data['parallax']))


# In[38]:


dist0


# In[17]:


gaia_data.to_pandas()


# In[39]:


BP = u.Quantity(gaia_data['phot_bp_mean_mag'])
RP = u.Quantity(gaia_data['phot_rp_mean_mag'])
Color = BP - RP
Color


# ### Calculando la magnitud absoluta
# 
# - Lo bueno de los datos de GAIA es que tenemos la distancia medida de manera directa usando la paralaje.
# - Esto quiere decir que podemos usar esa distancia para calcular las magnitudes absolutas $M$ para una banda o filtro dado.
# - Esto se hace con la ecuación:
# 
# $$ m - M = 5 \log{\left(\dfrac{distancia}{10pc}\right)} $$
# 
# - Despejando para la magnitud ($m$) y usando las distancias calculadas arriba podemos despejar para $M$
# - Pero para ahorrar tiempo y usar el potencial del modulo <code>astropy</code> usaremos la función <code>distmod</code>.
# - De esta manera calcularemos $M$ usando simplemente:
# 
# $$ M = m - distmod $$

# In[40]:


# calculando el modulo de la distancia
dist_mod = dist0.distmod

# obtenemos de los datos la magnitud aparente del filtro verde (G)
m = gaia_data['phot_g_mean_mag']

# Calculamos la magnitud absoluta
M = m - dist_mod


# ### Haciendo el diagrama Hertzsprung-Russell
# 
# - Con todo esto ya podemos hacer nuestro gráfico $M$ vs. Color, que básicamente es un diagrama Hertzsprung-Russell.
# 
# **Nota: No olvide invertir los ejes de $M$ ya que la magnitud es una cantidad que crece
#  en luminosidad en cuanto mas baja es la magnitud.**

# In[42]:


fig, ax = plt.subplots(figsize=(10,10))

ax.plot(Color, M, 'o', label='Todos los datos', alpha=0.3)
plt.gca().invert_yaxis()

ax.set_xlabel("Color BP-RP Gaia",size=20)
ax.set_ylabel("Magnitud absoluta Gaia g",size=20)
ax.set_title("HR Diagram", size=30)
ax.legend()


# In[53]:


#gd = gaia_data[(gaia_data['parallax'] > 4 * u.mas) & (gaia_data['parallax'] < 7 * u.mas) & (gaia_data['phot_bp_mean_mag'] - gaia_data['phot_rp_mean_mag'] > 0.3 ) & (gaia_data['phot_bp_mean_mag'] - gaia_data['phot_rp_mean_mag'] < 0.9 )]

gd = gaia_data[(gaia_data['parallax'] > 4 * u.mas) & (gaia_data['parallax'] < 4.5 * u.mas) ]
gd


# In[54]:


dist_gd = coord.Distance(parallax=u.Quantity(gd['parallax']))

BP_gd = gd['phot_bp_mean_mag']
RP_gd = gd['phot_rp_mean_mag']
Color_gd = BP_gd - RP_gd

# calculando el modulo de la distancia
dist_mod_gd = dist_gd.distmod

# obtenemos de los datos la magnitud aparente del filtro verde (G)
m_gd = gd['phot_g_mean_mag']

# Calculamos la magnitud absoluta
M_gd = m_gd - dist_mod_gd


# In[55]:


#plotting the HR Diagram
fig, ax = plt.subplots(figsize=(10,10))

ax.plot(Color, M, 'o', c='k', label='Todos los datos', alpha=0.1)
ax.plot(Color_gd, M_gd, 'o', c='b', label='Subgrupo de datos C', alpha=0.1)

plt.gca().invert_yaxis()

ax.set_xlabel("Color BP-RP Gaia",size=20)
ax.set_ylabel("Magnitud absoluta Gaia g",size=20)
ax.set_title("HR Diagram", size=30)
ax.legend()


# In[ ]:




