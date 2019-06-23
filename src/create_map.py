import folium
from folium import IFrame

m = folium.Map(location=[43.6532, -79.3832],
               zoom_start=13)

m.save('funky.html')


