#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.read_csv('CT40_output2.csv')

# Keep ids, FN, LN, SSN, Spouse SSN, Dependent SSN(s), Zip code (columns A, B, C, D, F, G, N, R, U, X, AA)
keepvars = ['simulant_id','first_name','last_name','ssn', 'spouse_ssn']
keepvars += ['dependent_'+str(i)+'_ssn' for i in range(1,5)] 
keepvars += ['mailing_address_zipcode']
df = df[keepvars]

# Create Program variable=GetCTC
df['Program'] = 'GetCTC'

# Create Year variables and assign among (2021, 2022)
df['Year'] = np.random.choice([2021,2022], df.shape[0], replace=True)

# Create Status variable with values (Started, Submitted, Accepted, Other) with lower assignment of Other
df['Status'] = np.random.choice(['Started','Submitted','Accepted','Other'], df.shape[0], replace=True, p = [0.3,0.3,0.3,0.1])

# Create EITC_elig variable (0/1)
df['EITC_elig'] = np.random.choice([0,1], df.shape[0], replace=True)

# Create EITC_option variable (0/1) concentrating value=1 to EITC_elig=1
df['EITC_option'] = np.random.choice([0,1], df.shape[0], replace=True)*df['EITC_elig']

# Create EITC_claim variable (0/1) concentrating value=1 to EITC_elig=1
df['EITC_claim'] = np.random.choice([0,1], df.shape[0], replace=True)*df['EITC_elig']

# Create StartDate variable assigning values 01022021-04152021 for Year=2021 and values 01022022-04152022 for Year=2022
is2021 = df['Year']==2021
df.loc[is2021,'StartDate'] = np.random.choice(pd.date_range('01-02-2021', '04-14-2021'), int(np.sum(is2021)), replace = True)

is2022 = df['Year']==2022
df.loc[is2022,'StartDate'] = np.random.choice(pd.date_range('01-02-2022', '04-15-2022'), int(np.sum(is2022)), replace = True)

# Create Source variable indicating outreach source code (values 1, 2, 3, 4)
df['Source'] = np.random.choice([1,2,3,4], df.shape[0], replace=True)

# Create BasicInfo variable indicating client completed primary/spouse basic info (0/1) assigning value=0 to records lacking SSN and Name info
df['BasicInfo'] = ~df['first_name'].isna() & ~df['last_name'].isna() & ~df['ssn'].isna() & ~df['spouse_ssn'].isna()
df['BasicInfo'] = df['BasicInfo'].astype(int)
print(np.sum(df['BasicInfo']))

# Create Complete variable indicating that client completed all return information (0/1) assigning value=0 to records where BasicInfo=0 and to records lacking zip code
df['Complete'] = (df['BasicInfo']==1)  & ~df['mailing_address_zipcode'].isna()
df['Complete'] = df['Complete'].astype(int)
print(np.sum(df['Complete']))

# Create ClickSubmit variable (0/1) where 60% of sample has value=1
df['ClickSubmit'] = np.random.choice([0,1], df.shape[0], replace=True, p = [0.4, 0.6])

# Create SubmitIRS variable (0/1) to 80% of records where ClickSubmit=1 
df['SubmitIRS'] = np.random.choice([0,1], df.shape[0], replace=True, p = [0.2, 0.8])

df.to_csv('output7.csv', index = False)
