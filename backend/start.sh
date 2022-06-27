#!/bin/sh
service rabbitmq-server start
pm2 start worker.py --name worker-1
flask run --host=0.0.0.0