import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, AccSummary
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, setup_test):

    logger.info("Step 1: Open My Account modal")
    web_app.home_page.open_my_account()

    logger.info("Verify account summary against api data")
    exp_account_summary = APIClient().statistics.get_account_statistics(get_acc_balance=True)
    web_app.home_page.my_account_modal.verify_account_info(exp_account_summary)

    logger.info(f"Verify Available Account = {exp_account_summary.get(AccSummary.BALANCE)}")
    web_app.home_page.verify_available_account(exp_account_summary)


@pytest.fixture
def setup_test(web_app, symbol):
    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")

    logger.info("- Place order to make sure account has Margin Level")
    APIClient().trade.post_order(ObjTrade(order_type=OrderType.MARKET, symbol=symbol), update_price=False)

    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield

    logger.info("[Cleanup] Close My Account modal (if open)")
    web_app.home_page.my_account_modal.close()
