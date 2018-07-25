# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:29:34 2018

@author: mayur
"""

import os
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import urllib.parse
from nltk.corpus import stopwords

##... initial consts
BASE_URL = 'http://api.dbpedia-spotlight.org/en/annotate?text={text}&confidence={confidence}&support={support}'
path = '/Users/mayur/Documents/GitHub/Stateoftheunion/stateoftheunion_data/' 
##"E:/mayur/Stateoftheunion/stateoftheunion_data/"
all_files = os.listdir(path)
os.chdir('/Users/mayur/Documents/GitHub/Stateoftheunion/stateoftheunion_code/')
from retry import *

keywordlist = list()
os.chdir(path)

from retry import *

for j in range(len(all_files)):
    with open(all_files[j], encoding = 'utf8') as fd:
         Text = fd.read()
             
    len_text = len(Text)
    size = int(len_text/10)
    all_keywords = list()
    size1 = size +20
    
    
    for i in range(0,len_text,size):
        TEXT = Text[i:i+size1]
        if len(TEXT)>100:
    
            CONFIDENCE = '0.5'
            SUPPORT = '50'
        
        
            ###... Below three lines can be used to remove stop words and then join again
            ###... to form a string for processing urls
            
            #Text = Text.split()
            #Text1 = [word for word in Text if word not in stopwords.words('english')]
            #TEXT = ' '.join(Text1)
            
            ###... REQUEST is prepping the above text to be sent as an search url. Increasing
            ###... confidence decreases the number of key words extracted, less confidence gives
            ###... noisy or unwanted keywords
        
            REQUEST = BASE_URL.format(
                    text=urllib.parse.quote_plus(TEXT), 
                confidence=CONFIDENCE, 
                support=SUPPORT
                )
            HEADERS = {'Accept': 'application/json'}
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            
            ###... All the urls which are to be used for mining data from DBpedia are stored
            ###... in the all_urls
            
            all_urls = []
            
            r = retried_func(url = REQUEST, headers=HEADERS)
            #r = requests.get(url = REQUEST , headers=HEADERS)
            response = r.json()
            resources = response['Resources']
            
            ###... storing all the urls in resources in all_urls and then formatting them 
            ###... into a string named 'values' to be passed into the sparql query
            
            for res in resources:
                all_urls.append(res['@URI'])
            
            
                
            values = '(<{0}>)'.format('>) (<'.join(all_urls))
            
            sparql.setQuery(
                """PREFIX vrank:<http://purl.org/voc/vrank#>
                   SELECT DISTINCT ?l ?rank ?sname
                   FROM <http://dbpedia.org> 
                   FROM <http://people.aifb.kit.edu/ath/#DBpedia_PageRank>
                   WHERE {
                       VALUES (?s) {""" + values + 
                """    }
                   ?s rdf:type ?p .
                   ?p rdfs:label ?l.
                    ?s dct:subject ?sub .
                       ?sub rdfs:label ?sname.
                   FILTER (lang(?l) = 'en')
                } order by ?rank limit 3
                       
                    """)
            
            ###... The above sparql query extracts the following details:
            ###... ?s gives resource of the url,
            ###... ?p is type/ontology of resource ?s
            ###... ?l is the label of the ontology class of ?p
            ###... ?sub gives the subject of the resource and ?sname its label 
            ###... Thus, in all, we extract the labels of ontology classes and its subjects
            
            
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
                
            
            for result in results["results"]["bindings"]:
                all_keywords.append( result['l']['value'])
                
            for result in results["results"]["bindings"]:
                all_keywords.append( result['sname']['value'])
                
            #print (y).
            #print(x)
                    
            #item = list()
            for res in resources:
                all_keywords.append(res['@surfaceForm'])
                
    unique_keywords = set(all_keywords)
    #print(unique_keywords)
    keywordlist.append([])
    [keywordlist[j].append(x) for x in unique_keywords]
    
    print(len(all_keywords))
    print(len(unique_keywords))


import pandas as pd      
Result_df= pd.DataFrame(columns = ['FileNames', 'President', 'Year' , 'KeyWords'])
Result_df['FileNames']= all_files

presidents = list()
year = list()
for i in range(29):
    presidents.append(all_files[i][:-9])
    temp_year = all_files[i][-8:]
    year.append(temp_year[:-4])
    
Result_df['President']= presidents
Result_df['Year']= year
Result_df['KeyWords']= keywordlist

Result_df.sort_values('Year', inplace = True)
os.chdir('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/')
Result_df.to_csv('Results1.csv', encoding = 'utf-8')











    
