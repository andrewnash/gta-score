import folium
from folium import IFrame
import json

style = """
<style>
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

m = folium.Map(location=[43.6532, -79.3832],
               zoom_start=13)

for ad in ads.values():
    ad['Title'] = ad['Title'].translate(translation_table)
    ad['Image'] = ad['Image'].translate(translation_table)
    
    html = f'<center><a href={ad["Url"]} target=_blank>{ad["Title"]}</a></center> <br> \
            <div class="clearfix float-my-children"> \
                <div> \
                    <b>Price:</b> {ad["Price"]} <br> \
                    <b>Date:</b> {ad["Date"]} <br> \
                    <b>Crime Score:</b> NA <br> \
                    <b>Health Score:</b> NA <br> \
                    <b>Emergency Score:</b> NA <br> \
                    <b>Overall Score:</b> NA <br> \
                </div> \
                {ad["Image"]} \
            </div> \
            {style}'
    
    iframe = IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)

    folium.Marker([ad['long'], ad['lat']], popup=popup).add_to(m)

m.save('index.html')
