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
# load json filee
# def loadjson(tx):
#     pathh = "file:///D:/Advanced_DB/HospitalManagement/sample.json"

#     nodes = tx.run("call apoc.load.json($pathh) yield value UNWIND value.results as res MERGE(address:Address{id:res.id}) ON CREATE SET address.address = res.address, address.lat = res.location.lat, address.lng = res.location.lng MERGE(add_name:Location {name:res.name})merge (add_name)-[:ISAT]->(address) merge(address)-[:HAS]->(add_name)")
    


# Use case to get location 
def base():
    PatientName = input("Please enter pateint name")
    

patname= input("Please enter Patient Name")
print(patname)
landmarkAdd = input("please enter landmark 1")
print(landmarkAdd)
landmark1 = input("please enter landmark 2")
print(landmark1)




def getLocationOnUniqueLandmark(tx):
    nodes = tx.run("MATCH (Location {name:'Coffee to go'})-[r:ISAT]->(Address) return Address.address as address, Address.lat as latitude, Address.lng as Longitude")
    for node in nodes:
        loc.append(node)
        
    # print("LOCATION:", loc)

def getfirstlandmark(tx,landmark1,landmarkAdd):
    
    firstlandmark = tx.run("MATCH (Location {name: $landmark1})-[r:ISAT]->(Address where Address.address contains $landmarkAdd ) return Address.address as address, Address.lat as latitude, Address.lng as Longitude,Location.name as name",landmark1=landmark1,landmarkAdd=landmarkAdd)
    for nodes in firstlandmark:
        print("nodes"+str(nodes))
        load.append(nodes)
        # print("this is how to print")
        # print(load[0]['address'])
        
    # print("LIDL DATA :", load)

landmark3= input("please enter landmark 3")
print(landmark3)    
def getsecondlandmark(tx,landmark3,landmarkAdd):
    
    
    firstlandmark = tx.run("MATCH (Location {name: $landmark3})-[r:ISAT]->(Address where Address.address contains $landmarkAdd ) return Address.address as address, Address.lat as latitude, Address.lng as Longitude,Location.name as name",landmark3=landmark3,landmarkAdd=landmarkAdd)
    for nodes in firstlandmark:
        print("nodes"+str(nodes))


        load2.append(nodes)
        # print(load2[0])

add1=""
add2=""

def arraymatch(tx,add1,add2):
    
    for nodes in load:
        for n in load2:

            # print("forlooppp")
            add1 = nodes['address']
            add2=  n['address']
            arraymatch2 = tx.run("MATCH (a:Location)-[:ISAT]->(p:Address where p.address= $add1),(b:Location)-[:ISAT]->(o:Address where o.address= $add2) RETURN distance(point({latitude: p.lat , longitude: p.lng}),point({latitude: o.lat, longitude: o.lng})) / 1000.0 as km, a.name,b.name,p.address,o.address, p.lat, p.lng, o.lat,o.lng ORDER BY km ASC LIMIT 5",add1=add1,add2=add2)
            for nodes in arraymatch2:
                # print("printingarraymatch2")
                # print(nodes)
                finalResults.append(nodes)
    # print("SORTED KEYS ::::::::")            
    # print(sorted(finalResults,key=lambda x:x['km']))

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
   









def getwithinDistance(tx):  
    getDist = tx.run("",) 



with driver.session() as session:
    session.read_transaction(getfirstlandmark,landmark1,landmarkAdd)
    session.read_transaction(getsecondlandmark,landmark3,landmarkAdd)
    session.read_transaction(arraymatch,add1,add2)
    session.read_transaction(getLocationOnUniqueLandmark)




#     MATCH (a:Address)
#     WITH a
# MATCH (b:Address) WHERE id(b)<>id(a) 
#     WITH a, b, distance( point({ latitude: a.lat, longitude:a.lng }),point({ latitude: b.lat, longitude:b.lng }) ) as dist 
#         WHERE dist<=50
# RETURN a.address,b.address, dist order by dist ASC     



    
add1 = load[0]
add2 = load2[0]  
   

driver.close()
# else:
#     with open(filename,'r+') as file:
#         file_data = json.load(file)
#         file_data['results'].append(json_object)
#         file.seek(0)
#         json.dump(file_data,file)






    

       