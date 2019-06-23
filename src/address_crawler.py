import json
import requests
from bs4 import BeautifulSoup


with open('ads.json', encoding='utf8') as json_file:  
    ads = json.loads(json_file.read())

missing_info = []

for ad_name, ad in ads.items():
    url = ad['Url']
    html = requests.get(url, verify=False)
    soup = BeautifulSoup(html.text, 'html.parser')
    address = soup.select_one("span[class*=address]")
    
    if address is not None:
        ad['address'] = address.text
        print(ad['address'])
    else:
        missing_info.append(ad_name)

for ad in missing_info:
    del ads[ad]
    
with open('ads.json', 'w') as outfile:  
    json.dump(ads, outfile)