import os
import jwt
import time
from datetime import datetime
from flask import jsonify, request, g
from functools import wraps
from app.database.userWrapper import UserDatabase
from app.database.wrapper import Database
from app.database import db


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
    def generateAccessToken(payload: dict):
        return jwt.encode(
            {
                **payload,
                "exp": JsonWebToken.__nextExpirationTime()
            },
            os.environ.get("JWT_ACCESS_SECRET"),
            algorithm="HS256"
        )


    def generateRefreshToken(payload: dict):
        return jwt.encode(
            {
                **payload, "iat": int(time.time())
            },
            os.environ.get("JWT_REFRESH_SECRET"),
            algorithm="HS256"
        )


    def verifyAccessToken(token):
        return jwt.decode(token, os.environ.get("JWT_ACCESS_SECRET"), algorithms=["HS256"])


    def decodeRefreshToken(token):
        return jwt.decode(token, os.environ.get("JWT_REFRESH_SECRET"), algorithms=["HS256"])


    def __nextExpirationTime():
        return (
            int(time.time()) +
            int(os.environ.get("JWT_LIFETIME_SECONDS", 60))
        )


class Middleware:
    def verifyAccessToken(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"]

            if not token:
                return errorResponse("Authentication token missing", 401)

            try:
                payload = JsonWebToken.verifyAccessToken(token)

                if (not payload.get("role")) or (not payload.get("user_id")):
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


    def verifyRefreshToken(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            refreshToken = request.cookies.get("refreshToken")

            if (
                not refreshToken or
                len(refreshToken) == 0 or
                not Database.refresh_token_is_active(refreshToken)
            ):
                return errorResponse("Token expired", 401)

            try:
                payload = JsonWebToken.decodeRefreshToken(refreshToken)
                g.refreshTokenPayload = payload

            except jwt.ExpiredSignatureError:
                return errorResponse("Token Expired", 401)

            except jwt.InvalidTokenError:
                return errorResponse("Invalid Token", 401)

            except jwt.PyJWKError as e:
                print(e)
                return errorResponse("Unexpected error occured", 500)

            return f(*args, **kwargs)

        return decorated


    def verifyLoginData(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            loginData = request.json

            if "username" not in loginData: return errorResponse("Username missing")
            if "password" not in loginData: return errorResponse("Password missing")

            user = UserDatabase.get_user_by_username(loginData.get("username"))
            if (not user): return errorResponse("Wrong username or password")

            if user.can_login_after and datetime.now() < user.can_login_after:
                return errorResponse("you entered your last password, say goodbye 🔫", 403)
            
            if not user.password_matches(loginData.get("password")):
                UserDatabase.increaseFailedLoginAttemps(user)

                if user.failed_logins >= 3:
                    UserDatabase.setTimeout(user)

                db.session.commit()
                return errorResponse("Wrong username or password")
            
            UserDatabase.resetTimeout(user)
               
            return f(user, *args, **kwargs)

        return decorated


    def invalidateRefreshToken(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get('refreshToken')

            if not token or len(token) == 0:
                # the token is invalid already, blame Ibo :D
                return successResponse()

            Database.update_refresh_token(token, isActive=False)

            return f(*args, **kwargs)

        return decorated
    