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

vacant_clients = {}

def registerWorkload(user_id: str, artefact_url: str, spec: object):
    #generate workload ID
    workload_id = str(uuid.uuid4())

    #insert database entity
    try:
        doc_ref = db.collection(u'workloads').document(workload_id)
        doc_ref.set({
            'workload_id' : workload_id,
            'user_id' : user_id,
            'artefact_url' : artefact_url,
            'spec' : spec
        })
        return workload_id
    except Exception as e:
        print(e)
        return NULL