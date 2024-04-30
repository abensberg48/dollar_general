# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 08:15:17 2024

@author: lnbens
"""
#Reading merged csv and counting the number of stores in each county, then picking out top five and graphing them. 
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi']=300
output_folder = './Outputs/'

file_path = './Outputs/census_data_tract.csv'
wholestate =pd.read_csv(file_path)
file_path2 = './Outputs/merged.csv'
merged =pd.read_csv(file_path2)

numstores = merged['County'].value_counts()
print(f'Number of Stores per County: {numstores}')

top5 = numstores.iloc[0:5]

#Creating series with just income data
med_income = merged['med_income']

#Converting to thousands for prettier graph
med_income = med_income/1000

#Doing the same thing for med_income at state level, dropping missing observations
med_incomestate = wholestate['med_income']
med_incomestate = med_incomestate[med_incomestate>0]
med_incomestate = med_incomestate/1000

#%%
#Graphs 

#Bar graph of 5 counties with most stores. 
fig1, ax1 = plt.subplots(figsize=(6, 4))
top5.plot.barh(title='Counties with the Most Dollar General Stores',ax=ax1)
ax1.set_ylabel("")
fig1.tight_layout()
fig1.savefig(output_folder + 'most-stores.png')

#Histogram with distribution of median income for census tracts with Dollar Generals
fig2, ax1 = plt.subplots(figsize=(8, 6))
med_income.plot.hist(ax=ax1,bins=15,title='Distribution of Median Income in Census Tracts with Dollar Generals')
ax1.set_xlabel('Median Income (thousands)')
fig2.tight_layout()
fig2.savefig(output_folder + 'med-incomeDG.png')

#Histogram with median income distribution for all NY census tracts
fig3, ax1 = plt.subplots(figsize=(8, 6))
med_incomestate.plot.hist(ax=ax1, bins=20, title='Distribution of Median Income in NY Census Tracts')
ax1.set_xlabel('Median Income (thousands)')
fig3.tight_layout()
fig3.savefig(output_folder + 'med-incomeNY.png')




