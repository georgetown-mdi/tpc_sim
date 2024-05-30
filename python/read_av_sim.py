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

from python.match_settings import match_vars, match_settings, block_vars, comp_vars

#df1 = pd.read('CT40_output3')
#df1_targs = ['CT40_output3', 'CT40_output2']
df1_targs = ['CT40_output2', 'CT40_output3']
df2_targs = ['CT99_aug', 'CT40_aug']

res = {}
dyads = []
for df1t in df1_targs:
    for df2t in df2_targs:
        dyad = df1t+"_to_"+df2t
        dyads.append(dyad)
        with open("pickles/"+dyad+".pkl", 'rb') as f:
            #res[dyad] = precs, recls, exec_time = pickle.load(f)
            res[dyad] = pd.DataFrame(pickle.load(f)).T
            res[dyad].columns = ['Precision','Recall','Time (s)']

#plt.figure(figsize=[8,8])
plt.figure(figsize=[6,6])
for dy, dyad in enumerate(dyads):
    plt.subplot(2,2,dy+1)
    df = res[dyad]
    mask = paretoset(df[["Precision","Recall"]], sense=["max", "max"])
    pset = [v for i,v in enumerate(df.index) if mask[i]]

    plt.scatter(x = df['Precision'], y = df['Recall'], alpha = 0.)
    #plt.scatter(x = df.loc[mask, 'Precision'], y = df.loc[mask, 'Recall'], alpha = 1.)

    for v in df.index:
        if v in pset:
            col = 'orange'
        else:
            col = 'black'
        plt.text(x = df.loc[v,'Precision'], y = df.loc[v,'Recall'], s =v, color =col, fontdict = {'weight':'bold'})
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    #plt.title(dyad)
    plt.title("Task %d"%(dy+1))
    #plt.scatter(x = df['Precision'], y = df['Recall'])
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
    plt.ylabel("Execution Time")
    plt.xlabel("Linkage Strategy")
    #plt.title(dyad)
    plt.title("Task %d"%(dy+1))
plt.tight_layout()
plt.savefig("exec_time.pdf")
plt.close()
