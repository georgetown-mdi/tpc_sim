#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('data/CT40.csv')

# Determine the number of records to blank (20% of total records)
num_records_to_blank = int(len(df) * 0.2)

# Select 20% of the SSN records randomly and blank them
ssn_records_to_blank = np.random.choice(df[df['ssn'].notnull()].index, num_records_to_blank, replace=False)
df.loc[ssn_records_to_blank, 'ssn'] = np.nan

# Determine the number of remaining SSN records with noo-zero values. 
remaining_ssn_records = df['ssn'].count()

# Determine the number of SSN records to corrupt (5% of remaining records)
num_ssn_records_to_corrupt = int(remaining_ssn_records * 0.05)

# Select 5% of the remaining SSN records randomly
ssn_records_to_corrupt = np.random.choice(df[df['ssn'].notnull()].index, num_ssn_records_to_corrupt, replace=False)

# Corrupt the selected SSN records with '000-00-0000' or '999-99-9999' or just drop one random character (including -), with 1/3% probability each
for index in ssn_records_to_corrupt:
    u = np.random.rand()
    if u < 1./3.:
        df.at[index, 'ssn'] = '000-00-0000'
    elif u < 2./3.:
        df.at[index, 'ssn'] = '999-99-9999'
    else:
        dropind = np.random.choice(11, 1)[0]
        s = df.at[index, 'ssn']
        df.at[index, 'ssn'] = s[:dropind] + s[(dropind+1):]

df.to_csv('CT40_output2.csv', index=False)
