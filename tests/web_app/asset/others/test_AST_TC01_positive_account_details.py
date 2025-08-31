import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features, AccInfo, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, setup_teardown, symbol):
    acc_balance, acc_info, order_ids = setup_teardown

    logger.info("Step 1: Navigate to Asset Page")
    web_app.home_page.navigate_to(Features.ASSETS)

    logger.info("Verify account info (against API data)")
    web_app.assets_page.verify_account_details(acc_info)

    logger.info("Verify account balance summary (against API data)")
    web_app.assets_page.verify_account_balance_summary(acc_balance)

    logger.info("Step 2: Navigate to Home Page")
    web_app.assets_page.navigate_to(Features.HOME)

    logger.info(f"Step 3: Search and select symbol: {symbol!r}")
    web_app.home_page.search_and_select_symbol(symbol)

    profit_loss = 0

    logger.info(f"Step 4: Close {len(order_ids)} Market orders ({', '.join(order_ids)})")
    for i, _id in enumerate(order_ids):
        profit_loss += web_app.trade_page.asset_tab.get_profit_loss()[0]

        web_app.trade_page.asset_tab.full_close_position(order_id=_id, wait=True)

        logger.info(f"Verify order closed successfully (id: {_id!r})")
        web_app.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, _id, is_display=False)

    logger.info("Step 5: Navigate back to Asset Page")
    web_app.trade_page.navigate_to(Features.ASSETS)

    # update expected value after closing orders
    acc_balance[AccInfo.REALISED_PROFIT_LOSS] = acc_balance[AccInfo.REALISED_PROFIT_LOSS] + profit_loss
    acc_balance[AccInfo.BALANCE] = acc_balance[AccInfo.BALANCE] + profit_loss

    logger.info(f"Verify Acc Balance vs Profit Loss are changed ~{round(profit_loss, 2)!r}")
    web_app.assets_page.verify_account_balance_summary(acc_balance, tolerance_percent=1, tolerance_fields=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS])

    logger.info("Step 6: Get account statistic using API again")
    acc_balance = APIClient().statistics.get_account_statistics(get_asset_acc=True)

    logger.info("Verify account info against API data again")
    web_app.assets_page.verify_account_balance_summary(acc_balance)


@pytest.fixture
def setup_teardown(web_app, symbol):
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

    logger.info(f">> Setup Summary: Placed order ID: {', ' .join(str(item) for item in order_ids)}")
    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield account_summary, account_info, order_ids
