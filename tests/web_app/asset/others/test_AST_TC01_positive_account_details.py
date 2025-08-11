import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, SLTPType, Features, AccInfo, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, setup_teardown, symbol):
    acc_balance, acc_info, order_ids, sum_profit = setup_teardown

    logger.info("Step 1: Navigate to Asset Page")
    web_app.home_page.navigate_to(Features.ASSETS)

    logger.info("Verify account info")
    web_app.assets_page.verify_account_details(acc_info)

    logger.info("Verify account balance summary")
    web_app.assets_page.verify_account_balance_summary(acc_balance)

    logger.info("Step 2: Navigate to Home Page")
    web_app.assets_page.navigate_to(Features.HOME)

    logger.info(f"Step 3: Search and select symbol: {symbol!r}")
    web_app.home_page.search_and_select_symbol(symbol)

    logger.info(f"Step 4: Close orders: {', '.join(order_ids)!r}")
    for i, _id in enumerate(order_ids):
        web_app.trade_page.asset_tab.full_close_position(order_id=_id, wait=True)

        logger.info("Verify closed order successfully")
        web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, _id, is_display=False)

    logger.info("Step 5: Navigate back to Asset Page")
    web_app.trade_page.navigate_to(Features.ASSETS)

    # update expected value after closing orders
    acc_balance[AccInfo.REALISED_PROFIT_LOSS] = acc_balance[AccInfo.REALISED_PROFIT_LOSS] + sum_profit
    acc_balance[AccInfo.BALANCE] = acc_balance[AccInfo.BALANCE] + sum_profit

    logger.info(f"Verify Profit Loss and Account Balance are changed")
    web_app.assets_page.verify_account_balance_summary(acc_balance, tolerance_percent=1, tolerance_fields=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS])

    logger.info("Step 6: Get updated API data")
    acc_balance = APIClient().statistics.get_account_statistics(get_asset_acc=True)

    logger.info("Verify account info against API data again")
    web_app.assets_page.verify_account_balance_summary(acc_balance)


@pytest.fixture
def setup_teardown(web_app, symbol):
    close_amount = 5
    account_summary = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    account_info = APIClient().user.get_user_account(get_acc=True)

    logger.info("- Prepare order data")
    resp_ord = APIClient().order.get_orders_details(order_type=OrderType.MARKET)
    cur_orders = [item for item in resp_ord if item["symbol"] == symbol]

    if not cur_orders:
        logger.debug(f"- POST {close_amount!r} MARKET orders")
        for _ in range(close_amount):
            trade_object = ObjTrade(order_type=OrderType.MARKET, indicate=SLTPType.POINTS, symbol=symbol)
            APIClient().trade.post_order(trade_object)

        cur_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    order_ids = [item["orderId"] for item in cur_orders[:close_amount]]
    profit = [item["profit"] for item in cur_orders[:close_amount]]

    logger.debug(f"- Sum Profit: {sum(profit)}")

    yield account_summary, account_info, order_ids, sum(profit)
