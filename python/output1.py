#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import string

df = pd.read_csv('data/CT40_aug.csv')
df = df.iloc[:,:16]

for i in range(df.shape[0]):
    if np.random.choice([0,1])==1:
        df.loc[i,'middle_name'] = np.nan
    else:
        df.loc[i,'middle_initial'] = np.nan

df.to_csv('CT40_output1.csv', index = False)
