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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages as pp
import os

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
"""
non_value_keywords= [ 'country', 'person', 'place', 'populated place', 'agent', 'organisation' , 'Office holder', 'Work']
filtered_keywords = list()
[filtered_keywords.append(x) for x in list_keywords if x not in non_value_keywords ]


counter_filtered_keywords = Counter(filtered_keywords)
freq= list()
x =  (counter_filtered_keywords.most_common(30))


most_common_filtered_keywords = list()
for i,j in x:
    most_common_filtered_keywords.append(i)  
for i,j in x:
    freq.append(j)
most_common_df = pd.DataFrame(columns = ['KeyWords', 'Frequency'])
most_common_df['KeyWords'] = most_common_filtered_keywords
most_common_df['Frequency'] = freq

sns.set(style = 'darkgrid')
sns.barplot(x = 'Frequency', y = 'KeyWords', data =most_common_df  )
"""
def filter(list_keywords):
    #list_keywords = list_keywords.apply(
     #   lambda x: ast.literal_eval(x))
    non_value_keywords= [ 'country', 'person', 'place', 'populated place', 'agent', 'organisation' , 'Office holder', 'Work']
    filtered_keywords = list()
    [filtered_keywords.append(x) for x in list_keywords if x not in non_value_keywords ]
    counter_filtered_keywords = Counter(filtered_keywords)
    keywords, count = zip(*counter_filtered_keywords.items())
    most_common_df = pd.DataFrame(columns = ['KeyWords', 'Frequency'])
    most_common_df['KeyWords'] = keywords
    most_common_df['Frequency'] = count
    most_common_df.sort_values('Frequency')
    return most_common_df[:5]


def plotgraph(pp, most_common_df):
    sns.set(style = 'darkgrid')
    my_plot = sns.barplot(x = 'Frequency', y = 'KeyWords', data =most_common_df  )   
    ##path of mayur's macbook
    #plt.savefig('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/my')
    ##path for server
    pp.savefig()
    #return x


##path of mayur's macbook
#os.chdir('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/')

##path for server
os.chdir('E:/mayur/State of the union/Stateoftheunion/Results/')
pp = PdfPages("Plots.pdf")
for i in range(len(Results)):
    a = filter(Results.iloc[i,4])
    plotgraph(pp, a)
    
pp.close()


    
    
    
    
    
    
    
    
    
    



