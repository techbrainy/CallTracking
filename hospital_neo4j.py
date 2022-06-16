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


filename = 'D://Advanced_DB//HospitalManagement//sample.json'
json_object = json.dumps(response1)
# if path.isfile(filename) is False:
    
with open("sample.json", "w") as outputfile:
    outputfile.write(json_object)  
loc=[]
load=[]
load2=[]
finalResults=[]


# Use case to get location 

    

patname= input("Please enter Patient Name")
print(patname)
landmarkAdd = input("please enter landmark 1")
print(landmarkAdd)
landmark1 = input("please enter landmark 2")
print(landmark1)


# Get users location by getting random locations as input and puuting it into these below functions getfirstlandmark and getsecondlandmark
# and then getting distance of results in arraymatch

def getfirstlandmark(tx,landmark1,landmarkAdd):
    
    firstlandmark = tx.run("MATCH (Location {name: $landmark1})-[r:ISAT]->(Address where Address.address contains $landmarkAdd ) return Address.address as address, Address.lat as latitude, Address.lng as Longitude,Location.name as name",landmark1=landmark1,landmarkAdd=landmarkAdd)
    for nodes in firstlandmark:
        print("nodes"+str(nodes))
        load.append(nodes)
      

landmark3= input("please enter landmark 3")
print(landmark3)    
def getsecondlandmark(tx,landmark3,landmarkAdd):
    
    
    firstlandmark = tx.run("MATCH (Location {name: $landmark3})-[r:ISAT]->(Address where Address.address contains $landmarkAdd ) return Address.address as address, Address.lat as latitude, Address.lng as Longitude,Location.name as name",landmark3=landmark3,landmarkAdd=landmarkAdd)
    for nodes in firstlandmark:
        print("nodes"+str(nodes))


        load2.append(nodes)
        
add1=""
add2=""

def arraymatch(tx,add1,add2):
    
    for nodes in load:
        for n in load2:

            add1 = nodes['address']
            add2=  n['address']
            arraymatch2 = tx.run("MATCH (a:Location)-[:ISAT]->(p:Address where p.address= $add1),(b:Location)-[:ISAT]->(o:Address where o.address= $add2) RETURN distance(point({latitude: p.lat , longitude: p.lng}),point({latitude: o.lat, longitude: o.lng})) / 1000.0 as km, a.name,b.name,p.address,o.address, p.lat, p.lng, o.lat,o.lng ORDER BY km ASC LIMIT 5",add1=add1,add2=add2)
            for nodes in arraymatch2:
            
                finalResults.append(nodes)
   

    print("******************************")
    print("USER's EXACT LOCATION ::")
    # print(" ADDRESS "+str(finalResults[0]['p.address']))
   
    finalResults_abc = sorted(finalResults,key=lambda x:x['km'])
    address = finalResults_abc[0]['p.address']
    Lat = finalResults_abc[0]['o.lat']
    lng = finalResults_abc[0]['o.lng']

 
   
    response1 ={
        "PatientName": patname,
        "Address": address,
        "Latitude": Lat,
        "Longitude": lng

    }
    db = cluster["Location"]
    collection = db["Location"]

    collection.insert_one(response1)
    print(response1)
   

with driver.session() as session:
    session.read_transaction(getfirstlandmark,landmark1,landmarkAdd)
    session.read_transaction(getsecondlandmark,landmark3,landmarkAdd)
    session.read_transaction(arraymatch,add1,add2)

 
   

driver.close()




    

       