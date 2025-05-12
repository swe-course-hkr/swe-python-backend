import json
from .conftest import client, app

#add device
# def test_addDevice(client):
#     jsonPost = {"name":"test_device1",
#             "type":"LIGHT",
#             "description":"test device 1"}
#     response = client.post('/device/create', json=jsonPost)

#     strJson = response.data.decode('utf-8')
#     jsonResponse = json.loads(strJson)

#     #check data
#     for v in jsonPost:
#        assert jsonResponse["data"][v] == jsonPost[v]
    
#     #check statuscode
#     assert response.status_code == 201


# #update device
# def test_updateDevice(client):
#     #get devices from database
#     response = client.get("/device/all")
#     strJson = response.data.decode('utf-8')
#     jsonResponse = json.loads(strJson)

#     #get data of first device in list
#     deviceData = jsonResponse["data"]["devices"][0]
#     deviceId = deviceData["id"]

#     #send data
#     jsonPost = {"id": deviceId,
#                 "type":"SENSOR"}
  
#     response = client.patch('/device/'+str(deviceId), json=jsonPost)

#     #check response (data and statuscode)
#     strJson = response.data.decode('utf-8')
#     jsonResponse = json.loads(strJson)
#     assert jsonResponse["data"]["type"] == jsonPost["type"]
#     assert response.status_code == 201


# #remove device
# def test_removeDevice(client):
#     #get devices from database
#     response = client.get("/device/all")
#     strJson = response.data.decode('utf-8')
#     jsonResponse = json.loads(strJson)

#     #get data of first device in list
#     deviceData = jsonResponse["data"]["devices"][0]
#     deviceId = deviceData["id"]   

#     #check response (data and statuscode)
#     response = client.delete('/device/'+str(deviceId))
#     assert response.status_code == 200

# #remove all devices
# def test_removeAllDevices(client):
#     #get devices from database
#     response = client.get("/device/all")
#     strJson = response.data.decode('utf-8')
#     jsonResponse = json.loads(strJson)

#     #get data of first device in list
#     nrDevices = len(jsonResponse["data"]["devices"])

#     if nrDevices > 0:
#         for i in range(0,nrDevices):
#             deviceData = jsonResponse["data"]["devices"][i]
#             deviceId = deviceData["id"]   

#             #check response (data and statuscode)
#             response = client.delete('/device/'+str(deviceId))
#             assert response.status_code == 200    
