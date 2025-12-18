# kernel_network.py
# BRANCH: main
# ROLE: Kernel network binding (SAFE)

from network_null import NullNetwork


class KernelNetwork:
    def __init__(self):
        self.client = NullNetwork()

    def get(self, url: str):
        return self.client.get(url)

    def post(self, url: str, data):
        return self.client.post(url, data)
