from google.cloud import firestore
from google.oauth2 import service_account
import os

env_path = './keys/sharer-cloud-dev-a3df1d0f3647.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_path

def updateSystemSpecs(specs, token):
    db = firestore.Client()
    doc_ref = db.collection(u'devices').document(token)
    doc_ref.set(specs)