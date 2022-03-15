from main import getVacantClients
import time

machine_types = ["L2-DS"]

# Update active clients list after x seconds
while(True):
    for machine in machine_types:
        getVacantClients(machine)
    time.sleep(10)