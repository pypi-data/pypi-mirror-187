def getSlaList(vmanage, deviceId):
    """
    Get SLA class list from device (Real Time)
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/app-route/sla-class?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getStatList(vmanage, remote_system_ip, local_color, remote_color, deviceId):
    """
    Get application-aware routing statistics from device (Real Time)
    
    Parameters:
    remote-system-ip	 (string):	Remote system IP
	local-color	 (string):	Local color
	remote-color	 (string):	Remote color
	deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/app-route/statistics?remote-system-ip={remote_system_ip}&local-color={local_color}&remote-color={remote_color}&deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
