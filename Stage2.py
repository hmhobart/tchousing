# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:39:11 2022

@author: hmhob
"""

import pandas as pd
import geopandas as gpd
import os

#%%Importing the layers & filtering them to Teton County if necessary

#Census files
county = gpd.read_file('tl_2020_us_county.zip')
county = county.query("GEOID == '56039'")
# Trims county info to Teton County 

jh = gpd.read_file('tl_2019_56_place.zip')
jh = jh.query("GEOID == '5640120'")

roads = gpd.read_file('tl_2019_56_prisecroads.zip')

#Teton County files-- make sure they are unzipped
parcels = gpd.read_file('ownership_shp/ownership.shp')

#There are a variety of conservation entities in Jackson,
# we will have to combine all of their shape files

jhlt = gpd.read_file('conserv_esmnt/JHLT_Protected_Properties.shp')
jhlt['Name'] = jhlt['NAME']
nc = gpd.read_file('conserv_esmnt/NatureConserv.shp')
tcspt = gpd.read_file('conserv_esmnt/TCSPT.shp')
usa = gpd.read_file('conserv_esmnt/USA.shp')
wgf = gpd.read_file('conserv_esmnt/WGF.shp')
wgf['Name'] = wgf['NAME']

keep_col = ['Name', 'geometry']

conserv_list = [jhlt, nc, tcspt,usa, wgf]

for v in conserv_list:
    v = v[keep_col]

conserv = pd.concat(conserv_list)

zoning = gpd.read_file('stage1_zoning.gpkg', layer = 'tc_zoning')

layer_list = [county, jh, roads, parcels, conserv, zoning]

#%% Projecting layers & building the buffer that will define 
#   the area that is considered Jackson Hole

#UTM projection for Wyoming
utm12n = 32612

# for loop to reproject each layer

for l in layer_list:
    l.to_crs(epsg=utm12n, inplace=True)
    
#Checking conversion
print( parcels.crs)

#distance in meters that the bufffer around Jackson will be
radius = 25000

#create buffer layer
jh_buffer = jh.buffer(radius)

#%% Using the buffer to define the area in the rest of the layers

def clip(input_list,buffer):
    clipped_list = []
    for l in input_list:
        clipped = l.clip(buffer, keep_geom_type=True)
        clipped_list.append(clipped)
    return clipped_list


input_list = [county, roads, parcels, conserv, zoning]


jh_clipped = clip(input_list, jh_buffer)

# separating the layers

jh_county = jh_clipped[0]
jh_roads = jh_clipped[1]
jh_parcels = jh_clipped[2]
jh_conserv = jh_clipped[3]
jh_zoning = jh_clipped[4]

#%% Building the geopackage

out_file = 'stage2_jh.gpkg'

if os.path.exists(out_file):
    os.remove(out_file)

jh_county.to_file(out_file, layer="county", index=False)
jh_roads.to_file(out_file, layer="roads", index=False)
jh_parcels.to_file(out_file, layer="parcels", index=False)
jh_conserv.to_file(out_file, layer="conserv", index=False)
jh_zoning.to_file(out_file, layer="zoning", index=False)





