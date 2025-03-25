from dotenv import load_dotenv
from app.routes.device import deviceRouter, ser
from app.routes.user import userRouter
from app.routes.testsuite import testSuiteRouter
from app import create_app
from app.database import db
from app.socket import socketio
import eventlet
import threading
from threading import Lock


load_dotenv()

thread = None
thread_lock = Lock()

app = create_app()
socketio.init_app(app, async_mode='eventlet')

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(deviceRouter)
app.register_blueprint(userRouter)
app.register_blueprint(testSuiteRouter)

@socketio.on('connect')
def client_connect(auth):
    print("client: ", auth)

    global thread

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(
                target=ser
            )


@socketio.on('disconnect')
def client_disconnect(reason):
    print('Client disconnected, reason:', reason)


if __name__ == '__main__':
    
    socketio.run(
        app, 
        allow_unsafe_werkzeug=True, 
        debug=True, 
        host="0.0.0.0", 
        port=5000
    )
    
    

