from flask import Blueprint, request, g
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

    # TODO:
    # Before sending the JWT,
    # check that user is in our db
    # and credentials are correct

    # when successful, jwt should be
    # sent back to the user in response body
    jwt = JsonWebToken.generateJWT({
        "user_id": 1,
        "role": "bodadiz"
    })

    return successResponse(data={ "token": jwt })


@userRouter.route('/user/normal', methods=["GET"])
@Middleware.validateJWT
def user_normal():
    print("tokenPayload: ", g.get("tokenPayload"))
    return successResponse()


@userRouter.route('/user/admin', methods=["GET"])
@Middleware.validateJWT
@Middleware.requiredRole("admin")
def user_admin():
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