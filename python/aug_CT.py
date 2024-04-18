#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import string
import numpy as np

np.random.seed(123)

df40 = pd.read_csv('data/CT40.csv')
df99 = pd.read_csv('data/CT99.csv')

df40 = df40.drop('Unnamed: 0', axis = 1)
df99 = df99.drop('Unnamed: 0', axis = 1)

#midnames = np.array(pd.read_csv('data/MOCK_DATA.csv').iloc[:,0])
midnames = list(set(df40['first_name']))
middict = {}
for i in list(string.ascii_uppercase):
    #middict[i] = [x for x in midnames if type(x)==str and (x[0]).upper==i]
    middict[i] = [x for x in midnames if type(x)==str and x[0]==i]
#midnames = np.tile(midnames,10)

#df['middle_initial'] = midnames
toins = np.where(df40.columns=='middle_initial')[0][0]
df40.insert(toins+1, column='middle_name', value= np.nan)
toins = np.where(df99.columns=='middle_initial')[0][0]
df99.insert(toins+1, column='middle_name', value= np.nan)

toins = np.where(df40.columns=='ssn')[0][0]
df40.insert(toins+1, column='dob', value= np.nan)
toins = np.where(df99.columns=='ssn')[0][0]
df99.insert(toins+1, column='dob', value= np.nan)

## Add some stuff.
possible_dates = pd.date_range('01-01-1950', '01-01-2000').date
for i in range(df40.shape[0]):
    sid = df40.loc[i,'simulant_id']
    has99 = np.sum(sid==df99['simulant_id']) > 0
    if has99:
        where99 = df99['simulant_id']==sid

    ## Middle name.
    mi = df40.loc[i,'middle_initial']
    if type(mi)==str and (mi in string.ascii_uppercase):
        mn = np.random.choice(middict[mi])
        df40.loc[i,'middle_name'] = mn
        #df40.loc[i,'middle_name'] = mn
        if has99:
            df99.loc[where99,'middle_name'] = mn

    ## DOB
    dob = np.random.choice(possible_dates, 1).astype(str)[0]
    df40.loc[i,'dob'] = dob
    if has99:
        df99.loc[where99,'dob'] = dob

df40.to_csv('data/CT40_aug.csv')
df99.to_csv('data/CT99_aug.csv')

#i = 2
#df99.loc[df99['simulant_id']==df40.loc[i,'simulant_id'],'middle_name']
#df40.loc[i,'middle_name']
