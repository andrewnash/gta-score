# -*- coding: utf-8 -*-

import csv
import operator

weight = {'Fatal' : 1.0, 'Major' : 0.6, 'Minor' : 0.45, 'Minimal' : 0.35, 'None': 0.2}

def carInciRates():
    score = {}
    
    with open('CSV/KSI.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Hood_ID'] == '0':
                continue
            
            if row['Hood_ID'] not in score:
                score[row['Hood_ID']] = 0
            
            if row['INJURY'] == ' ':
                weightS = 0.2
            else:
                weightS = weight[row['INJURY']]
            score[row['Hood_ID']] = score[row['Hood_ID']] + weightS

    maxV = max(score.items(), key=operator.itemgetter(1))[1]
    
    score = {k: (v / maxV) * 100 for k, v in score.items()}
    
    return score

if __name__ == '__main__':
    score = carInciRates()
    print(score)