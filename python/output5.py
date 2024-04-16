#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.read_csv('CT40_output2.csv')

# Drop most columns
#df = df[['first_name','middle_initial','last_name','ssn','mailing_address_street_number','mailing_address_street_name','mailing_address_unit_number','mailing_address_po_box','mailing_address_city','mailing_address_state','mailing_address_zipcode']]

# Keep personal identifiers (columns A-N) and Dependents 1-2 (columns S-X)
#df = df.drop(['spouse_first_name','spouse_middle_initial','spouse_last_name','spouse_ssn'], axis = 1)
# Drop all columns with spouse or dependent 3/4 in them.
df = df.drop([x for x in df.columns if 'spouse' in x or any(['dependent_'+str(i) in x for i in [3,4]])], axis = 1)
df = df.drop('tax_year', axis = 1)

# Create DOB variable (character string)
possible_dates = pd.date_range('01-01-1950', '01-01-2000').date
df['DOB'] = np.random.choice(possible_dates, df.shape[0], replace = True).astype(str)

# Concatenate address fields to create “Street Address” combining columns H-I-J-K
df['Street Address'] = df['mailing_address_street_number'] + ' ' + df['mailing_address_street_name'] + ' ' + df['mailing_address_unit_number'].fillna('') + df['mailing_address_po_box'].fillna('')
df['Street Address'] = df['Street Address'].apply(lambda x: ' '.join(x.split()).title() if type(x)==str else x) # Gets rid of multiple subsequent spaces.

# Create Parent flag (values custodial parent, noncustodial parent) where 60% are custodial parents
# Q1
df['Parent'] = np.random.choice(['Custodial','Noncustodial'], df.shape[0], replace = True)

# Create Public Benefits flag (0/1) where 70% of sample =1
df['Public Benefits'] = np.random.choice([0,1], df.shape[0], replace = True, p = [0.3, 0.7])

# Create Treatment indicator (values 0, 1, 2) assigning 20% to value 0, 50% to value 1, and 30% to value 2 
df['Treatment'] = np.random.choice([0,1,2], df.shape[0], replace = True, p = [0.2,0.5,0.3])

df.to_csv('CT40_output.csv', index = False)
