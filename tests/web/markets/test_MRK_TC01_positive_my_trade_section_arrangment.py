import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features, MarketsSection, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, disable_OCT):
    logger.info("Step 1: Get current open positions on Assets Page")
    cur_symbols = web.assets_page.asset_tab.get_symbols()[:5]

    logger.info(f"Step 2: Navigate to Market Page and check My Trade Section")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Verify symbols list displayed in My Trade are: {cur_symbols}")
    web.markets_page.verify_my_trade_items_list(cur_symbols)

    logger.info(f"Step 3: Place Pending Order for symbol: {cur_symbols[-1]}")
    web.markets_page.select_symbol(MarketsSection.MY_TRADE)
    web.trade_page.place_order_panel.place_order(ObjTrade(symbol=cur_symbols[-1], order_type=OrderType.LIMIT), submit=True)

    logger.info(f"Step 4: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info("Verify displaying symbols are not changed")
    web.markets_page.verify_my_trade_items_list(cur_symbols)

    logger.info("Step 5: Navigate to Asset Page and close order")
    web.markets_page.navigate_to(Features.ASSETS, wait=True)
    web.assets_page.asset_tab.full_close_position(wait=True)

    logger.info("Step 6: Get current symbols after closing order")
    cur_symbols = web.assets_page.asset_tab.get_symbols()[:5]

    logger.info("Step 7: Navigate to Market Page")
    web.assets_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Verify symbols list displayed in My Trade are: {cur_symbols}")
    web.markets_page.verify_my_trade_items_list(cur_symbols)



@pytest.fixture(autouse=True)
def setup_test(web, get_asset_tab_amount, ):
    tab_amount = get_asset_tab_amount(OrderType.MARKET)

    logger.info("- Navigate to Assets Page")
    web.markets_page.navigate_to(Features.ASSETS, wait=True)

    if not tab_amount:
        logger.info(f"- Create some Markets order")
        for _ in range(5):
            trade_obj = ObjTrade(order_type=OrderType.MARKET)
            APIClient().trade.post_order(trade_obj, update_price=False)

        # wait for loading new created data
        web.trade_page.asset_tab.wait_for_tab_amount(AssetTabs.OPEN_POSITION, expected_amount=tab_amount + 5)

    yield
    logger.info("- Navigate back to markets page")
    web.home_page.navigate_to(Features.MARKETS)