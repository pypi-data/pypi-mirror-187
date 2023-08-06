def getGroups(vmanage, deviceId):
    """
    Get IGMP neighbor list from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/igmp/groups?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getInterfaces(vmanage, deviceId):
    """
    Get IGMP interface list from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/igmp/interface?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getStats(vmanage, deviceId):
    """
    Get IGMP statistics list from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/igmp/statistics?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getSummary(vmanage, deviceId):
    """
    Get IGMP summary from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/igmp/summary?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
