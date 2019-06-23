import json
import re

with open('ads.json', encoding='utf8') as json_file:  
    ads = json.loads(json_file.read())

missing_info = []

for ad_name, ad in ads.items():
    postal_code = re.search(r'\w\d[a-z|A-Z]\s?\d[a-z|A-Z]\d', ad['address'])
    
    if postal_code is not None and postal_code.group(0)[0].upper() == 'M':
        postal_code = postal_code.group(0).upper()
        
        # add space to middle of postal code
        if len(postal_code) == 6:
            front = postal_code[:3]
            back = postal_code[3:]
            postal_code = f'{front} {back}'
        
        ad['postal_code'] = postal_code
    else:
        missing_info.append(ad_name)


for ad in missing_info:
    del ads[ad]


with open('ads.json', 'w') as outfile:  
    json.dump(ads, outfile)
