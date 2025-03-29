import sys
import json
import random

sys.path.insert(0, './')

from . import client, app

#add user
def test_addUser(client):
    nr = random.randint(0, 1000)
    name = "user"+str(nr)
    jsonPost = {"username":name,
            "email":name+"@hkr.se",
            "password":"hello123"}
    response = client.post('/user/register', json=jsonPost)

    strJson = response.data.decode('utf-8')
    jsonResponse = json.loads(strJson)

    #check data
    for v in jsonPost:
       assert jsonResponse["data"][v] == jsonPost[v]
    
    #check statuscode
    assert response.status_code == 201


#update user
def test_updateUser(client):
    #get users from database
    response = client.get("/users")
    strJson = response.data.decode('utf-8')
    jsonResponse = json.loads(strJson)

    #get data of first device in list
    userData = jsonResponse["data"]["users"][0]
    userId = userData["id"]

    #send data
    nr = random.randint(0, 1000)
    newEmail = "new"+str(nr)+"@hkr.se"

    jsonPost = {"id": userId,
                "email":newEmail}
  
    response = client.patch('/user/'+str(userId), json=jsonPost)

    #check response (data and statuscode)
    strJson = response.data.decode('utf-8')
    jsonResponse = json.loads(strJson)
    assert jsonResponse["data"]["email"] == jsonPost["email"]
    assert response.status_code == 201


#create a user with an existing username
def test_createDoubleUser(client):
    #get users from database
    response = client.get("/users")
    strJson = response.data.decode('utf-8')
    jsonResponse = json.loads(strJson)

    #get data of first device in list
    nrUsers = len(jsonResponse["data"]["users"])
    userData = jsonResponse["data"]["users"][0]
    userId = userData["id"]   
    username = userData["username"]

    jsonPost = {"username":username,
            "email":"random@hkr.se",
            "password":"hello123"}
    response = client.post('/user/register', json=jsonPost)

    strJson = response.data.decode('utf-8')  
    assert response.status_code == 500


    #check if no users were added
    response = client.get("/users")
    strJson = response.data.decode('utf-8')
    jsonResponse = json.loads(strJson)
    nrUsers1 = len(jsonResponse["data"]["users"])

    assert nrUsers == nrUsers1




