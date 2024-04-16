#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#  output3.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 04.09.2024


# This file is based on generate-data-english from the geco package.

print("Hey, this file has to be run in Python 2.7")

import pandas as pd
import sys
sys.path.insert(0,'./geco/')
#import os
#os.chdir('./geco')

import basefunctions  # Helper functions
import attrgenfunct   # Functions to generate independent attribute values
import contdepfunct   # Functions to generate dependent continuous attribute
                      # values
import generator      # Main classes to generate records and the data set
import corruptor      # Main classes to corrupt attribute values and records

import random
random.seed(42)  # Set seed for random generator, so data generation can be
                 # repeated

#unicode_encoding_used = 'ascii'
unicode_encoding_used = 'utf8'
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)

## Read in and format our data.
df = pd.read_csv('./CT40_output1.csv')
#s = df.loc[df['simulant_id']=='4561_947743','mailing_address_unit_number'].iloc[0]
df = df.applymap(lambda s: str(s).decode('ascii', errors='ignore'))
#df = df[['last_name','first_name','mailing_address_zipcode','mailing_address_city']]
df = df.drop(u'Unnamed: 0', axis = 1)
#col_orders = list(df.columns)
#df = df[sorted(df.columns)]
dd = df.to_dict(orient='index_names')
for v in dd:
    dd[v] = [str(dd[v][x]) for x in df.columns]
dd = dict([('rec-'+str(i)+'-org',dd[i]) for i in dd])

# -----------------------------------------------------------------------------
# Define how the generated records are to be corrupted (using methods from
# the corruptor.py module).

# For a value edit corruptor, the sum or the four probabilities given must
# be 1.0.
#
edit_corruptor = \
    corruptor.CorruptValueEdit(\
          position_function = corruptor.position_mod_normal,
          char_set_funct = basefunctions.char_set_ascii,
          insert_prob = 0.5,
          delete_prob = 0.5,
          substitute_prob = 0.0,
          transpose_prob = 0.0)

edit_corruptor2 = \
    corruptor.CorruptValueEdit(\
          position_function = corruptor.position_mod_uniform,
          char_set_funct = basefunctions.char_set_ascii,
          insert_prob = 0.25,
          delete_prob = 0.25,
          substitute_prob = 0.25,
          transpose_prob = 0.25)

surname_misspell_corruptor = \
    corruptor.CorruptCategoricalValue(\
          lookup_file_name = 'geco/lookup-files/surname-misspell.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

ocr_corruptor = corruptor.CorruptValueOCR(\
          position_function = corruptor.position_mod_normal,
          lookup_file_name = 'geco/lookup-files/ocr-variations.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

keyboard_corruptor = corruptor.CorruptValueKeyboard(\
          position_function = corruptor.position_mod_normal,
          row_prob = 0.5,
          col_prob = 0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(\
          lookup_file_name = 'geco/lookup-files/phonetic-variations.csv',
          has_header_line = False,
          unicode_encoding = unicode_encoding_used)

missing_val_corruptor = corruptor.CorruptMissingValue()

postcode_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_val='missing')

given_name_missing_val_corruptor = corruptor.CorruptMissingValue(\
       missing_value='unknown')

#attr_mod_prob_dictionary = {'first_name':0.25,'last_name':0.25,
#                            'mailing_address_zipcode':0.25,'mailing_address_city':0.25}
modp_dict = {}
modcols = list(df.columns)
modcols.remove('household_id')
modcols.remove('simulant_id')
for v in df.columns:
    if v in modcols:
        modp_dict[v] = 1./len(modcols)
    else:
        modp_dict[v] = 0.

fn_corrupt = [(0.1, edit_corruptor2),
            (0.1, ocr_corruptor),
            (0.1, keyboard_corruptor),
            (0.7, phonetic_corruptor)]
ln_corrupt = [(0.1, surname_misspell_corruptor),
            (0.1, ocr_corruptor),
            (0.1, keyboard_corruptor),
            (0.7, phonetic_corruptor)]
num_corrupt = [(0.8, keyboard_corruptor),
            (0.2, postcode_missing_val_corruptor)]
city_corrupt = [(0.1, edit_corruptor),
            (0.1, missing_val_corruptor),
            (0.4, keyboard_corruptor),
            (0.4, phonetic_corruptor)]


modt_dict = {
        'first_name':fn_corrupt,
        'middle_name':fn_corrupt,
        'last_name':ln_corrupt,
        'ssn':num_corrupt,
        'mailing_address_street_number':num_corrupt,
        'mailing_address_street_name':fn_corrupt,
        'mailing_address_unit_number':num_corrupt,
        'mailing_address_po_box':num_corrupt,
        'mailing_address_city':city_corrupt,
        'mailing_address_state':city_corrupt,
        'mailing_address_zipcode':num_corrupt,
        }

cols = list(df.columns)

# Nothing to change here - set-up the data set corruption object
#
test_data_corruptor = corruptor.CorruptDataSet(number_of_org_records = df.shape[0],
                                          number_of_mod_records = df.shape[0],
                                          max_num_dup_per_rec = 1,
                                          num_dup_dist = 'zipf',
                                          attribute_name_list = cols,
                                          max_num_mod_per_attr =  1,
                                          num_mod_per_rec =  1,
                                          attr_mod_prob_dict = modp_dict,
                                          attr_mod_data_dict = modt_dict)

# =============================================================================
# No need to change anything below here

# Start the data generation process
#
# Corrupt (modify) the original records into duplicate records
#
test_data_corruptor.corrupt_records(dd)

outdd = dict([(v,dd[v]) for v in dd if v.split('-')[2]=='dup'])
#for v in outdd:
#    outdd[v] = [str(x) for x in zip(cols, outdd[v])]

df_out = pd.DataFrame.from_dict(outdd, orient = 'index')
df_out.columns = df.columns
#df_out = df_out[col_orders]
df_out.index = [int(x.split('-')[1]) for x in df_out.index] 
df_out = df_out.sort_index()

#import numpy as np
#np.where(np.array(df_out['mailing_address_city']) != np.array(df['mailing_address_city']))[0][0]

df_out.to_csv('CT40_output3.csv', index = False)

