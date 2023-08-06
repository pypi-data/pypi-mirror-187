def getClients(vmanage, deviceId):
    """
    Get DOT1x client from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dot1x/clients?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getInterfaces(vmanage, deviceId):
    """
    Get DOT1x interface from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dot1x/interfaces?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getRadius(vmanage, deviceId):
    """
    Get DOT1x Radius from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dot1x/radius?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
