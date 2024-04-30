# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:53:11 2024

@author: lnbens
"""
import geopandas as gpd

# Reading Census shapefile into New York Counties Map
wgs84 = 4326
utm18n = 26918
output_folder = './Outputs/'
out_file = output_folder + "NYDGs.gpkg"
file_path = './Outputs/NYDGs.csv'
stores = gpd.read_file(file_path)
file_path2 = './Inputs/cb_2022_us_county_500k.zip'
CBF = gpd.read_file(file_path2)
CBF = CBF.query("STATEFP == '36'")
CBF = CBF.to_crs(utm18n)

#Reading DAC information on Census Tracts, isolating New York
file_path3 = './Inputs/usa.zip'
DAC = gpd.read_file(file_path3)
DAC = DAC.to_crs(utm18n)
DAC = DAC.query("SF == 'New York'")


#Coordinates for DGs in State
DGcoords = gpd.GeoSeries.from_wkt(stores['Georeference'])
data_only = stores.drop(columns='Georeference')
geoDG = gpd.GeoDataFrame(data=data_only, geometry=DGcoords, crs=wgs84)

#Saving as GeoPackage with layers for stores, NY counties, and DAC information
geoDG = geoDG.to_crs(utm18n)
geoDG.to_file(out_file, layer='stores')
CBF.to_file(out_file, layer='counties')
DAC.to_file(out_file, layer='DAC')

#Reading Census Tracts
file_path4 = './Inputs/cb_2022_36_tract_500k.zip'
tracts = gpd.read_file(file_path4)
tracts = tracts.to_crs(utm18n)


#Spatially joining the census tracts onto the file containing the coordinates for Dollar Generals and writing the joined data into a CSV file. 
join = geoDG.sjoin(tracts, how='left')
join.to_csv(output_folder + 'DGjoined.csv')




