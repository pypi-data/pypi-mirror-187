def getStatDataRawData(vmanage, query):
    """
    Get stats raw data
    
    Parameters:
    query	 (string):	Query string
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd?query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def getStatsRawData(vmanage, statsquerystring):
    """
    Get stats raw data
    
    Parameters:
    statsquerystring:	Stats query string
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd"
    response = vmanage.apiCall("POST", endpoint, statsquerystring)
    return response
def getAggregationDataByQuery(vmanage, query):
    """
    Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
    
    Parameters:
    query	 (string):	Query filter
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/aggregation?query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def getPostAggregationDataByQuery(vmanage, statsquerystring):
    """
    Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
    
    Parameters:
    statsquerystring:	Stats query string
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd/aggregation"
    response = vmanage.apiCall("POST", endpoint, statsquerystring)
    return response
def getPostAggregationAppDataByQuery(vmanage, statsquerystring):
    """
    Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
    
    Parameters:
    statsquerystring:	Stats query string
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd/app-agg/aggregation"
    response = vmanage.apiCall("POST", endpoint, statsquerystring)
    return response
def createFlowsGrid(vmanage, vpn, deviceId, limit, query):
    """
    Generate cflowd flows list in a grid table
    
    Parameters:
    vpn	 (string):	VPN Id
	deviceId	 (string):	Device IP
	limit	 (integer):	Limit
	query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/applications?vpn={vpn}&deviceId={deviceId}&limit={limit}&query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def createFlowssummary(vmanage, limit, query):
    """
    Generate cflowd flows list in a grid table
    
    Parameters:
    limit	 (integer):	Limit
	query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/applications/summary?limit={limit}&query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def getStatDataRawDataAsCSV(vmanage, query):
    """
    Get raw data with optional query as CSV
    
    Parameters:
    query	 (string):	Query string
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/csv?query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def createFlowDeviceData(vmanage, query):
    """
    Generate cflowd flows list in a grid table
    
    Parameters:
    query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/device/applications?query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def getCount(vmanage, query):
    """
    Get response count of a query
    
    Parameters:
    query	 (string):	Query
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/doccount?query={query_string}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def getCountPost(vmanage, query):
    """
    Get response count of a query
    
    Parameters:
    query:	Query
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd/doccount"
    response = vmanage.apiCall("POST", endpoint, query)
    return response
def getStatDataFields(vmanage):
    """
    Get fields and type
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd/fields"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getStatBulkRawData(vmanage, query, scrollId, count):
    """
    Get stats raw data
    
    Parameters:
    query	 (string):	Query string
	scrollId	 (string):	ES scroll Id
	count	 (string):	Result size
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/cflowd/page?query={query_string}&scrollId={scrollId}&count={count}"
    response     = vmanage.apiCall("GET", endpoint)
    return response
def getPostStatBulkRawData(vmanage, statsquerystring, scrollId, count):
    """
    Get stats raw data
    
    Parameters:
    statsquerystring:	Stats query string
	scrollId	 (string):	ES scroll Id
	count	 (string):	Result size
    
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd/page?scrollId={scrollId}&count={count}"
    response = vmanage.apiCall("POST", endpoint, statsquerystring)
    return response
def getStatQueryFields(vmanage):
    """
    Get query fields
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/cflowd/query/fields"
    response = vmanage.apiCall("GET", endpoint)
    return response
