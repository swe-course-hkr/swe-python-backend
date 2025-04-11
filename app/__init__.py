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
    TOKENS = ["JWT_ACCESS_TOKEN", "JWT_REFRESH_TOKEN"]
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/.."

    for token in TOKENS:
        variableExists = token in os.environ

        if variableExists and len(os.environ.get(token)) > 0:
            print(f" 🟢 — {token} found.")
            continue

        print(f" 🔴 — {token} not found. Generating new ...")
        newToken = secrets.token_hex(32)
        os.environ[token] = newToken
        set_key(dotenv_path=ROOT_DIR + "/.env", key_to_set=token, value_to_set=newToken)
        print(f" 🟢 — Generated new {token}")
