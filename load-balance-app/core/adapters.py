"""
Adapter discovery and management
"""
import psutil
import socket
import uuid
from typing import List, Dict


class AdapterService:
    def list_adapters(self) -> List[Dict]:
        """
        Returns a list of network adapters with basic info.
        Each dict contains:
        - name: friendly name
        - mac: MAC address
        - speed: link speed in Mbps
        - status: 'up' or 'down'
        """
        adapters = []
        for name, addrs in psutil.net_if_addrs().items():
            stats = psutil.net_if_stats().get(name)
            if not stats:
                continue
            mac = next((addr.address for addr in addrs if addr.family == psutil.AF_LINK), "")
            adapters.append({
                "name": name,
                "mac": mac,
                "speed": stats.speed or 0,
                "status": "up" if stats.isup else "down"
            })
        return adapters
