import time
import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features, AccInfo, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_test, disable_OCT):
    acc_balance, acc_info, order_ids, sum_profit = setup_test

    logger.info("Step 1: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Verify account info on top bar (against API data)")
    web.home_page.verify_account_details(acc_info)

    logger.info("Verify account info in Asset Page (against API data)")
    web.assets_page.verify_account_info(acc_info)

    logger.info("Verify account balance summary in Asset Page (against API data)")
    web.assets_page.verify_account_balance_summary(acc_balance)

    logger.info(f"Step 2: Close {len(order_ids)} Market orders ({', '.join(order_ids)})")
    for _id in order_ids:
        web.assets_page.asset_tab.full_close_position(order_id=_id, wait=True)

        logger.info(f"Verify order closed successfully (id: {_id!r})")
        web.assets_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, order_id=_id, is_display=False)

    # update new values for acc balance and profit loss
    acc_balance[AccInfo.BALANCE] = acc_balance[AccInfo.BALANCE] + sum_profit
    acc_balance[AccInfo.REALISED_PROFIT_LOSS] = acc_balance[AccInfo.REALISED_PROFIT_LOSS] + sum_profit

    logger.info(f"Verify Acc Balance and Profit Loss are changed: {sum_profit!r}")
    web.assets_page.verify_account_balance_summary(
        acc_balance,
        acc_items=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS],
        tolerance_fields_specific={AccInfo.BALANCE: 0.1, AccInfo.REALISED_PROFIT_LOSS: 10}
    )

    logger.info("Verify other infos are not changed")
    web.assets_page.verify_account_balance_summary(acc_balance, acc_items=AccInfo.list_values(except_val=[AccInfo.BALANCE, AccInfo.REALISED_PROFIT_LOSS]))

    logger.info("Step 3: Get account statistic using API again")
    acc_balance = APIClient().statistics.get_account_statistics(get_asset_acc=True)

    logger.info("Verify account info against API data again")
    web.assets_page.verify_account_balance_summary(acc_balance)


@pytest.fixture
def setup_test(web, symbol):
    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")
    
    close_amount = 5
    account_summary = APIClient().statistics.get_account_statistics(get_asset_acc=True)
    account_info = APIClient().user.get_user_account(get_acc=True)

    logger.info("- Check current placed market orders")
    cur_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    if not cur_orders:
        logger.info("- No market order, placing new order using API")
        for _ in range(close_amount):
            APIClient().trade.post_order(ObjTrade(order_type=OrderType.MARKET, symbol=symbol), update_price=False)
            time.sleep(1)

        logger.info("- Get placed market orders again")
        cur_orders = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    order_ids = [item["orderId"] for item in cur_orders[:close_amount]]
    profit = [item["profit"] for item in cur_orders[:close_amount]]

    logger.info(f">> Setup Summary: order_ids: {', ' .join(str(item) for item in order_ids)}, Total profit/loss: {round(sum(profit), 2)}")
    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield account_summary, account_info, order_ids, round(sum(profit), 2)
