def getUmbrellaDevReg(vmanage, deviceId):
    """
    Get Umbrella device registration from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/umbrella/device-registration?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getUmbrellaDNSCrypt(vmanage, deviceId):
    """
    Get Umbrella DNScrypt information from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/umbrella/dnscrypt?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getUmbrellaDpStats(vmanage, deviceId):
    """
    Get Umbrella dp-stats from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/umbrella/dp-stats?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getUmbrellaOverview(vmanage, deviceId):
    """
    Get Umbrella overview from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/umbrella/overview?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getUmbrellaConfig(vmanage, deviceId):
    """
    Get Umbrella configuration from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/umbrella/umbrella-config?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
