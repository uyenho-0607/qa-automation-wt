from idlelib.pyparse import C_NONE

import requests
from requests.adapters import HTTPAdapter

from src.core.config_manager import Config
from src.core.decorators import after_request
from src.data.project_info import RuntimeConfig


class BaseAPI:
    def __init__(self, headers=None):
        self.headers = headers or RuntimeConfig.headers
        self.session = self._create_session()

    @staticmethod
    def _create_session():
        """Create a session with connection pooling"""
        session = requests.Session()

        # Configure connection pooling only
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20)

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session
    
    @staticmethod
    def api_url():
        return Config.config.api_url if not RuntimeConfig.url else f"{RuntimeConfig.url}/api"

    @after_request(max_retries=3, base_delay=1.0, max_delay=10.0)
    def get(self, endpoint: str, params: dict = None):
        resp = self.session.get(url=f"{self.api_url()}{endpoint}", headers=self.headers, params=params or {})
        return resp

    @after_request(max_retries=3, base_delay=1.0, max_delay=10.0)
    def post(self, endpoint: str, payload: dict = None):
        resp = self.session.post(url=f"{self.api_url()}{endpoint}", headers=self.headers, json=payload)
        return resp

    @after_request(max_retries=3, base_delay=1.0, max_delay=10.0)
    def put(self, endpoint: str, payload: dict = None):
        resp = self.session.put(url=f"{self.api_url()}{endpoint}", headers=self.headers, data=payload)
        return resp
    
    @after_request(max_retries=3, base_delay=1.0, max_delay=10)
    def delete(self, endpoint: str,  params: dict = None):
        resp = self.session.delete(url=f"{self.api_url()}{endpoint}", params=params, headers=self.headers)
        return resp

    @after_request(max_retries=3, base_delay=1.0, max_delay=10.0)
    def patch(self, endpoint: str, payload: dict = None):
        resp = self.session.patch(url=f"{self.api_url()}{endpoint}", headers=self.headers, json=payload)
        return resp

    def __del__(self):
        """Clean up session when object is destroyed"""
        if hasattr(self, 'session'):
            self.session.close()
