def getAllTenants(vmanage, deviceId):
    """
    Lists all the tenants on the vManage
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    deviceId	 (string):	List all tenants associated with a vSmart
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant?deviceId={deviceId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def createTenant(vmanage, tenantModel):
    """
    Create a new tenant in Multi-Tenant vManage
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantModel:	Tenant model
    
    tenantModel Parameter example
    
    param = {
        "password": "12345",
        "tenantIdList": [
        "0f4f1c6e-47da-40c4-8517-9d1e918965d9",
        "6b7b23bf-5dba-4cca-a36c-1c3cc2254d68"
        ]
    }
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant"
    response = vmanage.apiCall("POST", endpoint, tenantModel)
    return response
def createTenantAsync(vmanage, tenantModel):
    """
    Create a new tenant in Multi-Tenant vManage asynchronously
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantModel:	Tenant model
    
    tenantModel Parameter example
    
    param = {
        "password": "12345",
        "tenantIdList": [
        "0f4f1c6e-47da-40c4-8517-9d1e918965d9",
        "6b7b23bf-5dba-4cca-a36c-1c3cc2254d68"
        ]
    }
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/async"
    response = vmanage.apiCall("POST", endpoint, tenantModel)
    return response
def createTenantAsyncBulk(vmanage, tenantModel):
    """
    Create multiple tenants on vManage asynchronously
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantModel:	Tenant model
    
    tenantModel Parameter example
    
    param = {
        "password": "12345",
        "tenantIdList": [
        "0f4f1c6e-47da-40c4-8517-9d1e918965d9",
        "6b7b23bf-5dba-4cca-a36c-1c3cc2254d68"
        ]
    }
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/bulk/async"
    response = vmanage.apiCall("POST", endpoint, tenantModel)
    return response
def deleteTenantAsyncBulk(vmanage, tenantModel):
    """
    Delete multiple tenants on vManage asynchronously
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantModel:	Tenant model
    
    tenantModel Parameter example
    
    param = {
        "password": "12345",
        "tenantIdList": [
        "0f4f1c6e-47da-40c4-8517-9d1e918965d9",
        "6b7b23bf-5dba-4cca-a36c-1c3cc2254d68"
        ]
    }
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/bulk/async"
    response = vmanage.apiCall("DELETE", endpoint, tenantModel)
    return response
def getTenantvSmartMapping(vmanage):
    """
    Retrieve mapping of tenants to vSmarts
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/vsmart"
    response = vmanage.apiCall("GET", endpoint)
    return response
def tenantvSmartMtMigrate(vmanage):
    """
    Migrate tenants from single tenant vSmarts to multi-tenant capable vSmarts
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/vsmart-mt/migrate"
    response = vmanage.apiCall("POST", endpoint)
    return response
def getTenantHostingCapacityOnvSmarts(vmanage):
    """
    Lists all the vsmarts on the vManage and its tenant hosting capacity
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/vsmart/capacity"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getTenant(vmanage, tenantId):
    """
    Get a tenant by Id
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantId	 (string):	Tenant Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/{tenantId}"
    response = vmanage.apiCall("GET", endpoint)
    return response
def updateTenant(vmanage, tenantModel, tenantId):
    """
    Update a tenant in Multi-Tenant vManage
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantModel:	Tenant model
	tenantId	 (string):	Tenant Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/{tenantId}"
    response = vmanage.apiCall("PUT", endpoint, tenantModel)
    return response
def deleteTenant(vmanage, tenantModel, tenantId):
    """
    Delete a tenant by Id
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantModel:	Tenant model
	tenantId	 (string):	Tenant Id
    
    tenantModel Parameter example
    
    param = {
        "password": "12345",
        "tenantIdList": [
        "0f4f1c6e-47da-40c4-8517-9d1e918965d9",
        "6b7b23bf-5dba-4cca-a36c-1c3cc2254d68"
        ]
    }
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/{tenantId}/delete"
    response = vmanage.apiCall("POST", endpoint, tenantModel)
    return response
def switchTenant(vmanage, tenantId):
    """
    Switch to a specific tenant
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantId	 (string):	Tenant Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/{tenantId}/switch"
    response = vmanage.apiCall("POST", endpoint)
    return response
def vSessionId(vmanage, tenantId):
    """
    Get VSessionId for a specific tenant
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
    tenantId	 (string):	Tenant Id
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenant/{tenantId}/vsessionid"
    response = vmanage.apiCall("POST", endpoint)
    return response
def getAllTenantStatuses(vmanage):
    """
    List all tenant status
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenantstatus"
    response = vmanage.apiCall("GET", endpoint)
    return response
def forceStatusCollection(vmanage):
    """
    Force tenant status collection
    NOTE: In a multitenant vManage system, this API is only available in the Provider view.
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/tenantstatus/force"
    response = vmanage.apiCall("POST", endpoint)
    return response
