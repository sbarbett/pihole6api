import warnings

class PiHole6Metrics:
    def __init__(self, connection):
        """
        Handles Pi-hole metrics and stats API endpoints.
        :param connection: Instance of PiHole6Connection for API requests.
        """
        self.connection = connection

    # History API Endpoints
    def get_history(self):
        """Get activity graph data"""
        return self.connection.get("history")

    def get_history_clients(self, clients=20):
        """
        Get per-client activity graph data

        :param num: Number of clients to return, 0 will return all clients
        """
        params = {"n": clients}
        return self.connection.get("history/clients", params=params)

    def get_history_database(self, start, end):
        """
        Get long-term activity graph data
        
        :param start: Start date in unix timestamp format
        :param end: End date in unix timestamp format
        """
        params = {"from": start, "until": end}
        return self.connection.get("history/database", params=params)

    def get_history_database_clients(self, start, end):
        """
        Get per-client long-term activity graph data
        
        :param start: Start date in unix timestamp format
        :param end: End date in unix timestamp format
        """
        params = {"from": start, "until": end}
        return self.connection.get("history/database/clients", params=params)

    # Query API Endpoints
    def get_queries(self, length=100, from_ts=None, until_ts=None, upstream=None, domain=None, client=None, cursor=None, **kwargs):
        """
        Get query log with optional filtering parameters.

        :param int length: Number of queries to retrieve (default: 100). 
            (Note: The old parameter 'n' is deprecated and will be removed in a future version.)
        :param int from_ts: Unix timestamp to filter queries from this time onward (optional).
        :param int until_ts: Unix timestamp to filter queries up to this time (optional).
        :param str upstream: Filter queries sent to a specific upstream destination (optional).
        :param str domain: Filter queries for specific domains, supports wildcards `*` (optional).
        :param str client: Filter queries originating from a specific client IP (optional).
        :param str cursor: Cursor for pagination to fetch the next chunk of results (optional).
        """
        # Check for deprecated "n" parameter
        if "n" in kwargs:
            warnings.warn(
                "The 'n' parameter is deprecated; please use 'length' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            length = kwargs.pop("n")
        
        if kwargs:
            raise TypeError("Unexpected keyword arguments: " + ", ".join(kwargs.keys()))
        
        params = {
            "length": length,
            "from": from_ts,
            "until": until_ts,
            "upstream": upstream,
            "domain": domain,
            "client_ip": client,
            "cursor": cursor,
        }
        # Remove any parameters that are None
        params = {k: v for k, v in params.items() if v is not None}
        return self.connection.get("queries", params=params)

    def get_query_suggestions(self):
        """Get query filter suggestions"""
        return self.connection.get("queries/suggestions")

    # Stats Database API Endpoints
    def get_stats_database_query_types(self, start, end):
        """
        Get query types (long-term database)
        
        :param start: Start date in unix timestamp format
        :param end: End date in unix timestamp format
        """
        params = {"from": start, "until": end}
        return self.connection.get("stats/database/query_types", params=params)

    def get_stats_database_summary(self, start, end):
        """
        Get database content details
        
        :param start: Start date in unix timestamp format
        :param end: End date in unix timestamp format
        """
        params = {"from": start, "until": end}
        return self.connection.get("stats/database/summary", params=params)

    def get_stats_database_top_clients(self, start, end, blocked=None, count=None):
        """
        Get top clients (long-term database).

        :param int start: Start date in Unix timestamp format.
        :param int end: End date in Unix timestamp format.
        :param bool blocked: Return information about permitted or blocked queries (optional).
        :param int count: Number of requested items (optional).
        """
        params = {
            "from": start,
            "until": end,
            "blocked": str(blocked).lower() if blocked is not None else None,
            "count": count
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.connection.get("stats/database/top_clients", params=params)

    def get_stats_database_top_domains(self, start, end, blocked=None, count=None):
        """
        Get top domains (long-term database)
        
        :param int start: Start date in Unix timestamp format.
        :param int end: End date in Unix timestamp format.
        :param bool blocked: Return information about permitted or blocked queries (optional).
        :param int count: Number of requested items (optional).
        """
        params = {
            "from": start,
            "until": end,
            "blocked": str(blocked).lower() if blocked is not None else None,
            "count": count
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.connection.get("stats/database/top_domains", params=params)

    def get_stats_database_upstreams(self, start, end):
        """
        Get upstream metrics (long-term database)
        
        :param start: Start date in unix timestamp format
        :param end: End date in unix timestamp format
        """
        params = {"from": start, "until": end}
        return self.connection.get("stats/database/upstreams", params=params)

    # Stats API Endpoints
    def get_stats_query_types(self):
        """Get current query types"""
        return self.connection.get("stats/query_types")

    def get_stats_recent_blocked(self, count=None):
        """
        Get most recently blocked domain
        
        :param int count: Number of requested items (optional).    
        """
        params = {"count": count}
        params = {k: v for k, v in params.items() if v is not None}
        return self.connection.get("stats/recent_blocked", params=params)  

    def get_stats_summary(self):
        """Get an overview of Pi-hole activity"""
        return self.connection.get("stats/summary")

    def get_stats_top_clients(self, blocked=None, count=None):
        """
        Get top clients
        
        :param bool blocked: Return information about permitted or blocked queries (optional).
        :param int count: Number of requested items (optional).
        """
        params = {
            "blocked": str(blocked).lower() if blocked is not None else None,
            "count": count
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.connection.get("stats/top_clients", params=params)

    def get_stats_top_domains(self, blocked=None, count=None):
        """
        Get top domains
        
        :param bool blocked: Return information about permitted or blocked queries (optional).
        :param int count: Number of requested items (optional).
        """
        params = {
            "blocked": str(blocked).lower() if blocked is not None else None,
            "count": count
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.connection.get("stats/top_domains", params=params)

    def get_stats_upstreams(self):
        """Get upstream destinations"""
        return self.connection.get("stats/upstreams")
