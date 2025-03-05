from flask_sse import sse

def emit_event(app, eventType, data):
    with app.app_context():
        sse.publish(data, type=eventType)