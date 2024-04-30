# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:20:50 2024

@author: lnbens
"""
#Reading NY store data, identifying Dollar General stores in the state, creating a CSV with the stores. 
import pandas as pd

file_path = './Inputs/Retail_Food_Stores_20240415.csv'

# Read the CSV file
all_stores = pd.read_csv(file_path)

is_dg = all_stores['DBA Name'].str.contains('DOLLAR GENERAL', case=False)

dollargenerals = all_stores[is_dg]

output_folder = './outputs/'

# Save the filtered DataFrame as a CSV file in the outputs folder
dollargenerals.to_csv(output_folder + 'NYDGs.csv', index=False)
#dollargenerals.to_csv('NYDGs.csv')
#%%
#Doing descriptive analyses of Dollar General locations, isolating top 5 counties, and writing the top 5 counties to a separate CSV file
totalstores = is_dg.value_counts()
print(f'Number of Stores per County: {totalstores}')

group_by_county = dollargenerals.groupby('County')
num_rows = group_by_county.size()
num_rows = num_rows.sort_values(ascending=False)
print( '\nStores in each County:' )
print( num_rows )

is_top5 = dollargenerals.query("County == 'ERIE' or County == 'ONONDAGA' or County == 'CHAUTAUQUA' or County == 'NIAGARA' or County == 'ONEIDA'")
is_top5.to_csv(output_folder + 'top5counties.csv')
is_top5 = is_top5.groupby('County')
num_stores = is_top5.size()
num_stores = num_stores.sort_values(ascending=False)
print( '\nFive Counties with the Most Dollar General Stores:' )
print( num_stores )

