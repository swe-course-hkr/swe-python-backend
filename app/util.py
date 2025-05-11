import os
import jwt
import time
from datetime import datetime
from flask import jsonify, request, g
from functools import wraps
from app.database.userWrapper import UserDatabase
from app.database.wrapper import Database
import re
from app.database import db

"""
This contains utility functions, middlewares and JWT handling.

It contains the following:
- JsonWebToken: Generates and verifies JWT tokens.
- Middleware: Has flask decorators for verifying tokens, user authentication.
- Response functions: Gives back standardized API responses.
"""


def successResponse(data=None, statusCode=200):
    """
    Returns a success response in JSON

    args:
    - data: the data to return.
    - error: no error to return since its success.

    returns:
    - statusCode:  HTTP status code (200)
    """
    return jsonify({
        "data": data,
        "error": None
    }), statusCode


def errorResponse(error=None, statusCode=401):
    """
    Returns an error response in JSON

    args:
    - data: no data to return since its error.
    - error: the error message to return.

    returns:
    - statusCode:  HTTP status code (401)
    """
    return jsonify({
        "data": None,
        "error": {
            "message": error,
            "code": statusCode
        }
    }), statusCode


class JsonWebToken():
    """
    Utility class to handle JTW operations like token generation and verification.
    """
    def generateAccessToken(payload: dict):
        """
        Creates a JTW access token with experitation time.

        args:
        - payload: user information to include in the token.
        - exp: expiration time.

        returns:
        encoded JTW access token.
        """
        return jwt.encode(
            {
                **payload,
                "exp": JsonWebToken.__nextExpirationTime()
            },
            os.environ.get("JWT_ACCESS_SECRET"),
            algorithm="HS256"
        )


    def generateRefreshToken(payload: dict):
        """
        creates a JWT refresh token.

        args:
        - payload: user information to include in the token.
        - iat: issued at time.

        returns:
        encoded JWT refresh token.
        """
        return jwt.encode(
            {
                **payload, "iat": int(time.time())
            },
            os.environ.get("JWT_REFRESH_SECRET"),
            algorithm="HS256"
        )


    def verifyAccessToken(token):
        """
        Checks access token and decodes it
        
        args:
        token: encoded JWT access token.

        returns:
        decoded payload from token
        """
        return jwt.decode(token, os.environ.get("JWT_ACCESS_SECRET"), algorithms=["HS256"])


    def decodeRefreshToken(token):
        """
        dcodes refresh token.
        
        args:
        token: encoded JWT refresh token.

        returns:
        decoded payload from token.
        """
        return jwt.decode(token, os.environ.get("JWT_REFRESH_SECRET"), algorithms=["HS256"])


    def __nextExpirationTime():
        """
        calculates the next experation time for token.

        returns:
        the next timestamp when token should expire.
        """
        return (
            int(time.time()) +
            int(os.environ.get("JWT_LIFETIME_SECONDS", 600))
        )


class Middleware:
    """
    flask decorators to hand requests, token verification and authentication related checks.
    """
    def verifyAccessToken(f):
        """
        middleware to verify JWT access token from authorization header.
        it then adds decoded token payload to global object.

        returns:
        the wrapped function.
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"]

            if not token:
                Database.write_log(
                role      = "auth",
                action    = "Authorization Token Missing.",
                user_id   = 0,
                device_id = 0
                )
                return errorResponse("Authentication token missing", 401)

            try:
                payload = JsonWebToken.verifyAccessToken(token)

                if (not payload.get("role")) or (not payload.get("user_id")):
                    Database.write_log(
                    role      = payload.get("role", "unknown"),
                    action    = "Invalid Authentication Token.",
                    user_id   = payload.get("user_id", 0),
                    device_id = 0
                    )
                    return errorResponse("Invalid Authentication token", 401)

                # NOTE:
                # the "g" is a global object to store data for current request
                # when current request is processed, this object is cleared
                g.tokenPayload = payload

            except jwt.ExpiredSignatureError:
                Database.write_log(
                    role      = payload.get("role", "unknown"),
                    action    = "Token expired.",
                    user_id   = payload.get("user_id", 0),
                    device_id = 0
                )
                return errorResponse("Token Expired", 401)

            except jwt.InvalidTokenError:
                Database.write_log(
                role      = "auth",
                action    = "Invalid Token",
                user_id   = 0,
                device_id = 0
                )
                return errorResponse("Invalid Token", 401)

            except jwt.PyJWKError as e:
                print(e)
                Database.write_log(
                role      = "auth",
                action    = f"Unexpected Error Occured: {e}",
                user_id   = 0,
                device_id = 0
                )
                return errorResponse("Unexpected error occured", 500)

            return f(*args, **kwargs)

        return decorated


    def verifyRefreshToken(f):
        """
        Middleware to verify the refresh token from cookies.
        it adds decoded payload to global object.

        returns:
        wrapped function
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            refreshToken = request.cookies.get("refreshToken")

            if (
                not refreshToken or
                len(refreshToken) == 0 or
                not Database.refresh_token_is_active(refreshToken)
            ):
                Database.write_log(
                role      = "auth",
                action    = "Refresh Token Expired",
                user_id   = 0,
                device_id = 0
                )
                return errorResponse("Token expired", 401)

            try:
                payload = JsonWebToken.decodeRefreshToken(refreshToken)
                g.refreshTokenPayload = payload

            except jwt.ExpiredSignatureError:
                Database.write_log(
                role      = payload.get("role", "unknown"),
                action    = "Token Expired",
                user_id   = payload.get("user_id", 0),
                device_id = 0
                )
                return errorResponse("Token Expired", 401)

            except jwt.InvalidTokenError:
                Database.write_log(
                role      = "auth",
                action    = "Invalid Token",
                user_id   = 0,
                device_id = 0
                )
                return errorResponse("Invalid Token", 401)

            except jwt.PyJWKError as e:
                print(e)
                Database.write_log(
                role      = "auth",
                action    = f"Unexpected Error Occured: {e}",
                user_id   = 0,
                device_id = 0
                )
                return errorResponse("Unexpected error occured", 500)

            return f(*args, **kwargs)

        return decorated


    def verifyLoginData(f):
        """
        this middleware checks that username and password are present and correct.
        it passes the authenticated user object to wrapped function.

        returns:
        wrapped function
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            loginData = request.json

            if "username" not in loginData: 
                Database.write_log(
                    role      = "system",
                    action    = "Username Missing",
                    user_id   = 0,
                    device_id = 0
                )
                return errorResponse("Username missing")

            if "password" not in loginData: 
                Database.write_log(
                    role      = "system",
                    action    = f"Password Missing for {loginData.get('username')}",
                    user_id   = 0,
                    device_id = 0
                )
                return errorResponse("Password missing")

            user = UserDatabase.get_user_by_username(loginData.get("username"))
            if (not user): 
                Database.write_log(
                role      = "auth",
                action    = "Login attempt for unknown username",
                user_id   = 0,
                device_id = 0
            )
                return errorResponse("Wait a minute, who are you?")

            if user.can_login_after and datetime.now() < user.can_login_after:
                Database.write_log(
                    role      = "system",
                    action    = f"Login blocked for ({user.id} {user.username})",
                    user_id   = user.id,
                    device_id = 0
                )
                nextPossibleTime = str(user.can_login_after.strftime("%m/%d/%Y, %H:%M:%S"))
                return errorResponse("You.. shall not.. pass! (until: " + nextPossibleTime + ")", 403)
            
            if not user.password_matches(loginData.get("password")):
                UserDatabase.increaseFailedLoginAttemps(user)
                Database.write_log(
                    role      = "auth",
                    action    = f"Failed login for ({user.id} {user.username})",
                    user_id   = user.id,
                    device_id = 0
                )

                if user.failed_logins >= 3:
                    UserDatabase.setTimeout(user)
                    Database.write_log(
                        role      = "system",
                        action    = f"({user.id} {user.username}) locked out after 3 failed attempts",
                        user_id   = user.id,
                        device_id = 0
                    )
                    return errorResponse("You entered your last password, say goodbye 🔫", 403)
                
                return errorResponse("Go touch grass. You can't see the keyboard.")
            
            UserDatabase.resetTimeout(user)
            Database.write_log(
                role      = "system",
                action    = f"({user.id} {user.username}) logged in successfully",
                user_id   = user.id,
                device_id = 0
            )
               
            return f(user, *args, **kwargs)

        return decorated


    def invalidateRefreshToken(f):
        """
        this deactives the refresh token in database when user logs out.
        if no present token, continues as normal (or blame Ibo)

        returns:
        wrapped function
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get('refreshToken')

            if not token or len(token) == 0:
                # the token is invalid already, blame Ibo :D
                return successResponse()

            Database.update_refresh_token(token, isActive=False)

            return f(*args, **kwargs)

        return decorated
    
    def verifyPasswordRules(f):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-\+?_=,<>/]).{8,}$'
        @wraps(f)               
        def decorated(*args, **kwargs):
            registerData = request.json
            password = registerData.get("password", "")
            email = registerData.get("email","")
            username = registerData.get("username","")

            if not email:
                return errorResponse("Please provide an Email!", 400)

            if not password:
                return errorResponse("Password cannot be empty", 400)
            
            if len(password) < 8:
                return errorResponse("Password needs to be at least 8 characters long")

            if not re.match(pattern, password):
                return errorResponse(
                    " 👀 if u don't have at least one of a-z A-Z 0-9, and a special character (!@#$%^&*()-+?_=,<>/) , i keal u ", 
                    400
                    )

            if username.lower() in password.lower() or email.lower().split("@")[0] in password.lower():
                return errorResponse("Your password should not contain your username or email!", 400)

            return f(*args, **kwargs)
        return decorated