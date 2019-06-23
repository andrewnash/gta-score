# -*- coding: utf-8 -*-

import csv
import operator



weight = {'Assault' : 0.70, 'BreakandEnter' : 0.6, 'Robbery' : 0.45, 
          'TheftOver' : 0.25, 'AutoTheft' : 0.15, 'Homicide' : 1.0}

def crimeScore():
    scores = {}
    with open('CSV/Neighbourhood_Crime_Rates_Boundary_File.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Assault_AVG'] == 'N/A':
                assault = 0
            else:
                assault = float(row['Assault_AVG'])
            
            if row['AutoTheft_AVG'] == 'N/A':
                autotheft = 0
            else:
                autotheft = float(row['AutoTheft_AVG'])
                
            if row['BreakandEnter_AVG'] == 'N/A':
                breakenter = 0
            else:
                breakenter = float(row['BreakandEnter_AVG'])
            
            if row['Robbery_AVG'] == 'N/A':
                robbery = 0
            else:
                robbery = float(row['Robbery_AVG'])
            
            if row['TheftOver_AVG'] == 'N/A':
                theftover = 0
            else:
                theftover = float(row['TheftOver_AVG'])
            
            if row['Homicide_AVG'] == 'N/A':
                homicide = 0
            else:
                homicide = float(row['Homicide_AVG'])
 
            
            scores[row['Hood_ID']] = (assault * weight['Assault'] + autotheft * weight['AutoTheft']
            + breakenter * weight['BreakandEnter'] + robbery * weight['Robbery'] +
            theftover * weight['TheftOver'] + homicide * weight['Homicide'])/float(row['Population'])
            

    maxV = max(scores.items(), key=operator.itemgetter(1))[1]
    
    scores = {k: (v / maxV) * 100 for k, v in scores.items()}
    
    return scores

    
    
if __name__ == '__main__':
    scores = crimeScore()