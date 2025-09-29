import pytest

from src.apis.api_client import APIClient
from src.data.enums import AccSummary, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.common_utils import line_break
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_teardown):
    exp_account_summary, acc_details = setup_teardown

    logger.info("Step 1: Open account dropdown details")
    web.home_page.toggle_account_selector()

    logger.info("Verify account dropdown info against API data")
    web.home_page.verify_account_dropdown_details(acc_details)

    logger.info("Step 2: Close account dropdown details")
    web.home_page.toggle_account_selector(open=False)

    logger.info("Verify account details in Home Page against API data")
    web.home_page.verify_account_details(acc_details)

    logger.info("Step 3: Toggle balance summary and show all account summary items")
    web.home_page.check_uncheck_balance_items(AccSummary.checkbox_list())
    exp_account_summary = APIClient().statistics.get_account_statistics(get_acc_balance=True)

    logger.info("Verify Account Balance against API data")
    web.home_page.verify_acc_balance_value(exp_account_summary)

    logger.info("Step 4: Toggle balance summary")
    web.home_page.toggle_balance_summary()

    logger.info("Verify Account Summary against Account Dropdown")
    web.home_page.verify_acc_summary_dropdown()

    logger.info("Verify Account Note item against API data")
    web.home_page.verify_acc_note_values(exp_account_summary)


@pytest.fixture
def setup_teardown(web, symbol):
    line_break("Setup Test - Start")

    logger.info("[Setup] Place order to make sure account has Margin Level", setup=True)
    APIClient().trade.post_order(ObjTrade(order_type=OrderType.MARKET, symbol=symbol), update_price=False)

    logger.info("[Setup] Refresh Page to load data", setup=True)
    web.home_page.refresh_page()

    logger.info("[Setup] Send API to get account statistic and details", setup=True)
    account_summary = APIClient().statistics.get_account_statistics(get_acc_balance=True)
    account_details = APIClient().user.get_user_account()

    line_break("Setup Test - End")

    yield account_summary, account_details

    logger.info("[Cleanup] Show all account summary items", teardown=True)
    web.home_page.check_uncheck_balance_items(AccSummary.checkbox_list())



