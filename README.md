# tchousing

# Summary

This project was built to help identify areas that could be targeted to 
increase community and workforce housing in the Jackson Hole area. It also shows 
the area of the valley that is in conservation easements and not available for development in the future. 
#
# Files
This project utilizes files from various sources including the Census, and the 
Teton County, WY GIS archives. 

Census: https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2020&layergroup=Counties+%28and+equivalent%29
- You will need to dowload county, and road data from the census.

Teton County:https://www.greenwoodmap.com/tetonwy/mapserver/download/download.html?
- You will need to download the zoning, ownership, and conservation easements packages from this archive.

The census files can remain zipped, however, each of the Teton County files 
will need to be unzipped to extract various parts of each file to ensure a 
complete dataset. 

There are also two included CSV files that indicate which zones are potentialy developable as high density neighborhoods. 
These can be adjusted based on the assumptions made about the zones, 1 indicates they are developable and 2 indicates that there is potenital for development there.  

Files should be run in the order indicated by the stages.
#

# Outputs
These scripts create a geopackage that can identify areas that are zoned for higher density
development in Teton County. It can also give an idea of what the value of these developbable areass is. 
This is pictured in the maps included below.

## Map 1

![alt text](https://github.com/hmhobart/tchousing/blob/main/county_zoning.png 'Jackson Hole Zoning')

This map shows the areas in Jackson Hole that are tagged as developable and conserved as indicated in the legend. There is a closer look at the town of Jackson included in the file as well. 

## Map 2
![alt text](https://github.com/hmhobart/tchousing/blob/main/heatmap.png 'Jackson Hole Pricing')

This map is a heat map of the value of each parcel of land. The 3rd stage of these scripts identify the mean parcel value being greater than $1.8M, and when compared, Maps 1 & 2 indicate 
significant overlap in the most expensive regions of the valley. 
