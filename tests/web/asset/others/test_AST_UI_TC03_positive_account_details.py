import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, SLTPType, Features, AccInfo
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_teardown, disable_OCT):
    acc_balance, acc_info, order_ids, sum_profit = setup_teardown

    logger.info("Step 1: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Verify account info on top bar")
    web.home_page.verify_account_details(acc_info)

    logger.info("Verify account info")
    web.assets_page.verify_account_info(acc_info)

    logger.info("Verify account balance summary")
    web.assets_page.verify_account_balance_summary(acc_balance)

    logger.info("Step 2: Close some orders")
    for _id in order_ids:
        web.assets_page.asset_tab.full_close_position(_id)

    logger.info(f"Verify Profit/Loss and account balance are changed an amount of ~{sum_profit!r} after closing positions")
    acc_balance[AccInfo.REALISED_PROFIT_LOSS] = acc_balance[AccInfo.REALISED_PROFIT_LOSS] + sum_profit
    acc_balance[AccInfo.BALANCE] = acc_balance[AccInfo.BALANCE] + sum_profit

    web.assets_page.verify_account_balance_summary(acc_balance, acc_items=AccInfo.BALANCE, tolerance=0.1)
    web.assets_page.verify_account_balance_summary(acc_balance, acc_items=AccInfo.REALISED_PROFIT_LOSS, tolerance=0.07)

    logger.info("Verify other info is not changed")
    web.assets_page.verify_account_balance_summary(acc_balance, acc_items=AccInfo.list_values(except_val=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS]))

    logger.info("Verify account info against API data again")
    acc_balance = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    web.assets_page.verify_account_balance_summary(acc_balance)


@pytest.fixture
def setup_teardown(web, symbol):
    close_amount = 5
    account_summary = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    account_info = APIClient().user.get_user_account(get_acc=True)

    logger.info("- Preparing order data")
    cur_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    if not cur_orders:
        for _ in range(close_amount):
            trade_object = ObjectTrade(order_type=OrderType.MARKET, indicate=SLTPType.POINTS, symbol=symbol)
            APIClient().trade.post_order(trade_object)

        cur_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    order_ids = [item["orderId"] for item in cur_orders[:close_amount]]
    profit = [item["profit"] for item in cur_orders[:close_amount]]

    yield account_summary, account_info, order_ids, sum(profit)
