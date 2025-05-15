from .models import UserModel, DeviceModel
from . import db

users = [
    { "username": "user1", "email": "email@user1.com", "password": "Password0123!" },
    { "username": "user2", "email": "email@user2.com", "password": "Password0123!" },
    { "username": "user3", "email": "email@user3.com", "password": "Password0123!" },
    { "username": "user4", "email": "email@user4.com", "password": "Password0123!" }
]

devices = [
    {"name": 'White_LED',     "type": 'LED',        "description": 'This device belongs to Ibo'},
    {"name": 'Yellow_LED',    "type": 'LED',        "description": 'Lights in the kitchen (maybe :D)'},
    {"name": 'Buzzer',        "type": 'BUZZER',     "description": 'Boredom solution, plays bzz bzz noises.'},
    {"name": 'Relay',         "type": 'RELAY',      "description": 'I don''t know what relay is.'},
    {"name": 'Fan',           "type": 'FAN',        "description": 'Cool summer breeze.'},
    {"name": 'Door',          "type": 'SERVO',      "description": 'Know what door is now, nedeez'},
    {"name": 'Window',        "type": 'SERVO',      "description": 'Window is for wasp to get through and terrorize nedeez'},
    {"name": 'Gas_Sensor',    "type": 'SENSOR',     "description": 'Detects gas, in case of assassination attempts'},
    {"name": 'Photocell',     "type": 'SENSOR',     "description": 'Sends a redstone signal when it''s day time'},
    {"name": 'PIR_Sensor',    "type": 'SENSOR',     "description": 'if you move, you lose'},
    {"name": 'Soil_Humidity', "type": 'SENSOR',     "description": 'It will let you know when mars can be terraformed'},
    {"name": 'Steam_Sensor',  "type": 'SENSOR',     "description": ''},
]

def create_users():
    db.session.add_all([
        UserModel(**userData) for userData in users
    ])
    db.session.commit()


def create_devices():
    db.session.add_all([
        DeviceModel(**deviceData) for deviceData in devices
    ])
    db.session.commit()
