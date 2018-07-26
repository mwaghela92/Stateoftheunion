#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:17:54 2018

@author: mayur
"""

import pandas as pd
import ast
Results = pd.read_csv('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/Results1.csv')

Results['KeyWords'] = Results['KeyWords'].apply(
        lambda x: ast.literal_eval(x))

# Creating an empty list to store ingredients
list_keywords = list()

    # Iterating to combine all ingredients in one list
for idx, val in enumerate(Results['KeyWords']):
    list_keywords.extend(Results.loc[idx, 'KeyWords'])

unique_keywords = set(list_keywords)
len(unique_keywords)