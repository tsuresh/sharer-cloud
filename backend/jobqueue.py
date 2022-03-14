import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#This function is used to place workloads on the respective queue
def placeWorkload(workload_id: str, artefact_url: str, spec: object, machine_type: str):
    channel.queue_declare(queue=str(machine_type), durable=True)
    message = {
        'workload_id' : workload_id,
        'artefact_url' : artefact_url,
        'spec' : spec
    }
    channel.basic_publish(
        exchange='',
        routing_key=str(machine_type),
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(" [x] Sent %r" % message)
    connection.close()