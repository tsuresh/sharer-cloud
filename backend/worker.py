#!/usr/bin/env python
from asyncio.windows_events import NULL
from distutils.command.config import config
from pydoc import cli
import pika
import time
import utils
import json
import ast
from types import SimpleNamespace

machine_type = "L2-DS"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=machine_type, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):

    configs = json.loads(json.dumps(ast.literal_eval(body.decode())), object_hook=lambda d: SimpleNamespace(**d))

    print("Workload with ID {workload_id} is ready to be allocated...".format(workload_id=configs.workload_id))

    # Get vacant clients: @TODO to be removed along with automation process
    utils.makeRestCall("requestVacantClients",{})
    time.sleep(6)

    # Get all vacant clients
    clients = utils.makeRestCall("getVacantClients",{"machine_type" : machine_type})
    chosen_client = NULL

    # Allocate task to one vacant client 
    if len(clients) > 0:

        # Clients list should be sorted in prior @TODO: develop round robin algorithm

        chosen_client = clients[0]

        print("Workload with ID {workload_id} is allocated to client with device token {device_token}".format(workload_id=configs.workload_id, device_token=configs.device_token))

        reqBody = {
                "workload_id" : configs.workload_id, 
                "artefact_url" : configs.artefact_url,
                "spec_url" : configs.spec_url,
                "target_sid" : chosen_client.sid,
                "machine_type" : machine_type
        }

        # Place workload on a peer
        placementCall = utils.makeRestCall("placeWorkload",reqBody)

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