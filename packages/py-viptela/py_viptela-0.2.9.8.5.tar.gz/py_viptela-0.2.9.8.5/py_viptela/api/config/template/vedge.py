def generatePolicyTemplateList(vmanage):
    """
    Get policy details
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge"
    response = vmanage.apiCall("GET", endpoint)
    return response

def createVEdgeTemplate(vmanage, templatepolicy):
    """
    Create template
    
    Parameters:
    templatepolicy:	Template policy
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge"
    response = vmanage.apiCall("POST", endpoint, templatepolicy)
    return response

def getVEdgeTemplate(vmanage, policyId):
    """
    Get template
    
    Parameters:
    policyId	 (string):	Policy Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge/definition/{policyId}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def getVEdgePolicyDeviceList(vmanage):
    """
    Get device list
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge/devices"
    response = vmanage.apiCall("GET", endpoint)
    return response

def getDeviceListByPolicy(vmanage, policyId):
    """
    Get device list by policy
    
    Parameters:
    policyId	 (string):	Policy Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge/devices/{policyId}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def editVEdgeTemplate(vmanage, templatepolicy, policyId):
    """
    Edit template
    
    Parameters:
    templatepolicy:	Template policy
	policyId	 (string):	Policy Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge/{policyId}"
    response = vmanage.apiCall("PUT", endpoint, templatepolicy)
    return response

def deleteVEdgeTemplate(vmanage, policyId):
    """
    Delete template
    
    Parameters:
    policyId	 (string):	Policy Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge/{policyId}"
    response = vmanage.apiCall("DELETE", endpoint)
    return response

def changePolicyResourceGroup(vmanage, policyId, resourceGroupName):
    """
    Change policy resource group
    
    Parameters:
    policyId	 (string):	Policy Id
	resourceGroupName	 (string):	Resrouce group name
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/template/policy/vedge/{resourceGroupName}/{policyId}"
    response = vmanage.apiCall("POST", endpoint)
    return response
