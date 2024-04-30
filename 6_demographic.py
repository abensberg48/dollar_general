# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:10:41 2024

@author: lnbens
"""

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi']=300
output_folder = './Outputs/'
#%%
#Reading Census Tract Data csv
file_path = './Outputs/census_data_tract.csv'
wholestate =pd.read_csv(file_path)

#Dropping the missing income data
wholestate2 = wholestate[wholestate['med_income']>=0] #Dropping Missing Data
file_path2 = './Outputs/merged.csv'
merged = pd.read_csv(file_path2)

#Creating a column in merged that has a 1 for every observation, setting index, deleting columns that aren't DG, and deleting observations where there are more than 1 DG per tract
merged_copy = merged
merged_copy['DG']=1
merged_copy = merged_copy.set_index('DG')
merged_copy = merged_copy['GEOID']
merged_copy = merged_copy.drop_duplicates()
merged_copy = merged_copy.reset_index()

#Merging the DG GEOIDs with the whole state
is_notDG = wholestate2.merge(merged_copy,
                   on=['GEOID'],
                   how='left',
                   validate='1:1',
                   indicator=True)
#Filling the DG column's missing values with 0 (for when there's no DG in a tract)
is_notDG['DG']=is_notDG['DG'].fillna('0')
is_notDG = is_notDG.dropna()

#Cleaning Dataframe
columns = ['_merge' , 'state', 'tract']
for c in columns:
    is_notDG.drop(c, axis=1, inplace=True)

#%%
#Calculating the two demographic variables of interest, Percentage Non-White and Percentage Renting for each census tract in the data frame and writing this to a csv file. 
is_notDG['pernonwhite'] = (1-(is_notDG['pop_white']/is_notDG['pop_total']))*100
is_notDG['perrent'] = (1-(is_notDG['housing_owned']/is_notDG['housing_total']))*100

is_notDG.to_csv(output_folder + 'is_notDG.csv')

#%%
#Isolating information for the previously identified top 5 counties and replacing their county codes with the county names for graphing purposes. 
top5counties = is_notDG.query("county == 67 or county == 65 or county ==63 or county == 29 or county == 13")
countynames = {67:'Onondaga', 65:'Oneida', 63:'Niagara', 29:'Erie', 13:'Chautauqua'}
#Renaming some columns for graphing purposes
top5counties = top5counties.rename(columns={'med_income':'Median Income', 'perrent':'Percentage Renting', 'pernonwhite': 'Non-White Population Percentage', 'county':'County'})
top5counties = top5counties.replace(countynames)

top5counties['DG'] = top5counties['DG'].astype(int)
dollargeneral = {1: 'Dollar General', 0: 'No Dollar General'}
top5counties['DG'] = top5counties['DG'].replace(dollargeneral)


#%%
#Creating split violin plots for the top 5 counties to compare distributions of variables for census tracts with and without Dollar Generals. 
fig1, ax1 = plt.subplots(figsize=(8, 6))
nonwhite = sns.violinplot(data=top5counties,x='County',y="Non-White Population Percentage", hue= 'DG', split=True)
nonwhite.legend(loc='upper right')
fig1.figure.suptitle("Race Distribution by Dollar General Presence")
fig1.tight_layout()
fig1.savefig(output_folder +'nonwhite.png')


fig2, ax1 = plt.subplots(figsize=(8, 6))
perrent = sns.violinplot(data=top5counties, x='County', y="Percentage Renting", hue='DG', split=True)
perrent.legend(loc='upper right')  # Set the legend position
fig2.figure.suptitle("Renter Distribution by Dollar General Presence")
fig2.tight_layout()
fig2.savefig(output_folder +'renter.png')


fig3, ax1 = plt.subplots(figsize=(8, 6))
medincome = sns.violinplot(data=top5counties,x='County',y="Median Income", hue= 'DG', split=True)
medincome.legend(loc='upper right')
fig3.figure.suptitle("Median Income Distribution by Dollar General Presence")
fig3.tight_layout()
fig3.savefig(output_folder +'med-income.png')

