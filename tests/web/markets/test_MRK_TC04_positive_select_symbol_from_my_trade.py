import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import MarketsSection, WatchListTab, OrderType, Features
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_test):
    select_symbol = setup_test

    logger.info(f"Step 1: Select symbol {select_symbol!r} from My Trade (result from setup test)")
    web.markets_page.select_symbol(MarketsSection.MY_TRADE, select_symbol)

    logger.info(f"Verify Tab ALL on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.ALL)

    logger.info(f"Verify symbol {select_symbol} is selected")
    web.trade_page.watch_list.verify_symbol_selected(select_symbol)

    logger.info("Verify symbol selected in chart")
    web.trade_page.chart.verify_symbol_selected(select_symbol)

@pytest.fixture
def setup_test(web):

    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")

    logger.info(f"- Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info("- Get symbols in My Trade section")
    symbols = web.markets_page.get_symbols(MarketsSection.MY_TRADE)

    if not symbols:
        logger.info("- No symbol in My Trade -> Send API request to place new Market order")
        for _ in range(3):
            APIClient().trade.post_order(ObjTrade(order_type=OrderType.MARKET), update_price=False)

        web.markets_page.refresh_page()
        web.markets_page.wait_for_spin_loader()

        logger.info("- Get symbols in My Trade section again")
        symbols = web.markets_page.get_symbols(MarketsSection.MY_TRADE)

    selected_symbol = random.choice(symbols)

    logger.info(f">> Setup Summary: random symbol from My Trade: {selected_symbol!r}")
    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield selected_symbol

