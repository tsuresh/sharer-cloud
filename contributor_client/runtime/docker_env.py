import docker

# Retrive docker status
try:
    client = docker.from_env()
except:
    print('Docker has not started or not running')

containerLabel = "sharercloud-wl"

# Pull the user prefered images
def pullImages(configs: object):
    for environment in configs.environments:
        if environment not in client.images.list():
            print("Fetching image..." + environment)
            client.images.pull(environment)
            print("Fetching image successful..." + environment)
    return True

# Create the container under the given system boundaries
def create(name: str, image: str, deployCmd: list, envars: list, configs: object):
    try:
        container = client.containers.run(
            image= image,
            #command= "/bin/bash mkdir test",
            name= name,
            cpu_count= configs.cpu_count or 1,
            cpu_percent= configs.cpu_percent or 100,
            #device_requests= configs.device_requests,
            mem_limit= configs.mem_limit,
            environment= envars,
            labels= [containerLabel],
            auto_remove= True,
        )
        print("Container created")
        print(container)
        return True
    except Exception as e:
        print(e)
        return False

# Starts the container and execute the initial commands
def start(name: str, image: str, cmd: list):
    print("Container starting...")
    try:
        container = client.containers.get(name).start()
        print("Container logs")
        print(container)
        return container
    except Exception as e:
        print("Error starting the container")
        print(e)
        return False

# Get a list of all running workloads
def getRunningWorkloads():
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