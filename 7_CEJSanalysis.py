# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:39:31 2024

@author: lnbens
"""
#Reading DAC data, singling out NY info, reading DG csv, figuring out difference in observations, merging them, dropping Census Tracts with no observations. 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
plt.rcParams['figure.dpi']=300
output_folder = './Outputs/'
#%%
file_path = './Inputs/1.0-communities.csv'
DAC = pd.read_csv(file_path)
DAC = DAC[DAC["State/Territory"] == "New York"]
DAC = DAC.rename(columns={'Census tract 2010 ID':'GEOID', 'Identified as disadvantaged':'DAC', 'Is low income?': 'low_income'})
DAC = DAC.set_index('GEOID')
#%%
#Creating DataFrames to identify which census tracts are considered Disadvantaged Communities or Low_Income
DAC1 = DAC['DAC']
DAC1 = DAC1.reset_index()
Low_Inc = DAC['low_income']
Low_Inc = Low_Inc.reset_index()
#%%
#Reading previously creating CSV file
file_path2 = './Outputs/is_notDG.csv'
DG = pd.read_csv(file_path2)
#%%
#Merging DAC data onto DG data and dropping tracts that do not have DAC data 
DACDG = DG.merge(DAC1,
                 on=['GEOID'],
                 how='left',
                 validate='1:1',
                 indicator=True)
print(DACDG["_merge"].value_counts())
DACDG = DACDG.dropna()
#%%
#Merging Low Income data onto DG data and dropping tracts that do not have Low Income data 
LIDG = DG.merge(Low_Inc,
                 on=['GEOID'],
                 how='left',
                 validate='1:1',
                 indicator=True)
print(LIDG["_merge"].value_counts())
LIDG = LIDG.dropna()
#%%
#Running a linear probability model to test the impact of a Census Tract being a disadvantaged community on the likelihood of having a Dollar General

LIDG['low_income'] = LIDG['low_income'].astype(int)
LIDG['intercept'] = 1
X = LIDG[['intercept', 'low_income']]
y = LIDG['DG']
model = sm.OLS(y, X).fit(cov_type='HC3')
print(model.summary())

#Running a linear probability model to test the impact of a Census Tract being a low-income community on the likelihood of having a Dollar General
DACDG['DAC'] = DACDG['DAC'].astype(int)
DACDG['intercept'] = 1
X = DACDG[['intercept', 'DAC']]
y = DACDG['DG']
model2 = sm.OLS(y, X).fit(cov_type='HC3')
print(model2.summary())  
#%%
#Replacing Values for Graphing Purposes
LIDG['DG'] = LIDG['DG'].astype(int)
dollargeneral = {1: 'Dollar General', 0: 'No Dollar General'}
LIDG['DG'] = LIDG['DG'].replace(dollargeneral)
DACDG['DG'] = DACDG['DG'].astype(int)
DACDG['DG'] = DACDG['DG'].replace(dollargeneral)
lowinc = {1:'True', 0:'False'}
LIDG['low_income'] = LIDG['low_income'].replace(lowinc)
DACDG['DAC'] = DACDG['DAC'].replace(lowinc)
#%%
#Creating a barchart to see the distribution of Disadvantaged communities across the state in comparison to disadvantaged communities with Dollar Generals. 
fig1, ax1 = plt.subplots(figsize=(8, 6))
frequency = DACDG.groupby(['DAC', 'DG']).size().unstack(fill_value=0)
frequency.plot.bar(stacked=False, ax=ax1)
plt.xticks(rotation=0)
plt.ylabel('Frequency')
plt.xlabel('Is a Disadvantaged Community')
plt.title('Frequency of Disadvantaged Communities by Dollar General Location')
fig1.tight_layout()
fig1.savefig(output_folder + 'disadvantaged.png')

#Creating a barchart to see the distribution of Disadvantaged communities across the state in comparison to disadvantaged communities with Dollar Generals. 
fig2, ax2 = plt.subplots(figsize=(8, 6))
frequency2 = LIDG.groupby(['low_income', 'DG']).size().unstack(fill_value=0)
frequency2.plot.bar(stacked=False, ax=ax2)
plt.xticks(rotation=0)
plt.ylabel('Frequency')
plt.xlabel('Is a Low-Income Community')
plt.title('Frequency of Low-Income Communities by Dollar General Location')
fig2.tight_layout()
fig2.savefig(output_folder + 'low-income.png')




