from flask import Blueprint, request, jsonify
from app.database.wrapper import Database
from app.socket import socketio
from app.util import successResponse, errorResponse


from app.routes.forms import UserForm
from flask import render_template, redirect, flash

deviceRouter = Blueprint('device', __name__)

@deviceRouter.route('/')
def index(): 
    print("gek")
    user = {"username": 'aap'}
    return render_template('index.html', title='Home',user=user)



@deviceRouter.route('/device/all', methods=['GET'])
def get_all_devices():
    return successResponse(data={
        'devices': [device.toDict() for device in Database.fetch_all_devices()]
    })


@deviceRouter.route('/device/create', methods=['POST'])
def create_device():
    body = request.json
    created = Database.add_device(**body)
    socketio.emit('device:create', created.toDict())

    return successResponse(
        data = created.toDict(),
        statusCode = 201
    )


@deviceRouter.route('/device/<deviceId>', methods=['PATCH'])
def update_device(deviceId):
    body = request.json
    updated_row = Database.update_device(deviceId, **body)

    if updated_row is None:
        return errorResponse(
        error = "Device not found",
        statusCode = 404
    )
    else:
        socketio.emit('device:update', updated_row.toDict())
        return successResponse(
        data = updated_row.toDict(),
        statusCode = 201
    )


@deviceRouter.route('/device/<deviceId>', methods=['DELETE'])
def delete_device(deviceId):
    deleted_count = Database.remove_device(deviceId)
    socketio.emit('device:delete', { "device_id": deviceId })

    if deleted_count > 0:
        return successResponse()

    return errorResponse(
        error = "Device not found",
        statusCode = 404
    )


@deviceRouter.route('/logs', methods=['GET'])
def get_logs():
    return successResponse(data={
        'logs': [log.toDict() for log in Database.fetch_logs()]
    })