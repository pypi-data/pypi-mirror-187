def createSmuList(vmanage, deviceId):
    """
    Get software list from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/smu?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def createSyncedSmuList(vmanage, deviceId):
    """
    Get software list from device synchronously
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/smu/synced?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getSoftwareList(vmanage, deviceId):
    """
    Get software list from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/software?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getSyncedSoftwareList(vmanage, deviceId):
    """
    Get software list from device synchronously
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/software/synced?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
