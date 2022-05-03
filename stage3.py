# -*- coding: utf-8 -*-
"""
Created on Mon May  2 08:27:41 2022

@author: hmhob
"""
# This script begins to analyze Jackson's breakdown of conserved areas and
# potentially developable tracts.

import geopandas as gpd
import matplotlib.pyplot as plt

# reading in Jackson Geopackage

jh_county = gpd.read_file('stage2_jh.gpkg', layer = 'county')
jh_roads = gpd.read_file('stage2_jh.gpkg', layer = 'roads')
jh_parcels = gpd.read_file('stage2_jh.gpkg', layer = 'parcels')
jh_conserv = gpd.read_file('stage2_jh.gpkg', layer = 'conserv')
jh_zoning = gpd.read_file('stage2_jh.gpkg', layer = 'zoning')


#%% Land area calculations

#m^2 to acres conversion
conversion = 0.000247105

# area of conserved areas in Jackson
area_conserv = ((jh_conserv.area.sum())*conversion).round(2)

print(f'The total area of conserved land in Jackson Hole is {area_conserv} acres')

# area of potetially developable zones
resdev = jh_zoning.query('resdev>=1')
area_resdev = ((resdev.area.sum())*conversion).round(2)
print(f'The total area of potentially developable land in Jackson Hole is {area_resdev} acres')

#mean acctval or value of a piece of land with or without a structure on it
print(jh_parcels['acctval'].mean().round(2))


# area of empty lots total

# area of empty lots id'd as resdev

#%% Figures- scatter plot on price/area of parcel acctval

# needs work

fig1,ax1 = plt.subplots(jh_parcels['acctval'], jh_parcels.area, dpi=300)





























