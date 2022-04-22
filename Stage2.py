# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:39:11 2022

@author: hmhob
"""

import pandas as pd
import geopandas as gpd

#%%Importing the layers & filtering them to Teton County if necessary

#Census files
county = gpd.read_file('tl_2020_us_county.zip')
county = county.query("GEOID == '56039'")
# Trims county info to Teton County 

jh = gpd.read_file('tl_2019_56_place.zip')
jh = jh.query("GEOID == '5640120'")

roads = gpd.read_file('tl_2019_56_prisecroads.zip')

#Teton County files
parcels = gpd.read_file('ownership_shp.zip')

conserv = gpd.read_file('conserv_esmnt.zip')

#insert created zoning gpkg from stage 1

var_list = [county, jh,roads, parcels, conserv]

#%% Projecting layers & building the buffer that 

#projection
utm12n = 32612

for v in var_list:
    v = v.to_crs(epsg = utm12n)








