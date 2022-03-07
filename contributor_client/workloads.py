from queue import Empty
import yaml
import config
import runtime.docker_env

#place workloads within running containers
def placeWorkloads(payloadId, payloadUrl, spec, config):

    parsedSpec = parseSpec(spec)

    #create a container and deploy the workload
    containerStatus = runtime.docker_env.create(
        "sharercloud-wl-" + payloadId,
        parsedSpec["image"],
        #["mkdir sc_wl_" + payloadId, "cd sc_wl_" + payloadId, "wget " + payloadUrl, "unzip " + str(payloadId) + ".zip"],
        ["echo test"],
        parsedSpec["envars"],
        config
    )

    print(containerStatus)

    #start deploy commands
    # if containerStatus is True:
    #     resultLog = runtime.docker_env.start(
    #         "sharercloud-wl-" + payloadId,
    #         parsedSpec["image"],
    #         parsedSpec["start_commands"]
    #     )
    #     print("Got the final result")
    #     print(resultLog)
    # else:
    #     print("Unable to create the container")

    #pass result to frontend

def checkPlaceability(spec, config):

    parsedSpec = parseSpec(spec)

    #Check subscribed images
    if parsedSpec["image"] not in config.images:
        print("Incompatible image")
        return {
            'status' : False,
            'message' : 'Incompatible image'
        }

    #Check if there's existing processes
    if len(runtime.docker_env.getRunningWorkloads()) > 0:
        print("There are existing processes running")
        return {
            'status' : False,
            'message' : 'There are existing processes running'
        }

    #Check if the spec matches the hardware
    if parsedSpec["cpu_count"] is not None:
        if parsedSpec["cpu_count"] > config.cpu_count:
            print("Required CPU count is not sufficient")
            return {
                'status' : False,
                'message' : 'Required CPU count is not sufficient'
            }

    #Check for CPU percentage allocation
    if parsedSpec["cpu_percent"] is not None:
        if parsedSpec["cpu_percent"] > config.cpu_percent:
            print("Required CPU percentage is not sufficient")
            return {
                'status' : False,
                'message' : 'Required CPU percentage is not sufficient'
            }

    #Check for special requests
    if all(item in config.device_requests for item in parsedSpec["device_requests"]) is False:
        print("Required special features are not available in device")
        return {
            'status' : False,
            'message' : 'Required special features are not available in device'
        }
    
    return {
        'status' : True,
        'message' : 'Container is ready to be scheduled'
    }

def parseSpec(parsedSpec):
    spec = {}

    if parsedSpec["spec"]["image"] is not None:
        spec["image"] = parsedSpec["spec"]["image"]

    if parsedSpec["spec"]["cpu_count"] is not None:
        spec["cpu_count"] = parsedSpec["spec"]["cpu_count"]

    if parsedSpec["spec"]["cpu_percent"] is not None:
        spec["cpu_percent"] = parsedSpec["spec"]["cpu_percent"]

    if parsedSpec["spec"]["device_requests"] is not []:
        spec["device_requests"] = parsedSpec["spec"]["device_requests"]

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

placeability = checkPlaceability(
    getYamlConfig(),
    config.configs
)

print(placeability)

placement = placeWorkloads(
    "123456",
    "https://inforwaves.com/",
    getYamlConfig(),
    config.configs
)

