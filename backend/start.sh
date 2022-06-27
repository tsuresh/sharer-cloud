#!/bin/sh
service rabbitmq-server start

# Start worker node 1
pm2 start worker.py --name worker-1

# Start worker node 2
pm2 start worker.py --name worker-2

# Refresh network for every 1 minute
pm2 start get_devices_cron.py --name refresh-network-job --cron "*/1 * * * *"

# Refresh dataset daily at 1AM
pm2 start dataset_update_cron.py --name update-dataset-job --cron "0 1 * * *"

# Start web server
flask run --host=0.0.0.0