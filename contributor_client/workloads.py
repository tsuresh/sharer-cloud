import yaml
import runtime.docker_env
import requests
import os

#place workloads within running containers
def placeWorkloads(payloadId, payloadUrl, spec, config):

    parsedSpec = parseSpec(spec)

    startCommands = ' && '.join(parsedSpec["start_commands"])

    postCommands = 'zip -r output.zip . && curl -F "workload_id={workload_id}" -F "file=@output.zip" -F "contributor_id={contributor_id}" -F "status={status}" -F "time_consumed={time_consumed}" -F "type=output" http://host.docker.internal:5000/upload'.format(workload_id=payloadId, contributor_id=config.contributor_id, status="success", time_consumed="1")

    #pull missing images
    runtime.docker_env.pullImages(config)

    #create a container and deploy the workload
    containerLogs = runtime.docker_env.create(
        "sharercloud-wl-" + payloadId,
        parsedSpec["image"],
        parsedSpec["envars"],
        "apt-get update -y && apt-get install -y unzip zip curl && mkdir sc_wl_{payloadId} && cd sc_wl_{payloadId} && wget {payloadUrl} && unzip {fileName} && {startCommands} > console.out && {postCommands}".format(payloadId=payloadId, payloadUrl=payloadUrl, startCommands=startCommands, fileName=os.path.basename(payloadUrl), postCommands=postCommands),
        config
    )

    return containerLogs

def deployArtefacts(url: str, container_name: str):

    dest_folder = "./artefacts"

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

        dst = "{container_name}:/var/{file_name}".format(container_name=container_name, file_name=filename)
        print(dst)

        data = open(file_path, 'rb').read()
        status = runtime.docker_env.addArtefacts(container_name, dst, data)
        print(status)

    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

def checkMachineVacantStatus(config: object, sid=None, deviceToken=None):
    #Check if there's existing processes
    if len(runtime.docker_env.getRunningWorkloads()) > 0:
        print("There are existing processes running")
        return {
            'status' : False,
            'message' : 'There are existing processes running',
            'sid' : sid,
            'token' : deviceToken,
            'machine_type' : config.machine_type,
            'contributor_id' : config.contributor_id,
            'machine_name' : config.machine_name
        }

    return {
        'status' : True,
        'message' : 'Machine is vacant',
        'sid' : sid,
        'token' : deviceToken,
        'machine_type' : config.machine_type,
        'contributor_id' : config.contributor_id,
        'machine_name' : config.machine_name
    }

def checkPlaceability(spec: str, config: object, workloadId=None, sid=None, deviceToken=None):

    parsedSpec = parseSpec(spec)

    #Check subscribed images
    if parsedSpec["image"] not in config.images:
        print("Incompatible image")
        return {
            'status' : False,
            'message' : 'Incompatible image',
            'sid' : sid,
            'token' : deviceToken,
            'workload_id' : workloadId,
            'machine_type' : config.machine_type
        }

    #Check if there's existing processes
    if len(runtime.docker_env.getRunningWorkloads()) > 0:
        print("There are existing processes running")
        return {
            'status' : False,
            'message' : 'There are existing processes running',
            'sid' : sid,
            'token' : deviceToken,
            'workload_id' : workloadId,
            'machine_type' : config.machine_type
        }

    #Check if the spec matches the hardware
    if parsedSpec["cpu_count"] is not None:
        if parsedSpec["cpu_count"] > config.cpu_count:
            print("Required CPU count is not sufficient")
            return {
                'status' : False,
                'message' : 'Required CPU count is not sufficient',
                'sid' : sid,
                'token' : deviceToken,
                'workload_id' : workloadId,
                'machine_type' : config.machine_type
            }

    #Check for CPU percentage allocation
    if parsedSpec["cpu_percent"] is not None:
        if parsedSpec["cpu_percent"] > config.cpu_percent:
            print("Required CPU percentage is not sufficient")
            return {
                'status' : False,
                'message' : 'Required CPU percentage is not sufficient',
                'sid' : sid,
                'token' : deviceToken,
                'workload_id' : workloadId,
                'machine_type' : config.machine_type
            }
    
    return {
        'status' : True,
        'message' : 'Container is ready to be scheduled',
        'sid' : sid,
        'token' : deviceToken,
        'workload_id' : workloadId,
        'machine_type' : config.machine_type
    }

def parseSpec(parsedSpec):
    spec = {}

    if parsedSpec["spec"]["image"] is not None:
        spec["image"] = parsedSpec["spec"]["image"]

    if parsedSpec["spec"]["cpu_count"] is not None:
        spec["cpu_count"] = parsedSpec["spec"]["cpu_count"]

    if parsedSpec["spec"]["cpu_percent"] is not None:
        spec["cpu_percent"] = parsedSpec["spec"]["cpu_percent"]

    # if parsedSpec["spec"]["device_requests"] is not []:
    #     spec["device_requests"] = parsedSpec["spec"]["device_requests"]

    if parsedSpec["spec"]["resultType"] is not None:
        spec["resultType"] = parsedSpec["spec"]["resultType"] #rawOut, fileWrite, noOut

    if parsedSpec["spec"]["start_commands"] is not []:
        spec["start_commands"] = parsedSpec["spec"]["start_commands"]

    if parsedSpec["spec"]["envars"] is not []:
        spec["envars"] = []
        for envar in parsedSpec["spec"]["envars"]:
            envarKey = list(envar.keys())[0]
            envarVals = list(envar.values())[0]
            spec["envars"].append(envarKey + "=" + envarVals);

    return spec

def getYamlConfig():
    with open("spec.yaml", "r") as stream:
        try:
            yamldata = yaml.safe_load(stream)
            return yamldata
        except yaml.YAMLError as exc:
            print(exc)

# placeability = checkPlaceability(
#     getYamlConfig(),
#     config.configs
# )

# print(placeability)

# placement = placeWorkloads(
#     "123456",
#     "https://inforwaves.com/",
#     getYamlConfig(),
#     config.configs
# )

# print(placement)
