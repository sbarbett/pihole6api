import json
import urllib.parse

class PiHole6Configuration:
    def __init__(self, connection):
        """
        Handles Pi-hole configuration API endpoints.
        :param connection: Instance of PiHole6Connection for API requests.
        """
        self.connection = connection

    def export_settings(self):
        """
        Export Pi-hole settings via the Teleporter API.
        :return: Binary content of the exported settings archive.
        """
        return self.connection.get("teleporter", is_binary=True)

    def import_settings(self, file_path, import_options=None):
        """
        Import Pi-hole settings using a Teleporter archive.

        :param file_path: Path to the .tar.gz Teleporter file.
        :param import_options: Dictionary of import options (default: import everything).
        :return: API response.
        """
        with open(file_path, "rb") as file:
            files = {"file": (file_path, file, "application/gzip")}
            data = {"import": json.dumps(import_options)} if import_options else {}

            return self.connection.post("teleporter", files=files, data=data)

    def get_config(self, detailed=False):
        """
        Get the current configuration of Pi-hole.

        :param detailed: Boolean flag to get detailed configuration.
        :return: API response containing configuration data.
        """
        return self.connection.get("config", params={"detailed": str(detailed).lower()})

    def update_config(self, config_changes):
        """
        Modify the Pi-hole configuration.

        :param config_changes: Dictionary containing configuration updates.
        :return: API response confirming changes.
        """
        payload = {"config": config_changes}
        return self.connection.patch("config", data=payload)

    def get_config_section(self, element, detailed=False):
        """
        Get a specific part of the Pi-hole configuration.

        :param element: The section of the configuration to retrieve.
        :param detailed: Boolean flag for detailed output.
        :return: API response with the requested config section.
        """
        return self.connection.get(f"config/{element}", params={"detailed": str(detailed).lower()})

    def add_config_item(self, element, value):
        """
        Add an item to a configuration array.

        :param element: The config section to modify.
        :param value: The value to add.
        :return: API response confirming the addition.
        """
        return self.connection.put(f"config/{element}/{value}")

    def delete_config_item(self, element, value):
        """
        Delete an item from a configuration array.

        :param element: The config section to modify.
        :param value: The value to remove.
        :return: API response confirming the deletion.
        """
        return self.connection.delete(f"config/{element}/{value}")

    def add_local_a_record(self, host, ip):
        """
        Add a local A record to Pi-hole.

        :param host: The hostname (e.g., "foo.dev")
        :param ip: The IP address (e.g., "192.168.1.1")
        :return: API response
        """
        encoded_value = urllib.parse.quote(f"{ip} {host}")
        return self.connection.put(f"config/dns/hosts/{encoded_value}")

    def remove_local_a_record(self, host, ip):
        """
        Remove a local A record from Pi-hole.

        :param host: The hostname (e.g., "foo.dev")
        :param ip: The IP address (e.g., "192.168.1.1")
        :return: API response
        """
        encoded_value = urllib.parse.quote(f"{ip} {host}")
        return self.connection.delete(f"config/dns/hosts/{encoded_value}")

    def add_local_cname(self, host, target, ttl=None):
        """
        Add a local CNAME record to Pi-hole.

        :param host: The CNAME alias (e.g., "bar.xyz")
        :param target: The target hostname (e.g., "foo.dev")
        :param ttl: Time-to-live for the record (None for no TTL)
        :return: API response
        """
        if ttl is None:
            encoded_value = urllib.parse.quote(f"{host},{target}")
        else:
            encoded_value = urllib.parse.quote(f"{host},{target},{ttl}")
        return self.connection.put(f"config/dns/cnameRecords/{encoded_value}")

    def remove_local_cname(self, host, target, ttl=None):
        """
        Remove a local CNAME record from Pi-hole.

        :param host: The CNAME alias (e.g., "bar.xyz")
        :param target: The target hostname (e.g., "foo.dev")
        :param ttl: Time-to-live for the record (None for no TTL)
        :return: API response
        """
        if ttl is None:
            encoded_value = urllib.parse.quote(f"{host},{target}")
        else:
            encoded_value = urllib.parse.quote(f"{host},{target},{ttl}")
        return self.connection.delete(f"config/dns/cnameRecords/{encoded_value}")
