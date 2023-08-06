def getClient(vmanage, deviceId):
    """
    Get DHCP client from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dhcp/client?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getInterface(vmanage, deviceId):
    """
    Get DHCP interfaces from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dhcp/interface?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getServer(vmanage, deviceId):
    """
    Get DHCP server from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dhcp/server?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getV6Interface(vmanage, deviceId):
    """
    Get DHCPv6 interfaces from device
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/dhcpv6/interface?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
