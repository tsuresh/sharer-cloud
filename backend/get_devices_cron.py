import utils

try:
    utils.makeRestCall("requestVacantClients",{})
except Exception as e:
    print(str(e))