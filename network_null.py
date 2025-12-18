# network_null.py
# BRANCH: main
# ROLE: Null network implementation (OFFLINE SAFE)

from network_port import NetworkPort


class NullNetwork(NetworkPort):
    def get(self, url: str):
        return None

    def post(self, url: str, data):
        return None
