# -*- coding: utf-8 -*-

from streetSearch import load_postal_code, streetSearch, findNeighbourhood, parseQuery
from CrimeScore import crimeScore
from IncidenceScore import carInciRates
from EmergencyScore import emergency

if __name__ == '__main__':
    postal_code = load_postal_code()
    crimeScores = crimeScore()
    InciScores = carInciRates()
    print(len(postal_code))

    while(1):
        query = input('Search query: ') 
        query = parseQuery(query)
        
        emerScore = emergency(postal_code, query)
        
        if query == 'exit':
            break
        
        neighbourhood = streetSearch(query, postal_code)
        
        crimeScore = float("{0:.2f}".format(crimeScores[neighbourhood]))
        InciScore = float("{0:.2f}".format(InciScores[neighbourhood]))
        emerScore = float("{0:.2f}".format(emerScore))
        
        print("Crime Risk Score: " + str(crimeScore))
        print("Traffic Incidence Risk Score: " + str(InciScore))
        print("Scarcity of Emergency Service Risk Score: " + str(emerScore))
    
