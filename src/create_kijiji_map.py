import folium
from folium import IFrame
import json
import csv

style = """
<link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
<style>
body, a {
    font-family: 'Roboto';font-size: 14px;
}
.float-my-children > * {
    float:left;
    margin-right:5px;
}
.clearfix {
    *zoom:1 /* for IE */
}
.clearfix:before, .clearfix:after {
    content: " ";
    display: table;
}
.clearfix:after {
    clear: both;
}
</style>"""


translation_table = dict.fromkeys(map(ord, '{}%'), None)

with open('ads.json', encoding='utf8') as json_file:  
    ads = json.loads(json_file.read())
    
with open('scores.csv', mode='r') as infile:
    reader = csv.reader(infile)
    postal_codes = dict((rows[0],{'long':rows[1],
                                 'lat': rows[2],
                                 'crime_score': rows[3],
                                 'traffic_score': rows[4],
                                 'emerg_score': rows[5]}) for rows in reader)

m = folium.Map(location=[43.6532, -79.3832],
               zoom_start=13)

for ad in ads.values():
    ad['Title'] = ad['Title'].translate(translation_table)
    ad['Image'] = ad['Image'].translate(translation_table)
    
    postal_code = ad['postal_code'].replace(' ', '')
    
    html = f'<center><a href={ad["Url"]} target=_blank>{ad["Title"]}</a></center> <br> \
            <div class="clearfix float-my-children"> \
                <div> \
                    <b>Price:</b> {ad["Price"]} <br> \
                    <b>Date:</b> {ad["Date"]} <br> \
                    <b>Crime Score:</b> {postal_codes[postal_code]["crime_score"]} <br> \
                    <b>Traffic Score:</b> {postal_codes[postal_code]["traffic_score"]} <br> \
                    <b>Emergency Score:</b> {postal_codes[postal_code]["emerg_score"]} <br> \
                </div> \
                {ad["Image"]} \
            </div> \
            {style}'
    
    iframe = IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)

    folium.Marker([ad['long'], ad['lat']], popup=popup).add_to(m)

m.save('kijiji_map.html')
