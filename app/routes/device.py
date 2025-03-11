from flask import Blueprint, Response, request, current_app, jsonify
from app.database.wrapper import Database
from app.util import emit_event

deviceRouter = Blueprint('device', __name__)

@deviceRouter.route('/')
def index(): return '👀 wat u lookin for m8'


@deviceRouter.route('/device/create', methods=['POST'])
def create_device():
    if not request.json:
        return Response(status=400)

    try:
        new_row = Database.add_device(**request.json)
    except ValueError as e:
        return Response(status=400, response=str(e))

    # yeet the potatos at clients in real time :DDDDDD
    emit_event(current_app, "device:create", new_row.toDict())
    return Response(status=201)


@deviceRouter.route('/device/<deviceId>/update', methods=['POST'])
def update_device(deviceId):
    # TODO: implement update device route
    pass


@deviceRouter.route('/device/<deviceId>/delete', methods=['POST'])
def delete_device(deviceId):
    # TODO: implement delete device route
    pass


@deviceRouter.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({
        'logs': [log.toDict() for log in Database.fetch_logs()]
    })
