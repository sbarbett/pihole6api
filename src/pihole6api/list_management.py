import urllib.parse


class PiHole6ListManagement:
    def __init__(self, connection):
        """
        Handles Pi-hole list management API endpoints.
        :param connection: Instance of PiHole6Connection for API requests.
        """
        self.connection = connection

    def add_list(self, address, list_type, comment=None, groups=None, enabled=True):
        """
        Add a new list to Pi-hole.

        :param address: URL of the blocklist/allowlist.
        :param list_type: Type of list ("allow" or "block").
        :param comment: Optional comment for the list.
        :param groups: Optional list of group IDs.
        :param enabled: Whether the list is enabled (default: True).
        """
        if list_type not in ["allow", "block"]:
            raise ValueError("list_type must be 'allow' or 'block'.")

        payload = {
            "address": address if isinstance(address, list) else [address],
            "comment": comment,
            "groups": groups if groups else [],
            "enabled": enabled
        }

        return self.connection.post(f"lists?type={list_type}", data=payload)

    def batch_delete_lists(self, lists):
        """
        Delete multiple lists.

        :param lists: List of dictionaries with keys "item" and "type".
                      Example: [{"item": "https://example.com/blocklist.txt", "type": "block"}]
        """
        if not isinstance(lists, list):
            raise ValueError("lists must be a list of dictionaries.")

        return self.connection.post("lists:batchDelete", data=lists)

    def get_list(self, address, list_type):
        """
        Retrieve information about a specific list.

        :param address: URL of the blocklist/allowlist.
        :param list_type: The type of list ("allow" or "block").
        """
        encoded_address = urllib.parse.quote(address, safe="")
        params = {"type": list_type}
        return self.connection.get(f"lists/{encoded_address}", params=params)

    def get_lists(self, list_type=None):
        """
        Retrieve all lists or lists of a specific type.

        :param list_type: The type of list ("allow" or "block") (optional).
        """
        params = {"type": list_type} if list_type else {}
        return self.connection.get("lists", params=params)

    def update_list(self, address, list_type, comment=None, groups=None, enabled=True):
        """
        Update an existing list.

        :param address: URL of the blocklist/allowlist.
        :param list_type: Type of list ("allow" or "block").
        :param comment: Updated comment (optional).
        :param groups: Updated list of group IDs (optional).
        :param enabled: Whether the list is enabled (default: True).
        """
        encoded_address = urllib.parse.quote(address, safe="")
        payload = {
            "comment": comment,
            "groups": groups if groups else [],
            "enabled": enabled
        }

        return self.connection.put(f"lists/{encoded_address}?type={list_type}", data=payload)

    def delete_list(self, address, list_type):
        """
        Delete a specific list entry.

        :param address: The URL of the list to delete.
        :param list_type: The type of list ("allow" or "block").
        """
        encoded_address = urllib.parse.quote(address, safe="")
        params = {"type": list_type}
        return self.connection.delete(f"lists/{encoded_address}", params=params)

    def search_list(self, domain, num=None, partial=False, debug=False):
        """
        Search for a domain in Pi-hole's lists.

        :param domain: Domain to search for.
        :param num: Maximum number of results to be returned (optional).
        :param partial: Boolean flag to enable partial matching (optional).
        :param debug: Boolean flag to add debug information to the response (optional).
        """
        params = {
            "partial": str(partial).lower(),
            "debug": str(debug).lower(),
        }
        if num is not None:
            params["n"] = num

        return self.connection.get(f"search/{domain}", params=params)
