#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import string


df = pd.read_csv('data/CT40.csv')
df = df.iloc[:,:14]

#midnames = np.array(pd.read_csv('data/MOCK_DATA.csv').iloc[:,0])
midnames = list(set(df['first_name']))
middict = {}
for i in list(string.ascii_uppercase):
    #middict[i] = [x for x in midnames if type(x)==str and (x[0]).upper==i]
    middict[i] = [x for x in midnames if type(x)==str and x[0]==i]
#midnames = np.tile(midnames,10)

#df['middle_initial'] = midnames
df.insert(4, column='middle_name', value= np.nan)
for i in range(df.shape[0]):
    if np.random.choice([0,1])==1:
        mi = df.loc[i,'middle_initial']
        if type(mi)==str and (mi in string.ascii_uppercase):
            df.loc[i,'middle_name'] = np.random.choice(middict[mi])
            df.loc[i,'middle_initial'] = np.nan

#df['middle_initial'] = midnames
#df = df.rename({'middle_initial' : 'middle_name'}, axis = 1)

df.to_csv('CT40_output1.csv', index = False)
