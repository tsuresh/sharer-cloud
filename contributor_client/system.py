import platform,socket,re,uuid,psutil,logging,cpuinfo,GPUtil,api,speedtest

def updateSystemStatus(token):
    api.updateSystemSpecs(getSystemInfo(), token)

def updateNetworkStatus(token):
    api.updateSystemSpecs(getNetworkSpeed(), token)

def updateCpuUsage(token):
    api.updateSystemSpecs(getProcessorInfo(), token)

def updateGpuUsage(token):
    api.updateSystemSpecs(getGPUInfo(), token)

def updateContainerInfo(token):
    print("Update container status")

# Get processor info
def getProcessorInfo():
    info = {}
    info['arch'] = cpuinfo.get_cpu_info()['arch']
    info['bits'] = cpuinfo.get_cpu_info()['bits']
    info['arch_string_raw'] = cpuinfo.get_cpu_info()['arch_string_raw']
    info['brand_raw'] = cpuinfo.get_cpu_info()['brand_raw']
    info['hz_actual_friendly'] = cpuinfo.get_cpu_info()['hz_actual_friendly']
    info['hz_actual'] = cpuinfo.get_cpu_info()['hz_actual'] #power
    info['flags'] = cpuinfo.get_cpu_info()['flags']
    return {'cpu' : info}

# Get GPU related info
def getGPUInfo():
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        info = {}
        info['id'] = gpu.id
        info['name'] = gpu.name
        info['load'] = f"{gpu.load * 100}%"
        info['memoryFree'] = gpu.memoryFree
        info['memoryUsed'] = gpu.memoryUsed
        info['memoryTotal'] = gpu.memoryTotal
        info['temperature'] = gpu.temperature
        info['uuid'] = gpu.uuid
        list_gpus.append(info)
        return {'gpu' : list_gpus}

# Get system related info
def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return {'system' : info}
    except Exception as e:
        logging.exception(e)
    
# Get network speed
def getNetworkSpeed():
    network = speedtest.Speedtest()
    info={}
    info['download-speed']=network.upload()
    info['upload-speed']=network.download()
    return {'network', info}

def updateAll(token):
    updateSystemStatus(token)
    updateCpuUsage(token)
    updateGpuUsage(token)

updateAll('12346546546')