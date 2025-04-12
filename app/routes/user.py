from flask import Blueprint, request, make_response, g
from app.database.userWrapper import UserDatabase
from app.socket import socketio
from app.util import (
    successResponse,
    errorResponse,
    JsonWebToken,
    Middleware
)

userRouter = Blueprint('user', __name__)

@userRouter.route('/user/login', methods=["POST"])
def user_login():
    loginData = request.json

    if "username" not in loginData: return errorResponse("Username missing")
    if "password" not in loginData: return errorResponse("Password missing")

    print(loginData)
    user = UserDatabase.getUserByUsername(loginData.get("username"))

    # TODO: gonna have to verify against encrypted password later
    if not user: # or not (user.password == loginData.password):
        return errorResponse("Wrong username or password")

    tokenData = {
        "user_id": user.id,
        "username": user.username,
        "role": "bodadiz"
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
    return response


@userRouter.route('/user/normal', methods=["GET"])
@Middleware.verifyAccessToken
def user_normal():
    print("tokenPayload: ", g.get("tokenPayload"))
    return successResponse()


@userRouter.route('/user/<userID>',methods=["PATCH"])
def update_details(userID):

    body = request.json
    updated = UserDatabase.update_user_details(userID, **body)

    if updated is None:
        return errorResponse(
        error = "User not found",
        statusCode = 404
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
def create_user():
    body = request.json
    new_user = UserDatabase.create_user(**body)
    socketio.emit('user:create', new_user.toDict())
    
    return successResponse(
        data = new_user.toDict(),
        statusCode = 201
    )