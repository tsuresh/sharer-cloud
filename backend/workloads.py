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

def registerWorkload(user_id: str, artefact_url: str, spec_url: str):
    #generate workload ID
    workload_id = str(uuid.uuid4())

    #insert database entity
    try:
        doc_ref = db.collection(u'workload_requests').document(workload_id)
        doc_ref.set({
            'workload_id' : workload_id,
            'user_id' : user_id,
            'artefact_url' : artefact_url,
            'spec_url' : spec_url
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