from asyncio.windows_events import NULL
from pydoc import cli
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import members
import workloads
import jobqueue

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

client_connections = []

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
        socketio.emit('vacantCheck', namespace='/'+str(machine_type))
        print("Vacant check request broadcasted over network")
        return True
    except Exception as e:
        print(e)
        return False

# Request received when a client machine responds its vacancy
@socketio.on('vacantCheckResp')
def vacantCheckResp(data):
    try:
        vacant_clients = workloads.vacant_clients[data["machine_type"]]
    except:
        vacant_clients = []
    vacant_clients.append({"device_token":data["token"],"sid":data["sid"]})
    workloads.vacant_clients[data["machine_type"]] = vacant_clients
    print(workloads.vacant_clients)
    return True

# Request workload processing 
@app.route('/requestWorkloadProcess', methods=['POST'])
def requestWorkloadProcess():
    
    request_json = request.get_json()
    user_id = request_json.get('user_id')
    artefact_url = request_json.get('artefact_url')
    spec = request_json.get('spec')

    response_content = {}
    workload_id = workloads.registerWorkload(user_id, artefact_url, spec)
    if workload_id is not NULL:
        jobqueue.placeWorkload(workload_id, artefact_url, spec, spec["machine_type"])
        response_content = {
            "message" : "success",
            "machine_type" : workload_id
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

# Handle when a new client is connected
@socketio.on('connect')
def connectClient():
    print("Client connected")

# Handle when a new client is disconnected
@socketio.on('disconnect')
def disconnectClient():
    print("Disconnected")

if __name__ == '__main__':
    socketio.run(app)