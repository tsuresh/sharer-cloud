import docker
from contributor_client.config import configs

#chosen environments @TODO make it choosable
environments = ['busybox']

# Retrive docker status
try:
    client = docker.from_env()
    print(client.containers.list())
except:
    print('Docker has not started or not running')

# Pull the user prefered images
def pullImages():
    for environment in config.environments:
        if environment not in client.images.list():
            print("Fetching image..." + environment)
            client.images.pull(environment)
            print("Fetching image successful..." + environment)

# Create the container under the given system boundaries
def create(name, image, deployCmd, envars):
    container = client.containers.create(
        name= name,
        image= image,
        command= deployCmd,
        cpu_count= configs.cpu_count or 1,
        cpu_percent= configs.cpu_percent or 100,
        device_requests= configs.device_requests,
        mem_limit= configs.mem_limit,
        entrypoint= entryPoint,
        environment= envars
    )
    print("Container created: " + container)

# Starts the container and execute the initial commands
def start(name, cmd):
    container = client.containers.run(
        name= name,
        command= cmd,
        auto_remove= True,
    )
    print("Container started: " + container)

def startContainer():
    print('start containers')

initiateContainer('busybox')