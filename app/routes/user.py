from flask import Blueprint, request
from app.database.userWrapper import UserDatabase
from app.socket import socketio
from app.util import successResponse, errorResponse

userRouter = Blueprint('user', __name__)

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
def update_email():
    return successResponse(data={
        'users': [users.toDict() for users in UserDatabase.fetch()]
    })

# TODO: Create route done By AC