from flask import Blueprint, request, jsonify
from app.database.wrapper import Database
from app.socket import socketio

deviceRouter = Blueprint('device', __name__)

@deviceRouter.route('/')
def index(): return '👀 wat u lookin for m8'


@deviceRouter.route('/device/create', methods=['POST'])
def create_device():
    body = request.json
    created = Database.add_device(**body)
    socketio.emit('device:create', created.toDict())

    return jsonify(created.toDict()), 201


@deviceRouter.route('/device/<deviceId>', methods=['PATCH'])
def update_device(deviceId):
    body = request.json
    updated_row = Database.update_device(deviceId, **body)
    return jsonify({ "data": updated_row.toDict() }), 201


@deviceRouter.route('/device/<deviceId>', methods=['DELETE'])
def delete_device(deviceId):
    deleted_count = Database.remove_device(deviceId)
    
    if deleted_count > 0:
        return jsonify({"message": "Device deleted successfully", "ID": deviceId}), 200
    else:
        return jsonify({"error": "Device not found"}), 404


@deviceRouter.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({
        'logs': [log.toDict() for log in Database.fetch_logs()]
    })
