import pytest

from app import create_app
from app.socket import socketio
from app.database import db
from app.database.models import UserModel
from app.routes.device import deviceRouter
from app.routes.user import userRouter
from dotenv import load_dotenv

from flask import Flask
from flask.testing import FlaskClient

load_dotenv()

SAMPLE_USERS_DATA = [
    { "username": "user1", "email": "email@user1.com", "password": "Password0123!" },
    { "username": "user2", "email": "email@user2.com", "password": "Password0123!" },
    { "username": "user3", "email": "email@user3.com", "password": "Password0123!" },
    { "username": "user4", "email": "email@user4.com", "password": "Password0123!" }
]

@pytest.fixture
def app():
    print("\033[92m" + "[TESTS]: Initializing app ..." + "\033[0m")
    app = create_app(initForTests=True)
    app.config.update({
        "TESTING": True,
    })

    socketio.init_app(app, async_mode='eventlet')

    db.init_app(app)

    print("\033[92m" + "[TESTS]: Building schema ..." + "\033[0m")
    with app.app_context():
        db.create_all()

    print("\033[92m" + "[TESTS]: Registering routes ..." + "\033[0m")
    app.register_blueprint(deviceRouter)
    app.register_blueprint(userRouter)

    print("\033[92m" + "[TESTS]: Setup done." + "\033[0m")

    return app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture(autouse=True)
def _provide_app_context(app: Flask):
    with app.app_context():
        yield


@pytest.fixture
def with_sample_users(app: Flask):
    with app.app_context():
        db.session.add_all([
            UserModel(**userData) for userData in SAMPLE_USERS_DATA
        ])
        db.session.commit()
