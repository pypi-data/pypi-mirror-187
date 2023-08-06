def getAclAssociations(vmanage, deviceId):
    """
    Get access list associations from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/accesslistassociations?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclCounters(vmanage, deviceId):
    """
    Get access list counter from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/accesslistcounters?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclNames(vmanage, deviceId):
    """
    Get access list names from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/accesslistnames?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclPolicers(vmanage, deviceId):
    """
    Get access list policers from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/accesslistpolicers?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAppRouteFilter(vmanage, deviceId):
    """
    Get approute policy filter from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/approutepolicyfilter?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getDataPolicyFilter(vmanage, deviceId):
    """
    Get data policy filters from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/datapolicyfilter?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getFilterMemUsage(vmanage, deviceId):
    """
    Get data policy filter memory usage from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/filtermemoryusage?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclAssocV6(vmanage, deviceId):
    """
    Get access list associations from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/ipv6/accesslistassociations?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclCountersV6(vmanage, deviceId):
    """
    Get access list counters from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/ipv6/accesslistcounters?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclNamesV6(vmanage, deviceId):
    """
    Get access list names from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/ipv6/accesslistnames?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getAclPolicersV6(vmanage, deviceId):
    """
    Get access list policers from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/ipv6/accesslistpolicers?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getQosMapInfo(vmanage, deviceId):
    """
    Get QoS map information from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/qosmapinfo?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getQosSchedulerInfo(vmanage, deviceId):
    """
    Get QoS scheduler information from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/qosschedulerinfo?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getRewriteAssocInfo(vmanage, deviceId):
    """
    Get rewrite associations information from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/rewriteassociations?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getSdwanPolicyFromVsmart(vmanage, deviceId):
    """
    show Sdwan Policy From Vsmart
    
    Parameters:
    deviceId	 (string):	Device Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/vsmart?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getZoneDropStats(vmanage, deviceId):
    """
    Get zone drop statistics from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/zbfwdropstatistics?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getZbfwStats(vmanage, deviceId):
    """
    Get zone based firewall statistics from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/zbfwstatistics?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getZonePairSessions(vmanage, deviceId):
    """
    Get zone pair sessions from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/zonepairsessions?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getZonePairs(vmanage, deviceId):
    """
    Get zone pair statistics from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/zonepairstatistics?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getZonePolicyFilters(vmanage, deviceId):
    """
    Get zone policy filter from device
    
    Parameters:
    deviceId	 (string):	Device IP
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/device/policy/zonepolicyfilter?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
