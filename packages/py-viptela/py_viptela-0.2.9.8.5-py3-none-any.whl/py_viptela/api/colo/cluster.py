def getDetail(vmanage, clusterName):
    """
    Get details of all existing Clusters
    
    Parameters:
    clusterName	 (string):	Cluster name
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster?clusterName={clusterName}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def update(vmanage, clusterconfig):
    """
    Update a existing cluster
    
    Parameters:
    clusterconfig:	Cluster config
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster"
    response = vmanage.apiCall("PUT", endpoint, clusterconfig)
    return response

def create(vmanage, clusterconfig):
    """
    Add a new cluster
    
    Parameters:
    clusterconfig:	Cluster config
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster"
    response = vmanage.apiCall("POST", endpoint, clusterconfig)
    return response

def acitvate(vmanage, clusterName):
    """
    Activate a cluster
    
    Parameters:
    clusterName	 (string):	Cluster name
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/activate?clusterName={clusterName}"
    response = vmanage.apiCall("POST", endpoint)
    return response

def dummyccm(vmanage, clusterName):
    """
    Activate dummp cluster
    
    Parameters:
    clusterName	 (string):	Cluster name
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/activateClusterDummy?clusterName={clusterName}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def dummycspState(vmanage, clusterName, state):
    """
    Activate cluster in a state
    
    Parameters:
    clusterName	 (string):	Cluster name
	state	 (string):	Cluster state
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/activateClusterDummyState?clusterName={clusterName}&state={state}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def updateCspToCluster(vmanage, cspconfig):
    """
    Update attached csp to cluster
    
    Parameters:
    cspconfig:	CSP config
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/attached/csp"
    response = vmanage.apiCall("PUT", endpoint, cspconfig)
    return response

def preview(vmanage, serialNumber):
    """
    Clouddock cluster preview
    
    Parameters:
    serialNumber	 (string):	Serial number
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/config?serialNumber={serialNumber}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def deAcitvate(vmanage, clusterId):
    """
    Deactivate clouddock cluster
    
    Parameters:
    clusterId	 (string):	Cluster Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/deactivate?clusterId={clusterId}"
    response = vmanage.apiCall("POST", endpoint)
    return response

def getDetailById(vmanage, clusterId):
    """
    Get cluster by Id
    
    Parameters:
    clusterId	 (string):	Cluster Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/id?clusterId={clusterId}"
    response = vmanage.apiCall("GET", endpoint)
    return response

def rmaCloudDockCsp(vmanage, bodyParameter, clusterName):
    """
    RMA operation for CSP device
    
    Parameters:
    bodyParameter:	Description
	clusterName	 (string):	Cluster name
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/rma?clusterName={clusterName}"
    response = vmanage.apiCall("POST", endpoint, bodyParameter)
    return response

def deleteByName(vmanage, clustername):
    """
    Delete cluster by name
    
    Parameters:
    clustername	 (string):	Cluster name
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/colocation/cluster/{clustername}"
    response = vmanage.apiCall("DELETE", endpoint)
    return response
