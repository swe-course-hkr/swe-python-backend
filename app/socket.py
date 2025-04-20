from flask_socketio import SocketIO

"""
Sets up websocket connections for the server.

flask-socketIO is used to handle websocket connections.
cors_allowed_origins is set to allow connections from specific clients.
* allows all origins.
"""
socketio = SocketIO(cors_allowed_origins=[
    "http://192.168.87.116:3000", 
    "http://172.27.176.1:3000", 
    "http://192.168.50.234:3000",
    "http://localhost:3000",
    ]
)
