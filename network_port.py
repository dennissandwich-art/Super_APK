# network_port.py
# BRANCH: main
# ROLE: Network abstraction (INTERFACE ONLY)

"""
Defines how network MAY be used later.
No requests, no sockets, no imports.
"""

class NetworkPort:
    def get(self, url: str):
        raise NotImplementedError

    def post(self, url: str, data):
        raise NotImplementedError
