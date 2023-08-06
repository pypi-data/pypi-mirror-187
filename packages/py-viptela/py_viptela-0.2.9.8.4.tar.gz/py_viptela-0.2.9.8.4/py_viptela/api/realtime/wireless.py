def getClients(vmanage, deviceId):
    """
    Get wireless clients from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wireless/client?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getRadios(vmanage, deviceId):
    """
    Get wireless Radios from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wireless/radio?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getSsid(vmanage, deviceId):
    """
    Get wireless SSID from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/wireless/ssid?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
