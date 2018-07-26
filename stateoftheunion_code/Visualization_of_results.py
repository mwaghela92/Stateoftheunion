#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:17:54 2018

@author: mayur
"""

import pandas as pd
import ast
from collections import Counter
import seaborn as sns

#path for mayur's macbook
#Results = pd.read_csv('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/Results1.csv')
#path for server
Results = pd.read_csv('E:/mayur/State of the union/Stateoftheunion/Results/Results1.csv')



Results['KeyWords'] = Results['KeyWords'].apply(
        lambda x: ast.literal_eval(x))

# Creating an empty list to store keywords
list_keywords = list()

# Iterating to combine all keywords in one list
for idx, val in enumerate(Results['KeyWords']):
    list_keywords.extend(Results.loc[idx, 'KeyWords'])


##... findig unique keywords and their lengths.
unique_keywords = set(list_keywords)
print( 'Length of unique keywords: ' , len(unique_keywords))
print ('Length of all key words list: ', len(list_keywords))


##... Frequency count of keywords
counter_keywords = Counter(list_keywords)
print (counter_keywords.most_common(50))

##... removing non value adding keywords from 50 most common ones
##... keywords identified for removal: 1.	Person 2.	Place 3.	Populated place
##... 4.	Agent 5.	Organisation 6.	Office holder 7.	Work

non_value_keywords= [ 'country', 'person', 'place', 'populated place', 'agent', 'organisation' , 'Office holder', 'Work']
filtered_keywords = list()
[filtered_keywords.append(x) for x in list_keywords if x not in non_value_keywords ]


counter_filtered_keywords = Counter(filtered_keywords)
print (counter_filtered_keywords.most_common(30))

sns.set(style = 'darkgrid')
filtered_keyword_plot = sns.countplot(filtered_keywords)