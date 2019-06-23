# -*- coding: utf-8 -*-

import requests, json, csv
import sys

from math import sin, cos, sqrt, atan2, radians

R = 6371.0
# enter your api key here 
#api_key = 'AIzaSyAe08pwvRJhOkmYOgiETLkeljpQsRkcLWk'
  
# url variable store url 
#url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

def load_postal_code():
    postal_code = {}
    with open('CSV/Canadian_Postal_Codes.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            postal_code[row['PostalCode']] = [row['Latitude'], row['Longitude']]
            
    return postal_code

def parseQuery(query):
    query = query.replace(" ", "").upper()
    return query


def streetSearch(query, postal_code):
    # The text string on which to search 
    
      
    # get method of requests module 
    # return response object 
    '''r = requests.get(url + 'address=' + query +
                            '&key=' + api_key)
 
    '''
    location = postal_code[query]
    #x = r.json() 

 
    #print(x['results'][0])
    
    #location = x['results'][0]['geometry']['location']
    #print(location)
    neighbourhood = findNeighbourhood(location)
    
    return neighbourhood


def findNeighbourhood(location):
    
    lat1 = radians(float(location[0]))
    lon1 = radians(float(location[1]))
    
    with open('CSV/centres_of_neighbour.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        min = sys.maxsize 
        neighbour = 0;
        
        for row in csv_reader:

            
            lat2 = radians(float(row['Lat']))
            lon2 = radians(float(row['Long']))
            
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            
            distance = R * c
            
            if distance < min :
                neighbour = row['Hood_ID']
                min = distance
            
    return neighbour

