#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:17:54 2018.

@author: mayur
"""

import pandas as pd
import ast
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

#path for mayur's macbook
#Results = pd.read_csv('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/Results1.csv')
#path for server
Results = pd.read_csv('E:/mayur/State of the union/Stateoftheunion/Results/'+
                      'Results4_withoutbroader_withresources.csv')
pp = PdfPages("Plotswith2charts.pdf")


Results['KeyWords'] = Results['KeyWords'].apply(
        lambda x: ast.literal_eval(x))
Results['Resources'] = Results['Resources'].apply(
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
    most_common_df.sort_values('Frequency', inplace = True, ascending = False)
    return most_common_df

def resourcefilter(resources):
    counter_resources = Counter(resources)
    resources, count = zip(*counter_resources.items())
    most_common_df = pd.DataFrame(columns = ['Resources', 'Count'])
    most_common_df['Resources'] = resources
    most_common_df['Count'] = count
    most_common_df.sort_values('Count', inplace = True, ascending = False)
    return most_common_df
    


def plotgraph(pp, most_common_df1,  most_common_df2, president, year):
    sns.set(style = 'darkgrid')
    #sns.set_context({"figure.figsize": (5, 5)})
    plt.subplot(1,2,1)
    my_plot = sns.barplot(x = 'Frequency', y = 'KeyWords', data =most_common_df1  )   
    plt.title(" Keywords " + str(president) + " " + str(year) )
    
    plt.subplot(1,2,2)
    my_plot = sns.barplot(x = 'Count', y = 'Resources', data =most_common_df2  )   
    plt.title(" Resources " + str(president) + " " + str(year) )
    
    
    pp.savefig(bbox_inches = 'tight')
    #return x


##path of mayur's macbook
#os.chdir('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/')

##path for server
os.chdir('E:/mayur/State of the union/Stateoftheunion/Results/')

for i in range(len(Results)):
    #i = 0
    a = filter(Results.iloc[i,4])
    b = resourcefilter(Results.iloc[i,5])
    plotgraph(pp, a[:20], b[:20] , Results.loc[i,'President'] , Results.loc[i,'Year' ])
    
pp.close()
 
    
    
    

    
    
    



