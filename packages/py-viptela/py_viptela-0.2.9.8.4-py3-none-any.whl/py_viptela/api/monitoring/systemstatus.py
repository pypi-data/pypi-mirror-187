def getStatDataRawData(vmanage, query):
    """
    Get stats raw data
    
    Parameters:
    query	 (string):	Query string
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/system/stats?query={query_string}"
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
    
    endpoint = f"dataservice/statistics/system/stats"
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
    endpoint = f"dataservice/statistics/system/stats/aggregation?query={query_string}"
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
    
    endpoint = f"dataservice/statistics/system/stats/aggregation"
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
    
    endpoint = f"dataservice/statistics/system/stats/app-agg/aggregation"
    response = vmanage.apiCall("POST", endpoint, statsquerystring)
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
    endpoint = f"dataservice/statistics/system/stats/csv?query={query_string}"
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
    endpoint = f"dataservice/statistics/system/stats/doccount?query={query_string}"
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
    
    endpoint = f"dataservice/statistics/system/stats/doccount"
    response = vmanage.apiCall("POST", endpoint, query)
    return response
def getStatDataFields(vmanage):
    """
    Get fields and type
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/system/stats/fields"
    response = vmanage.apiCall("GET", endpoint)
    return response
def getStatBulkRawData(vmanage, query, scrollId, count):
    """
    Get stats raw data
    
    Parameters:
    query	     (string):	Query string
	scrollId	 (string):	ES scroll Id
	count	     (string):	Result size
    
    Returns
    response    (dict)
    
    
    """
    query_string = vmanage.builder.generateQuery(query)
    endpoint = f"dataservice/statistics/system/stats/page?query={query_string}&scrollId={scrollId}&count={count}"
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
    
    endpoint = f"dataservice/statistics/system/stats/page?scrollId={scrollId}&count={count}"
    response = vmanage.apiCall("POST", endpoint, statsquerystring)
    return response
def getStatQueryFields(vmanage):
    """
    Get query fields
    
    Parameters:
            
    Returns
    response    (dict)
    
    
    """
    
    endpoint = f"dataservice/statistics/system/stats/query/fields"
    response = vmanage.apiCall("GET", endpoint)
    return response
