from src.apis.auth_api import AuthAPI
from src.apis.chart_api import ChartAPI
from src.apis.market_api import MarketAPI
from src.apis.order_api import OrderAPI
from src.apis.statistics_api import StatisticsAPI
from src.apis.trade_api import TradeAPI
from src.apis.user_api import UserAPI


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
        self.trade = TradeAPI()
        self.order = OrderAPI()
        self.user = UserAPI()
        self.market = MarketAPI()
        self.chart = ChartAPI()
        self.statistics = StatisticsAPI()
