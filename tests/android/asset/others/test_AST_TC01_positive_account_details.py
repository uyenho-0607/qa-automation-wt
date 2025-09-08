import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features, AccInfo, WatchListTab
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, setup_teardown, symbol):
    acc_balance, acc_info, order_ids, sum_profit = setup_teardown

    logger.info("Step 1: Navigate to Asset Page")
    android.home_screen.navigate_to(Features.ASSETS)

    logger.info("Verify account info")
    android.assets_screen.verify_account_details(acc_info)

    logger.info("Verify account balance summary")
    android.assets_screen.verify_account_balance_summary(acc_balance)

    logger.info("Step 2: Navigate to Trade Page")
    android.assets_screen.navigate_to(Features.HOME)

    logger.info(f"Step 3: Select symbol {symbol}")
    android.trade_screen.watch_list.select_tab(WatchListTab.ALL)
    android.trade_screen.watch_list.select_symbol(symbol=symbol)

    logger.info("Step 4: Close some orders")
    for _id in order_ids:
        android.trade_screen.asset_tab.full_close_position(_id)

    logger.info("Step 5: Navigate back to Asset Page")
    android.trade_screen.navigate_to(Features.ASSETS)

    logger.info(f"Verify Profit/Loss and account balance are changed an amount of ~{sum_profit!r} after closing positions")
    acc_balance[AccInfo.REALISED_PROFIT_LOSS] = acc_balance[AccInfo.REALISED_PROFIT_LOSS] + sum_profit
    acc_balance[AccInfo.BALANCE] = acc_balance[AccInfo.BALANCE] + sum_profit

    android.assets_screen.verify_account_balance_summary(acc_balance, tolerance_percent=0.1, tolerance_fields=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS])

    logger.info("Verify account info against API data again")
    acc_balance = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    android.assets_screen.verify_account_balance_summary(acc_balance)


@pytest.fixture
def setup_teardown(android, symbol):
    close_amount = 5
    account_summary = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    account_info = APIClient().user.get_user_account(get_acc=True)

    logger.info("- Prepare order data")
    resp_ord = APIClient().order.get_orders_details(order_type=OrderType.MARKET)
    cur_orders = [item for item in resp_ord if item["symbol"] == symbol]

    if not cur_orders:
        for _ in range(close_amount):
            trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
            APIClient().trade.post_order(trade_object)

        cur_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    order_ids = [item["orderId"] for item in cur_orders[:close_amount]]
    profit = [item["profit"] for item in cur_orders[:close_amount]]

    yield account_summary, account_info, order_ids, sum(profit)
