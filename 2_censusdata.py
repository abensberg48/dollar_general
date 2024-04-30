# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:28:09 2024

@author: lnbens
"""

#DATA BY COUNTY
#Importing numpy, requests, and pandas
import requests
import pandas as pd

# Creating a dictionary to later change the names of columns to variables we're interested in.
variables = {'B02001_001E':'pop_total', 'B02001_002E':'pop_white', 'B25003_001E':'housing_total', 'B25003_002E':'housing_owned', 'B25003_003E':'housing_rental', 'B20002_001E':'med_income'}

# Creating a list of the keys in the dictionary just created and joining the keys with a comma.
var_list = variables.keys()
var_string = ",".join(var_list)

# Formatting the api, requesting data from the census, putting it into a pandas dataframe, handling missing numbers, and then using the dictionary variables to rename the relevant columns
api = "https://api.census.gov/data/2020/acs/acs5"
for_clause = 'county:*'
in_clause = 'state:36'
payload = {'get':var_string, 'for':for_clause, 'in':in_clause}
response = requests.get(api, payload)
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
census_data= pd.DataFrame(columns=colnames, data=datarows )
census_data = census_data.rename(columns=variables)

# Creating a new column called GEOID that is the concatenation of multiple columns and then setting that as an index. 
census_data["GEOID"] = census_data["state"]+census_data["county"]
census_data = census_data.set_index('GEOID')
output_folder = './outputs/'
census_data.to_csv(output_folder + 'census_data.csv')

#%%
#Repeating the previous steps for Census Tract-level data in NY. 
# Creating a dictionary to later change the names of columns to variables we're interested in.
variables = {'B02001_001E':'pop_total', 'B02001_002E':'pop_white', 'B25003_001E':'housing_total', 'B25003_002E':'housing_owned', 'B25003_003E':'housing_rental', 'B20002_001E':'med_income'}

# Creating a list of the keys in the dictionary just created and joining the keys with a comma.
var_list = variables.keys()
var_string = ",".join(var_list)

# Formatting the api, requesting data from the census, putting it into a pandas dataframe, handling missing numbers, and then using the dictionary variables to rename the relevant columns
api = "https://api.census.gov/data/2020/acs/acs5"
for_clause = 'tract:*'
in_clause = 'state:36 county:*'
payload = {'get':var_string, 'for':for_clause, 'in':in_clause}
response = requests.get(api, payload)
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
census_data_tract = pd.DataFrame(columns=colnames, data=datarows )
census_data_tract = census_data_tract.rename(columns=variables)

# Creating a new column called GEOID that is the concatenation of multiple columns and then setting that as an index. 
census_data_tract["GEOID"] = census_data_tract["state"]+census_data_tract["county"]+census_data_tract["tract"]
census_data_tract = census_data_tract.set_index('GEOID')

census_data_tract.to_csv(output_folder + 'census_data_tract.csv')