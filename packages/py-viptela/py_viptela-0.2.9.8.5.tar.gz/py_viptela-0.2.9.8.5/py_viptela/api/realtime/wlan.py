def getWLANClients(vmanage, deviceId):
    """
    Get WLAN client from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wlan/clients?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getWLANInterfaces(vmanage, deviceId):
    """
    Get WLAN interface from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wlan/interfaces?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getWLANRadios(vmanage, deviceId):
    """
    Get WLAN Radios from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wlan/radios?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getWLANRadius(vmanage, deviceId):
    """
    Get WLAN RADIUS authentication from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wlan/radius?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
