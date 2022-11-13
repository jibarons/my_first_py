# Libraries
import numpy as np
import pandas as pd
import re

# Get data
hh_data = pd.read_csv('..\\data\\opt_msna22_data_raw.csv', low_memory = False)


hh_data = hh_data[0:7514] # remove aberrant last line

# Exploration
list(hh_data.columns)

## Descriptive sample
# region sample
pd.crosstab(index=hh_data['region'], columns="count")# base py: hh_data.value_counts(['region'])
# region + strata sample
pd.crosstab(
  index=hh_data['strata'], columns=hh_data['region'], 
  margins=True, margins_name="Total"
)

# Create storage df
indicators_df = hh_data['X_uuid']

# Demography indicators ####

## Gender of the head of household ####
indicators_df['hoh_gender'] = np.where(
  hh_data['hhh'] == 'yes', hh_data['gender_respondent'], hh_data['gender_hhh']
)

## Dependency ratio ####

i_dep_ratio = hh_data[[
  'X_uuid',
  'hh_size_boys_0_4', 'hh_size_girls_0_4',
  'hh_size_boys_5_10', 'hh_size_girls_5_10',
  'hh_size_boys_11_15', 'hh_size_girls_11_15',
  'hh_size_boys_16_17', 'hh_size_girls_16_17',
  'hh_size_men_18.29', 'hh_size_women_18.29',
  'hh_size_men_30_64', 'hh_size_women_30_64',
  'hh_size_men_65', 'hh_size_women_65'
]]
# Rename to fix gender age pattern
i_dep_ratio.rename(columns={
  'hh_size_boys_0_4': 'boys-0_4', 
  'hh_size_girls_0_4': 'girls-0_4',
  'hh_size_boys_5_10': 'boys-5_10', 
  'hh_size_girls_5_10': 'girls-5_10',
  'hh_size_boys_11_15': 'boys-11_15', 
  'hh_size_girls_11_15': 'girls-11_15',
  'hh_size_boys_16_17': 'boys-16_17', 
  'hh_size_girls_16_17': 'girls-16_17',
  'hh_size_men_18.29': 'men-18_29', 
  'hh_size_women_18.29': 'women-18_29',
  'hh_size_men_30_64': 'men-30_64', 
  'hh_size_women_30_64': 'women-30_64',
  'hh_size_men_65': 'men-65', 
  'hh_size_women_65': 'women-65'
}, inplace=True)
# Get var names to unpivot
dep_ratio_vars = list(i_dep_ratio.columns[1:len(i_dep_ratio.columns)])
# Get stub names
groups = [re.sub("^(.+)\-(.+)$", "\\1", v) for v in dep_ratio_vars]
# Un pivot
i_dep_ratio = (pd.wide_to_long(
  i_dep_ratio, #, 
  stubnames = list(set(groups)),
  i = 'X_uuid', j = 'age', sep='-', suffix='.+'
)
.stack()
.reset_index(name='num')
.rename(columns={'index':'cat', 'level_2':'gender'})
)

# Distanace to hospita recat

# Set list of conditions
condlist = ([
  (hh_data.distance_hospital < 5),#.fillna(False),
  hh_data.distance_hospital.between(5, 10, inclusive='left'),#.fillna(False),
  hh_data.distance_hospital.between(10, 15, inclusive='left'),#.fillna(False),
  (hh_data.distance_hospital > 15)#.fillna(False)
])

# Set list of corresponding choices
choicelist = ["less_than_5km", "between_5_10km", "between_10_15km", "more_than_15km"]
# recode variable
i_dist_hospital_cat = np.select(condlist, choicelist, np.nan)


