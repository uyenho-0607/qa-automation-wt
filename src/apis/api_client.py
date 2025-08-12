from src.apis.auth_api import AuthAPI
from src.apis.chart_api import ChartAPI


class APIClient:
    """
    Main API client that provides access to all API services.
    This client manages authentication and provides access to trading,
    order management, and user operations.
    """
    
    def __init__(self, userid=None, password=None):
        # Initialize authentication first
        self.auth = AuthAPI(userid=userid, password=password)
        
        # Initialize other API clients with shared session
        self.chart = ChartAPI()
