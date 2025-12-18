"""
NTRLI SuperAPK - Network Module
Phase 1: Tor/VPN connectivity, proxies, network health
Enhanced with async operations for better performance
"""

import requests
import socket
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

try:
    from modules.ai_core import AI_CONSOLE
except ImportError:
    from ai_core import AI_CONSOLE

class NetworkManager:
    """Handles network connectivity, proxies, Tor/VPN with async support"""

    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.proxy_config = None
        self.tor_enabled = False
        self.vpn_enabled = False
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.timeout = 10  # Default timeout
        self.log("NetworkManager initialized with async support")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[NETWORK] {msg}", level)
        else:
            print(f"[NETWORK] {msg}")
    
    def check_connectivity(self):
        """Check if internet connection is available"""
        test_urls = [
            "https://www.google.com",
            "https://www.cloudflare.com",
            "https://1.1.1.1"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.log(f"Connectivity OK: {url}")
                    return True, "Connected"
            except Exception as e:
                self.log(f"Connectivity check failed for {url}: {e}", "WARNING")
                continue
        
        self.log("No internet connectivity", "ERROR")
        return False, "No connection"
    
    def get_public_ip(self):
        """Get public IP address"""
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            ip = response.json()["ip"]
            self.log(f"Public IP: {ip}")
            return ip
        except Exception as e:
            self.log(f"Failed to get public IP: {e}", "ERROR")
            return None
    
    def enable_tor_proxy(self, host="127.0.0.1", port=9050):
        """Enable Tor SOCKS5 proxy"""
        try:
            self.proxy_config = {
                "http": f"socks5h://{host}:{port}",
                "https": f"socks5h://{host}:{port}"
            }
            self.tor_enabled = True
            self.log(f"Tor proxy enabled: {host}:{port}")
            return True, "Tor enabled"
        except Exception as e:
            self.log(f"Failed to enable Tor: {e}", "ERROR")
            return False, str(e)
    
    def disable_proxy(self):
        """Disable all proxies"""
        self.proxy_config = None
        self.tor_enabled = False
        self.vpn_enabled = False
        self.log("Proxies disabled")
        return True, "Proxies disabled"
    
    def test_tor_connection(self):
        """Test if Tor is working"""
        if not self.tor_enabled:
            return False, "Tor not enabled"
        
        try:
            response = requests.get(
                "https://check.torproject.org/api/ip",
                proxies=self.proxy_config,
                timeout=10
            )
            data = response.json()
            if data.get("IsTor"):
                self.log("Tor connection verified")
                return True, "Tor working"
            else:
                self.log("Tor check failed: Not using Tor", "WARNING")
                return False, "Not using Tor"
        except Exception as e:
            self.log(f"Tor connection test failed: {e}", "ERROR")
            return False, str(e)
    
    def make_request(self, url, method="GET", data=None, headers=None, timeout=10):
        """Make HTTP request with proxy support"""
        try:
            kwargs = {
                "timeout": timeout,
                "headers": headers or {}
            }
            
            if self.proxy_config:
                kwargs["proxies"] = self.proxy_config
            
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            elif method.upper() == "POST":
                kwargs["json"] = data
                response = requests.post(url, **kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            self.log(f"Request to {url}: {response.status_code}")
            return True, response
        except Exception as e:
            self.log(f"Request to {url} failed: {e}", "ERROR")
            return False, str(e)
    
    def get_network_info(self):
        """Get comprehensive network information"""
        info = {
            "timestamp": datetime.now().isoformat(),
            "connectivity": None,
            "public_ip": None,
            "tor_enabled": self.tor_enabled,
            "vpn_enabled": self.vpn_enabled,
            "proxy_config": self.proxy_config
        }
        
        connected, msg = self.check_connectivity()
        info["connectivity"] = {"connected": connected, "message": msg}
        
        if connected:
            info["public_ip"] = self.get_public_ip()
        
        return info
    
    def check_port_open(self, host, port, timeout=3):
        """Check if a port is open on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                self.log(f"Port {port} on {host} is OPEN")
                return True
            else:
                self.log(f"Port {port} on {host} is CLOSED")
                return False
        except Exception as e:
            self.log(f"Port check failed: {e}", "ERROR")
            return False

    # ========== ASYNC METHODS FOR PERFORMANCE ==========

    async def async_make_request(self, url, method="GET", data=None, headers=None, timeout=None):
        """
        Async HTTP request with proxy support

        Args:
            url: Request URL
            method: HTTP method (GET, POST)
            data: Request data
            headers: Request headers
            timeout: Request timeout

        Returns:
            (success, response)
        """
        timeout = timeout or self.timeout
        loop = asyncio.get_event_loop()

        try:
            # Run requests in thread pool to avoid blocking
            response = await loop.run_in_executor(
                self.executor,
                lambda: self._sync_request(url, method, data, headers, timeout)
            )
            return True, response
        except Exception as e:
            self.log(f"Async request to {url} failed: {e}", "ERROR")
            return False, str(e)

    def _sync_request(self, url, method, data, headers, timeout):
        """Helper for synchronous request in executor"""
        kwargs = {
            "timeout": timeout,
            "headers": headers or {}
        }

        if self.proxy_config:
            kwargs["proxies"] = self.proxy_config

        if method.upper() == "GET":
            return requests.get(url, **kwargs)
        elif method.upper() == "POST":
            kwargs["json"] = data
            return requests.post(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

    async def async_check_connectivity_batch(self, urls=None):
        """
        Check connectivity to multiple URLs concurrently

        Args:
            urls: List of URLs to check (uses defaults if None)

        Returns:
            dict of {url: (success, latency_ms)}
        """
        test_urls = urls or [
            "https://www.google.com",
            "https://www.cloudflare.com",
            "https://1.1.1.1"
        ]

        self.log(f"Checking connectivity to {len(test_urls)} URLs concurrently")

        tasks = [self._async_ping_url(url) for url in test_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return dict(zip(test_urls, results))

    async def _async_ping_url(self, url):
        """Async ping a single URL"""
        import time
        start = time.time()

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                lambda: requests.get(url, timeout=5)
            )

            latency = (time.time() - start) * 1000  # Convert to ms

            if response.status_code == 200:
                return True, latency
            return False, latency

        except Exception as e:
            return False, 0
