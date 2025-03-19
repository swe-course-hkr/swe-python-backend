import os

from flask_sse import sse
from flask import Flask

from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    if (("SECRET_APP_KEY" not in os.environ) or ("SECRET_APP_KEY" == "")):
        raise Exception("SECRET_APP_KEY not found in environment variables.")

    app.secret_key = os.environ.get("SECRET_APP_KEY")

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
