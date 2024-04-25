#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from splink.duckdb.linker import DuckDBLinker
from splink.duckdb.blocking_rule_library import block_on
import altair as alt
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl ## Hey they also have template functions

### Specify Parameters.
block_vars = {}
for ms in ['e','f','g','h','i','m','n','o']:
    block_vars[ms] = ['mailing_address_zipcode']
for ms in ['j','k','l','p','q','r']:
    block_vars[ms] = ['zip3']
for ms in ['s','t']:
    block_vars[ms] = ['age']
for ms in ['a','b','c','d','u','v']:
    block_vars[ms] = []

comp_vars = {}
comp_vars['a'] = ['ssn','ch4_last_name']
comp_vars['b'] = ['ssn']
comp_vars['c'] = ['ssn','ch4_last_name']
comp_vars['d'] = ['ssn4','last_name']
comp_vars['e'] = ['first_name','last_name','middle_initial']
comp_vars['f'] = ['first_name','last_name','mailing_address_street_name']
comp_vars['g'] = ['first_name','last_name','middle_name']
comp_vars['h'] = ['first_name','last_name','middle_initial']
comp_vars['i'] = ['ch2_first_name','last_name']
comp_vars['j'] = ['first_name','last_name','middle_name']
comp_vars['k'] = ['first_name','last_name','middle_name']
comp_vars['l'] = ['last_name','ch2_first_name']
comp_vars['m'] = ['last_name','first_name','age']
comp_vars['n'] = ['last_name','first_initial','mailing_address_street_name']
comp_vars['o'] = ['last_name','first_initial','age']
comp_vars['p'] = ['last_name','first_name','age']
comp_vars['q'] = ['last_name','first_initial','age']
comp_vars['q'] = ['last_name','first_name','age']
comp_vars['r'] = ['last_name','first_name','age']
comp_vars['s'] = ['last_name','ch2_first_name','zip3']
comp_vars['t'] = ['ch4_last_name','ch2_first_name','zip3']
comp_vars['u'] = ['last_name','ch2_first_name','middle_initial','age']
comp_vars['v'] = ['last_name','ch2_first_name','middle_initial','age']

comp_type = {}
for ms in ['a','b','d','e','f','j','m','n','p','q','u']:
    comp_type[ms] = 'exact'
for ms in ['c','g','h','i','k','l','o','r','s','t','v']:
    comp_type[ms] = 'fuzzy'

### Construct settings.
match_vars = {}
for ms in comp_vars:
    match_vars[ms] = block_vars[ms]+comp_vars[ms]

match_settings = {}
for ms in comp_vars:
    comps = []
    for v in comp_vars[ms]:
        if comp_type[ms]=='exact':
            comps.append(cl.exact_match(v, term_frequency_adjustments=True))
        elif comp_type[ms]=='fuzzy':
            if ms in ['c','v']:
                comps = [cl.exact_match('ch4_last_name', term_frequency_adjustments=True),
                        cl.damerau_levenshtein_at_thresholds('ssn', [1,2])
                        ]
            else:
                if 'name' in v:# ['first_name','last_name','mailing_address_street_name']
                    comps.append(ctl.name_comparison(v))
                elif 'initial' in v:
                    comps.append(cl.exact_match(v, term_frequency_adjustments=True))
                elif v in ['mailing_address_zipcode','zip3']:
                    comps.append(ctl.postcode_comparison(v))
                elif v=='age':
                    comps.append(cl.damerau_levenshtein_at_thresholds('age', [1]))
                else:
                    raise Exception("Unknown Fuzzy Strategy for variable "+v)
        else:
            raise Exception("Unknown comp_type "+comp_type[ms])

    blocks = []
    for v in block_vars[ms]:
        blocks.append(block_on(v))

    match_settings[ms] = {
        "link_type": "link_and_dedupe",
        "comparisons": comps,
        "retain_matching_columns": True,
        "retain_intermediate_calculation_columns": False,
    }
    if len(blocks)>0:
        match_settings[ms]['blocking_rules_to_generate_predictions'] = blocks
