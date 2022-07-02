import docker
import os

# Retrive docker status
try:
    client = docker.from_env()
except:
    print('Docker has not started or not running')

containerLabel = "sharercloud-wl"

# Pull the user prefered images
def pullImages(configs: object):
    for environment in configs.images:
        if environment not in client.images.list():
            print("Fetching image..." + environment)
            client.images.pull(environment)
            print("Fetching image successful..." + environment)
    return True

# Create the container under the given system boundaries
def create(name: str, image: str, envars: list, deployCmd: str, configs: object):
    envars.append({
        'RUNQ_MEM' : configs.mem_limit
    })
    envars.append({
        'RUNQ_CPU' : configs.cpu_count
    })
    print("Container creating...")
    try:
        container = client.containers.run(
            image,
            command= ["/bin/sh", "-c", deployCmd],
            name= name,
            cpu_count= configs.cpu_count or 1,
            cpu_percent= configs.cpu_percent or 100,
            #device_requests= configs.device_requests,
            mem_limit= configs.mem_limit,
            environment= envars,
            labels= [containerLabel]
        )
        print("Container created")
        return container
    except Exception as e:
        print(e)
        return False

# Starts the container and execute the initial commands
def start(name: str):
    print("Container starting...")
    try:
        container = client.containers.get(name).start()
        print("Container logs..")
        print(container)
        return container
    except Exception as e:
        print("Error starting the container")
        print(e)
        return False

# Get a list of all running workloads
def getRunningWorkloads():
    print("Getting workloads...")
    try:
        workloads = client.containers.list(
            filters={
                'label' : [containerLabel],
                'status' : 'running'
            }
        )
        return workloads
    except Exception as e:
        print(e)
        return []

# Add files via cmd
def addArtefacts(container_name, dst, data):
    print("Adding artefacts...")
    try:
        container = client.containers.get(container_name)
        print(container)
        print(os.path.dirname(dst))
        container.put_archive(container_name, os.path.dirname(dst), data)
    except Exception as e:
        print(e)
        return False