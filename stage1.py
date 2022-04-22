# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:53:37 2022

@author: hmhob
"""

import pandas as pd
import geopandas as gpd
import os

#%% Merge function definiton

# Creating a function that will read the zoning layers from Teton County,
# and merge them with the zones we have identified as possible devlopment  
# targets in the two CSVs provided.


def z_merge(input_layer, working_file):
    zoning = gpd.read_file(input_layer)
    
    resdev = pd.read_csv(working_file)
    
    resdev['frequency'] = resdev['zoning']
    resdev['zoning'] = resdev['code']
    
    merged = zoning.merge(resdev, on="zoning",validate="m:1",how="outer",indicator=True)
    print(merged['_merge'].value_counts())
    
    merged = merged.drop(columns = ['_merge','frequency'])
    
    return merged

#%% Using the function to merge the zoning layers and the developement targets


towndev = z_merge('zoning_shp/TOJ_Zoning.shp', 'working_codes_town.csv')

countydev = z_merge('zoning_shp/Zoning.shp', 'working_codes_county.csv')

#%% Concatenating the merged variables & exporting to a geopackage

# for this analysis we will not need the columns date and ordinance in towndev,
# or date and resolution in countydev, so we will drop them

towndev = towndev.drop(columns = ['date', 'ordinance'])

countydev = countydev.drop(columns = ['date', 'resolution'])

# Combining the dataframes to create a cohesive dataframe for the county

tc_zoning = pd.concat([towndev,countydev])

# Write this to a geopackage to be used in the next stages of the analysis
out_file = 'stage1_zoning.gpkg'

if os.path.exists(out_file):
    os.remove(out_file)

tc_zoning.to_file(out_file, layer='tc_zoning')



# save to gpkg stage1_zoning.gpkg

#then build second gpkg for stage2