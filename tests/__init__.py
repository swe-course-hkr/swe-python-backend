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

    # other setup can go here
    app = create_app()
    socketio.init_app(app, async_mode='eventlet')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(deviceRouter)
    app.register_blueprint(userRouter)

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


#@pytest.fixture()
#def client(app):
#    app.test_client()

#    yield client


'''
def test_request_example(client):
    response = client.get("/")
    print("aap")
    assert b"OK" in response.data

'''




'''
def test_access():
    app = create_app()

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(deviceRouter)
    app.register_blueprint(userRouter)
    app.register_blueprint(testSuiteRouter)


    client = app.test_client()
    #response = client.get('/')
    landing = client.get('/logs')
    html = landing.data.decode()
    print(html)

test_access()
'''

'''
@pytest.fixture()
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    app.testing=True
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
'''
