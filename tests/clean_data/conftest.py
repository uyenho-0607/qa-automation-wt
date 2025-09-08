import pytest

from src.apis.api_client import APIClient
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import Features, OrderType
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web():
    DriverManager.get_driver()
    yield WebContainer()
    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(autouse=True)
def disable_OCT(disable_OCT):
    pass


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(web, symbol):
    logger.info("- Login to MemberSite")
    web.home_page.goto()
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()

    logger.info("- Select Asset Page")
    web.home_page.navigate_to(Features.ASSETS)


@pytest.fixture
def get_order_list(web):

    def _handler(order_type: OrderType = OrderType.MARKET):
        all_orders = APIClient().order.get_orders_details(order_type=order_type)

        orders_list = [
              {
                  "orderId": item.get("orderId"),
                  "symbol": item.get("symbol"),
                  "lotSize": item.get("lotSize"),
                  "fillPolicy": item.get("fillPolicy")
              }
              for item in all_orders
              if item.get("orderId") and item.get("symbol")
          ][:30]  # Limit to first 30

        # Decide return format based on the order_type
        return {"orderList": orders_list} if order_type == OrderType.MARKET else orders_list

    return _handler
