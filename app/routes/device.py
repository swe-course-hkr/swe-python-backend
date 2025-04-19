'''
Device related routes

Routes:

index -> main index route should not be accessed by user

get_all_devices -> route to fetch all devices in the database

create_device -> route to create a new device, user must be logged in to do so

update_device -> route to update an existing device in the database, based on a device ID

delete_device -> route to delete a device using a device ID

get_logs -> route to get server logs (unit team wanted this route)

SocketIO & Serial Communication Functions:

command() -> Emits a message received from the serial device to clients via SocketIO.

serial_ports() -> Detects and filters available COM ports. On Windows, filters for "CP210x" devices.

ser() -> Opens a serial connection using a detected COM port and reads data continuously from the hardware.

received() -> SocketIO event handler that receives data from clients and writes it to the serial device.
'''

from flask import Blueprint, request
from app.database.wrapper import Database
from app.socket import socketio
from app.util import successResponse, errorResponse, Middleware
import serial.tools.list_ports
import sys
import glob


''' Define a Blueprint for device-related routes '''
deviceRouter = Blueprint('device', __name__)

@deviceRouter.route('/')
def index():
    return "what are you looking at"

@deviceRouter.route('/device/all', methods=['GET'])
def get_all_devices():
    print(request.cookies.get("refreshToken"))
    return successResponse(data={
        'devices': [device.toDict() for device in Database.fetch_all_devices()]
    })


@deviceRouter.route('/device/create', methods=['POST'])
@Middleware.verifyAccessToken
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
@Middleware.verifyAccessToken
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

'''
Create a Serial instance.
Essentially turning the server into a serial monitor
'''
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
            

@socketio.on('device:update')
def received(data):
    print(data)
    serialInst.write(str(data).encode('utf-8'))
    
