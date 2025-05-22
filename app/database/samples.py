from .models import UserModel, DeviceModel
from . import db

users = [
    { "username": "user1", "email": "email@user1.com", "password": "Password0123!" },
    { "username": "user2", "email": "email@user2.com", "password": "Password0123!" },
    { "username": "user3", "email": "email@user3.com", "password": "Password0123!" },
    { "username": "user4", "email": "email@user4.com", "password": "Password0123!" }
]

devices = [
    {"name": 'White_LED',     "display_name": "Outdoors lamp",      "type": 'LED',        "description": 'This device belongs to Ibo'},
    {"name": 'Yellow_LED',    "display_name": "Kitchen Lights",     "type": 'LED',        "description": 'Lights in the kitchen (maybe :D)'},
    {"name": 'Buzzer',        "display_name": "JukeBox like in MC", "type": 'BUZZER',     "description": 'Boredom solution, plays bzz bzz noises.'},
    {"name": 'Relay',         "display_name": "Mysterious Thing",   "type": 'RELAY',      "description": 'I don''t know what relay is.'},
    {"name": 'Fan',           "display_name": "Cool Fan in room",   "type": 'FAN',        "description": 'Cool summer breeze.'},
    {"name": 'Door',          "display_name": "Entrance Door",      "type": 'SERVO',      "description": 'Know what door is now, nedeez'},
    {"name": 'Window',        "display_name": "Tiny Glass Door",    "type": 'SERVO',      "description": 'Window is for wasp to get through and terrorize nedeez'},
    {"name": 'Gas_Sensor',    "display_name": "Gas Sensor",         "type": 'SENSOR',     "description": 'Detects gas, in case of assassination attempts'},
    {"name": 'Photocell',     "display_name": "Light Sensor",       "type": 'SENSOR',     "description": 'Sends a redstone signal when it''s day time'},
    {"name": 'PIR_Sensor',    "display_name": "Motion Sensor",      "type": 'SENSOR',     "description": 'if you move, you lose'},
    {"name": 'Soil_Humidity', "display_name": "Humidity Sensor",    "type": 'SENSOR',     "description": 'It will let you know when mars can be terraformed'},
    {"name": 'Steam_Sensor',  "display_name": "Steam/Fog sensor",   "type": 'SENSOR',     "description": 'Knows when your tea is ready'},
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
