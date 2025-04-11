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

@userRouter.route('/users/<userID>')
def get_user(userID):
    user = UserDatabase.get_user_by_id_method(userID)

    if user is None:
        return errorResponse(
        error = "User not found",
        statusCode = 404
    )

    return successResponse(data= user.toDict())