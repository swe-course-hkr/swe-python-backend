import os
import secrets

from flask_sse import sse
from flask import Flask

from flask_cors import CORS
from dotenv import set_key

"""
This file is responsible for creating the Flask app and configuring it.
Sets up the database connection, JWT tokens, and CORS.

Called when starting the sterver
"""

def create_app(initForTests=False):
    """
    creates and configures flask.
    - Checks if SECRET_APP_KEY exists in environment.
    - Checks if SQLALCHEMY_DATABASE_URI exists in environment. if not, a default is used.
    - Allows Cors so unit can talk with server
    - calls checkJWTtokens() to make sure JTW tokens exist.

    Returns:
        app: flask app instance
    """
    app = Flask(__name__)

    if (("SECRET_APP_KEY" not in os.environ) or ("SECRET_APP_KEY" == "")):
        raise Exception("SECRET_APP_KEY not found in environment variables.")

    app.secret_key = os.environ.get("SECRET_APP_KEY")

    checkJWTtokens()

    if (("SQLALCHEMY_DATABASE_URI" not in os.environ) or ("SQLALCHEMY_DATABASE_URI" == "")):
        print("SQLALCHEMY_DATABASE_URI not found. Using default --> sqlite:///project.db")

    if initForTests:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DATABASE_URL",
            "sqlite:///project.db"
        )

    CORS(
        app,
        resources={
            r"/*": {"origins": "*"}
        },
        supports_credentials=True
    )

    return app


def checkJWTtokens():
    """
    Checks if JTW token exist in environment for user authentication.
    If they do, it will use the existing tokens.
    if not, it will generate a new secure random token and save it to environment.
    """
    jwtSecrets = ["JWT_ACCESS_SECRET", "JWT_REFRESH_SECRET"]
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/.."

    for jwtSecret in jwtSecrets:
        variableExists = jwtSecret in os.environ

        if variableExists and len(os.environ.get(jwtSecret)) > 0:
            print(f" 🟢 — {jwtSecret} found.")
            continue

        print(f" 🔴 — {jwtSecret} not found. Generating new ...")
        newJwtSecret = secrets.token_hex(32)
        os.environ[jwtSecret] = newJwtSecret
        set_key(dotenv_path=ROOT_DIR + "/.env", key_to_set=jwtSecret, value_to_set=newJwtSecret)
        print(f" 🟢 — Generated new {jwtSecret}")
