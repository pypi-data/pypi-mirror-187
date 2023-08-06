def getAccessTokenforDevice(vmanage):
    """
    getAccessTokenforDevice Description
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/accesstoken"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAzureToken(vmanage, bodyParameter):
    """
    Get Azure token
    
    Parameters:
    bodyParameter:	Description
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/authtoken"
    response = vmanage.apiCall("POST", endpoint, bodyParameter)
    return response
def connect(vmanage):
    """
    Telemetry Opt In
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/connect"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getCloudCreds(vmanage):
    """
    Get cloud service credentials
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/credentials"
    response = vmanage.apiCall("GET", endpoint)
    return response
def addCloudCreds(vmanage, bodyParameter):
    """
    Get cloud service settings
    
    Parameters:
    bodyParameter:	Description
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/credentials"
    response = vmanage.apiCall("POST", endpoint, bodyParameter)
    return response
def getDeviceCode(vmanage):
    """
    Get Azure device code
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/devicecode"
    response = vmanage.apiCall("POST", endpoint)
    return response
def isStaging(vmanage):
    """
    Check if testbed or production
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/staging"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getTelemetryState(vmanage):
    """
    Get Telemetry state
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/telemetry"
    response = vmanage.apiCall("GET", endpoint)
    return response
def optIn(vmanage, bodyParameter):
    """
    Telemetry Opt In
    
    Parameters:
    bodyParameter:	Description
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/telemetry/optin"
    response = vmanage.apiCall("PUT", endpoint, bodyParameter)
    return response
def optOut(vmanage, bodyParameter):
    """
    Telemetry Opt Out
    
    Parameters:
    bodyParameter:	Description
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/cloudservices/telemetry/optout"
    response = vmanage.apiCall("DELETE", endpoint, bodyParameter)
    return response
def getCloudSettings(vmanage):
    """
    Get cloud service settings
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/dca/cloudservices"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getOTP(vmanage):
    """
    Get cloud service OTP value
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/dca/cloudservices/otp"
    response = vmanage.apiCall("GET", endpoint)
    return response
def updatetOTP(vmanage, cloudserviceotpvalue):
    """
    Update cloud service OTP value
    
    Parameters:
    cloudserviceotpvalue:	Cloud service OTP value
    
    Returns
    response    (dict)
    
    
    """
    
    vmanage.client.session.headers['Content-Type'] = "application/octet-stream"
    endpoint = f"dataservice/dca/cloudservices/otp"
    response = vmanage.apiCall("PUT", endpoint, cloudserviceotpvalue)
    return response
def listEntityOwnerInfo(vmanage):
    """
    List all entity ownership info
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/entityownership/list"
    response = vmanage.apiCall("GET", endpoint)
    return response
def entityOwnerInfo(vmanage):
    """
    Entity ownership info grouped by buckets
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/entityownership/tree"
    response = vmanage.apiCall("GET", endpoint)
    return response
