# -*- coding: utf-8 -*-

import csv

lat = {}
long = {}
count = {}

with open('CSV/MCI_total.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        if(row['Hood_ID'] not in count):
            lat[row['Hood_ID']] = 0
            long[row['Hood_ID']] = 0
            count[row['Hood_ID']] = 0
            
        lat[row['Hood_ID']] += float(row['Lat'])
        long[row['Hood_ID']] += float(row['Long'])
        count[row['Hood_ID']] += 1;
        
        
with open('CSV/centres_of_neighbour.csv', mode = 'w') as csv_file:
    fieldnames = ['Hood_ID', 'Lat', 'Long']
    writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    
    writer.writeheader()
    
    for hi in count:
        writer.writerow({'Hood_ID' : hi, 'Lat' : lat[hi]/count[hi], 
                         'Long' : long[hi]/count[hi]})
    