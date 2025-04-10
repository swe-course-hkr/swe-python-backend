from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins=["http://192.168.87.116:3000", "http://172.27.176.1:3000", "http://192.168.50.234:3000", "*"])
