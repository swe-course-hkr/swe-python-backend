import sys
import json

sys.path.insert(0, './')

from . import client, app

#add log
def test_addLog(client):
    jsonPost = {"log_level":"info",
            "action":"unittest",
            "user_id":1,
            "device_id":1}
    response = client.post('/logs/create', json=jsonPost)

    strJson = response.data.decode('utf-8')
    jsonResponse = json.loads(strJson)

    #check data
    for v in jsonPost:
       if v == "log_level":  var = "level"
       else: var = v
       assert jsonResponse["data"][var] == jsonPost[v]
    
    #check statuscode
    assert response.status_code == 201

