from flask import Blueprint, Response, request, current_app
from app.models import ThingModel
from app.db import db
from app.util import emit_event

thingRouter = Blueprint('thing', __name__)

@thingRouter.route('/')
def index(): return '👀 wat u lookin for m8'


@thingRouter.route('/thing/create', methods=['POST'])
def create_thing():
    if not request.json:
        return Response(status=400)

    try:
        new_row = ThingModel(**request.json)
        db.session.add(new_row)
        db.session.commit()
    except ValueError as e:
        return Response(status=400, response=str(e))

    emit_event(current_app, "thing:create", {
        "id": new_row.uid,
        "name": new_row.name,
        "description": new_row.description
    })

    return Response(status=201)


@thingRouter.route('/thing/<thingId>/update', methods=['POST'])
def update_thing(thingId):
    # TODO: update the <thing> and pass the updated row to
    # the emit event function
    emit_event(current_app, "thing:update", { # we'll pass the updated_row here later
        "id": thingId,
        "name": "thing1",
        "description": "This is thing 1"
    })

    return Response(status=200)
