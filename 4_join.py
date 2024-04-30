# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:11:46 2024

@author: lnbens
"""

#Cleaning the joined dataframe, merging it with the census data (for interested variables) and then writing it to a new csv (this csv has all dgs in NY and their GEOID). 
import pandas as pd
output_folder = './Outputs/'
file_path = './Outputs/DGjoined.csv'
joined =pd.read_csv(file_path)
columns = ['Unnamed: 0', 'Address Line 2', 'Address Line 3','Operation Type','Establishment Type','AFFGEOID','NAME','NAMELSAD','STUSPS','STATE_NAME','Square Footage','index_right','STATEFP','COUNTYFP','NAMELSADCO']

for c in columns:
    joined.drop(c, axis=1, inplace=True)
 
file_path2 = './Outputs/census_data_tract.csv'
census_data_tract = pd.read_csv(file_path2)
merged = joined.merge(census_data_tract,
                   on=['GEOID'],
                   how='left',
                   validate='m:m',
                   indicator=True)

merged = merged.set_index(['County','GEOID'])
merged = merged.sort_index(ascending=False)
merged.to_csv(output_folder + 'merged.csv')