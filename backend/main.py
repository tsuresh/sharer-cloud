from asyncio.windows_events import NULL
from pydoc import cli
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import members
import workloads

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
@app.route('/getClients', methods=['POST'])
def getClients():
    response_content = None
    request_json = request.get_json()
    workload_id = request_json.get('workload_id')
    spec = request_json.get('spec')
    socketio.emit('specCheck', {
        'workload_id' : workload_id,
        'spec' : spec
    })
    response_content = {
        "message" : "success",
        "device_token" : "test"
    }
    return jsonify(response_content)

#Re

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