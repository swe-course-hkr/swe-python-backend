import os
import jwt
import time
from flask import jsonify, request, current_app, g

from enum import Enum
from functools import wraps
from app.database.userWrapper import UserDatabase


def successResponse(data=None, statusCode=200):
    return jsonify({
        "data": data,
        "error": None
    }), statusCode


def errorResponse(error=None, statusCode=401):
    return jsonify({
        "data": None,
        "error": {
            "message": error,
            "code": statusCode
        }
    }), statusCode


class JsonWebToken():
    def generateJWT(payload: dict):
        return jwt.encode(
            {
                **payload,
                "exp": JsonWebToken.__nextExpirationTime()
            },
            os.environ.get("SECRET_APP_KEY"),
            algorithm="HS256"
        )


    def decode(token):
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )


    def __nextExpirationTime():
        return (
            int(time.time()) +
            int(os.environ.get("JWT_LIFETIME_SECONDS", 60))
        )


class Middleware:
    def validateJWT(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"]

            if not token:
                return errorResponse("Authentication token missing", 401)

            try:
                payload = JsonWebToken.decode(token)

                if (
                    (not payload.get("role")) or
                    (not payload.get("user_id")) or
                    (UserDatabase.getUserById(payload["user_id"]) is None)
                ):
                    return errorResponse("Invalid Authentication token", 401)

                # NOTE:
                # the "g" is a global object to store data for current request
                # when current request is processed, this object is cleared
                g.tokenPayload = payload

            except jwt.ExpiredSignatureError:
                # TODO: we should write these errors' details in logs 
                return errorResponse("Token Expired", 401)

            except jwt.InvalidTokenError:
                return errorResponse("Invalid Token", 401)

            except jwt.PyJWKError as e:
                print(e)
                return errorResponse("Unexpected error occured", 500)

            return f(*args, **kwargs)

        return decorated


    def requiredRole(requiredRole):
        def decorator(f):
            def decorated(*args, **kwargs):
                payload = g.get("tokenPayload")

                if (payload is None) or (payload.get("role") is not requiredRole):
                    return errorResponse("Access Forbidden", 403)

                f(*args, **kwargs)

            return decorated

        return decorator
