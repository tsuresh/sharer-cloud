#!/usr/bin/env python
import pika
import time
import utils
import json
import ast
from types import SimpleNamespace
import workloads
import contribLogging

machine_type = "L2-DS"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=machine_type, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):

    configs = json.loads(json.dumps(ast.literal_eval(body.decode())), object_hook=lambda d: SimpleNamespace(**d))

    print("Workload with ID {workload_id} is ready to be allocated...".format(workload_id=configs.workload_id))
    
    time.sleep(6)

    # Get all vacant clients
    clients = utils.makeRestCall("getVacantClients",{"machine_type" : machine_type})
    chosen_client = None

    # Allocate task to one vacant client 
    if len(clients) > 0:

        # Get the first item from clients list: already sorted
        chosen_client = clients[0]

        print("Workload with ID {workload_id} is allocated to client with contributor ID {device_token}".format(workload_id=configs.workload_id, device_token=chosen_client.contributor_id))

        reqBody = {
                "workload_id" : configs.workload_id, 
                "artefact_url" : configs.artefact_url,
                "spec_url" : configs.spec_url,
                "target_sid" : chosen_client.sid,
                "machine_type" : machine_type,
                "contributor_id" : chosen_client.contributor_id
        }

        # Place workload on a peer
        utils.makeRestCall("placeWorkload",reqBody)

        # Update workload status
        workloads.setStatus(configs.workload_id, "Allocated to: " + chosen_client.contributor_id)

        # Set contribution logging 
        contribLogging.assign_task(chosen_client.contributor_id)

        # Acknowledge the request
        ch.basic_ack(delivery_tag=method.delivery_tag)

    else:
        print("No clients are currently available.")

        # Reject and requeue request
        ch.basic_reject(delivery_tag=method.delivery_tag)

    # Wait for ack, if not allocate to next client until successful ack

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=machine_type, on_message_callback=callback)

channel.start_consuming()