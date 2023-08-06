def onboardMDP(vmanage, onboard):
    """
    Start MDP onboarding operation
    
    Parameters:
    onboard:	Onboard
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/mdp/onboard"
    response = vmanage.apiCall("POST", endpoint, onboard)
    return response

def getOnboardStatus(vmanage):
    """
    Get MDP onboarding status
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/mdp/onboard/status"
    response = vmanage.apiCall("GET", endpoint)
    return response

def updateOnboardingPayload(vmanage, onboard, nmsId):
    """
    update MDP onboarding document
    
    Parameters:
    onboard:	Onboard
	Parameter Description
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/mdp/onboard/{nmsId}"
    response = vmanage.apiCall("PUT", endpoint, onboard)
    return response
