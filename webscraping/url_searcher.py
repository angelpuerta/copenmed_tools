# Author: Ana Sanmartin
#
# This file runs all the urls present in the xlsx file 

#Dependencies are

# IMPORTS 

import argparse
import os
from time import perf_counter

import pandas as pd

from check_resource import check_resource_retrieved_before
from downloader import download_text
from searcher import search_only
from searcher import urls2doc

## CAN BE ESTABLISHED BY THE USER ##

output = os.getcwd()
document = ''
min_searches = 10
searches_threshold = 25
url_list = []

def main(document, output, min_searches):

    # Load from the xlsx the resources (recursos) page to obtain the url 
    # and the entities (entidades) page to obtain the entity word (query)
    
    xls = pd.ExcelFile(document)
    df_entities = pd.read_excel(xls, 'entidades')
    #print(df_entities)
    df_resources = pd.read_excel(xls, 'recursos')
    
    print("Checking if the urls in the xlsx are in any url.txt")
    

    for i in range(len(df_resources['URL'])):
        url = df_resources['URL'][i]
        word = list(df_entities.loc[df_entities['IdEntidad'] == df_resources['IdEntidad'][i] , 'Entidad'])
        #print(word)
        #google_search(word[-1], url, 1, 'www.google.com', output)
        
        #We add all the urls to the document if they were not searched before
        if not check_resource_retrieved_before(url, output):
            print("Number of elements in excel is: " + str(len(df_resources['URL'])))
            print("We are in: " + str(i))
            print("The url " + url + " has no match, adding to text file")
            urls2doc(url, word[-1], output) 

                
    t0 = perf_counter()
    download_text(output)  
    t1 = perf_counter()
    
    t2 = perf_counter()        
    

 
    for i in range(len(df_entities['IdEntidad'])):
    # We must check how many resources we will have for each entity. If we have less than 10 we will add manual search
    # for each entity until we reach 10.
    # We will not search for any resource if the resources for any entity surpasses a number of documents (30 is a temporal number)
    
        num_resources_for_entity = df_resources.loc[df_resources['IdEntidad'] == df_resources['IdEntidad'][i]].shape[0]
        print("We are now padding searches until we reach " + min_searches + " for entity " + df_entities['Entidad'][i] + " which is " + str(i) + "/" + str(len(df_entities['IdEntidad'])))
        
        if os.path.exists(output + "/dir/" + str(df_entities['IdEntidad'][i])):
            if len(os.listdir(output + "/dir/" + str(df_entities['IdEntidad'][i]))) < searches_threshold:
                 
                if num_resources_for_entity < min_searches:
                    url_list = search_only(df_entities['Entidad'][i], min_searches - num_resources_for_entity, output)
                else:
                    break
        else:
            if num_resources_for_entity < min_searches:
                url_list = search_only(df_entities['Entidad'][i], min_searches - num_resources_for_entity, output)
            
        if len(url_list) != 0:
            for m in url_list:
                urls2doc(m, df_entities['Entidad'][i], output)
    
    t3 = perf_counter() 
    
    t4 = perf_counter()
    download_text(output)  
    t5 = perf_counter()
      
    print("Total time for creating corpus for the xmls is: " + str(t1-t0))
    print("Total time for download of new urls is: " + str(t3-t2))
    print("Total time for creating corpus for the new downloaded urls is: " + str(t5-t4))
    
    f = open("time.txt", "w")
    f.write("Total time for creating corpus for the xmls is: " + str(t1-t0))
    f.write("Total time for download of new urls is: " + str(t3-t2))
    f.write("Total time for creating corpus for the new downloaded urls is: " + str(t5-t4))
    f.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Search by terms")

    parser.add_argument('-d',
                    "--document",
                    type=str,
                    help="xlsx document to process")
    
    parser.add_argument('-m',
                    "--min_searches",
                    type=int,
                    help="minimum number of searches needed for each entity")

    parser.add_argument('-o',
                    "--output",
                    type=str,
                    help="Output path where files are going to be stored")

    # Parseo de los argumentos
    arguments = vars(parser.parse_args())

    if arguments['document']:
        if isinstance(arguments['document'], str):
            document = arguments['document']
        else:
            print("ERROR: Please enter valid document")
            exit()
            
    if arguments['min_searches']:
        if isinstance(arguments['min_searches'], int):
            min_searches = arguments['min_searches']
        else:
            print("ERROR: Please enter valid number")
            exit()
    
    if arguments['output']:
        if isinstance(arguments['output'], str):
            output = arguments['output']
        else:
            print("ERROR: Please enter a valid search engine.")
            exit()
        


    main(document, output, min_searches)
    
    
