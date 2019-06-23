# -*- coding: utf-8 -*-
from streetSearch import load_postal_code, streetSearch, findNeighbourhood, parseQuery
from CrimeScore import crimeScore
from IncidenceScore import carInciRates
from EmergencyScore import emergency
import csv

if __name__ == '__main__':
    postal_code = load_postal_code()
    crimeScores = crimeScore()
    InciScores = carInciRates()
    
    
    with open('CSV/Scores.csv', mode = 'w') as csv_file:
        
        fieldnames = ['PostalCode', 'Lat', 'Long', 'CrimeScore', 'IncidenceScore', 'EmergencyScore']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            
        writer.writeheader()
        
        for id in postal_code:
            emerScore = emergency(postal_code, id)
            neighbourhood = streetSearch(id, postal_code)
            
            crimeScore = float("{0:.2f}".format(crimeScores[neighbourhood]))
            InciScore = float("{0:.2f}".format(InciScores[neighbourhood]))
            emerScore = float("{0:.2f}".format(emerScore))
        
            writer.writerow({'PostalCode' : id, 'Lat' : postal_code[id][0], 'Long' : postal_code[id][1], 
                             'CrimeScore' : crimeScore, 'IncidenceScore' : InciScore, 'EmergenyScore' : emerScore})