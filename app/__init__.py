import os
import secrets

from flask_sse import sse
from flask import Flask

from flask_cors import CORS
from dotenv import set_key

def create_app():
    app = Flask(__name__)

    if (("SECRET_APP_KEY" not in os.environ) or ("SECRET_APP_KEY" == "")):
        raise Exception("SECRET_APP_KEY not found in environment variables.")

    app.secret_key = os.environ.get("SECRET_APP_KEY")

    checkJWTtokens()

    if (("SQLALCHEMY_DATABASE_URI" not in os.environ) or ("SQLALCHEMY_DATABASE_URI" == "")):
        print("SQLALCHEMY_DATABASE_URI not found. Using default --> sqlite:///project.db")

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
