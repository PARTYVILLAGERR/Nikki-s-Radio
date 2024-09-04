#!/bin/env python
import socket
import random
import urllib.request
import urllib.error
import json
import logging

class Radio:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.server = "https://de1.api.radio-browser.info"
        logging.basicConfig(level=logging.INFO)

    def get_radiobrowser_base_urls(self):
        """
        Get all base URLs of currently available RadioBrowser servers.

        Returns: 
        list: A list of strings representing base URLs.
        """
        hosts = []
        # Get all hosts from DNS
        ips = socket.getaddrinfo('all.api.radio-browser.info',
                                 80, 0, 0, socket.IPPROTO_TCP)
        for ip_tuple in ips:
            ip = ip_tuple[4][0]
            # Do a reverse lookup on each IP to get a human-readable host name
            host_addr = socket.gethostbyaddr(ip)
            # Add the host name to the list if not already present
            if host_addr[0] not in hosts:
                hosts.append(host_addr[0])

        # Sort list of host names and add "https://" to each
        hosts.sort()
        return [f"https://{host}" for host in hosts]

    def downloadUri(self, uri, param=None):
        """
        Download file with the correct headers set.

        Returns: 
        str: The response data as a string.
        """
        headers = {
            'User-Agent': 'RadioBrowserApp/0.1',
            'Content-Type': 'application/json'
        }
        
        if param is not None:
            param_encoded = json.dumps(param).encode('utf-8')
            print(f'Request to {uri} Params: {json.dumps(param)}')
        else:
            param_encoded = None
            print(f'Request to {uri}')
        
        req = urllib.request.Request(uri, data=param_encoded)
        for key, value in headers.items():
            req.add_header(key, value)
        
        try:
            with urllib.request.urlopen(req) as response:
                data = response.read()
            return data.decode('utf-8')
        except urllib.error.HTTPError as e:
            print(f'HTTP error occurred: {e.code} - {e.reason}')
            raise
        except urllib.error.URLError as e:
            print(f'URL error occurred: {e.reason}')
            raise
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            raise
    
    def downloadRadioBrowser(self, path, param):
        """
        Download file with relative url from a random api server. Retry with other api servers if failed.
        Returns:
            str: result data
        """
        print('Server: ' + self.server)
        uri = self.server + path

        try:
            data = self.downloadUri(uri, param)
            if data:
                return data
            else:
                print("No data returned from API.")
                return None
        except Exception as e:
            print("Unable to download from API URL: " + uri, e)
            return None

    def downloadRadioBrowserStats(self):
        """
        Download and return the RadioBrowser stats.

        Returns:
        dict: The stats as a dictionary.
        """
        stats = self.downloadRadioBrowser("/json/stats", None)
        return json.loads(stats)
    
    def downloadRadioBrowserStations(self, offset, limit):
        """
        Download all radio stations from RadioBrowser servers.
        This function attempts to fetch all stations without pagination.

        Returns:
        list: A list of radio stations as dictionaries.
        """
        path = f"/json/stations?limit={limit}&offset={offset}"
        stations = self.downloadRadioBrowser(path, None)
        return json.loads(stations)