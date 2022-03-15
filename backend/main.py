from asyncio.windows_events import NULL
from pydoc import cli
from tkinter.messagebox import NO
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, join_room
import members
import workloads
import jobqueue
import time
import threading
import requests
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

client_connections = []

vacant_clients = {}

# Handle cluster join request and issue a token back
@app.route('/join', methods=['POST'])
def join_network():
    request_json = request.get_json()
    client_id = request_json.get('client_id')
    system_configs = request_json.get('system_configs')
    response_content = None
    device_token = members.join_network(client_id, system_configs)
    if device_token is not NULL:
        response_content = {
            "message" : "success",
            "device_token" : device_token
        }
    else:
        response_content = {
            "message" : "error",
            "device_token" : device_token
        }
    return jsonify(response_content)

# Broadcast status check request over the network
def getClients(workload_id, spec):
    try:
        socketio.emit('specCheck', {
            'workload_id' : workload_id,
            'spec' : spec
        })
        print("Spec check request broadcasted over network")
        return True
    except Exception as e:
        print(e)
        return False

# Status update from a given machine type
def getVacantClients(machine_type):
    try:
        vacant_clients[machine_type] = {}
    except:
        print("vacant_clients list is already empty for " + str(machine_type))
    
    try:
        socketio.emit('vacantCheck', namespace='/'+str(machine_type))
        print("Vacant check request broadcasted over network")
        return True
    except Exception as e:
        print(e)
        return False

def placeWorkload(workload_id: str, artefact_url: str, spec: object, target_sid: str, machine_type: str):
    try:
        socketio.emit('placeWorkload', {
            'workload_id': workload_id,
            'artefact_url': artefact_url,
            'spec': spec
        })
        print("Workload placement request has been sent to " + target_sid)
        return True
    except Exception as e:
        print(e)
        return False

# Request received when a client machine responds its vacancy
@socketio.on('vacantCheckResp')
def vacantCheckResp(data):
    global vacant_clients
    try:
        vacant_clients_tmp = list(vacant_clients[data["machine_type"]])
    except:
        vacant_clients_tmp = []
    vacant_clients_tmp.append(
        {
            "device_token":data["token"],
            "sid":data["sid"]
        }
    )
    vacant_clients[data["machine_type"]] = vacant_clients_tmp
    print("Vacant peers.....................")
    print(vacant_clients)
    return True

# Request workload processing 
@app.route('/requestWorkloadProcess', methods=['POST'])
def requestWorkloadProcess():
    
    request_json = request.get_json()
    user_id = request_json.get('user_id')
    artefact_url = request_json.get('artefact_url')
    spec_url = request_json.get('spec_url')
    machine_type = request_json.get('machine_type')

    response_content = {}
    workload_id = workloads.registerWorkload(user_id, artefact_url, spec_url)
    if workload_id is not NULL:
        jobqueue.placeWorkload(workload_id, artefact_url, spec_url, machine_type)
        response_content = {
            "message" : "success",
            "workload_id" : workload_id
        }
    return jsonify(response_content)

# Received when a new client is connected
@socketio.on('registerClient')
def registerClient(data):
    client_connections.append(data)
    print(data)

# Request received when a client responds the possibility of processing
@socketio.on('specCheckResp')
def specCheckResp(data):
    try:
        temp_clients = workloads.workload_client_queue[data["workload_id"]]
    except:
        temp_clients = []
    temp_clients.append({"device_token":data["token"],"sid":data["sid"]})
    workloads.workload_client_queue[data["workload_id"]] = temp_clients
    return True

# Received when a workload response is received
@socketio.on('placeWorkloadResp')
def placeWorkloadResp(data):
    workload_id = data['workload_id']
    device_token = data['device_token']
    resultRaw = data['resultRaw']
    workloads.setResults(workload_id, device_token, resultRaw)
    print("Results for {workload_id} has been inserted to database..".format(workload_id=workload_id))

# Handle when a new client is connected
@socketio.on('connect')
def connectClient():
    print("Client connected")

# Handle when a new client is disconnected
@socketio.on('disconnect')
def disconnectClient():
    print("Disconnected")

# Request for vacant clients 
@app.route('/requestVacantClients', methods=['POST'])
def requestVacantClientsReq():
    response_content = {}
    machine_types = ["L2-DS"]
    for machine in machine_types:
        getVacantClients(machine)
    response_content = {
        "message" : "success"
    }
    return jsonify(response_content)

# Get active clients via HTTP req
@app.route('/getVacantClients', methods=['POST'])
def getVacantClientsReq():
    request_json = request.get_json()
    machine_type = request_json.get('machine_type')
    if machine_type is not NULL or machine_type is not None:
        try:
            vacant_clients_tmp = list(vacant_clients[machine_type])
        except:
            vacant_clients_tmp = []
    return jsonify(vacant_clients_tmp)

# Place workload in the machine
@app.route('/placeWorkload', methods=['POST'])
def placeWorkloadReq():
    request_json = request.get_json()
    workload_id = request_json.get('workload_id')
    artefact_url = request_json.get('artefact_url')
    spec_url = request_json.get('spec_url')
    target_sid = request_json.get('target_sid')
    machine_type = request_json.get('machine_type')

    # Download YAML and encode it to json; throw is there's any errors
    specContent = requests.get(spec_url)
    spec = yaml.full_load(specContent.text)

    placeWorkloadStatus = placeWorkload(workload_id, artefact_url, spec, target_sid, machine_type)
    response_content = {
        "status" : placeWorkloadStatus,
        "message" : "success"
    }
    return jsonify(response_content)

if __name__ == '__main__':
    # Initiate thread
    socketio.run(app)