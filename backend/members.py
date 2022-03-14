from asyncio.windows_events import NULL
from google.cloud import firestore
from google.oauth2 import service_account
import uuid
import os

# Firestore
env_path = './keys/sharer-cloud-dev-a3df1d0f3647.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_path
db = firestore.Client()

# Handle cluster join request and issue a token back
def join_network(client_id: str, system_configs: object):
    if client_id is not None and client_id is not None:
        device_token = str(uuid.uuid4())
        try:
            doc_ref = db.collection(u'network').document(device_token)
            doc_ref.set({
                'client_id' : client_id,
                'system_configs' : system_configs,
                'device_token' : device_token
            })
            return device_token
        except Exception as e:
            print(e)
            return NULL
    else:
        print("Missing mandatory params")
        return NULL