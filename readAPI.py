from neo4j import GraphDatabase
import json
import requests
import http.client
import pandas as pd

from os import path
import pymongo
import certifi
import json

import http.client

cluster = pymongo.MongoClient("mongodb+srv://teamblue:teamblue@cluster0.ezeqtyg.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())



driver = GraphDatabase.driver(uri="bolt://localhost:7687",auth=("neo4j","adb123"))
session=driver.session()

url = "https://trueway-places.p.rapidapi.com/FindPlacesNearby"

querystring = {"location":"49.4819352,8.4687091","type":"supermarket","radius":"5000","language":"en"}

headers = {
	"X-RapidAPI-Key": "e086f4d6dbmsheb0b74c657a4f7cp1a12d1jsn9b296f03af77",
	"X-RapidAPI-Host": "trueway-places.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response1 = response.json()
print(response1)

filename = 'D://Advanced_DB//HospitalManagement//sample.json'
json_object = json.dumps(response1)
# if path.isfile(filename) is False:
    
with open("sample.json", "w") as outputfile:
    outputfile.write(json_object)  
 
