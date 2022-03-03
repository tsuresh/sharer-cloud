import platform,socket,re,uuid,json,psutil,logging,cpuinfo,GPUtil

def getProcessorInfo():
    info = {}
    info['arch'] = cpuinfo.get_cpu_info()['arch']
    info['bits'] = cpuinfo.get_cpu_info()['bits']
    info['arch_string_raw'] = cpuinfo.get_cpu_info()['arch_string_raw']
    info['brand_raw'] = cpuinfo.get_cpu_info()['brand_raw']
    info['hz_actual_friendly'] = cpuinfo.get_cpu_info()['hz_actual_friendly']
    info['hz_actual'] = cpuinfo.get_cpu_info()['hz_actual'] #power
    info['flags'] = cpuinfo.get_cpu_info()['flags']
    return json.dumps(info)

def getGPUInfo():
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        gpu_id = gpu.id
        gpu_name = gpu.name
        gpu_load = f"{gpu.load * 100}%"
        gpu_free_memory = f"{gpu.memoryFree}MB"
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature, gpu_uuid
        ))
        return json.dumps(list_gpus)

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
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)

json.loads(getSystemInfo())