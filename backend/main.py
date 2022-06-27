from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import members
import workloads
import jobqueue
import uploads
import time
import requests
import yaml
import time
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)
cors = CORS(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "tmp/"

client_connections = []
vacant_clients = {}

images = {
    'DS' : "intel/intel-optimized-tensorflow",
    'RD' : "gazebo"
}

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
        print("Vacant check request broadcasted over network: " + machine_type)
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

    predictedScores = members.get_predicted_scores(data["contributor_id"])

    vacant_clients_tmp.append(
        {
            "device_token":data["token"],
            "sid":data["sid"],
            "machine_name":data["machine_name"],
            "machine_type":data["machine_type"],
            "connected_time":time.time(),
            "contributor_id":data["contributor_id"],
            "predicted_contributor_score" : predictedScores["predicted_contributor_score"],
            "predicted_contribution_hours" : predictedScores["predicted_contribution_hours"],
            "status":data["status"]
        }
    )
    vacant_clients[data["machine_type"]] = vacant_clients_tmp
    print("Vacant peers.....................")
    print(vacant_clients)

    # Sort contributor array
    vacant_clients.sort(key=lambda x: x.predicted_contributor_score, reverse=True)

    return True

# Get system image based on the passed values
def getImage(machine_type: str):
    global images
    splitted = machine_type.split("-", 1)
    category = splitted[1]
    try:
        return images[category]
    except:
        return "default"

# Get all workloads
@app.route('/getWorkloads', methods=['GET'])
@cross_origin()
def getWorkloads():
    return jsonify(workloads.getWorkloads())

# Get full network
@app.route('/getNetwork', methods=['GET'])
@cross_origin()
def getNetwork():
    networkList = []
    for key, value in vacant_clients.items():
        for mcnType in value:
            networkList.append({
                'id' : mcnType["sid"],
                'name': mcnType["machine_name"],
                'machineType': mcnType["machine_type"],
                'uptime': "%.2f Sec" % (time.time() - mcnType["connected_time"]),
                'status': mcnType["status"]
            })
    return jsonify(networkList)

# Request workload processing 
@app.route('/requestWorkloadProcess', methods=['POST'])
@cross_origin()
def requestWorkloadProcess():
    
    request_json = request.get_json()
    user_id = request_json.get('user_id')
    artefact_url = request_json.get('artefact_url')
    spec_url = request_json.get('spec_url')
    machine_type = request_json.get('machine_type')
    machine_image = getImage(machine_type)
    workload_name = request_json.get('workload_name')
    replicas = request_json.get('replicas') or "1"

    response_content = {}
    workload_id = workloads.registerWorkload(user_id, workload_name, artefact_url, spec_url, machine_type, machine_image, replicas)
    if workload_id is not None:
        # Place workloads based on the replica count
        for x in range(int(replicas)):
            jobqueue.placeWorkload(workload_id, artefact_url, spec_url, machine_type)
        response_content = {
            "message" : "success",
            "workload_id" : workload_id
        }
    return jsonify(response_content)

# Get workload detail
@app.route('/getWorkloadDetail', methods=['GET'])
@cross_origin()
def getWorkloadDetail():
    workload_id = request.args.get('id')
    return jsonify(workloads.getWorkload(workload_id))

# Request workload processing 
@app.route('/getWorkloadResponses', methods=['GET'])
@cross_origin()
def getWorkloadResponses():
    workload_id = request.args.get('id')
    return jsonify(workloads.getWorkloadResponses(workload_id))

# Received when a new client is connected
@socketio.on('registerClient')
def registerClient(data):
    members.join_network(data['contributor_id'], data['device_token'], data['sid'])
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
    contributor_id = data['contributor_id']
    resultRaw = ''
    workloads.setResults(workload_id, device_token, contributor_id, resultRaw)
    print("Results for {workload_id} has been inserted to database..".format(workload_id=workload_id))

# Handle when a new client is connected
@socketio.on('connect')
def connectClient():
    print("Client connected")

# Handle when a new client is disconnected
@socketio.on('disconnect')
def disconnectClient():
    print("Disconnected")

# Request for vacant clients: Broadcasr request over network
@app.route('/requestVacantClients', methods=['POST'])
@cross_origin()
def requestVacantClientsReq():
    response_content = {}
    machine_types = ["L1-DS", "L2-DS", "L3-DS", "L1-RD", "L2-RD", "L3-RD"]
    for machine in machine_types:
        getVacantClients(machine)
    response_content = {
        "message" : "success"
    }
    return jsonify(response_content)

# Get active clients via HTTP req: List Output
@app.route('/getVacantClients', methods=['POST'])
@cross_origin()
def getVacantClientsReq():
    request_json = request.get_json()
    machine_type = request_json.get('machine_type')
    if machine_type is not None or machine_type is not None:
        try:
            vacant_clients_tmp = list(vacant_clients[machine_type])
        except:
            vacant_clients_tmp = []
    return jsonify(vacant_clients_tmp)

# Place workload in the machine: Send request to machine
@app.route('/placeWorkload', methods=['POST'])
@cross_origin()
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

# Upload files
@app.route('/upload',methods=["POST"])
@cross_origin()
def upload():
    try:
        if request.method == 'POST':
            f = request.files['file']
            file_type = request.form['type']

            if file_type == "spec":
                path = f"specs/{str(uuid.uuid4().hex)}-spec.yaml"
            elif file_type == "output":
                path = f"outputs/{str(uuid.uuid4().hex)}-output.zip"
            else:
                path = f"artefacts/{str(uuid.uuid4().hex)}-artefact.zip"

            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            #Start Do Main Process Here
            TMP_FILE_NAME = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename))
            BUCKET_NAME = 'sharer-cloud-dev.appspot.com'
            result = uploads.upload_blob(BUCKET_NAME, TMP_FILE_NAME, path)

            #Update database if its a output
            if file_type == "output":
                workload_id = request.form['workload_id']
                contributor_id = request.form['contributor_id']
                status = request.form['status']
                time_consumed = request.form['time_consumed']
                workloads.setOutputs(workload_id, contributor_id, f"https://storage.googleapis.com/sharer-cloud-dev.appspot.com/{str(result)}", time_consumed, status)

            #End Do Main Process Here
            response_content = {
                "url" : f"https://storage.googleapis.com/sharer-cloud-dev.appspot.com/{str(result)}",
                "message" : "success"
            }
            return jsonify(response_content)
    except Exception as e:
        response_content = {
            "url" : None,
            "message" : "error",
            "detail" : str(e)
        }
        return jsonify(response_content)

if __name__ == '__main__':
    # Initiate thread
    socketio.run(app)