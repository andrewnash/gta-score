from flask import Flask, render_template, send_from_directory
import folium
from folium import IFrame
import csv
import json
from flask_cors import CORS, cross_origin
import webbrowser

app = Flask(__name__)
CORS(app)

with open('src/scores.csv', mode='r') as infile:
    reader = csv.reader(infile)
    postal_codes = dict((rows[0],{'long':rows[1],
                                 'lat': rows[2],
                                 'crime_score': rows[3],
                                 'traffic_score': rows[4],
                                 'emerg_score': rows[5]}) for rows in reader)
    
with open('src/scores.csv', mode='r') as infile:
    codes = [row.split(',')[0] for row in infile]
    
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


@app.route("/", defaults={'path': 'index'})
@app.route("/<path:path>")
def home(path):
    return render_template(f'{path}.html')


@app.route('/lookup_postal_code/<postal_code>')
def lookup_postal_code(postal_code):    
    generate_map(postal_code)
    
    webbrowser.open(f'file://C:/Users/adn11/Documents/Git/to-score/templates/{postal_code}.html')
    return json.dumps({'data': "data"})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img/', 'favicon.ico', 
                               mimetype='static/img/vnd.microsoft.icon')


def generate_map(postal_code):
    og_name = postal_code
    
    if postal_code in postal_codes:
        data = postal_codes[postal_code]
    else:
        data = None
        
    # sudo fuzzy matching for missing postal code
    while data is None:
        postal_code = postal_code[:-1]
        for code in codes:
            if postal_code in code:
                postal_code = code
                break
        if postal_code in postal_codes:
            data = postal_codes[postal_code]   
        
    
    m = folium.Map(location=[data['long'], data['lat']],
               zoom_start=16)
    
    html = f'<b>Crime Score:</b> {data["crime_score"]} <br> \
             <b>Traffic Score:</b> {data["traffic_score"]} <br> \
             <b>Emergency Score:</b> {data["emerg_score"]} <br> \
             {style}'
    
    iframe = IFrame(html=html, width=200, height=100)
    popup = folium.Popup(iframe, max_width=200)

    folium.Marker([data['long'], data['lat']], popup=popup).add_to(m)

    m.save(f'templates/{og_name}.html')
    

if __name__ == '__main__':
   app.run()