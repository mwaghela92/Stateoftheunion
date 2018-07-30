# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:29:34 2018

@author: mayur
"""

import os
from SPARQLWrapper import SPARQLWrapper, JSON
#import requests
import urllib.parse
#from nltk.corpus import stopwords
import pandas as pd  
import time
import datetime


##... initial consts
BASE_URL = 'http://api.dbpedia-spotlight.org/en/annotate?text={text}&confidence={confidence}&support={support}'


## paths for Mayur's macbook
"""
path = '/Users/mayur/Documents/GitHub/Stateoftheunion/stateoftheunion_data/' 
all_files = os.listdir(path)
os.chdir('/Users/mayur/Documents/GitHub/Stateoftheunion/stateoftheunion_code/')
"""

### paths for server
path = 'E:/mayur/State of the union/Stateoftheunion/stateoftheunion_data'
all_files = os.listdir(path)
os.chdir('E:/mayur/State of the union/Stateoftheunion/stateoftheunion_code')



from retry import *

##... 
keywordlist = list() 
all_keywords_list = list()
all_resources_list = list()

os.chdir(path)

from retry import *

for j in range(len(all_files)):
#for j in range(3):
    keywordlist_iter = list()
    all_resources = list()
    with open(all_files[j], encoding = 'utf8') as fd:
         Text = fd.read()
             
    len_text = len(Text)
    size = int(len_text/20)
    all_keywords = list()
    size1 = size +10
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Starting of loop "+ str(j)+ "\n\n")
    
    for i in range(0,len_text,size):
        
        StartReadTime = time.time()
        
        TEXT = Text[i:i+size1]
        if len(TEXT)>40:
    
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
                   SELECT DISTINCT ?sname
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
                }  
                
                       
                    """)
            
            ###... The above sparql query extracts the following details:
            ###... ?s gives resource of the url,
            ###... ?p is type/ontology of resource ?s
            ###... ?l is the label of the ontology class of ?p
            ###... ?sub gives the subject of the resource and ?sname its label 
            ###... Thus, in all, we extract the labels of ontology classes and its subjects
            
            
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            """    
            all_keywords_label = list()
            for result in results["results"]["bindings"]:
                all_keywords_label.append( result['l']['value'])
                
            unique_keywordslabel_in_iter = set(all_keywords_label)
            """
            all_keywords_subject = list()
            for result in results["results"]["bindings"]:
                all_keywords_subject.append( result['sname']['value'])
                
            unique_keywordssubject_in_iter = set(all_keywords_subject)
            
            #[keywordlist_iter.append(x) for x in unique_keywordslabel_in_iter]
            [keywordlist_iter.append(x) for x in unique_keywordssubject_in_iter]
            
            
                
            #print (y).
            #print(x)
                    
            #item = list()
            for res in resources:
                all_keywords.append(res['@surfaceForm'])
            
            for res in resources:
                all_resources.append(res['@surfaceForm'])
            
            
                
    #unique_keywords = set(all_keywords)
    #print(unique_keywords)
    #keywordlist.append([])
    all_keywords_list.append([])
    all_resources_list.append([])
    #[keywordlist[j].append(x) for x in unique_keywords]
    #[all_keywords_list[j].append(x) for x in all_keywords]
    [all_keywords_list[j].append(x) for x in keywordlist_iter]
    [all_resources_list[j].append(x) for x in all_resources]
    
    #print(len(all_keywords))
    print(len(keywordlist_iter), '\n\n' )
    EndReadTime = time.time()
    TotalReadTime = round((EndReadTime - StartReadTime), 2)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      "End of loop " + str(j))
    print("Total loop" + str(j) + " time : "+str(TotalReadTime)+" seconds.")

###... Creating a data frame to store the resulting keywords
    
Result_df= pd.DataFrame(columns = ['FileNames', 'President', 'Year' , 'KeyWords',
                                   'Resources'])

###... appending the names and years in a list and then storing the values to the 
###... data frame.

presidents = list()
year = list()
for i in range(29):
    presidents.append(all_files[i][:-9])
    temp_year = all_files[i][-8:]
    year.append(temp_year[:-4])

Result_df['FileNames']= all_files   
Result_df['President']= presidents
Result_df['Year']= year
Result_df['KeyWords']= all_keywords_list
Result_df['Resources']= all_resources_list




###... Sorting the data frame by year and exporting it to a csv file

Result_df.sort_values('Year', inplace = True)
Result_df = Result_df.reset_index(drop=True)



##path of mayur's macbook
#os.chdir('/Users/mayur/Documents/GitHub/Stateoftheunion/Results/')

##path for server
os.chdir('E:/mayur/State of the union/Stateoftheunion/Results/')

Result_df.to_csv('Results4_withoutbroader_withresources.csv', encoding = 'utf-8')












    
