#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  read_av_sim.py Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 04.22.2024

import pandas as pd
import numpy as np
from splink.duckdb.linker import DuckDBLinker
from splink.duckdb.blocking_rule_library import block_on
import altair as alt
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl ## Hey they also have template functions
import string
from time import time
import pickle
import matplotlib.pyplot as plt
from paretoset import paretoset
from adjustText import adjust_text

from python.match_settings import match_vars, match_settings, block_vars, comp_vars
import pandas as pd

#mode = 'fastLink_default'
mode = 'fastLink_splink'
#mode = 'splink'
assert mode in ['fastLink_default','fastLink_splink','splink']

#df1 = pd.read('CT40_output3')
#df1_targs = ['CT40_output3', 'CT40_output2']
df1_targs = ['CT40_output2', 'CT40_output3']
#df2_targs = ['CT99_aug', 'CT40_aug']
df2_targs = ['CT99_aug', 'CT40_aug']
#df1_targs = ['CT40_output3']
#df2_targs = ['CT99_aug']

adjust = False

res = {}
dyads = []
for df1t in df1_targs:
    for df2t in df2_targs:
        dyad = df1t+"_to_"+df2t
        dyads.append(dyad)
        if 'fastLink' in mode:
            suf = mode.split('_')[1]
            #res[dyad] = pd.read_csv('sim_out/match_av_'+df1t + '_' + df2t + '_'+suf+'.csv', index_col = 0)
            res[dyad] = pd.read_csv('sim_out/fastLink_'+df1t + '_' + df2t + '_'+suf+'.csv', index_col = 0)
            res[dyad].columns = ['Precision','Recall','Time (s)']
        elif mode=='splink':
            with open("pickles/"+dyad+".pkl", 'rb') as f:
                #res[dyad] = precs, recls, exec_time = pickle.load(f)
                res[dyad] = pd.DataFrame(pickle.load(f)).T
                res[dyad].columns = ['Precision','Recall','Time (s)']
        else:
            raise Exception("Unknown mode.")

#plt.figure(figsize=[8,8])
plt.figure(figsize=[6,6])
for dy, dyad in enumerate(dyads):
    print(dyad)
    plt.subplot(2,2,dy+1)
    df = res[dyad]
    mask = paretoset(df[["Precision","Recall"]], sense=["max", "max"])
    pset = [v for i,v in enumerate(df.index) if mask[i]]

    plt.scatter(x = df['Precision'], y = df['Recall'], alpha = 0.)
    #plt.scatter(x = df.loc[mask, 'Precision'], y = df.loc[mask, 'Recall'], alpha = 1.)

    print(dyad)
    print(pset)

    reorder = [x for x in df.index if not x in pset] + pset

    texts = []
    for v in reorder:
        if v in pset:
            col = 'orange'
            print(v)
        else:
            col = 'black'
        #txt = plt.text(x = df.loc[v,'Precision'], y = df.loc[v,'Recall'], s =v, color =col, fontdict = {'weight':'bold'})
        txt = plt.text(x = df.loc[v,'Precision'], y = df.loc[v,'Recall'], s =v.upper(), color =col, fontdict = {'weight':'bold'})
        texts.append(txt)
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    #plt.title(dyad)
    plt.title("Task %d"%(dy+1))
    #plt.scatter(x = df['Precision'], y = df['Recall'])
    if adjust:
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color='blue', lw=2,alpha=0))
plt.tight_layout()
plt.savefig("paretto.pdf")
plt.close()

plt.figure(figsize=[8,8])
fig = plt.figure()
for dy, dyad in enumerate(dyads):
    plt.subplot(2,2,dy+1)
    df = res[dyad]
    df = df.copy()
    hasna = np.any(np.isnan(df), axis = 1)
    df.loc[hasna,'Time (s)'] = -500
    plt.bar(df.index, df['Time (s)'])
    plt.ylabel("Execution Time (s)")
    plt.xlabel("Match Pass")
    #plt.yscale('log')
    #plt.title(dyad)
    plt.title("Task %d"%(dy+1))
plt.tight_layout()
plt.savefig("exec_time.pdf")
plt.close()

dfs_2_tasks = {
        'CT40_output2_to_CT99_aug' : 'Task 1',
        'CT40_output2_to_CT40_aug' : 'Task 2',
        'CT40_output3_to_CT99_aug' : 'Task 3',
        'CT40_output3_to_CT40_aug' : 'Task 4'
        }

#with pd.ExcelWriter('av_results.xlsx') as xcf:
#    for v in dfs_2_tasks:
#        res[v].to_excel(xcf, sheet_name = dfs_2_tasks[v])
#
#
## What proportion of people had 1099s?
#df1 = pd.read_csv('data/CT99_aug.csv', index_col = 0)
#df2 = pd.read_csv('data/CT40_aug.csv', index_col = 0)

#set(df1['simulant_id']).intersection(set(df2['simulant_id']))
