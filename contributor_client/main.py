import socketio
import config
import workloads
import json
from types import SimpleNamespace

device_token = "123456"

# standard Python
sio = socketio.Client()

# Socket connection request handeler
@sio.event
def connect():
    sio.emit('registerClient', {
        'sid': sio.sid,
        'device_token': device_token
    })
    print("Socket connection successful")

# Socket connections error handeler
@sio.event
def connect_error():
    print("Socket connection failed")

# Socket disconnected error handeler
@sio.event
def disconnect():
    print("Disconnected from socket")

# Listen to spec check requests
@sio.on('specCheck')
def catch_spec_check(data):
    placeability = workloads.checkPlaceability(
         data,
         config.configs,
         data["workload_id"],
         sio.sid,
         device_token
    )
    sio.emit('specCheckResp', placeability)

# Listen to workload placement requests
@sio.on('placeWorkload')
def place_workload(data):
    print("Place workload for session")

def init():
    sio.connect('ws://localhost:5000', wait_timeout = 10)

if __name__ == '__main__':
    init()