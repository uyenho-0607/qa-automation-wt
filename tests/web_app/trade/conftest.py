import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site, web_app, symbol, disable_OCT):

    logger.info(f"- Search and select symbol: {symbol}")
    web_app.home_page.search_and_select_symbol(symbol)

@pytest.fixture(scope="package")
def create_order_data(web_app, get_asset_tab_amount, symbol):
    def _handler(trade_object):

        tab = AssetTabs.get_tab(trade_object.order_type)
        current_amount = get_asset_tab_amount(trade_object.order_type)

        logger.info(f"- POST {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
        res = APIClient().trade.post_order(trade_object)

        web_app.trade_page.asset_tab.select_tab(tab.HISTORY)
        web_app.trade_page.asset_tab.select_tab(tab)

        # Loading new created data
        web_app.trade_page.asset_tab.wait_for_tab_amount(tab, expected_amount=current_amount + 1)

        return res, current_amount + 1

    return _handler
