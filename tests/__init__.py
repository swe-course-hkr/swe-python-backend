import pytest

import sys
sys.path.insert(0, './')

from app import create_app
from app.socket import socketio
from app.database import db
from app.routes.device import deviceRouter
from app.routes.user import userRouter
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    socketio.init_app(app, async_mode='eventlet')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(deviceRouter)
    app.register_blueprint(userRouter)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

