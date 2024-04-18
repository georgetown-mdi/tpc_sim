#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from splink.duckdb.linker import DuckDBLinker
from splink.duckdb.blocking_rule_library import block_on
import altair as alt
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl ## Hey they also have template functions
import string

from python.match_settings import match_vars, match_settings, block_vars, comp_vars

df1 = pd.read_csv('CT40_output3.csv')
df2 = pd.read_csv('./data/CT99_aug.csv')

## Add subset vars.
df1['ch2_first_name'] = [x[:2] if type(x)==str else x for x in df1['first_name']]
df2['ch2_first_name'] = [x[:2] if type(x)==str else x for x in df2['first_name']]

df1['first_initial'] = [x[:1] if type(x)==str else x for x in df1['first_name']]
df2['first_initial'] = [x[:1] if type(x)==str else x for x in df2['first_name']]

df1['ch4_last_name'] = [x[:4] if type(x)==str else x for x in df1['last_name']]
df2['ch4_last_name'] = [x[:4] if type(x)==str else x for x in df2['last_name']]

df1['zip3'] = [x[:3] if type(x)==str else x for x in df1['mailing_address_zipcode']]
df2['zip3'] = [x[:3] if type(x)==str else x for x in df2['mailing_address_zipcode']]

df1['ssn4'] = [x[-4:] if type(x)==str else x for x in df1['ssn']]
df2['ssn4'] = [x[-4:] if type(x)==str else x for x in df2['ssn']]

## Keep only subset cols
df1['unique_id'] = df1.index
df2['unique_id'] = df2.index

precs = {}
recls = {}
for ms in string.ascii_lowercase[4:22]:

    keepcols = ['unique_id'] + match_vars[ms]
    df1_sub = df1[keepcols]
    df2_sub = df2[keepcols]

    block_rule = block_on(block_vars[ms])

    settings = match_settings[ms]

    linker = DuckDBLinker([df1_sub, df2_sub], settings)

    ### Estimate parameters
    drs = "AND".join([' (l.'+v+' = r.'+v+') ' for v in match_vars[ms]])
    deterministic_rules = [drs]

    linker.estimate_probability_two_random_records_match(deterministic_rules, recall=0.7)
    linker.estimate_u_using_random_sampling(max_pairs=1e6)

    for v in comp_vars[ms]:
        training_blocking_rule = block_on([v])
        training_session_fname_sname = linker.estimate_parameters_using_expectation_maximisation(training_blocking_rule)

    ### Do actual matching.
    df_predictions = linker.predict(threshold_match_probability=0.1)
    mdf = df_predictions.as_pandas_dataframe()

    df1_key = df1[['simulant_id','unique_id']]
    df1_key = df1_key.rename(dict([(v,v+'_l') for v in df1_key]), axis = 1)
    mdf = mdf.merge(df1_key, on = 'unique_id_l')

    df2_key = df2[['simulant_id','unique_id']]
    df2_key = df2_key.rename(dict([(v,v+'_r') for v in df2_key]), axis = 1)
    mdf = mdf.merge(df2_key, on = 'unique_id_r')

    ### Evaluate
    num_correctly_matched = np.sum(mdf['simulant_id_l']==mdf['simulant_id_r'])
    num_matched = mdf.shape[0]
    num_incorrectly_matched = np.sum(mdf['simulant_id_l']!=mdf['simulant_id_r'])
    common_records = len(set(df1['simulant_id']).intersection(df2['simulant_id']))

    recall = num_correctly_matched/common_records
    precision = num_correctly_matched/num_matched

    precs[ms] = precision
    recls[ms] = recall
    print('------------------------')
    print(ms)
    print("Precision: %f"%precision)
    print("Recall: %f"%recall)
    print('------------------------')


