import socketio
import config
import workloads
#import json
from types import SimpleNamespace

device_token = "123456"

# standard Python
sio = socketio.Client()

# Socket connection request handeler
@sio.event
def connect():
    print(sio.sid)
    sio.emit('registerClient', {
        'sid': sio.sid,
        'device_token': device_token,
        'contributor_id' : config.configs.contributor_id
    })
    print("Socket connection successful")

# Socket connections error handeler
@sio.event
def connect_error(error):
    print("Socket connection failed")

# Socket disconnected error handeler
@sio.event
def disconnect():
    print("Disconnected from socket")

# Listen to spec check requests
@sio.on('vacantCheck', namespace='/'+config.configs.machine_type)
def catch_vacant_check():
    vacant_status = workloads.checkMachineVacantStatus(
        config.configs, 
        sio.sid, 
        device_token
    )
    sio.emit('vacantCheckResp', vacant_status)

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
    placementStatus = workloads.placeWorkloads(
        data['workload_id'],
        data['artefact_url'],
        data['spec'],
        config.configs
    )
    sio.emit('placeWorkloadResp', {
        'workload_id' : data['workload_id'],
        'resultRaw' : placementStatus,
        'device_token' : device_token,
        'contributor_id' : config.configs.contributor_id
    })
    print(placementStatus)
    print('Workload placed.')

def init():
    sio.connect('ws://localhost:5000', wait_timeout = 10)

if __name__ == '__main__':
    init()