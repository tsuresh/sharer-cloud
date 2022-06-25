from asyncio.windows_events import NULL
from google.cloud import firestore
from google.cloud import bigquery
from google.oauth2 import service_account
import members
import uuid
import os
from datetime import datetime
import math

#Firestore
env_path = './keys/sharer-cloud-dev-a3df1d0f3647.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_path
db = firestore.Client()

workload_client_queue = {}
workload_client_queue_timeouts = {}

todayDate = str(datetime.today().strftime('%Y-%m-%d'))

# Update task count on dataset
def assign_task(contributor_id: str):
    assigned_tasks = 0
    completed_tasks = 0
    contribution_hours = 0
    try:
         values = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors').document(contributor_id).get().to_dict()
         assigned_tasks = int(values['assigned_tasks'])
         completed_tasks = int(values['completed_tasks'])
         contribution_hours = int(values['contribution_hours'])
    except Exception as e:
        pass
    try:
        #Set output data
        doc_ref = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors').document(contributor_id)
        doc_ref.set({
            'assigned_tasks' : assigned_tasks+1,
            'completed_tasks' : completed_tasks,
            'contribution_hours' : contribution_hours
        })
        return "complete"
    except Exception as e:
        print(e)
        return NULL

# Update completed tasks count of dataset 
def complete_task(contributor_id: str):
    assigned_tasks = 0
    completed_tasks = 0
    contribution_hours = 0
    try:
         values = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors').document(contributor_id).get().to_dict()
         assigned_tasks = int(values['assigned_tasks'])
         completed_tasks = int(values['completed_tasks'])
         contribution_hours = int(values['contribution_hours'])
    except Exception as e:
        pass
    try:
        #Set output data
        doc_ref = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors').document(contributor_id)
        doc_ref.set({
            'assigned_tasks' : assigned_tasks,
            'completed_tasks' : completed_tasks+1,
            'contribution_hours' : contribution_hours
        })
        return "complete"
    except Exception as e:
        print(e)
        return NULL

# Add contribution hours count on dataset
def add_contribution_hours(contributor_id: str, hours: str):
    assigned_tasks = 0
    completed_tasks = 0
    contribution_hours = 0
    try:
         values = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors').document(contributor_id).get().to_dict()
         assigned_tasks = int(values['assigned_tasks'])
         completed_tasks = int(values['completed_tasks'])
         contribution_hours = int(values['contribution_hours'])
    except Exception as e:
        pass
    try:
        #Set output data
        doc_ref = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors').document(contributor_id)
        doc_ref.set({
            'assigned_tasks' : assigned_tasks,
            'completed_tasks' : completed_tasks,
            'contribution_hours' : contribution_hours+int(hours)
        })
        return "complete"
    except Exception as e:
        print(e)
        return NULL

# Add data to BigQuery
def add_to_bq(rows_to_insert):
    client = bigquery.Client()
    errors = client.insert_rows_json("sharer-cloud-dev.sharer_cloud_data.daily_stats", rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

# Get todays stats and add to BigQuery dataset (Cron function)
def update_daily_stats():
    rows_to_insert = []
    try:
        collnameref = db.collection(u'contributor_logs').document(todayDate).collection(u'contributors')
        docs = collnameref.stream()
        for doc in docs:
            docDict = doc.to_dict()

            docId = int(doc.id)
            completed_tasks = int(docDict['completed_tasks'])
            assigned_tasks = int(docDict['assigned_tasks'])
            contribution_hours = int(docDict['contribution_hours'])
            reliability_score = 0

            if assigned_tasks > 0:
                reliability_score = math.ceil((int(completed_tasks) / int(assigned_tasks))*100)

            rows_to_insert.append({
                "date": todayDate,
                "contributor_id": docId,
                "reliability_score" : reliability_score,
                "contribution_hours" : contribution_hours
            })

        add_to_bq(rows_to_insert)

        return rows_to_insert
    except:
        return []

# Update all predictions in the contributor_devices collection
def update_all_predictions():
    client = bigquery.Client()

    get_reliability_scores_query = client.query('SELECT contributor_id, forecast_value FROM ML.FORECAST(MODEL `sharer-cloud-dev.sharer_cloud_data.reliability_score`, STRUCT(30 AS horizon, 0.90 AS confidence_level)) WHERE forecast_timestamp = \'2022-06-25\''.format(today=todayDate))
    for row in get_reliability_scores_query.result():
        members.update_prediction_score(str(row.contributor_id), str(row.forecast_value))

    get_contribution_hours_query = client.query('SELECT contributor_id, forecast_value FROM ML.FORECAST(MODEL `sharer-cloud-dev.sharer_cloud_data.contribution_hours`, STRUCT(30 AS horizon, 0.90 AS confidence_level)) WHERE forecast_timestamp = \'2022-06-25\''.format(today=todayDate))
    for row in get_contribution_hours_query.result():
        members.update_contribution_hours(str(row.contributor_id), str(row.forecast_value))

    print("Added predicted data to database")

# Update dataset 
update_daily_stats()

# Conduct model updating

# Update all data in database
update_all_predictions()