import csv,sys
from math import sin, cos, sqrt, atan2, radians
R = 6371.0

def distanceHelper(lat1, lon1, lat2, lon2):
  lat_1 = lat1
  lon_1 = lon1
  lat_2 = lat2
  lon_2 = lon2
  dlon = lon_2 - lon_1
  dlat = lat_2 - lat_1
  a = sin(dlat / 2)**2 + cos(lat_1) * cos(lat_2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  distance = R * c
  return distance

def emergency(postal_code, query):
  #ambulanceNametoDistanceDict = {}
  with open('CSV/ambulance_facility.csv', mode='r') as csv_file0:
    csv_reader0 = csv.DictReader(csv_file0)
    smallest1 = sys.float_info.max
    for row in csv_reader0:
      lat1 = radians(float(row['LATITUDE']))
      lon1 = radians(float(row['LONGITUDE']))
      if(query in postal_code):
        lat2 = radians(float(postal_code[query][0]))
        lon2 = radians(float(postal_code[query][1]))
        #ambulanceNametoDistanceDict[row['NAME']] = distanceHelper(lat1, lon1, lat2, lon2)
        if(distanceHelper(lat1, lon1, lat2, lon2) < smallest1):
          smallest1 = distanceHelper(lat1, lon1, lat2, lon2)  
  #policeNametoDistanceDict = {}
  with open('CSV/police_facility.csv', mode='r') as csv_file1:
    csv_reader1 = csv.DictReader(csv_file1)
    smallest2 = sys.float_info.max
    for row in csv_reader1:
      lat1 = radians(float(postal_code[row['POSTAL_CD'].replace(" ","")][0]))
      lon1 = radians(float(row['LONGITUDE']))
      if(query in postal_code):
        lat2 = radians(float(postal_code[query][0]))
        lon2 = radians(float(postal_code[query][1]))
        #policeNametoDistanceDict[row['FACI_NAM']] = distanceHelper(lat1, lon1, lat2, lon2)
        if(distanceHelper(lat1, lon1, lat2, lon2) < smallest2):
          smallest2 = distanceHelper(lat1, lon1, lat2, lon2)
  return (smallest1 + smallest2)*1.25