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
nc = gpd.read_file('conserv_esmnt/NatureConserv.shp')
tcspt = gpd.read_file('conserv_esmnt/TCSPT.shp')
usa = gpd.read_file('conserv_esmnt/USA.shp')
wgf = gpd.read_file('conserv_esmnt/WGF.shp')

#dictionaries to make sure Name columns are consistent
name = {'name':'Name', 'NAME': 'Name'}


#Trim the easement datasets to name & geometry, add the source, 
#and align names column for a cohesive data set

conserv_list = {'jhlt':jhlt, 'nc':nc, 'tcspt': tcspt, 
                'usa': usa, 'wgf': wgf}

for source,data in conserv_list.items():
    data.rename(columns=name, inplace=True)
    data['source'] = source
    cols = data.columns
    cols = [c for c in cols if c not in ['source', 'Name', 'geometry']]
    data.drop(columns=cols, inplace= True)
    
#combining all of the conservation easements to one dataset
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

#create buffer layer that wil clip each layer to the area we are examining
jh_buffer = jh.buffer(radius)

#%% Using the buffer to define the area in the rest of the layers

def clip(input_list,buffer):
    clipped_list = []
    for l in input_list:
        bad = (l.is_valid == False).sum()
        if bad > 0:
            print(f'{bad} invalid objects found' )
            fixed = l.buffer(0)
            l['geometry'] = fixed.geometry
        clipped = l.clip(buffer, keep_geom_type=True)
        clipped_list.append(clipped)
    return clipped_list

# put all the layers you want to clip in this list
input_list = [county, roads, parcels, conserv, zoning]


jh_clipped = clip(input_list, jh_buffer)

# separating the layers from the resulting list of dataframes, so that you 
# end up with unique layers instead of a single layer

jh_county = jh_clipped[0]
jh_roads = jh_clipped[1]
jh_parcels = jh_clipped[2]
jh_conserv = jh_clipped[3]
jh_zoning = jh_clipped[4]

#%% Building the geopackage -- the rest of this data will be changed in QGIS

out_file = 'stage2_jh.gpkg'

if os.path.exists(out_file):
    os.remove(out_file)

jh_county.to_file(out_file, layer="county", index=False)
jh_roads.to_file(out_file, layer="roads", index=False)
jh_parcels.to_file(out_file, layer="parcels", index=False)
jh_conserv.to_file(out_file, layer="conserv", index=False)
jh_zoning.to_file(out_file, layer="zoning", index=False)




