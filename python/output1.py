#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.read_csv('data/CT40.csv')
df = df.iloc[:,:14]

midnames = np.array(pd.read_csv('data/MOCK_DATA.csv').iloc[:,0])
midnames = np.tile(midnames,10)

df['middle_initial'] = midnames
df = df.rename({'middle_initial' : 'middle_name'}, axis = 1)

df.to_csv('output1.csv', index = False)
