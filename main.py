from dotenv import load_dotenv
from app.routes.device import deviceRouter, ser
from app.routes.user import userRouter
from app import create_app
from app.database import db
from app.database.samples import create_users, create_devices
from app.database.models import DeviceModel, UserModel
from app.socket import socketio
import eventlet
import threading
from threading import Lock

"""
This is the main file that starts the flask server. 

It just sets up the database, routes and handles the websocket connections (to connect unit and device to each other in real time).

It also runs a background task to handle communication with the device.
"""

load_dotenv(override=True)

thread = None
thread_lock = Lock()

app = create_app()
socketio.init_app(app, async_mode='eventlet')

db.init_app(app)

with app.app_context():
    db.create_all()
    if len(db.session.query(DeviceModel).all()) == 0:
        print(" * Populating devices ...")
        create_devices()
    
    if len(db.session.query(UserModel).all()) == 0:
        print(" * Populating users ...")
        create_users()


app.register_blueprint(deviceRouter)
app.register_blueprint(userRouter)

@socketio.on('connect')
def client_connect(auth):
    """
    Handles the connection of a client to the server.
    if no background thread is running, it starts one.

    auth: the authentication data of the client.
    """
    print("client: ", auth)

    global thread

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(
                target=ser
            )


@socketio.on('disconnect')
def client_disconnect(reason):
    """
    Handles the disconnection of a client from the server.
    is also prints a reason for the disconnection.

    reason: the reason for the disconnection.
    """
    print('Client disconnected, reason:', reason)


if __name__ == '__main__':
    """
    Main function that runs the server.    
    """
    
    socketio.run(
        app, 
        allow_unsafe_werkzeug=True, 
        debug=True, 
        host="0.0.0.0", 
        port=5001
    )
    
    

