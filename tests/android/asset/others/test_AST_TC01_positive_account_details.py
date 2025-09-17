import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features, AssetTabs, AccInfo
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, setup_teardown, symbol):
    acc_balance, acc_info, order_ids = setup_teardown

    logger.info("Step 1: Navigate to Asset Page")
    android.home_screen.navigate_to(Features.ASSETS)

    logger.info("Verify account info (against API data)")
    android.assets_screen.verify_account_details(acc_info)

    logger.info("Verify account balance summary (against API data)")
    android.assets_screen.verify_account_balance_summary(acc_balance)

    logger.info("Step 2: Navigate to Home Page")
    android.assets_screen.navigate_to(Features.HOME)

    logger.info(f"Step 3: Search and select symbol: {symbol!r}")
    android.home_screen.search_and_select_symbol(symbol)

    profit_loss = 0

    logger.info(f"Step 4: Close {len(order_ids)} Market orders ({', '.join(order_ids)})")
    for i, _id in enumerate(order_ids):
        profit_loss += android.trade_screen.asset_tab.get_profit_loss()[0]

        android.trade_screen.asset_tab.full_close_position(order_id=_id, wait=True)

        logger.info(f"Verify order closed successfully (id: {_id!r})")
        android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, _id, is_display=False)

    logger.info("Step 5: Navigate back to Asset Page")
    android.trade_screen.navigate_to(Features.ASSETS)

    # update expected value after closing orders
    acc_balance[AccInfo.REALISED_PROFIT_LOSS] = acc_balance[AccInfo.REALISED_PROFIT_LOSS] + profit_loss
    acc_balance[AccInfo.BALANCE] = acc_balance[AccInfo.BALANCE] + profit_loss

    logger.info(f"Verify Acc Balance vs Profit Loss are changed ~{round(profit_loss, 2)!r}")
    android.assets_screen.verify_account_balance_summary(acc_balance, tolerance_percent=5, tolerance_fields=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS])

    logger.info("Step 6: Get account statistic using API again")
    acc_balance = APIClient().statistics.get_account_statistics(get_asset_acc=True)

    logger.info("Verify account info against API data again")
    android.assets_screen.verify_account_balance_summary(acc_balance)


@pytest.fixture
def setup_teardown(android, symbol):
    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")
    close_amount = 5

    account_summary = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    account_info = APIClient().user.get_user_account(get_acc=True)

    logger.info("- Check current placed market orders")
    cur_orders = APIClient().order.get_orders_details(symbol, order_type=OrderType.MARKET)

    if not cur_orders:
        logger.info("- No market order, send API to place new orders")
        for _ in range(close_amount):
            APIClient().trade.post_order(ObjTrade(order_type=OrderType.MARKET, symbol=symbol))

        logger.info("- Get placed market orders again")
        cur_orders = APIClient().order.get_orders_details(symbol, order_type=OrderType.MARKET)

    order_ids = [item["orderId"] for item in cur_orders[:close_amount]]

    logger.info(f">> Setup Summary: Placed order ID: {', '.join(str(item) for item in order_ids)}")
    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield account_summary, account_info, order_ids
