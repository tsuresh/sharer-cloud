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
        container = client.containers.create(
            name= name,
            image= image,
            command= deployCmd,
            cpu_count= configs.cpu_count or 1,
            cpu_percent= configs.cpu_percent or 100,
            #device_requests= configs.device_requests,
            mem_limit= configs.mem_limit,
            environment= envars,
            labels= [containerLabel]
        )
        print("Container created")
        print(container)
        return True
    except Exception as e:
        print(e)
        return False

# Starts the container and execute the initial commands
def start(name: str, cmd: list):
    try:
        container = client.containers.run(
            name= name,
            command= cmd,
            auto_remove= True,
        )
        print("Container logs")
        print(container)
        return container
    except:
        print("Unable to start container")
        return "Unable to start container"

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
    except:
        print("Unable to get containers")
        return []