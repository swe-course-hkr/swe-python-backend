from flask import Blueprint, Response, request, current_app, jsonify
from app.database.wrapper import Database
from app.util import emit_event

deviceRouter = Blueprint('device', __name__)

@deviceRouter.route('/')
def index(): return '👀 wat u lookin for m8'


@deviceRouter.route('/device/create', methods=['POST'])
def create_device():
    # TODO: implement create device route
    pass


@deviceRouter.route('/device/<deviceId>/update', methods=['POST'])
def update_device(deviceId):
    body = request.json
    updated_row = Database.update_device(deviceId, **body)
    return jsonify({ "data": updated_row.toDict() })


@deviceRouter.route('/device/<deviceId>/delete', methods=['POST'])
def delete_device(deviceId):
    # TODO: implement delete device route
    pass


@deviceRouter.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({
        'logs': [log.toDict() for log in Database.fetch_logs()]
    })
