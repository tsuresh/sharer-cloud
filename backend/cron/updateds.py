from asyncio.windows_events import NULL
from google.cloud import firestore
from google.cloud import bigquery
from google.oauth2 import service_account
import uuid
import os
from datetime import datetime

#Firestore
env_path = './keys/sharer-cloud-dev-a3df1d0f3647.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_path
db = firestore.Client()

def workloadAssignment(contributor_id: str, reliability_score: str, contribution_hours: str):
    client = bigquery.Client()
    rows_to_insert = [
        {
            "date": str(datetime.now().strftime('%Y-%m-%d')),
            "contributor_id": int(contributor_id),
            "reliability_score" : int(reliability_score),
            "contribution_hours" : int(contribution_hours)
        },
    ]
    errors = client.insert_rows_json("sharer-cloud-dev.sharer_cloud_data.daily_stats", rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

#def getDailyScores():
    