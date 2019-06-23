import json
import csv


with open('ads.json', encoding='utf8') as json_file:  
    ads = json.loads(json_file.read())

with open('to_postal_codes.csv', mode='r') as infile:
    reader = csv.reader(infile)
    postal_codes = dict((rows[0],(rows[2],rows[3])) for rows in reader)


missing_info = []

for ad_name, ad in ads.items():
    postal_code = ad['postal_code'].replace(' ', '')
    
    if postal_code in postal_codes:
        long, lat = postal_codes[postal_code]
        ad['long'] = long
        ad['lat'] = lat
    else:
        missing_info.append(ad_name)
        
for ad in missing_info:
    del ads[ad]
    

with open('ads.json', 'w') as outfile:  
    json.dump(ads, outfile)
