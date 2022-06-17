from asyncio.windows_events import NULL
from google.cloud import firestore
from google.oauth2 import service_account
import uuid
import os

#Firestore
env_path = './keys/sharer-cloud-dev-a3df1d0f3647.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_path
db = firestore.Client()

workload_client_queue = {}
workload_client_queue_timeouts = {}

def getWorkloads():
    output = []
    try:
        collnameref = db.collection(u'workload_requests')
        docs = collnameref.stream()
        for doc in docs:
            output.append(doc.to_dict())
        return output
    except:
        return output

def registerWorkload(user_id: str, workload_name: str, artefact_url: str, spec_url: str, machine_type: str, machine_image: str):
    #generate workload ID
    workload_id = str(uuid.uuid4())

    #insert database entity
    try:
        doc_ref = db.collection(u'workload_requests').document(workload_id)
        doc_ref.set({
            'workload_id' : workload_id,
            'workload_name' : workload_name,
            'user_id' : user_id,
            'artefact_url' : artefact_url,
            'spec_url' : spec_url,
            'machine_type' : machine_type,
            'machine_image' : machine_image,
            'status' : 'pending'
        })
        return workload_id
    except Exception as e:
        print(e)
        return NULL

def setResults(workload_id: str, device_token: str, resultsRaw: str):
    #update database entity
    try:
        doc_ref = db.collection(u'workload_requests').document(workload_id)
        doc_ref.update({
            'device_token' : device_token,
            'resultsRaw' : resultsRaw
        })
        return workload_id
    except Exception as e:
        print(e)
        return NULL