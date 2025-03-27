from flask import Blueprint, request, jsonify
from app.database.wrapper import Database
from app.socket import socketio
from app.util import successResponse, errorResponse
import serial.tools.list_ports
from flask import render_template, redirect, flash
import sys
import glob

serialInst = serial.Serial()

def command(command):
    socketio.emit('device:update', {'device message':command}, namespace="/")

running = False

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = serial.tools.list_ports.comports()

        ports = [str(p) for p in ports if "CP210x" in str(p)]

        if len(ports) > 0:
            ports = [ports[0].split("-")[0].strip()]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def ser():

    global running
    if running == True:
        return
    else:
        running = True
        
    print("serial running")

    pols = serial_ports()
    serialInst.baudrate = 9600

    if len(pols) == 0:
        print("list empty")
        return

    serialInst.port = pols[0]
    serialInst.open()

    while True:
        socketio.sleep(0)
        if serialInst.in_waiting:
            packet = serialInst.readline() # reads all the incoming bytes
            print(packet.decode('utf'))
            command(packet.decode('utf').strip('\n'))
            

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


@socketio.on('device:update')
def received(data):
    print(data)
    serialInst.write(str(data).encode('utf-8'))
    