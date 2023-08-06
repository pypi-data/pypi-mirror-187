def createApplicationsDetailList(vmanage, vpnId, application, query):
    """
    Get list of cloudexpress applications from device (Real Time)
    
    Parameters:
    vpnId	 (string):	VPN Id
	application	 (string):	Application
	query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/cloudx/application/detail?vpnId={vpnId}&application={application}&query={query}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def createApplicationsList(vmanage, vpnId, application, query):
    """
    Get list of cloudexpress applications from device (Real Time)
    
    Parameters:
    vpnId	 (string):	VPN Id
	application	 (string):	Application
	query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/cloudx/applications?vpnId={vpnId}&application={application}&query={query}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def createGatewayExitsList(vmanage, vpnId, application, deviceId):
    """
    Get list of cloudexpress gateway exits from device (Real Time)
    
    Parameters:
    vpnId	 (string):	VPN Id
	application	 (string):	Application
	deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/cloudx/gatewayexits?vpnId={vpnId}&application={application}&deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def createLbApplicationsList(vmanage, vpnId, application, query):
    """
    Get list of cloudexpress load balance applications from device (Real Time)
    
    Parameters:
    vpnId	 (string):	VPN Id
	application	 (string):	Application
	query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/cloudx/loadbalance?vpnId={vpnId}&application={application}&query={query}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def createLocalExitsList(vmanage, vpnId, application, deviceId):
    """
    Get list of cloudexpress local exits from device (Real Time)
    
    Parameters:
    vpnId	 (string):	VPN Id
	application	 (string):	Application
	deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/cloudx/localexits?vpnId={vpnId}&application={application}&deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
