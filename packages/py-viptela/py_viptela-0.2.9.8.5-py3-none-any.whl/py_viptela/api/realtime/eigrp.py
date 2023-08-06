def getInterface(vmanage, deviceId):
    """
    Get EIGRP interface list from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/eigrp/interface?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getRoute(vmanage, deviceId):
    """
    Get EIGRP route from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/eigrp/route?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getTopology(vmanage, deviceId):
    """
    Get EIGRP topology info from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/eigrp/topology?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
