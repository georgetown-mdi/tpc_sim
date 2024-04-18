#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  match_settings.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 04.18.2024

import pandas as pd
import numpy as np
from splink.duckdb.linker import DuckDBLinker
from splink.duckdb.blocking_rule_library import block_on
import altair as alt
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl ## Hey they also have template functions

### Specify Parameters.
block_vars = {}
for ms in ['e','f']:
    block_vars[ms] = ['mailing_address_zipcode']

comp_vars = {}
comp_vars['e'] = ['first_name','last_name','middle_initial']
comp_vars['f'] = ['first_name','last_name','mailing_address_street_name']

comp_type = {}
for ms in ['e','f']:
    comp_type[ms] = 'exact'

### Construct settings.
match_vars = {}
for ms in block_vars:
    match_vars[ms] = block_vars[ms]+comp_vars[ms]

match_settings = {}
for ms in block_vars:
    comps = []
    for v in comp_vars[ms]:
        if comp_type[ms]=='exact':
            comps.append(cl.exact_match(v, term_frequency_adjustments=True))

    blocks = []
    for v in block_vars[ms]:
        blocks.append(block_on(v))

    match_settings[ms] = {
        "link_type": "link_and_dedupe",
        "comparisons": comps,
        "blocking_rules_to_generate_predictions": blocks,
        "retain_matching_columns": True,
        "retain_intermediate_calculation_columns": False,
    }
