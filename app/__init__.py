import os

from flask_sse import sse
from flask import Flask

from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    if (("SECRET_APP_KEY" not in os.environ) or ("SECRET_APP_KEY" == "")):
        raise Exception("SECRET_APP_KEY not found in environment variables.")

    app.secret_key = os.environ.get("SECRET_APP_KEY")

    # if (("REDIS_HOST" not in os.environ) or ("REDIS_HOST" == "")):
    #     print("REDIS_HOST not found. Using default --> 127.0.0.1")
    
    # if (("REDIS_PORT" not in os.environ) or ("REDIS_PORT" == "")):
    #     print("REDIS_PORT not found. Using default --> 6379")

    # app.config['REDIS_URL'] = (
    #     f"redis://{os.environ.get('REDIS_HOST', '127.0.0.1')}:{os.environ.get('REDIS_PORT', 6379)}"
    # )

    if (("SQLALCHEMY_DATABASE_URI" not in os.environ) or ("SQLALCHEMY_DATABASE_URI" == "")):
        print("SQLALCHEMY_DATABASE_URI not found. Using default --> sqlite:///project.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///project.db"
    )

    CORS(
        app,
        resources={
            r"/*": {"origins": ["http://localhost:3000", "*"]}
        },
        supports_credentials=True
    )

    return app
