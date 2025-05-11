'''
User related routes

user_login -> route for a user to login, once user is logged in 2 tokens gets created

user_logout -> route to delete tokens and log user out.

create_new_access_token -> middleware to create a new access token when needed

update_details -> route to update user related data like password, username or email

fetch_all -> route to fetch all users in the database (mostly used for debugging)

create_user -> route to create a user

get_user -> route to get one user based on ID
'''

from flask import Blueprint, request, make_response, g
from app.database.userWrapper import UserDatabase
from app.database.wrapper import Database
from app.socket import socketio
from app.util import (
    successResponse,
    errorResponse,
    JsonWebToken,
    Middleware,
)
''' Define a Blueprint for user-related routes '''
userRouter = Blueprint('user', __name__)

@userRouter.route('/user/login', methods=["POST"])
@Middleware.verifyLoginData
def user_login(user):
    tokenData = {
        "user_id": user.id,
        "username": user.username,
        "role": "user"
    }

    accessToken = JsonWebToken.generateAccessToken(tokenData)
    refreshToken = JsonWebToken.generateRefreshToken(tokenData)

    response = make_response(successResponse(data={
        "accessToken": accessToken
    }))

    response.set_cookie(
        key="refreshToken",
        value=refreshToken,
        httponly=True,
        partitioned=True
    )

    Database.create_refresh_token(refreshToken)

    return response


@userRouter.route('/user/logout', methods=['POST'])
@Middleware.invalidateRefreshToken
def user_logout():
    response = make_response(successResponse())

    response.set_cookie(
        key="refreshToken",
        value="",
        httponly=True,
        partitioned=True,
        expires=0
    )

    return response


@userRouter.route('/user/token', methods=['POST'])
@Middleware.verifyRefreshToken
def create_new_access_token():
    newAccessToken = JsonWebToken.generateAccessToken(g.refreshTokenPayload)

    return successResponse(data={
        "accessToken": newAccessToken
    })


@userRouter.route('/user/normal', methods=["GET"])
@Middleware.verifyAccessToken
def user_normal():
    print("tokenPayload: ", g.get("tokenPayload"))
    return successResponse()


@userRouter.route('/user/<userID>',methods=["PATCH"])
@Middleware.verifyAccessToken
def update_details(userID):
    if not (int(g.tokenPayload["user_id"]) == int(userID)):
        return errorResponse("You may only update your own account.", 403)

    body = request.json
    updated, error = UserDatabase.update_user_details(userID, **body)

    if error:
        return errorResponse(error)
    
    Database.write_log(
        role      = g.tokenPayload["role"],
        action    = f"{g.tokenPayload["user_id"]} {g.tokenPayload["username"]} updated their account",
        user_id   = userID,
        device_id = 0,
    )
    socketio.emit('user:update', updated.toDict())
    return successResponse(
        data = updated.toDict(),
        statusCode = 201
    )

@userRouter.route('/users',methods=["GET"])
def fetch_all():
    return successResponse(data={
        'users': [users.toDict() for users in UserDatabase.fetch()]
    })

@userRouter.route('/user/register',methods=["POST"])
@Middleware.verifyPasswordRules
def create_user():
    body = request.json
    new_user, error = UserDatabase.create_user(**body)

    if error:
        return errorResponse(error)

    socketio.emit('user:create', new_user.toDict())

    return successResponse(
        data = new_user.toDict(),
        statusCode = 201
    )

@userRouter.route('/users/<userID>')
def get_user(userID):
    user = UserDatabase.get_user_by_id(userID)

    if user is None:
        return errorResponse(
        error = "User not found",
        statusCode = 404
    )

    return successResponse(data= user.toDict())