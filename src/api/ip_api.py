from typing import Dict, List

import requests


class IPStackAPI:
    def __init__(self, api_key: str = None):
        self.base_url = "http://api.ipstack.com/"
        self.api_key = api_key

    def get_ip_info(self, ips: List[str]) -> List[Dict]:
        results = []
        for ip in ips:
            try:
                response = requests.get(f"{self.base_url}{ip}?access_key={self.api_key}")
                results.append(response.json())
            except Exception as e:
                results.append({"ip": ip, "error": str(e)})
        return results
