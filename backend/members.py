from asyncio.windows_events import NULL
from google.cloud import firestore
from google.oauth2 import service_account
import uuid
import os
import math

# Firestore
env_path = './keys/sharer-cloud-dev-a3df1d0f3647.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_path
db = firestore.Client()

# Handle cluster join request and issue a token back
def join_network(contributor_id: str, device_token: str, sid: str):
    predicted_contribution_hours = 0
    predicted_contributor_score = 0
    try:
         values = db.collection(u'contributor_devices').document(contributor_id).get().to_dict()
         predicted_contribution_hours = int(values['predicted_contribution_hours'])
         predicted_contributor_score = int(values['predicted_contributor_score'])
    except Exception as e:
        pass
    try:
        doc_ref = db.collection(u'contributor_devices').document(contributor_id)
        doc_ref.set({
            'contributor_id' : int(contributor_id),
            'device_token' : device_token,
            'sid' : sid,
            'predicted_contributor_score' : int(predicted_contributor_score),
            'predicted_contribution_hours' : int(predicted_contribution_hours)
        })
        return device_token
    except Exception as e:
        print(e)
        return NULL

# Update contribution score on datastore
def update_prediction_score(contributor_id: str, predicted_contributor_score: str):
    try:
        doc_ref = db.collection(u'contributor_devices').document(contributor_id)
        doc_ref.update({
            'predicted_contributor_score' : math.ceil(float(predicted_contributor_score))
        })
        return True
    except Exception as e:
        return False

# Update contribution hours on datastore
def update_contribution_hours(contributor_id: str, predicted_contribution_hours: str):
    try:
        doc_ref = db.collection(u'contributor_devices').document(contributor_id)
        doc_ref.update({
            'predicted_contribution_hours' : math.ceil(float(predicted_contribution_hours))
        })
        return True
    except Exception as e:
        return False

# Get predicted DB scores
def get_predicted_scores(contributor_id: str):
    predicted_contribution_hours = 0
    predicted_contributor_score = 0
    try:
         values = db.collection(u'contributor_devices').document(contributor_id).get().to_dict()
         predicted_contribution_hours = int(values['predicted_contribution_hours'])
         predicted_contributor_score = int(values['predicted_contributor_score'])
         return {
            'predicted_contribution_hours' : predicted_contribution_hours,
            'predicted_contributor_score' : predicted_contributor_score
         }
    except Exception as e:
        return {
            'predicted_contribution_hours' : 0,
            'predicted_contributor_score' : 0
         }
        