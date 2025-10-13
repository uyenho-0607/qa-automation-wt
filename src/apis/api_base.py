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

    @after_request(max_retries=3, base_delay=1.0, max_delay=10.0)
    def get(self, endpoint: str, params: dict = None, **kwargs):
        resp = self.session.get(url=f"{Config.config.api_url}{endpoint}", headers=self.headers, params=params or {})
        return resp

    @after_request(max_retries=3, base_delay=1.0, max_delay=10.0)
    def post(self, endpoint: str, payload: dict = None, **kwargs):
        resp = self.session.post(url=f"{Config.config.api_url}{endpoint}", headers=self.headers, json=payload)
        return resp

    def __del__(self):
        """Clean up session when object is destroyed"""
        if hasattr(self, 'session'):
            self.session.close()
