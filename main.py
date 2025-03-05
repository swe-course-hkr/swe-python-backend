import redis

from flask_socketio import SocketIO
from dotenv import load_dotenv
from app.routes.thing import thingRouter
from app import create_app
from app.db import db

load_dotenv()

app = create_app()

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(thingRouter)

red = redis.StrictRedis()
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app)
